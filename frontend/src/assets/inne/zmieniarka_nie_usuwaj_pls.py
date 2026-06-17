#########################################################
#                                                       #
#     Skrypt ktory dostaje obrazki zetonow z frakcji    #
#     w INPUT_DIR, wycina je i wsadza do OUTPUT_DIR     #
#     grafika musi byc 150x140, inaczej pomija          #
#     musisz sam dodac tarcze do jednostek z pancerzem  #
#                                                       #
#########################################################

from PIL import Image, ImageChops
import cairosvg
import os
import xml.etree.ElementTree as ET
from io import BytesIO

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_DIR = os.path.join(BASE_DIR, "borgo")
OUTPUT_DIR = os.path.join(BASE_DIR, "borgo_wycieta")
SVG_FILE = os.path.join(BASE_DIR, "path_my_nie_usuwaj_pls.svg")
CROP_TO_PATH_BOUNDS = True

SVG_NS = "http://www.w3.org/2000/svg"
SHAPE_TAGS = {
    f"{{{SVG_NS}}}path",
    f"{{{SVG_NS}}}polygon",
    f"{{{SVG_NS}}}polyline",
    f"{{{SVG_NS}}}rect",
    f"{{{SVG_NS}}}circle",
    f"{{{SVG_NS}}}ellipse",
}


def open_as_rgba(path):
    image = Image.open(path)
    if image.mode == "P" and "transparency" in image.info:
        image.apply_transparency()

    return image.convert("RGBA")


def svg_mask_bytes(path):
    tree = ET.parse(path)
    root = tree.getroot()

    for element in root.iter():
        if element.tag not in SHAPE_TAGS:
            continue

        element.set("fill", "black")
        element.set("stroke", "none")
        element.attrib.pop("stroke-width", None)

        style = element.get("style")
        if style:
            rules = [
                rule.strip()
                for rule in style.split(";")
                if rule.strip() and not rule.strip().startswith(("fill:", "stroke:", "stroke-width:"))
            ]
            rules.extend(["fill:black", "stroke:none"])
            element.set("style", ";".join(rules))

    return ET.tostring(root, encoding="utf-8")

os.makedirs(OUTPUT_DIR, exist_ok=True)

png_data = cairosvg.svg2png(
    bytestring=svg_mask_bytes(SVG_FILE),
    output_width=150,
    output_height=140
)

mask = Image.open(BytesIO(png_data)).convert("RGBA")

alpha = mask.split()[3]
path_bbox = alpha.getbbox()

if path_bbox is None:
    raise ValueError("Maska z SVG jest pusta")

for filename in os.listdir(INPUT_DIR):
    if not filename.lower().endswith(".png"):
        continue

    src = open_as_rgba(os.path.join(INPUT_DIR, filename))

    # upewnij się że rozmiar się zgadza
    if src.size != (150, 140):
        print(f"Pomijam {filename}: {src.size}")
        continue

    src_alpha = src.getchannel("A")
    src.putalpha(ImageChops.multiply(src_alpha, alpha))

    if CROP_TO_PATH_BOUNDS:
        src = src.crop(path_bbox)

    src.save(
        os.path.join(OUTPUT_DIR, filename)
    )

    print("OK:", filename)

print("Gotowe")
