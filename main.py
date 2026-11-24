"""Write the 23 November 2026 world-news image to /output/entry.png
for make.fun's 'news-image-20261123' bounty.

Version 4: the poster was redrawn by draw_poster_v4.py in this
repository — the v3 front page with its craft faults fixed: the
COP31 lead banner is taller with a 46px one-line headline, the
story cards are tighter with darker decks, and the six footer
briefs run in a 2x3 grid that keeps a real bottom margin. Same
stories as v1:
COP31, the Strait of Hormuz, the Banten factory fire, the Peru
quake, Seoul's AI-cheating resignation, the 'El Chapo Isidro'
arrest, BepiColombo at Mercury, and the Nigeria boat accident.
The program copies the finished image.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if os.path.getsize(dst) != os.path.getsize(src):
        raise RuntimeError("entry.png copy is incomplete")
    os.chmod(dst, 0o644)


if __name__ == "__main__":
    main()
