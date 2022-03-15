"use strict";

const fs = require("fs");

const puzzle = `v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>`.split("\n");

solver(puzzle);

function solver(puzzle) {
  let seafloor = new Map();

  const max_y = puzzle.length;
  const max_x = puzzle[0].length;

  for (const [y, line] of puzzle.entries()) {
    for (const [x, char] of [...line].entries()) {
      if (">v".includes(char)) {
        const key = `${x}-${y}`;
        seafloor.set(key, char);
      }
    }
  }

  function print_seafloor(sf) {
    for (const y of Array(max_y).keys()) {
      let rowStr = "";
      for (const x of Array(max_x).keys()) {
        const key = `${x}-${y}`;
        rowStr += sf.get(key) ?? ".";
      }
      console.log(rowStr);
    }
    console.log();
  }

  function next_seafloor(seafloor) {
    let moved = 0;
    const new_seafloor = new Map();
    for (const [key, char] of seafloor) {
      //console.log("key", key);
      if (char == ">") {
        let [x, y] = key.split("-").map((x) => parseInt(x));
        const dest_key = `${(x + 1) % max_x}-${y}`;
        if (!seafloor.has(dest_key)) {
          moved++;
          new_seafloor.set(dest_key, ">");
        } else {
          new_seafloor.set(key, ">");
        }
      }
    }
    for (const [key, char] of seafloor) {
      if (char == "v") {
        let [x, y] = key.split("-").map((x) => parseInt(x));
        const dest_key = `${x}-${(y + 1) % max_y}`;
        if (seafloor.get(dest_key) != "v" && !new_seafloor.has(dest_key)) {
          moved++;
          new_seafloor.set(dest_key, "v");
        } else {
          new_seafloor.set(key, "v");
        }
      }
    }

    return { moved, new_seafloor };
  }

  //print_seafloor(seafloor);

  for (let x = 1; x < 1000; x++) {
    let { moved, new_seafloor } = next_seafloor(seafloor);
    seafloor = new_seafloor;
    //   console.log(`After ${x} steps:`);
    //   print_seafloor(seafloor);
    if (moved === 0) {
      console.log("part1", x);
      break;
    }
  }
}

fs.readFile("input25", "utf8", (err, data) => {
  if (err) {
    console.error(err);
    return;
  }
  const steps = data.split("\n").filter((x) => Boolean(x));
  solver(steps);
});
