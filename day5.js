"use strict";

const fs = require("fs");

const puzzle = `0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2`.split("\n");

function print_sample(gridmap, max_x, max_y) {
  for (let y = 0; y <= max_y; y++) {
    let lineStr = "";
    for (let x = 0; x <= max_x; x++) {
      const key = y * (max_x + 1) + x;
      if (gridmap.has(key)) lineStr += gridmap.get(key);
      else lineStr += ".";
    }
    console.log(lineStr);
  }
  console.log("");
}

function solve(puzzle) {
  const lines = puzzle.map((line) => {
    const bits = [...line.match(/\d+/g)].map((n) => parseInt(n));
    const obj = {};
    [obj.x1, obj.y1, obj.x2, obj.y2] = bits;
    return obj;
  });

  const min_x = Math.min(...lines.map((line) => [line.x1, line.x2]).flat());
  const max_x = Math.max(...lines.map((line) => [line.x1, line.x2]).flat());
  const min_y = Math.min(...lines.map((line) => [line.y1, line.y2]).flat());
  const max_y = Math.max(...lines.map((line) => [line.y1, line.y2]).flat());
  console.log(min_x, max_x, min_y, max_y);

  const gridmap = new Map();

  lines.forEach((line) => {
    if (line.x1 == line.x2 || line.y1 == line.y2) {
      const [x_min, x_max] =
        line.x1 < line.x2 ? [line.x1, line.x2] : [line.x2, line.x1];
      const [y_min, y_max] =
        line.y1 < line.y2 ? [line.y1, line.y2] : [line.y2, line.y1];
      for (let x = x_min; x < x_max + 1; x++) {
        for (let y = y_min; y < y_max + 1; y++) {
          const key = y * (max_x + 1) + x;
          gridmap.set(key, (gridmap.get(key) ?? 0) + 1);
        }
      }
    }
  });

  const part1 = [...gridmap.values()].filter((n) => n > 1).length;
  console.log("#1", part1);

  lines.forEach((line) => {
    if (line.x1 != line.x2 && line.y1 != line.y2) {
      const x_dir = line.x1 < line.x2 ? 1 : -1;
      const y_dir = line.y1 < line.y2 ? 1 : -1;
      for (let dist = 0; dist < Math.abs(line.x2 - line.x1) + 1; dist++) {
        const x = line.x1 + dist * x_dir;
        const y = line.y1 + dist * y_dir;
        const key = y * (max_x + 1) + x;

        gridmap.set(key, (gridmap.get(key) ?? 0) + 1);
      }
    }
  });

  const part2 = [...gridmap.values()].filter((n) => n > 1).length;

  console.log("#2", part2, gridmap.size);
}

console.log("# sample");
solve(puzzle);

fs.readFile("input5", "utf8", (err, data) => {
  if (err) {
    console.error(err);
    return;
  }
  const steps = data.split("\n").filter((x) => Boolean(x));
  console.log("# puzzle");
  solve(steps);
});
