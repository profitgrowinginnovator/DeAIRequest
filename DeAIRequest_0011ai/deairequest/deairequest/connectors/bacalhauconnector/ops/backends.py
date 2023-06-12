from bacalhauconnector.data.config import SameConfig
from bacalhauconnector.data.step import Step
from pathlib import Path
from typing import Tuple
import bacalhauconnector.ops.bacalhau as bacalhau
import bacalhauconnector.ops.helpers
import tempfile
import click


def render(target: str, steps: list, config: SameConfig, compile_path: str = None) -> Tuple[Path, str]:
    target_renderers = {
        "bacalhau": bacalhau.render,
    }

    render_function = target_renderers.get(target, None)
    if render_function is None:
        raise ValueError(f"Unknown backend: {target}")

    if compile_path is None:
        compile_path = str(tempfile.mkdtemp())

    compile_path, root_module_name = render_function(compile_path, steps, config)
    return (compile_path, root_module_name)


def deploy(target: str, base_path: Path, root_file: str, config: SameConfig):
    target_deployers = {
        "bacalhau": bacalhau.deploy,
    }

    deploy_function = target_deployers.get(target, None)
    if deploy_function is None:
        raise ValueError(f"Unknown backend: {target}")

    click.echo(f"Files persisted in: {base_path}")
    deploy_return = deploy_function(base_path, root_file, config)

    return deploy_return
