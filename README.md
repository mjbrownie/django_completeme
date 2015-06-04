# Django Template Editor Competion Engine

This is a rerwite of the htmldjango-omnicomplete vim plugin I released a while
back. I've set it up an app rather than as a vim plugin so vim no longer has to
have the django python code running inside it.

https://github.com/mjbrownie/vim-htmldjango_omnicomplete

So in theory it should be able to be converted into python3 based projects as
well as be generally a lot easier to debug and less likely to have instability
issues within your editor.

I am hoping to write a youcompleteme or standalone plugin so it can be used in
other editors if it is wanted.

INSTALLED_APPS 'completeme'

## TODO LIST

The current code is non functioning (although you can check out the tests to
see where I'm going)

* rewrite the template inspection (doneish completeme/parser.py)
* write context regexp matching
* write a yocompleteme completer script or light omnicomplete client
