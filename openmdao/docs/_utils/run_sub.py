"""
This is used by our doc build system to execute a code chunk in a subprocess while giving that code chunk
access to its containing module's globals.
"""

import os
import sys
import importlib
import numpy as np

if __name__ == '__main__':
    module_path = os.environ.get("OPENMDAO_CURRENT_MODULE", "").strip()
    if not module_path:
        raise RuntimeError("OPENMDAO_CURRENT_MODULE has not been set.")

    stdout_save = sys.stdout

    # send any output to dev/null during the import so it doesn't clutter our embedded code output
    with open(os.devnull, "w") as f:
        sys.stdout = f

        mod = importlib.import_module(module_path)

    sys.stdout = stdout_save

    code_to_run = os.environ.get("OPENMDAO_CODE_TO_RUN", "").strip()
    if not code_to_run:
        raise RuntimeError("OPENMDAO_CODE_TO_RUN has not been set")

    np.set_printoptions(precision=8)

    exec(code_to_run, mod.__dict__)

