import subprocess
# import py.
from src import main
import sys
from pathlib import Path

if __name__ == '__main__':
    # subprocess.run(["python", "src/main.py"])
    # os.s
    # sys.path.append(".")
    sys.path.append(str(Path(main.__file__).parent))
    main.main()