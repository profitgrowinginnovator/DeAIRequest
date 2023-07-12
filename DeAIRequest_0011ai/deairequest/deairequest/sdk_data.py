from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from os import path


class sdk_torch():
    remote=False

    def set_remote(self,remote: bool):
        self.remote=remote

    def get_remote(self)->bool:
        return self.remote
    def get_data(source: str, encrypt_remote: True)->Dataset:
        pass

    def load_data(source: str, encrypt_remote: True)->DataLoader:
        pass
