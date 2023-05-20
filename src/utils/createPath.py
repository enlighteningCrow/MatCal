from pathlib import Path

def createPath(path: Path):
    if not path.exists():
        # make that path if it does not exist
        for i in range(0, len(path.parts)):
            curPath = Path(*path.parts[0:i + 1])
            if not curPath.exists():
                curPath.mkdir()

