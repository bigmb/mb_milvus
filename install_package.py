#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##Run the make_version file to update the version number and then run this file to install the package and upload it to pipy.

import os
import subprocess
file = '/home/malav/Image-Similarity-Search-Milvus'

#subprocess.run(["cd",file]), check=True, stdout=subprocess.PIPE).stdout
os.system('cd ' + file)

if os.path.exists(file+'/dist'):
    os.system('rm -rf '+file+'/dist')
    os.system('rm -rf '+file+'/build')
#subprocess.run(["ls"]),check=True, stdout=subprocess.PIPE).stdout
os.system("ls")
subprocess.run(["git", "pull"], check=True, stdout=subprocess.PIPE).stdout
#os.system('git pull')
os.system('python3.8 -m setup bdist_wheel')
os.system('python3.8 -m pip install '+file + '/dist/' +os.listdir(file +'/dist')[-1])
os.system('python3.8 -m twine upload dist/*')
