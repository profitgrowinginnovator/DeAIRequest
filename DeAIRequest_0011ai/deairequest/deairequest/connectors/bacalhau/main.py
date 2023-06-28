from deairequest.connectors.bacalhau import notebooks, backends
import tempfile
import os
from pathlib import Path

def main(notebook:Path, name:str, imagetag:str)->str:

    target=tempfile.mkdtemp()
    config = dict({
        'notebook':{
            'name': name
        },
        'environments':{
            'default':{
                'image_tag': imagetag
            }
        }
    })
    base_path, root_file = notebooks.compile(notebook, target)
    return backends.bdeploy(base_path, root_file, config)

if __name__ == "__main__":
    main()