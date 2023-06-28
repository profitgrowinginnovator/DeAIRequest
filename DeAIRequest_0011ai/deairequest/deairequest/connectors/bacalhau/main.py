from deairequest.connectors.bacalhau import notebooks, backends
import tempfile
import os

def main():

    target=tempfile.mkdtemp()
    notebook_path=os.path.join("/Users/maarten/Downloads/example-bs4.ipynb")
    config = dict({
        'notebook':{
            'name': "test"
        },
        'environments':{
            'default':{
                'image_tag': 'python'
            }
        }
    })
    base_path, root_file = notebooks.compile(notebook_path, target)
    backends.bdeploy(base_path, root_file, config)

if __name__ == "__main__":
    main()