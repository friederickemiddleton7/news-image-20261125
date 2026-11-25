# World News — 25 November 2026

This repository holds one 1024×1024 PNG poster that sums up the world news of **25 November 2026**. The date names the day in the largest type on the page, and beneath it the day's most consequential stories are laid out across six continents and several fields, with short labels and flat pictograms so a reader who missed the day can follow each story, and an "ALSO TODAY" strip carrying further briefs.

`main.py` is the standard-library-only entrypoint: it copies the committed `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png`) byte-identically, validating the file size, the PNG signature and its 1024×1024 IHDR dimensions, and refusing anything else. `make_image.py` drew `entry.png` at build time with Pillow (2× supersampled for crisp edges), asserting that every text run stays inside its card, that no run overlaps another run or a pictogram, and that no type falls below 19 px; the grader never runs it.

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/friederickemiddleton7/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/friederickemiddleton7/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

[![license: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

Run: `MAKEFUN_OUTPUT_DIR=out python3 main.py`

Bounty page: https://make.fun/bounty/news-image-20261125
