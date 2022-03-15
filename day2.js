"use strict";

const fs = require("fs");

function part1(steps) {
  let depth = 0;
  let pos = 0;
  for (const { direction, dist } of steps) {
    switch (direction) {
      case "forward":
        pos += dist;
        break;
      case "down":
        depth += dist;
        break;
      case "up":
        depth -= dist;
        break;
    }
  }
  return depth * pos;
}

function part2(steps) {
  let aim = 0;
  let depth = 0;
  let pos = 0;
  for (const { direction, dist } of steps) {
    switch (direction) {
      case "forward":
        pos += dist;
        depth += dist * aim;
        break;
      case "down":
        aim += dist;
        break;
      case "up":
        aim -= dist;
        break;
    }
  }
  return depth * pos;
}

const sample = `forward 5
down 5
forward 8
up 3
down 8
forward 2
`
  .split("\n")
  .filter((x) => Boolean(x))
  .map((line) => {
    const parts = line.split(" ");
    return { direction: parts[0], dist: Number(parts[1]) };
  });

console.log("sample1", part1(sample));
console.log("sample2", part2(sample));

fs.readFile("input2", "utf8", (err, data) => {
  if (err) {
    console.error(err);
    return;
  }
  const steps = data
    .split("\n")
    .filter((x) => Boolean(x))
    .map((line) => {
      const [direction, num] = line.split(" ");
      const obj = { direction, dist: Number(num) };
      return obj;
    });
  console.log("part1", part1(steps));
  console.log("part2", part2(steps));
});
