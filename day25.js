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
  // let seafloor = new Map();

  const max_y = puzzle.length;
  const max_x = puzzle[0].length;
  // https://stackoverflow.com/questions/18163234/declare-an-empty-two-dimensional-array-in-javascript
  // cannot do: new Array(5).fill(new Array(4).fill(0))
  //let seafloor = new Array(max_y).fill(0).map(() => new Array(max_x).fill(0));
  let seafloor = Array.from({ length: max_y }, () => new Array(max_x).fill(0));

  // for (const [y, line] of puzzle.entries()) {
  //   for (const [x, char] of [...line].entries()) {
  puzzle.forEach((line, y) => {
    line.split("").forEach((char, x) => {
      if (">v".includes(char)) {
        // const key = `${x}-${y}`;
        // seafloor.set(key, char);
        seafloor[y][x] = char;
      }
    });
  });

  function print_seafloor(sf) {
    for (let y = 0; y < max_y; y++) {
      let rowStr = "";
      for (let x = 0; x < max_x; x++) {
        //const key = `${x}-${y}`;
        rowStr += sf[y][x] || ".";
      }
      console.log(rowStr);
    }
    console.log();
  }

  function next_seafloor(seafloor) {
    let moved = 0;
    const new_seafloor = new Array(max_y)
      .fill(0)
      .map(() => new Array(max_x).fill(0));
    //for (const [y, row] of seafloor.entries()) {
    //for (const [x, char] of row.entries()) {
    seafloor.forEach((row, y) => {
      row.forEach((char, x) => {
        //console.log("key", key);
        if (char == ">") {
          const [dest_x, dest_y] = [(x + 1) % max_x, y];
          if (!seafloor[dest_y][dest_x]) {
            moved++;
            new_seafloor[dest_y][dest_x] = ">";
          } else {
            new_seafloor[y][x] = ">";
          }
        }
      });
    });
    // for (const [y, row] of seafloor.entries()) {
    //   for (const [x, char] of row.entries()) {
    seafloor.forEach((row, y) => {
      row.forEach((char, x) => {
        if (char == "v") {
          const [dest_x, dest_y] = [x, (y + 1) % max_y];
          if (
            seafloor[dest_y][dest_x] != "v" &&
            !new_seafloor[dest_y][dest_x]
          ) {
            moved++;
            new_seafloor[dest_y][dest_x] = "v";
          } else {
            new_seafloor[y][x] = "v";
          }
        }
      });
    });

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
