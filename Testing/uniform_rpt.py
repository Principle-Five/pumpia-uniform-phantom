import sys
from pathlib import Path

if str(Path(__file__).resolve().parent.parent) not in sys.path:
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from pumpia_uniform_phantom.scripts.run_uniform_rpt import run_repeat_uniform

run_repeat_uniform()
