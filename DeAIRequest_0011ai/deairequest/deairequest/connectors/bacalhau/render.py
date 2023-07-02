from typing import Tuple#,Mapping
from pathlib import Path
import os
from pipreqs import pipreqs
#import filecmp
import subprocess
import sys
#import platform
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
    
    # Activate virtual environment
    #try:
    #    import virtualenv
    #except ModuleNotFoundError:
    #    subprocess.check_call([sys.executable, "-m", "pip install virtualenv"])
    #subprocess.check_call([sys.executable, "-m", "virtualenv", "bclenv"])
    #if platform.system() == "Windows":
    #    subprocess.check_call([".\bclenv\Scripts\activate"])
    #else:
    #    subprocess.check_call(["/bin/sh","-c", "source bclenv/bin/activate"])

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
            rforinstall = f2.read().splitlines()
    finally:
        f2.close()

    toinstall=[]

    for install in rforinstall:
        if install != "":
            y=re.split("([A-z-?]+)",install)
            if y[1] not in lines:
                toinstall.append(install)

    if len(toinstall) > 0:
        try:
            with open(req,'w') as f3:
                for install in toinstall:
                    f3.write(install)
                    f3.write("\n")
        finally:
            f3.close()

        # Download the remaining packages
        wheelsdir=os.path.join(target,"wheels")
        pythonversion=config.get('environments').get('default').get('python')
        for install in toinstall:
            try:
                #download specific version for specific platform
                y=re.split("([A-z-?]+)",install)
                subprocess.check_call([sys.executable, "-m", "pip", "download", "--python-version", pythonversion, "--platform", "manylinux2014_x86_64", "-d",wheelsdir,"--only-binary=:all:",install])        
            except Exception as excep:
                try:
                    #download specific version for linux
                    subprocess.check_call([sys.executable, "-m", "pip", "download", "--python-version", pythonversion, "--platform", "linux_x86_64", "-d",wheelsdir,"--only-binary=:all:",install])        
                except Exception as excep:
                    try:
                        #download any version
                        y=re.split("([A-z-?]+)",install)
                        subprocess.check_call([sys.executable, "-m", "pip", "download", "--python-version", pythonversion, "--platform", "linux_x86_64", "-d",wheelsdir,"--only-binary=:all:",y[1]]) 
                    except Exception as excep:
                        # fail if neither works
                        raise Exception(f"Sorry but we cannot download the package {install}, please use a docker image that includes this package")
 
    else:
        # Nothing to install
        os.remove(req)
       
    # Deactivate the venv
    #subprocess.check_call(["deactivate"])

    return (target, inputs)
