import unittest
from pathlib import Path
import os
import shutil
from .DeProtocolSelector import DeProtocolSelector
import time
from os.path import exists

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
        

    def test_submit_job(self):
        bp = DeProtocolSelector("Bacalhau")
        self.assertEqual(bp.get_name(),"Bacalhau","Expected name to be bacalhau")
        self.assertEqual(bp.get_icon(),Path(os.getcwd(),"logo.svg"), "Icon is not working")
        self.assertEqual(bp.get_ext(),"bhl", "Extension is not working")
        self.assertEqual(bp.get_data_types(),{"url","file","directory","ipfs"},"Expected data types")
        self.assertEqual(bp.get_url_data_type(),"url","Expected url data type")
        self.assertEqual(bp.get_file_data_type(),"file","Expected file data type")
        self.assertEqual(bp.get_directory_data_type(),"directory","Expected directory data type")
        self.assertEqual(bp.get_ipfs_data_type(),"ipfs","Expected ipfs data type")
        self.assertEqual(bp.get_docker_images(),["tensorflow/tensorflow:latest-gpu", "pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime", "python:3"],"Expected docker images")
        bp.add_docker_image("pypy:latest")
        bp.set_docker_image("pypy:latest")
        self.assertEqual(bp.get_docker_image(),"pypy:latest","set docker image not working")
        self.assertEqual(bp.get_docker_images(),["tensorflow/tensorflow:latest-gpu", "pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime", "python:3","pypy:latest"],"Expected docker image add function to work")
        bp.remove_docker_image("pypy:latest")
        self.assertEqual(bp.get_docker_images(),["tensorflow/tensorflow:latest-gpu", "pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime", "python:3"],"Expected docker image remove function to work")
        self.assertEqual(bp.get_docker_image(),"","Docker image is supposed to be not set")

        self.assertEqual(bp.get_datasets(),list(),"Expected empty datasets")
        bp.add_dataset(bp.get_url_data_type(),"url1",True)
        bp.add_dataset(bp.get_file_data_type(),"file1",False)
        bp.add_dataset(bp.get_directory_data_type(),"directory1",True)
        bp.add_dataset(bp.get_ipfs_data_type(),"ipfs1",False)
        compareds=[{"url":{"value":"url1","encrypted":True}},{"file":{"value":"file1","encrypted":False}},{"directory":{"value":"directory1","encrypted":True}},{"ipfs":{"value":"ipfs1","encrypted":False}}]
        bp.remove_dataset(bp.get_ipfs_data_type(),"ipfs1",False)
        compareds=[{"url":{"value":"url1","encrypted":True}},{"file":{"value":"file1","encrypted":False}},{"directory":{"value":"directory1","encrypted":True}}]
        self.assertEqual(bp.get_datasets(),compareds,"Remove dataset not working")

        bp.add_docker_image("amaksimov/python_data_science:latest")
        bp.set_docker_image("amaksimov/python_data_science:latest")
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