from pathlib import Path
import os
from deairequest.DeProtocol import DeProtocol
"""
Each method will raise an exception to test error scenarios
"""
class ErrorProtocol(DeProtocol):
    def get_name(self):
        return "Error"
    
    def get_icon(self):
        return Path(os.getcwd(),"logo.svg")
    
    def get_ext(self):
        return "err"

    def get_data_types(self):
        raise Exception("Data types not supported")
    
    @classmethod
    def add_docker_image(self,name):
        raise Exception("Docker image not supported")
    
    @classmethod
    def set_docker_image(self,name):
        raise Exception("Docker image not supported")
    
    @classmethod
    def get_docker_image(self)->str:
        raise Exception("Docker image not supported")

    @classmethod
    def remove_docker_image(self,name):
        raise Exception("Docker image not supported")

    @classmethod
    def add_dataset(self,type,name):
        raise Exception("dataset not supported")

    @classmethod
    def get_datasets(self):
        raise Exception("datasets not supported")
    
    @classmethod
    def remove_dataset(self,type,name):
        raise Exception("dataset not supported")

    @classmethod
    def submit_job(self, ipynb, params=""):
        raise Exception("job not supported")
        
    @classmethod
    def get_logs(self, job)->str:
        raise Exception("job not supported")
    
    @classmethod
    def get_results(self, job, output:Path):
        raise Exception("job not supported")
    
    @classmethod
    def get_state(self, job)->str:
        return "Error"