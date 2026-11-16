"""Render with a fresh Python kernel that is safe under amd64 emulation."""

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path


def main():
    # Preload modules that spawn subprocesses before ZeroMQ starts threads.
    # Rosetta can deadlock at fork after those threads block signals:
    # https://github.com/apple/container/issues/966
    bootstrap = """
import platform
platform.platform()
try:
    import matplotlib.pyplot
except ImportError:
    pass
try:
    from plotly.io import renderers
except ImportError:
    pass
from ipykernel.kernelapp import IPKernelApp
IPKernelApp.launch_instance()
"""
    with tempfile.TemporaryDirectory(prefix="ltee-jupyter-") as directory:
        kernel = Path(directory) / "kernels/python3"
        kernel.mkdir(parents=True)
        (kernel / "kernel.json").write_text(json.dumps({
            "argv": [sys.executable, "-c", bootstrap, "-f", "{connection_file}"],
            "display_name": "Python (LTEE locked environment)",
            "language": "python",
        }))
        env = os.environ.copy()
        env["JUPYTER_PATH"] = os.pathsep.join(
            p for p in (directory, env.get("JUPYTER_PATH", "")) if p
        )
        # No daemon may outlive this temporary kernelspec.
        result = subprocess.run([
            "quarto", "render", "reports/ltee-report.qmd", "--execute-daemon", "0"
        ], env=env)
        return result.returncode


if __name__ == "__main__":
    sys.exit(main())
