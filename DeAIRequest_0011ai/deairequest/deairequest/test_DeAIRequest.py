import unittest
from pathlib import Path
import os

from .DeProtocolSelector import DeProtocolSelector

"""
Test the DeAIRequest
"""
class TestDeAIRequest(unittest.TestCase):
    def assertNotEmpty(self, obj):
        self.assertTrue(obj)

    def test_submit_job(self):
        bp = DeProtocolSelector("Bacalhau")
        self.assertEqual(bp.get_name(),"bacalhau","Expected name to be bacalhau")
        self.assertEqual(bp.get_icon(),Path(os.getcwd(),"logo.svg"), "Icon is not working")
        self.assertEqual(bp.get_ext(),"bhl", "Extension is not working")
        self.assertEqual(bp.get_data_types(),{"url","file","directory","ipfs"},"Expected data types")
        self.assertEqual(bp.get_url_data_type(),"url","Expected url data type")
        self.assertEqual(bp.get_file_data_type(),"file","Expected file data type")
        self.assertEqual(bp.get_directory_data_type(),"directory","Expected directory data type")
        self.assertEqual(bp.get_ipfs_data_type(),"ipfs","Expected ipfs data type")
        self.assertEqual(bp.get_docker_images(),["tensorflow/tensorflow-gpu:latest", "pytorch/pytorch:3.24", "python/python-mini:3.10"],"Expected docker images")
        bp.add_docker_image("test")
        self.assertEqual(bp.get_docker_images(),["tensorflow/tensorflow-gpu:latest", "pytorch/pytorch:3.24", "python/python-mini:3.10","test"],"Expected docker image add function to work")
        bp.remove_docker_image("test")
        self.assertEqual(bp.get_docker_images(),["tensorflow/tensorflow-gpu:latest", "pytorch/pytorch:3.24", "python/python-mini:3.10"],"Expected docker image remove function to work")
        self.assertEqual(bp.get_docker_image(),"","Docker image is supposed to be not set")
        bp.set_docker_image("test")
        self.assertEqual(bp.get_docker_image(),"test","set docker image not working")
        
        self.assertEqual(bp.get_datasets(),list(),"Expected empty datasets")
        bp.add_dataset(bp.get_url_data_type(),"url1")
        bp.add_dataset(bp.get_file_data_type(),"file1")
        bp.add_dataset(bp.get_directory_data_type(),"directory1")
        bp.add_dataset(bp.get_ipfs_data_type(),"ipfs1")
        compareds=[{"url":"url1"},{"file":"file1"},{"directory":"directory1"},{"ipfs":"ipfs1"}]
        self.assertEqual(bp.get_datasets(),compareds,"Add dataset not working")
        bp.remove_dataset(bp.get_ipfs_data_type(),"ipfs1")
        compareds=[{"url":"url1"},{"file":"file1"},{"directory":"directory1"}]
        self.assertEqual(bp.get_datasets(),compareds,"Remove dataset not working")
        
        job = bp.submit_job(Path("."))
        self.assertEqual(job,"123","Job ID should be 123")   
        logs = bp.get_logs(job) 
        self.assertNotEmpty(logs)
        result = bp.get_results(job,Path("."))
        self.assertNotEmpty(result)

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


if __name__ == '__main__':
    unittest.main()