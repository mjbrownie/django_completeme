# Django Template Editor Competion Engine

This is a rerwite of the htmldjango-omnicomplete vim plugin I released a while
back. I've set it up an app rather than as a vim plugin so vim no longer has to
have the django python code running inside it.

https://github.com/mjbrownie/vim-htmldjango_omnicomplete

An omnicomplete tailored to django templates "tags/variables/filters/templates"

Screenshots:

![](https://raw.githubusercontent.com/mjbrownie/media/master/django_completeme.gif)

Eg.

    1. Filters

        {{ somevar|a<c-x><c-o>}} should complete 'add' , 'addslashes'

    2. Tags

        {% cy<c-x><x-o> %} should complete 'cycle'

    3. Load statements

        It also should grab any libs you have {% load tag_lib %} in the file.
        Although it needs them in INSTALLED_APPS.

        {% load <c-x><c-o> %} will complete libraries (eg. 'cache', 'humanize')

    4. template filenames

        {% extends '<c-x><c-o>' %} will list base.html ... etc

    5. url complete

        {% url <c-x><c-o> %} should complete views and named urls

    6. super block complete

        eg {% block c<c-x><c-o> %} to complete 'content' or something defined
        in an extended template.

    7. static files complete

        eg {% static "r<c-x><c-o>" %}

        <script src="{% static "<c-x><c-o>" %}" /> - completes js files in static
        <style src="{% static "<c-x><c-o>" %}" /> - completes css files in static
        <img src="{% static "<c-x><c-o>" %}" /> - completes img files in static

    8. optional variable name completion (placeholder)

        {{ s<c-x><x-o> }}

        will complete any maps defined in the python htmldjango_opts['variable']
        dict list. See below for info.


    Where possible info panels show the functions __doc__. Most of the
    internal ones are decent.
