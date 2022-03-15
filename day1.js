"use strict";

const fs = require("fs");

function part1(depths) {
  let increases = 0;
  let prev;
  for (const depth of depths) {
    if (depth > prev) increases++;
    prev = depth;
  }
  return increases;
}

function part2(depths) {
  // const depths = lines.map(x => Number(x));
  let last = depths.slice(0, 3).reduce((x, y) => x + y, 0);

  let counter = 0;
  for (let i = 1; i < depths.length - 2; i++) {
    const current = depths.slice(i, i + 3).reduce((x, y) => x + y, 0);
    //console.log(current, last)
    if (current > last) counter++;
    last = current;
  }
  return counter;
}

const sample = `199
200
208
210
200
207
240
269
260
263`
  .split("\n")
  .map((x) => Number(x));

console.log("sample", part1(sample), part2(sample));

fs.readFile("input1", "utf8", (err, data) => {
  if (err) {
    console.error(err);
    return;
  }
  const depths = data.split("\n").map((x) => Number(x));
  console.log("part1", part1(depths));
  console.log("part2", part2(depths));
});
