"""Write the 23 November 2026 world-news image to /output/entry.png
for make.fun's 'news-image-20261123' bounty.

Version 3: the poster was redrawn by draw_poster_v3.py in this
repository — a front page's hierarchy: COP31 as a full-width lead
banner, four more stories as pictogram cards, and the remaining
stories as footer briefs. Same stories as v1:
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
