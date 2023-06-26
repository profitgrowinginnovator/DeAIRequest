#from bacalhauconnector.data.config import SameConfig
from connectors.bacalhau.step import Step
from connectors.bacalhau.deploy import deploy
from connectors.bacalhau.render import render
from pathlib import Path
from typing import Tuple
#import bacalhauconnector.ops.bacalhau as bacalhau
#import bacalhauconnector.ops.helpers
import tempfile


def render(target: str, steps: list, compile_path: str = None) -> Tuple[Path, str]:
    if compile_path is None:
        compile_path = str(tempfile.mkdtemp())

    compile_path, root_module_name = render(compile_path, steps)
    return (compile_path, root_module_name)


def deploy(target: str, base_path: Path, root_file: str, config: SameConfig):
    target_deployers = {
        "bacalhau": bacalhau.deploy,
    }

    deploy_function = target_deployers.get(target, None)
    if deploy_function is None:
        raise ValueError(f"Unknown backend: {target}")

    #click.echo(f"Files persisted in: {base_path}")
    deploy_return = deploy_function(base_path, root_file, config)

    return deploy_return
