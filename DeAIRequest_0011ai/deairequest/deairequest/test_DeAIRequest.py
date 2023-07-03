import unittest
from pathlib import Path
import os
import shutil
from .DeProtocolSelector import DeProtocolSelector
import time
from os.path import exists
import ipfshttpclient

"""
Test the DeAIRequest
"""
class TestDeAIRequest(unittest.TestCase):
    def assertNotEmpty(self, obj):
        self.assertTrue(obj)

    def setUp(self):
        path = os.path.abspath(os.path.dirname(__file__))
        if os.path.isfile(os.path.join(path,"docker_images.pv")):
            os.rename(os.path.join(path,"docker_images.pv"),os.path.join(path,"docker_images.pv.bak"))
        shutil.copyfile(os.path.join(path,"docker_images.pv.test"),os.path.join(path,"docker_images.pv"))         

    def tearDown(self):
        path = os.path.abspath(os.path.dirname(__file__))
        os.remove(os.path.join(path,"docker_images.pv")) 
        if os.path.isfile(os.path.join(path,"docker_images.pv.bak")):
            os.rename(os.path.join(path,"docker_images.pv.bak"),os.path.join(path,"docker_images.pv"))
    def test_data(self):
        bp = DeProtocolSelector("Bacalhau")
        path = os.path.abspath(os.path.dirname(__file__))
        bp.add_docker_image("amaksimov/python_data_science:latest")
        bp.set_docker_image("amaksimov/python_data_science:latest")
        #bp.add_dataset(bp.get_url_data_type(),"https://raw.githubusercontent.com/awesomedata/apd-core/master/core/Museums/Minneapolis-Institute-of-Arts-metadata.yml",True)
        bp.add_dataset(bp.get_url_data_type(),"https://raw.githubusercontent.com/awesomedata/apd-core/master/core/Museums/Minneapolis-Institute-of-Arts-metadata.yml",False)
        #bp.add_dataset(bp.get_file_data_type(),os.path.join(path,Path("test.txt")),True)
        bp.add_dataset(bp.get_file_data_type(),os.path.join(path,Path("test.txt")),False)
        #bp.add_dataset(bp.get_directory_data_type(),os.path.join(path,Path("testdata")),True)
        bp.add_dataset(bp.get_directory_data_type(),os.path.join(path,Path("testdata")),False)
        try:
            api = ipfshttpclient.connect()
            cid = api.add(os.path.join(path,"testdata",Path("test.txt")))
            cid=cid.as_json().get("Hash")
        finally:
            if api != None:
                api.close()
        bp.add_dataset(bp.get_ipfs_data_type(),cid,True)
        bp.add_dataset(bp.get_ipfs_data_type(),cid,False)
        job = bp.submit_job(os.path.join(path,Path("test2.ipynb")))
        self.assertNotEmpty(job)
        #print(job)

    def test_submit_job(self):
        bp = DeProtocolSelector("Bacalhau")
        path = os.path.abspath(os.path.dirname(__file__))
        self.assertEqual(bp.get_name(),"Bacalhau","Expected name to be bacalhau")
        self.assertEqual(bp.get_icon(),Path(os.getcwd(),"logo.svg"), "Icon is not working")
        self.assertEqual(bp.get_ext(),"bhl", "Extension is not working")
        self.assertEqual(bp.get_data_types(),{"url","file","directory","ipfs"},"Expected data types")
        self.assertEqual(bp.get_url_data_type(),"url","Expected url data type")
        self.assertEqual(bp.get_file_data_type(),"file","Expected file data type")
        self.assertEqual(bp.get_directory_data_type(),"directory","Expected directory data type")
        self.assertEqual(bp.get_ipfs_data_type(),"ipfs","Expected ipfs data type")
        self.assertEqual(bp.get_docker_images(),["amaksimov/python_data_science:latest","tensorflow/tensorflow:latest-gpu-jupyter", "pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime", "python:3"],"Expected docker images")
        bp.add_docker_image("pypy:latest")
        bp.set_docker_image("pypy:latest")
        self.assertEqual(bp.get_docker_image(),"pypy:latest","set docker image not working")
        self.assertEqual(bp.get_docker_images(),["amaksimov/python_data_science:latest","tensorflow/tensorflow:latest-gpu-jupyter", "pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime", "python:3","pypy:latest"],"Expected docker image add function to work")
        bp.remove_docker_image("pypy:latest")
        self.assertEqual(bp.get_docker_images(),["amaksimov/python_data_science:latest","tensorflow/tensorflow:latest-gpu-jupyter", "pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime", "python:3"],"Expected docker image remove function to work")
        self.assertEqual(bp.get_docker_image(),"","Docker image is supposed to be not set")

        bp.remove_datasets()
        self.assertEqual(bp.get_datasets(),list(),"Expected empty datasets")
        bp.add_dataset(bp.get_url_data_type(),"https://raw.githubusercontent.com/awesomedata/apd-core/master/core/Museums/Minneapolis-Institute-of-Arts-metadata.yml",True)
        bp.add_dataset(bp.get_file_data_type(),os.path.join(path,"testdata",Path("test.txt")),False)
        bp.add_dataset(bp.get_directory_data_type(),os.path.join(path,"testdata"),True)
        bp.add_dataset(bp.get_ipfs_data_type(),"ipfs1",False)
        compareds=[{"url":{"value":"https://raw.githubusercontent.com/awesomedata/apd-core/master/core/Museums/Minneapolis-Institute-of-Arts-metadata.yml","encrypted":True}},{"file":{"value":os.path.join(path,"testdata",Path("test.txt")),"encrypted":False}},{"directory":{"value":os.path.join(path,"testdata"),"encrypted":True}},{"ipfs":{"value":"ipfs1","encrypted":False}}]
        bp.remove_dataset(bp.get_ipfs_data_type(),"ipfs1",False)
        compareds=[{"url":{"value":"https://raw.githubusercontent.com/awesomedata/apd-core/master/core/Museums/Minneapolis-Institute-of-Arts-metadata.yml","encrypted":True}},{"file":{"value":os.path.join(path,"testdata",Path("test.txt")),"encrypted":False}},{"directory":{"value":os.path.join(path,"testdata"),"encrypted":True}}]
        self.assertEqual(bp.get_datasets(),compareds,"Remove dataset not working")

        bp.add_docker_image("amaksimov/python_data_science:latest")
        bp.set_docker_image("amaksimov/python_data_science:latest")
        path = os.path.abspath(os.path.dirname(__file__))
        job = bp.submit_job(os.path.join(path,Path("test.ipynb")))
        #print(job)
        self.assertNotEmpty(job)
        state=bp.get_state(job)
        while state=="InProgress":
            time.sleep(0.25)
            state=bp.get_state(job)
        self.assertEqual(state,"Completed","Job state not working.")
        logs = bp.get_logs(job) 
        self.assertNotEmpty(logs)
        if not exists("temp"):
            os.mkdir("temp")
        try:
            bp.get_results(job,Path("temp"))
            for directory in os.listdir(Path("temp")):
                self.assertTrue(exists(os.path.join("temp",directory,"exitCode")))
                try:
                    f = open(os.path.join("temp",directory,"exitCode"),"r")
                    self.assertEqual(f.read(),"0","Bacalhau job did not finish successfully")
                finally:
                    f.close()
                self.assertTrue(exists(os.path.join("temp",directory,"stdout")))
                self.assertTrue(exists(os.path.join("temp",directory,"stderr")))
                self.assertTrue(exists(os.path.join("temp",directory,"outputs")))
        finally:
            shutil.rmtree("temp")

        bp.add_docker_image("python:3")
        bp.set_docker_image("python:3")
        path = os.path.abspath(os.path.dirname(__file__))
        job = bp.submit_job(os.path.join(path,Path("test.ipynb")))
        self.assertNotEmpty(job)
        state=bp.get_state(job)
        while state=="InProgress":
            time.sleep(0.25)
            state=bp.get_state(job)
        self.assertEqual(state,"Completed","Job state not working.")
        logs = bp.get_logs(job) 
        self.assertNotEmpty(logs)
        if not exists("temp"):
            os.mkdir("temp")
        try:
            bp.get_results(job,Path("temp"))
            for directory in os.listdir(Path("temp")):
                self.assertTrue(exists(os.path.join("temp",directory,"exitCode")))
                try:
                    f = open(os.path.join("temp",directory,"exitCode"),"r")
                    self.assertEqual(f.read(),"0","Bacalhau job did not finish successfully")
                finally:
                    f.close()
                    f = open(os.path.join("temp",directory,"stderr"),"r")
                    print(f.readlines())
                    f.close()
                self.assertTrue(exists(os.path.join("temp",directory,"stdout")))
                self.assertTrue(exists(os.path.join("temp",directory,"stderr")))
                self.assertTrue(exists(os.path.join("temp",directory,"outputs")))
        finally:
            shutil.rmtree("temp")

        
        

    def test_error_submit_job(self):
        ep = DeProtocolSelector("Error")
        with self.assertRaises(Exception) as context:
            ep.set_docker_image("test")
        self.assertTrue('Docker image not supported', context.exception)
        with self.assertRaises(Exception) as context:
            image=ep.get_docker_image()
        self.assertTrue('Docker image not supported', context.exception)
        with self.assertRaises(Exception) as context:
            job = ep.submit_job(Path("."))
        self.assertTrue('job not supported', context.exception)
        with self.assertRaises(Exception) as context:
            ep.get_logs("123")
        self.assertTrue('job not supported', context.exception)
        with self.assertRaises(Exception) as context:
            ep.get_results("123",Path("."))
        self.assertTrue('job not supported', context.exception)
        self.assertEqual(ep.get_state("123"),"Error","Get state is not working")

if __name__ == '__main__':
    unittest.main()