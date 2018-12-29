import os, sys

def install():
    if sys.platform == 'win32':
        python = 'py'
    else:
        python = 'python3'

    os.system('%s -m pip install bs4 requests lxml' % python)
