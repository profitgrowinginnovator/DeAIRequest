
import requests
from pathlib import Path
from deairequest.DeProtocol import DeProtocol

"""
The Bacalhau.org protocol
"""
class BacalhauProtocol(DeProtocol):
    docker_images = ["tensorflow/tensorflow-gpu:latest","pytorch/pytorch:3.24","python/python-mini:3.10"]
    docker_image = ""
    datasets = list(dict())

    """
    Get the type of protocol that is used
    @oaram self:
    @preturn: the name of the protocol
    @raise: exception is thrown if no name is supported
    """
    def get_name(self)->str:
        return "bacalhau"
    
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
        self.docker_images.append(value)

    """
    Set the docker image to use for this job
    @oaram self:
    @param value: the docker image
    @raise: exception is thrown if the docker image is not found
    """
    @classmethod
    def set_docker_image(self,value):
        self.docker_image = value

    """
    Remove a docker image
    @oaram self:
    @param value: the docker image
    @raise: exception is thrown if the docker image is not present or one of the standard images
    """
    @classmethod
    def remove_docker_image(self,value):
        self.docker_images.remove(value)

    """
    Add a dataset
    @oaram self:
    @param type: the type of data set
    @param value: the actual dataset
    @raise: exception is thrown if the type is not supported or the value is not valid.
    """
    @classmethod
    def add_dataset(self,type,value):
        self.datasets.append({type:value})

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
    @param value: the value of the dataset [e.g. if type is url, this is the url]
    """
    @classmethod
    def remove_dataset(self,type,value):
        self.datasets.remove({type:value})  

    """
    Submit a job to the specified protocol with optional params 
    @oaram self:
    @param ipynb Path: the Jupyter (Lab) Notebook to run remotely
    @param params: optional extra parameters
    @return: the job ID
    """
    @classmethod
    def submit_job(self, ipynb:Path, params="")->str:
        return "123"
    
    """
    Get the logs from the job
    @oaram self:
    @param job: the job id
    @return: the logs of the current job
    @raises: exception if the job id is not known
    """
    @classmethod
    def get_logs(self, job):
        return requests.get('https://httpbin.org/stream/20', stream=True)
    

    """
    Get the job results 
    @oaram self:
    @param job: the job id
    @param output Path: the directory where the output can be written
    @raises: exception if the job id is not known or the output path is not accessible
    """
    @classmethod
    def get_results(self, job, output:Path):
        return requests.get('https://httpbin.org/stream/20', stream=True)
    

