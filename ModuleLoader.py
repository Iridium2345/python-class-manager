import importlib
from pathlib import Path

import sys

def SubMods(ModulePath:Path,currpath):
    for i in ModulePath.iterdir():
        if i.is_dir():
            if i.joinpath("__init__.py").exists():
                yield i.name
        else:
            if i.suffix == ".py" and i!=currpath and i.name != "__main__.py":
                yield i.stem

def LoadAll(package,modpath:Path,currpath:Path):
    for i in SubMods(modpath,currpath):
        print(f"[ Auto Load ] Module {package}.{i} loaded")
        importlib.import_module(f".{i}",package)
        
print(sys.path)