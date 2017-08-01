from PIL import Image
from pathlib import Path
import colors
import PIL
import json
import sys

def fail(message):
    sys.exit(colors.red("ERROR: " + message))

def warn(message, confirm=False, confirmation_message=". Do you wish to continue?"):
    def abort():
        print(colors.red("Aborted"))
        sys.exit()
    print(colors.yellow("WARNING: " + message), end="")
    if confirm:
        print(colors.yellow(" " + confirmation_message + " ") + colors.green("Y") + colors.yellow("/") + colors.red("n"))
        answer = ""
        prompt = colors.yellow(">>> ")
        while answer != "y" and answer != "n" and answer != "yes" and answer != "no":
            try:
                answer = input(prompt).lower()
            except KeyboardInterrupt:
                print()
                abort()
            prompt = colors.yellow("I don't recognize that answer. Please answer with (") + colors.green("y") + colors.yellow(")es or (") + colors.red("n") + colors.yellow(")o")
        if answer == "n":
            abort()
    else:
        print()

if len(sys.argv) < 2:
    fail("You must specify a file")
    
file_path = Path(sys.argv[1]).resolve()

if not file_path.is_file():
    fail(f"The file \"{file_path}\" was not found")

if len(sys.argv) >= 3:
    output_directory = Path(sys.argv[2]).resolve()
    if not output_directory.is_dir():
        fail(f"The directory \"{output_directory}\" was not found")
else:
    output_directory = file_path.parent

should_warn_for_asset_bundle = True
for part in output_directory.parts:
    if part.endswith(".xcassets"):
        should_warn_for_asset_bundle = False

if should_warn_for_asset_bundle:
    warn("The output directory is not an asset bundle")

target_directory = output_directory / f"{file_path.stem}.imageset"

try:
    target_directory.mkdir()
except FileExistsError:
    warn(f"The file \"{target_directory}\" already exists.", confirm=True, confirmation_message="Overwrite?")

if len(sys.argv) >= 4:
    try:
        sizes = int(sys.argv[3])
    except ValueError:
        fail("The number of sizes must be an integer")
else:
    sizes = 3

try:
    base = Image.open(str(file_path))
except OSError:
    fail(f"\"{sys.argv[1]}\" is not an image")

contents_index = {"images": [], "info": {"verson": 1, "author": "xcresize"}}

for factor in reversed(range(1, sizes + 1)):
    size = tuple(int(dimension * (factor/sizes)) for dimension in base.size)
    new_file = Path(target_directory) / f"{file_path.stem}@{factor}x{file_path.suffix}"
    base.resize(size, Image.ANTIALIAS).save(str(new_file))
    contents_index["images"].append({"size": f"{size[0]}x{size[1]}", "idiom": "universal", "filename": new_file.name, "scale": f"{factor}x"})

with open(str(target_directory / "Contents.json"), "w") as contents_file:
    json.dump(contents_index, contents_file, indent=2, separators=(",", " : "))