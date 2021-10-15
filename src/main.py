from typing import Set
import urllib.request
import tempfile
import fontTools.subset as subset
import fire

WINDOWS_31J_URL = "https://www.unicode.org/Public/MAPPINGS/VENDORS/MICSFT/WINDOWS/CP932.TXT"
FONT_URL = "https://github.com/googlefonts/noto-cjk/raw/main/Sans/SubsetOTF/JP/NotoSansJP-Regular.otf"


def get_font_path() -> str:
    """Downloads the font file as a temporary file and then returns the font file path."""
    font_file_path = tempfile.NamedTemporaryFile().name + ".otf"
    urllib.request.urlretrieve(FONT_URL, font_file_path)
    return font_file_path


def get_windows31j_unicodes() -> Set[int]:
    f = urllib.request.urlopen(WINDOWS_31J_URL)
    codes = set()
    while True:
        line = f.readline()
        if line == b"":
            break
        line = line.decode("utf-8")
        if line.startswith("#"):
            continue
        try:
            code = int(line.split("\t")[1], 16)
            codes.add(code)
        except:
            pass
    return codes


def run(save_path: str):
    """Customize Google Fonts to the Windows-31J character set to reduce size.

    Args:
        save_path (str): Location where font files are saved.
    """
    font_path = get_font_path()
    codes = get_windows31j_unicodes()

    unicode_command = ",".join([hex(code) for code in codes])

    SUBSET_COMMAND = f"pyftsubset {font_path} --output-file={save_path} --drop-tables=GPOS --passthrough-tables --unicodes={unicode_command} --no-hinting --layout-features=vert --glyph-names --symbol-cmap --legacy-cmap --notdef-glyph --notdef-outline --name-IDs=* --name-legacy --name-languages=* --recalc-average-width --recalc-bounds --recalc-timestamp --prune-unicode-ranges"
    args = SUBSET_COMMAND.split(" ")[1:]
    subset.main(args)


def main():
    fire.Fire(run)
