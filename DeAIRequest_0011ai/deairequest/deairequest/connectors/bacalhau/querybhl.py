from bacalhau_sdk.api import submit, results, events, states
from bacalhau_sdk.config import get_client_id
from bacalhau_apiclient.models.storage_spec import StorageSpec
from bacalhau_apiclient.models.spec import Spec
from bacalhau_apiclient.models.job_spec_language import JobSpecLanguage
from bacalhau_apiclient.models.job_spec_docker import JobSpecDocker
from bacalhau_apiclient.models.resource_usage_config import ResourceUsageConfig
from bacalhau_apiclient.models.publisher_spec import PublisherSpec
from bacalhau_apiclient.models.deal import Deal
from pathlib import Path
import sys
import time
import ipfshttpclient
import re

def query(docker: str):
    data = dict(
        APIVersion='V1beta1',
        ClientID=get_client_id(),
        Spec=Spec(
            engine="Docker",
            verifier="Noop",
            publisher_spec=PublisherSpec(type="ipfs"),
            docker=JobSpecDocker(
                image=docker,
                entrypoint=["/bin/sh","-c","python --version;pip freeze"],
                working_directory="/inputs",
            ),
            resources=ResourceUsageConfig(
                gpu="0",
            ),
            outputs=[
                StorageSpec(
                    storage_source="IPFS",
                    name="outputs",
                    path="/outputs",
                )
            ],
            language=JobSpecLanguage(job_context=None),
            wasm=None,
            timeout=1800,
            deal=Deal(concurrency=1, confidence=0, min_bids=0),
            do_not_track=False,
        ),
    )

    try:
        # get the python version and requirements.txt job running on the docker
        res = submit(data)
        # get the job id and wait until it changes from state in progress to either completed or error
        id = res.job.metadata.id
        state=states(job_id=id).state.state
        while state == 'InProgress':
            state=states(job_id=id).state.state
            print(state)
            time.sleep(0.25)
        
        # get the result of the Bacalhau job
        resultout=results(job_id=id)
        cid=resultout.results[0].data.cid
        # download the CID of the outputs directory
        api = ipfshttpclient.connect()
        result=api.ls(cid)
        # get the CID of the stdout file and gets its content
        stderrcid=result.as_json().get("Objects")[0].get("Links")[3].get("Hash")
        # first line contains Python 3.11.2 [or other version], rest of the lines are the requirements.txt of the Docker image
        response=api.cat(stderrcid).decode('utf-8')
        #python=response.partition('\n')[0]
        x=re.split("Python (3.[0-9][0-9]*).[0-9]+",response.partition('\n')[0])
        pythonversion=x[1]
        reqtxt=response.rpartition('\n')[2]
        print(reqtxt)

    except Exception as err:
        raise RuntimeError(f"The 'bacalhau' backend gave an error: {err}")
    

def cli(argv):
    query(argv[1])

if __name__ == "__main__":
    cli(sys.argv)
    