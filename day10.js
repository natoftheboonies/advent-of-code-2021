"use strict";

const fs = require("fs");

const SCORES = new Map(
  Object.entries({ ")": 3, "]": 57, "}": 1197, ">": 25137 })
);

const PAIRS = new Map(
  Object.entries({ "(": ")", "{": "}", "[": "]", "<": ">" })
);

const COSTS = new Map(Object.entries({ ")": 1, "]": 2, "}": 3, ">": 4 }));

function solver(puzzle) {
  let total_score = 0;
  const costs = [];

  for (const line of puzzle) {
    // console.log("processing", line);
    let score = 0;
    let cost = 0;
    let stack = [];
    let corrupt = false;
    for (let char of [...line]) {
      // opening
      if (PAIRS.has(char)) stack.push(char);
      // closing
      else {
        // if ([...PAIRS.values()].includes(char))
        let left = stack.pop();
        if (PAIRS.get(left) != char) {
          //   console.log(`Expected ${PAIRS.get(left)}, but found ${char} instead`);
          score += SCORES.get(char);
          corrupt = true;
          break;
        }
      }
    }
    if (!corrupt) {
      while (stack.length > 0) {
        let left = stack.pop();
        cost *= 5;
        cost += COSTS.get(PAIRS.get(left));
      }
    }
    if (cost > 0) costs.push(cost);
    if (score > 0) total_score += score;
  }

  console.log("part1", total_score);
  const middle = costs.sort((a, b) => a - b)[Math.floor(costs.length / 2)];
  console.log("part2", middle);
}

const puzzle = `[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]`.split("\n");

//solver(puzzle);

fs.readFile("input10", "utf8", (err, data) => {
  if (err) {
    console.error(err);
    return;
  }
  const steps = data.split("\n").filter((x) => Boolean(x));
  solver(steps);
});
