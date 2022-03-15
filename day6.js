"use strict";

const fs = require("fs");

function solve(fishes) {
  const queue = [0, 0, 0, 0, 0, 0, 0, 0, 0];
  for (const fish of fishes) queue[fish]++;

  for (let t = 0; t < 80; t++) {
    const to_breed = queue[0];
    // push on end, shift is popleft
    queue.push(queue.shift());
    queue[6] += to_breed;
  }
  let result = queue.reduce((x, y) => x + y, 0);
  console.log("part1", result);
  for (let t = 80; t < 256; t++) {
    const to_breed = queue[0];
    queue.push(queue.shift());
    queue[6] += to_breed;
  }
  result = queue.reduce((x, y) => x + y, 0);
  console.log("part2", result);
}

const puzzle = "3,4,3,1,2".split(",").map((x) => Number(x));
console.log("# sample");
solve(puzzle);

fs.readFile("input6", "utf8", (err, data) => {
  if (err) {
    console.error(err);
    return;
  }
  const steps = data.split(",").map((line) => Number(line));
  console.log("# puzzle");
  solve(steps);
});
