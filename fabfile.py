import os

from fabric.api import *

project_dir = os.getcwd() + '/goalnet/'
print project_dir

def run():
    with lcd(project_dir):
        local("python goalnet.py", capture=False)

