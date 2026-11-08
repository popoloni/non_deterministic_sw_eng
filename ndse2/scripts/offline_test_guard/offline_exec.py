"""Run a Python command with an explicit test-only socket guard."""
from pathlib import Path
import os, runpy, sys
runpy.run_path(str(Path(__file__).with_name("sitecustomize.py")))
args=sys.argv[1:]
sys.path.insert(0, os.getcwd())
if not args:
    raise SystemExit("Expected a module, code string or script")
if args[0]=="-m":
    module=args[1];sys.argv=[module]+args[2:]
    runpy.run_module(module,run_name="__main__",alter_sys=True)
elif args[0]=="-c":
    code=args[1];sys.argv=["-c"]+args[2:]
    exec(compile(code,"<guarded command>","exec"),{"__name__":"__main__"})
else:
    script=Path(args[0]).resolve();sys.argv=[str(script)]+args[1:]
    sys.path.insert(0,str(script.parent))
    runpy.run_path(str(script),run_name="__main__")
