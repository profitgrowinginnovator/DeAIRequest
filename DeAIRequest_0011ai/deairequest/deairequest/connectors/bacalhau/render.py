from typing import Tuple#,Mapping
from pathlib import Path
import os
from pipreqs import pipreqs
#import filecmp
import subprocess
import sys
#import logging
import re

def render(target: str, steps: list, config: dict, compile_path: str = None) -> Tuple[Path, str]:
    inputs = "inputs"
    inputspath = os.path.join(target,inputs)
    os.mkdir(inputspath)
    codefile = os.path.join(inputspath,"code.py")

    # Extract the code from the notebook and write to code.py
    codewriter = open(codefile, "w")
    codewriter.writelines(steps.get('same_step_000').get('code'))
    codewriter.close()

    req=os.path.join(inputspath,"requirements.txt")
    
    # Create a requirements.txt file
    pipreqs.init({'<path>': inputspath, '--savepath': None, '--print': False,
                      '--use-local': None, '--force': True, '--proxy':None, '--pypi-server':None,
                      '--diff': None, '--clean': None, '--mode': 'gt'})
    # Remove all the packages which are already installed inside the docker image 
    # Step 1: get the req file for the docker image and read all the packages already in the docker image
    # Step 2: read the requirements.txt file and find all the packages that are already installed
    # Step 3: write the list of packages that are not in the docker image to the requirements.txt file
    name = config.get('environments').get('default').get('image_tag').replace("/","-")+".req"
    path = os.path.abspath(os.path.dirname(__file__))
    reqfile = os.path.abspath(os.path.join(path,"..","..",name))
    try:
        with open(reqfile) as f:
            lines = f.read().splitlines()
    finally:
        f.close()
    try:
        with open(req) as f2:
            toinstall = f2.read().splitlines()
    finally:
        f2.close()
    for install in toinstall:
        y=re.split("([a-z-?]+)",install)
        if y[1] in lines:
            toinstall.remove(install)
    try:
        with open(req,'w') as f3:
            for install in toinstall:
                print(install)
                f3.write(install)
                f3.write("\n")
    finally:
        f3.close()
    print(req)

    # Download the remaining packages
    wheelsdir=os.path.join(target,"wheels")
    pythonversion=config.get('environments').get('default').get('python')
    for install in toinstall:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "download", "--python-version", pythonversion, "--platform", "linux_x86_64", "-d",wheelsdir,"--only-binary=:all:",install])        
        except Exception as excep:
            subprocess.check_call([sys.executable, "-m", "pip", "download", "--python-version", pythonversion, "--platform", "linux_x86_64", "-d",wheelsdir,"--no-deps",install])
        
    return (target, inputs)
