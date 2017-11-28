from __future__ import unicode_literals
""""
Compatibility functions to attempt to stay useful for most django versions
(1.4 -> 18+)
"""
import os, sys
import django

try:
    #for OLD versions od django
    from django.template import get_library
except ImportError:
    #for django 1.8+
    try:
        from django.template.base import get_library
    except:
        from django.template.backends.django import get_installed_libraries
        def get_library(libname):
            return get_installed_libraries().get(libname, None)

from django.template.loaders import filesystem, app_directories
#Later versions of django seem to be fussy about get_library paths.
try:
    from django.template import import_library
except ImportError:
    try:
        from django.template.base import import_library
    except ImportError:
        import_library = get_library



try:
    from django.template.loaders.app_directories import app_template_dirs
except ImportError:
    from django.template.loaders.app_directories import get_app_template_dirs
    app_template_dirs = get_app_template_dirs('templates')

from django.conf import settings as mysettings

try:
    from django.template import get_templatetags_modules
except ImportError:
    #I've lifted this version from the django source
    try:
        from importlib import import_module
    except ImportError:
        from django.utils.importlib import import_module

    def get_templatetags_modules():
        """
        Return the list of all available template tag modules.

        Caches the result for faster access.
        """
        _templatetags_modules = []
        # Populate list once per process. Mutate the local list first, and
        # then assign it to the global name to ensure there are no cases where
        # two threads try to populate it simultaneously.
        for app_module in ['django'] + list(mysettings.INSTALLED_APPS):
            try:
                templatetag_module = '%s.templatetags' % app_module
                import_module(templatetag_module)
                _templatetags_modules.append(templatetag_module)
            except ImportError:
                continue
        return _templatetags_modules




