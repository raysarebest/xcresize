from PIL import Image
from pathlib import Path
import sys
import os

if len(sys.argv) < 2:
    sys.exit("You must specify a file")

if len(sys.argv) >= 3:
    sizes = sys.argv[2]
else:
    sizes = 3

file_path = Path(sys.argv[1]).resolve()

if not file_path.is_file():
    sys.exit(f"The file \"{file_path}\" was not found")

try:
    base = Image.open(str(file_path))
except OSError:
    sys.exit(f"\"{sys.argv[1]}\" is not an image")

for factor in reversed(range(1, sizes + 1)):
    size = tuple(int(dimension * (factor/sizes)) for dimension in base.size)
    base.resize(size).save(f"{file_path.parent / file_path.stem}@{factor}x{file_path.suffix}")
