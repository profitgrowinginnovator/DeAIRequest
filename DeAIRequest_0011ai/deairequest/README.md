# The Decentralised AI Request   

Enable for any AI python code to be executed on decentralised AI compute.  

Supported AI compute:  
[Bacalhau](https://bacalhau.org)  

Commands:
python -m build # build the project  
python -m unittest # run all unit tests  

Usage:  
from deairequest import DeProtocolSelector as selector  
bp = selector.DeProtocolSelector("Bacalhau")  
bp.get_docker_images()  
if a user wants a custom image  
bp.add_docker_image("custom_images")  
For each request you need to set the docker image to use  
bp.set_docker_image("the docker image to use")  
  
To add datasets of type URL:  
bp.add_dataset(bp.get_url_data_type(),"https://www...")  
Of type File:  
bp.add_dataset(bp.get_file_data_type(),"/path/to/file/name.csv")  
Of type Directory:  
bp.add_dataset(bp.get_directory_data_type(),"/path/to/directory/")  
Of type IPFS:  
bp.add_dataset(bp.get_ipfs_data_type(),"AW233dfD23dsds32323sdds") # The IPFS CID  
To get all the datasets:  
bp.get_datasets()  
output: [{"url":"https://www..."},{"file":"/path/to/file/name.csv"},{"directory":"/path/to/directory/"},{"ipfs":"AW233dfD23dsds32323sdds"}]  
  
Afterwards you can submit a job  
job = bp.submit_job(Path("/path/to/notebook.jpynb"))  
get the logs  
logs = bp.get_logs(job)   
and when the job is finished, get the results  
result = bp.get_results(job,Path("/path/to/output/directory/"))  