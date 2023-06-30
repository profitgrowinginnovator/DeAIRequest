
import requests
from pathlib import Path
import os
from .DeProtocol import DeProtocol
import deairequest.connectors.bacalhau.querybhl as query
import deairequest.connectors.bacalhau.main as bcljob
from bacalhau_sdk.api import results, states, events
import ipfshttpclient
from os.path import exists

"""
The Bacalhau.org protocol
"""
class BacalhauProtocol(DeProtocol):
    docker_images = []
    docker_images_pyv = {}
    docker_image = ""
    datasets = list(dict())
    encrypt = True

    """
    Get the type of protocol that is used
    @oaram self:
    @preturn: the name of the protocol
    @raise: exception is thrown if no name is supported
    """
    @classmethod
    def get_name(self)->str:
        return "Bacalhau"
    
    """
    Get the icon of protocol that is used
    @oaram self:
    @preturn: the icon of the protocol
    @raise: exception is thrown if no name is supported
    """
    @classmethod
    def get_icon(self)->Path:
        return Path(os.getcwd(),"logo.svg")
    
    """
    Get the extension of protocol that is used
    @oaram self:
    @preturn: the extension of the protocol
    @raise: exception is thrown if no extension is supported
    """
    @classmethod
    def get_ext(self)->str:
        return "bhl"
    
    """
    Get all the supported data types of this type of protocol
    @oaram self:
    @preturn: the list of data types
    @raise: exception is thrown if no datatypes are supported
    """
    @classmethod
    def get_data_types(self) ->list:
        return {"url","file","directory","ipfs"}
    
    """
    Get the url data type
    @oaram self:
    @preturn: the url data type
    """
    @classmethod
    def get_url_data_type(self)->str:
        return "url"
    
    """
    Get the file data type
    @oaram self:
    @preturn: the file data type
    """
    @classmethod
    def get_file_data_type(self)->str:
        return "file"
    
    """
    Get the directory data type
    @oaram self:
    @preturn: the directory data type
    """
    @classmethod
    def get_directory_data_type(self)->str:
        return "directory"
    
    """
    Get the ipfs data type
    @oaram self:
    @preturn: the ipfs data type
    """
    @classmethod
    def get_ipfs_data_type(self)->str:
        return "ipfs"
    
    """
    Get all the docker images
    @oaram self:
    @return: a list of all the docker images
    @raise: exception is thrown if no docker images are available
    """
    @classmethod
    def get_docker_images(self)->list:
        path = os.path.abspath(os.path.dirname(__file__))
        try:
            f = open(os.path.join(path,"docker_images.pv"),"r")
            images=f.readlines()
        finally:
            f.close()
        for image in images:
            v=image.split("*")
            self.docker_images_pyv[v[0]] = v[1] 
        self.docker_images = list(self.docker_images_pyv.keys())
        return self.docker_images
    
    """
    Get the docker image set for this job
    @oaram self:
    @return: the docker image set for this job
    @raise: exception is thrown if no docker image is set
    """
    @classmethod
    def get_docker_image(self)->str:
        return self.docker_image

    """
    Add a docker image
    @oaram self:
    @param value: the docker image
    @raise: exception is thrown if the docker image is not found
    """
    @classmethod
    def add_docker_image(self,value):
        pythonv, reqs = query.query(value)
        path = os.path.abspath(os.path.dirname(__file__))
        try:
            with open(os.path.join(path,"docker_images.pv"), 'a') as f:
                f.write('%s*%s\n' % (value,pythonv))
        finally:
            f.close()
        name = value.replace("/","-")
        print(name)
        try:
            file = open(os.path.join(path,name+".req"),'w')
            for req in reqs:
                file.write('%s\n' % (req))
        finally:
            file.close()
        self.docker_images.append(value)
        self.docker_images_pyv[value]=pythonv

    """
    Set the docker image to use for this job
    @oaram self:
    @param value: the docker image
    @raise: exception is thrown if the docker image is not found
    """
    @classmethod
    def set_docker_image(self,value):
        if value not in self.docker_images:
            self.add_docker_image(value)
        self.docker_image = value

    """
    Remove a docker image
    @oaram self:
    @param value: the docker image
    @raise: exception is thrown if the docker image is not present or one of the standard images
    """
    @classmethod
    def remove_docker_image(self,value):
        path = os.path.abspath(os.path.dirname(__file__))
        self.docker_images.remove(value)
        self.docker_images_pyv.pop(value)
        if self.docker_image == value:
            self.docker_image=''
        try:
            with open(os.path.join(path,"docker_images.pv"), 'w') as f:
                for x in self.docker_images_pyv:
                    f.write('%s*%s' % (x,self.docker_images_pyv[x]))
        finally:
            f.close()


    """
    Add a dataset
    @oaram self:
    @param type: the type of data set
    @param value: the actual dataset
    @param encrypyed: true if needs to be encrypted and false if does not need to be encrypted
    @raise: exception is thrown if the type is not supported or the value is not valid.
    """
    @classmethod
    def add_dataset(self,type,value,encrypted):
        self.datasets.append({type:{"value":value,"encrypted":encrypted}})

    """
    Get all supported datasets
    @oaram self:
    @return a list with all the datasets with each entry being a dictonary of type and value
    """
    @classmethod
    def get_datasets(self)->list:
        return self.datasets
    
    """
    Remove a data set
    @oaram self:
    @param type: the type of data set
    @param encrypyed: true if needs to be encrypted and false if does not need to be encrypted
    @param value: the value of the dataset [e.g. if type is url, this is the url]
    """
    @classmethod
    def remove_dataset(self,type,value,encrypted):
        self.datasets.remove({type:{"value":value,"encrypted":encrypted}})  

    """
    Submit a job to the specified protocol with optional params 
    @oaram self:
    @param ipynb Path: the Jupyter (Lab) Notebook to run remotely
    @param params: optional extra parameters
    @return: the job ID
    """
    @classmethod
    def submit_job(self, ipynb:Path, params="")->str:
        name=os.path.basename(ipynb)
        name=name.replace('.ipynb','')
        pythonversion=self.docker_images_pyv[self.get_docker_image()]
        return bcljob.main(ipynb,name,self.get_docker_image(),pythonversion)
    
    """
    Get the logs from the job
    @oaram self:
    @param job: the job id
    @return: the logs of the current job
    @raises: exception if the job id is not known
    """
    @classmethod
    def get_logs(self, job):
        return events(job_id=job)
    
    """
    Get the job results 
    @oaram self:
    @param job: the job id
    @preturn the state of the job, either InProgress, Completed or Error
    @raises: exception if the job id is not known or the output path is not accessible
    """
    @classmethod
    def get_state(self, job)->str:
        return states(job_id=job).state.state

    """
    Get the job results 
    @oaram self:
    @param job: the job id
    @param output Path: the directory where the output can be written
    @raises: exception if the job id is not known or the output path is not accessible
    """
    @classmethod
    def get_results(self, job, output:Path):
        # get the result of the Bacalhau job
        resultout=results(job_id=job)
        cid=resultout.results[0].data.cid
        try:
            api = ipfshttpclient.connect()
            if not exists(output):
                os.mkdir(output)
            api.get(cid,output)
        finally:
            api.close()

    