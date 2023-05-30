from abc import ABC,abstractmethod
from pathlib import Path

class DeProtocol(ABC):
    """
    Submit a job to the specified protocol with optional params 
    @oaram self:
    @param ipynb Path: the Jupyter (Lab) Notebook to run remotely
    @param params: optional extra parameters
    @return: the job ID
    """
    @abstractmethod
    def submit_job(self, ipynb:Path, params="")->str:
        pass

    """
    Get the logs from the job
    @oaram self:
    @param job: the job id
    @param params: optional extra parameters
    @return: the logs of the current job
    @raises: exception if the job id is not known
    """
    @abstractmethod
    def get_logs(self, job, params=""):
        pass

    """
    Get the job results 
    @oaram self:
    @param job: the job id
    @param output Path: the directory where the output can be written
    @raises: exception if the job id is not known or the output path is not accessible
    """
    @abstractmethod
    def get_results(self, job, output:Path):
        pass