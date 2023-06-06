# Hacks to support importing vendored dependencies as if they were installed
# locally via `poetry add`:
from pathlib import Path
import sys

conda_path = Path(__file__).parent / "vendor/conda"
sys.path.insert(0, str(conda_path))

pipreqs_path = Path(__file__).parent / "vendor/pipreqs"
sys.path.insert(0, str(pipreqs_path))

bacalhauapi_path = Path(__file__).parent / "vendor/bacalhau_apiclient/python"
sys.path.insert(0, str(bacalhauapi_path))

bacalhausdk_path = Path(__file__).parent / "vendor/bacalhau_sdk"
sys.path.insert(0, str(bacalhausdk_path))

# Clean up locals:
del Path
del sys
del conda_path
del pipreqs_path
del bacalhauapi_path
del bacalhausdk_path

# Imports and registers all backend runtime options:
import bacalhauconnector.ops.runtime_options
import bacalhauconnector.ops.bacalhau.options