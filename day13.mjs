import { promises } from "fs";

const sample = `6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5`;

solve(sample);
console.log("");
const input = await promises.readFile("input13");
solve(input.toString());

function solve(input) {
  const parts = input.split("\n\n");

  const dots = parts[0]
    .split("\n")
    .filter((e) => Boolean(e))
    .map((e) => e.match(/\d+/g).map((c) => Number(c)));

  const folds = parts[1]
    .split("\n")
    .filter((e) => Boolean(e))
    .map((e) => e.match(/([xy])=(\d+)/).slice(1, 3))
    .map((j) => [j[0], Number(j[1])]);

  // if fold along y, any y > y_fold turns into y_fold-(y-y_fold)
  // e.g. fold at 7, and 3,10 turns into 3,7-(10-7) = 3,4
  // or, 3, 2*y_fold-y, so 14-10
  let part1 = false;
  for (const fold of folds) {
    switch (fold[0]) {
      case "x":
        for (const dot of dots) {
          if (dot[0] > fold[1]) dot[0] = 2 * fold[1] - dot[0];
        }
        break;
      case "y":
        for (const dot of dots) {
          if (dot[1] > fold[1]) dot[1] = 2 * fold[1] - dot[1];
        }
        break;
      default:
        console.log(`bad fold ${fold}`);
    }
    if (!part1) {
      part1 = true;
      const dotsSet = new Set(dots.map((dot) => dot.join(",")));
      console.log(`#1: ${dotsSet.size}`);
    }
  }

  const dotsSet = new Set(dots.map((dot) => dot.join(",")));
  // x1, y1, x2, y2
  const minmax = dots.reduce(
    (m, dot) => [
      m ? Math.min(dot[0], m[0]) : dot[0],
      m ? Math.min(dot[1], m[1]) : dot[1],
      m ? Math.max(dot[0], m[2]) : dot[0],
      m ? Math.max(dot[1], m[3]) : dot[1],
    ],
    null
  );
  console.log("#2:");
  for (let y = minmax[1]; y <= minmax[3]; y++) {
    let row = "";
    for (let x = minmax[0]; x <= minmax[2]; x++) {
      if (dotsSet.has([x, y].join(","))) row += "#";
      else row += ".";
    }
    console.log(row);
  }
}
