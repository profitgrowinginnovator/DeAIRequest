#from bacalhauconnector.data.config import SameConfig
from deairequest.connectors.bacalhau.deploy import deploy
from deairequest.connectors.bacalhau.render import render
from pathlib import Path
from typing import Tuple
#import bacalhauconnector.ops.bacalhau as bacalhau
#import bacalhauconnector.ops.helpers
import tempfile


def brender(target: str, steps: list, config: dict, compile_path: str = None) -> Tuple[Path, str]:
    if compile_path is None:
        compile_path = str(tempfile.mkdtemp())

    compile_path, root_module_name = render(target, steps, config, compile_path)
    return (compile_path, root_module_name)


def bdeploy(base_path: Path, root_file: str, config: dict):

    #click.echo(f"Files persisted in: {base_path}")
    deploy_return = deploy(base_path, root_file, config)

    return deploy_return
