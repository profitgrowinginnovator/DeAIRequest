from pathlib import Path
from DeAIRequest_0011ai.DeProtocol import DeProtocol
"""
Each method will raise an exception to test error scenarios
"""
class ErrorProtocol(DeProtocol):
    def get_name(self):
        raise Exception("Deprotocol not supported")

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
    def get_logs(self, job):
        raise Exception("job not supported")
    
    @classmethod
    def get_results(self, job, output:Path):
        raise Exception("job not supported")