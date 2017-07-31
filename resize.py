from PIL import Image
from pathlib import Path
import json
import sys

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

target_directory = file_path.parent / f"{file_path.stem}.imageset"
target_directory.mkdir(exist_ok=True)

contents_index = {"images": [], "info": {"verson": 1, "author": "xcode"}}

for factor in reversed(range(1, sizes + 1)):
    size = tuple(int(dimension * (factor/sizes)) for dimension in base.size)
    new_file = Path(target_directory) / f"{file_path.stem}@{factor}x{file_path.suffix}"
    base.resize(size).save(str(new_file))
    contents_index["images"].append({"size": f"{size[0]}x{size[1]}", "idiom": "universal", "filename": new_file.name, "scale": f"{factor}x"})

with open(str(target_directory / "Contents.json"), "w") as contents_file:
    json.dump(contents_index, contents_file, indent=2, separators=(",", " : "))