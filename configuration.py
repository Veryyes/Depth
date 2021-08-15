import os
from pathlib import Path

STATIC_RESOURCES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "depth-ui", "build")

docs_dir = os.path.join(str(Path.home()), "Documents")
DB = os.path.join(docs_dir, "Depth.DB")