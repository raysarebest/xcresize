from PIL import Image
from pathlib import Path
import colors
import PIL
import json
import sys

if len(sys.argv) < 2:
    sys.exit("You must specify a file")
    
file_path = Path(sys.argv[1]).resolve()

if not file_path.is_file():
    sys.exit(f"The file \"{file_path}\" was not found")

if len(sys.argv) >= 3:
    output_directory = Path(sys.argv[2]).resolve()
    if not output_directory.is_dir():
        sys.exit(f"The directory \"{output_directory}\" was not found")
else:
    output_directory = file_path.parent

if output_directory.suffix != ".xcassets":
    print(colors.yellow("The output directory is not an asset bundle. Are you sure you wish to continue? ") + colors.green('Y') + colors.yellow("/") + colors.red('n'))

    answer = ""
    prompt = ">>> "
    while answer != "y" and answer != "n":
        answer = input(prompt).lower()
        prompt = "I don't recognize that answer. Please answer with (y)es or (n)o"
    
    if answer == "n":
        print("Aborted")
        sys.exit()

if len(sys.argv) >= 4:
    sizes = sys.argv[3]
else:
    sizes = 3

try:
    base = Image.open(str(file_path))
except OSError:
    sys.exit(f"\"{sys.argv[1]}\" is not an image")

target_directory = output_directory / f"{file_path.stem}.imageset"
target_directory.mkdir(exist_ok=True)

contents_index = {"images": [], "info": {"verson": 1, "author": "xcode"}}

for factor in reversed(range(1, sizes + 1)):
    size = tuple(int(dimension * (factor/sizes)) for dimension in base.size)
    new_file = Path(target_directory) / f"{file_path.stem}@{factor}x{file_path.suffix}"
    base.resize(size, Image.ANTIALIAS).save(str(new_file))
    contents_index["images"].append({"size": f"{size[0]}x{size[1]}", "idiom": "universal", "filename": new_file.name, "scale": f"{factor}x"})

with open(str(target_directory / "Contents.json"), "w") as contents_file:
    json.dump(contents_index, contents_file, indent=2, separators=(",", " : "))