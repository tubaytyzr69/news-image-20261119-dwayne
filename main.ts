// 19 November 2026 in one image — @dwayne's entry for make.fun's
// news-image-20261119 bounty. The picture is entry.png beside this
// file; this program copies it to the grader's output directory.
// Node 22, standard library only, no network, deterministic: the
// same bytes go out on every run.
//
// Local run: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
copyFileSync(new URL("./entry.png", import.meta.url), join(outDir, "entry.png"));
