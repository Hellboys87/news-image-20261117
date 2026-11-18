// main.ts -- the entry program for news-image-20261117.
//
// The artwork itself lives in this repository as entry.png, a
// 1024 x 1024 infographic of Tuesday 17 November 2026 that was drawn
// by generate.py. All this program has to do is deliver those exact
// bytes to the grader: it copies the PNG sitting next to this file
// into the output directory under the name entry.png.
//
// Where the copy lands:
//   * in the grading container, the MAKEFUN_OUTPUT_DIR variable is
//     unset and the destination defaults to /output/entry.png;
//   * for a local smoke test, point the variable anywhere writable:
//         mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//     and out/entry.png should come out byte-identical to entry.png.
//
// Node 22 standard library only; there is nothing to install.

import { copyFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Resolve the folder this file runs from, so the PNG is found no
// matter which directory the caller happens to stand in.
const here = dirname(fileURLToPath(import.meta.url));
const sourcePng = join(here, "entry.png");

// The grader's mount point, with the documented local override.
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const destination = join(outputDir, "entry.png");

copyFileSync(sourcePng, destination);
