# Django Template Editor Competion Engine

[![Join the chat at https://gitter.im/mjbrownie/django_completeme](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/mjbrownie/django_completeme?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

This is a rerwite of the htmldjango-omnicomplete vim plugin I released a while
back. I've set it up an app rather than as a vim plugin so vim no longer has to
have the django python code running inside it.

https://github.com/mjbrownie/vim-htmldjango_omnicomplete

An omnicomplete tailored to django templates "tags/variables/filters/templates"

## Screenshots:

![](https://raw.githubusercontent.com/mjbrownie/media/master/django_completeme.gif)

## Installation

## Easy method using vim plugged.

You can use my fork of valloric/YouCompleteMe (up to date / ahead with master as of writing).
Note I'm not looking to merge with the main repository unless there is a lot of demand for me to do so.


    function! BuildYCM(info)
      " info is a dictionary with 3 fields
      " - name:   name of the plugin
      " - status: 'installed', 'updated', or 'unchanged'
      " - force:  set on PlugInstall! or PlugUpdate!
      if a:info.status == 'installed' || a:info.force
        !./install.py
      endif
    endfunction

    call plug#begin()
    ...
    Plug 'mjbrownie/YouCompleteMe', { 'do': function('BuildYCM') }
    ...
    call plug#end()

### Manual Installation

The old school but explicit way. 

https://github.com/Valloric/YouCompleteMe#Installation

Once you are comfortable with youcompleteme working on your system (eg. with
python jedi), swap the daemon remote with my fork as follows.

    cd ~/.vim/bundle/youcompleteme/third_party/ycmd
    git remote add mjbrownie https://github.com/mjbrownie/ycmd.git
    git checkout --track -b mjbrownie mjbrownie/master
    git submodule init
    git submodule update
    git submodule foreach git pull origin master
    git submodule foreach git submodule init
    git submodule foreach git submodule update

Once Completed the directory structure should be as follows.

    ~/.vim/bundle/youcompleteme <--vim plugin (https://github.com/Valloric/YouCompleteMe.git)
    ~/.vim/bundle/youcompleteme/third_party/ycmd <-- backend (https://github.com/mjbrownie/ycmd.git)
    ~/.vim/bundle/youcompleteme/third_party/ycmd/third_party/django_completeme <-- djangoplugin (https://github.com/mjbrownie/django_completeme.git)


## Features

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

## Limited Jinja Support.

    I've added some jinja support for {% include '' %} {% extend "" %} and {% static "" %}

