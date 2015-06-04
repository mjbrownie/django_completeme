"""
competion Template Inspector
"""
import re, os
from django.template import Template
from django.template.loader_tags import ExtendsNode, BlockNode
from django.template.loader import get_template
from operator import itemgetter
from glob import glob
import pkgutil
from django.conf import settings as mysettings
from django.contrib.staticfiles import finders

from completeme.compat import app_template_dirs, \
        get_templatetags_modules, get_library, import_library

TEMPLATE_EXTS = ['.html','.txt','.htm', '.haml']

class TemplateInspector(object):
    """
    The inspector object will take a template file, determine the type of
    completion_type needed and return the completion options.
    """

    filename = None
    lineno = 1
    colno = 0

    line = []
    buff = None
    pattern = ""

    def __init__(self, filename, lineno=1, colno=0):
        self.filename, self.lineno, self.colno = filename, lineno, colno
        self.load_template(filename)

        self.pattern = "" #TODO pattern is determined via leader

    def _tags_or_filters(self, tagtype):

        """
        TODO This is a pretty messy import from the original omnicomplete
        plugin
        """

        def _get_doc(doc, name):
            """ get doc cleans __doc__ info in the vim window at top """
            if doc:
                return doc.replace('"', ' ').replace("'", ' ')
            return '%s: no doc' % name

        def _get_opt_dict(lib, tpl, libname=''):
            """ not sure what this does"""
            opts = getattr(lib, tpl)
            return [{'word':myfile, 'info': _get_doc(opts[myfile].__doc__, myfile),
            'menu':libname} for myfile in opts.keys()]

        matches = []

        for line in self.buff:
            match = re.compile('{% load (.*)%}').match(line)
            if match:
                for lib in match.groups()[0].rstrip().split(' '):
                    mylib = get_library(lib)
                    matches += _get_opt_dict(mylib, tagtype, lib)

        defaultlib = import_library('django.template.default%s' % tagtype)
        matches += _get_opt_dict(defaultlib, tagtype, 'default')

        return matches

    def _tags(self):
        """ matching any completions {% <here> %}"""
        return self._tags_or_filters('tags')

    def _filters(self):
        """ matching any completions {% varname|<here> %}"""
        return self._tags_or_filters('filters')

    def _staticfiles(self):
        """ matching any completions {% static '<here>' %}"""

        line = self.line

        # checking for <img <style <script tags to further filter results
        if 'script' in line:
            ext = r".*\.js$"
        elif 'style' in line:
            ext = r".*\.css$"
        elif 'img' in line:
            ext = r".*\.(gif|jpg|jpeg|png)$"
        else:
            ext = r'.*'

        matches = []

        for finder in finders.get_finders():
            for path, _ in finder.list([]):
                if re.compile(ext, re.IGNORECASE).match(path) \
                    and path.startswith(self.pattern):
                    matches.append(dict(word=path, info=''))

        return matches

    def _templates(self):
        """
        matching any completions {% include '<here>' %}
        or  {% extends '<here>' %}
        """
        dirs = mysettings.TEMPLATE_DIRS + app_template_dirs
        matches = []
        for mydir in dirs:
            mydir = mydir + ('/' if not mydir.endswith('/') else '')
            for match in glob(os.path.join(mydir, self.pattern + '*')):
                if os.path.isdir(match):
                    for root, _, filenames in os.walk(match):
                        for myfile in filenames:
                            _, ext = os.path.splitext(myfile)
                            if ext in TEMPLATE_EXTS:
                                matches.append({
                                    'word' : os.path.join(root, myfile).replace(
                                        mydir, ''),
                                    'info' : 'found in %s' % mydir
                                })
                else:
                    matches.append({
                        'word' : match.replace(mydir, ''),
                        'info' : 'found in %s' % mydir
                    })
        return matches

    def _blocks(self):
        """
        matching any completions {% block <here> %}
        """

        #use regexp for extends as get_template will fail on tag errors
        rexp = re.compile(r'{%\s*extends\s*[\'"](.*)["\']\s*%}')
        base = None
        templates = [] # for cycle detection

        #look for {% extends %} in the first 10 lines
        for line in self.buff[0:10]:
            match = rexp.match(line)
            if match:
                try:
                    base = get_template(match.groups()[0])
                except Exception as e:
                    return []


        if not base:
            return []

        def _get_blocks(tpl, menu_prefix=''):
            """
            recursive worker function
            """

            #TODO I Think this is a 1.8 compatibility thing sending the wrapper
            # class
            tpl = getattr(tpl,'name', None) and tpl or tpl.template

            if tpl.name in templates and isinstance(tpl, Template):
                print "cyclic extends detected!"
                return []
            else:
                templates.append(tpl.name)

            blocks = [(block, block.name, menu_prefix + tpl.name) \
                for block in tpl.nodelist if isinstance(block, BlockNode)]

            for block, _, name in blocks:
                blocks += _get_blocks(block, '%s%s > ' % (menu_prefix, name))

            if len(tpl.nodelist) > 0 and isinstance(tpl.nodelist[0], ExtendsNode):
                blocks += _get_blocks(get_template(tpl.nodelist[0].parent_name))

            return blocks

        matches = _get_blocks(base)


        return [{'word':name, 'menu':match} for _, name, match in matches if name.startswith(self.pattern)]

    def _urls(self):
        """
        matching any completions {% url '<here>' %}
        """
        matches = []
        try: #TODO not sure why this is here
            urls = __import__(mysettings.ROOT_URLCONF,fromlist=['foo'])
        except:
            return []

        def get_urls(urllist,parent=None):
            for entry in urllist:
                if hasattr(entry,'name') and entry.name:
                    matches.append(dict(
                        word = entry.name,
                        info = entry.regex.pattern,
                        menu = parent and parent.urlconf_name or '')
                        )
                if hasattr(entry, 'url_patterns'):
                    get_urls(entry.url_patterns, entry)
        get_urls(urls.urlpatterns)
        return matches

    def _context_vars(self):
        """
        return context variables

        TODO I haven't figured a way to do this yet but it would likely involve
        either a MIDDLEWARE method similar to how the django_tebug_toolbar
        grabs context_vars.

        """
        return []

    def _find_completion_type(self):
        """
        TODO checks the buffer and returns what type of completion is needed
        """
        pass

    def completions(self, lineno=None, colno=None):
        """ return completion dict """
        self.lineno, self.colno = lineno or self.lineno, colno or self.colno
        func = self._find_completion_type()
        return func()

    def load_template(self, filename):
        """ Load a new template """
        self.filename = filename
        self.buff = open(filename, 'r').readlines()
        self.line = self.buff[self.lineno]
