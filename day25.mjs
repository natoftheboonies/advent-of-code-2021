import { promises } from "fs";

let sample = `...>...
.......
......>
v.....>
......>
.......
..vvv..`;

sample = `v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>`;

const printGrid = (grid) => grid.forEach((row) => console.log(row.join("")));

function march(input) {
  const stage1 = input.map((row) => row.slice());
  const max_y = input.length;
  const max_x = input[0].length;
  let stuck = true;
  // move right
  input.forEach((row, y) =>
    row.forEach((char, x) => {
      if (char == ">") {
        const dest_x = x < max_x - 1 ? x + 1 : 0;
        if (input[y][dest_x] == ".") {
          stuck = false;
          stage1[y][x] = ".";
          stage1[y][dest_x] = ">";
        }
      }
    })
  );

  const stage2 = stage1.map((row) => row.slice());
  // move down
  stage1.forEach((row, y) =>
    row.forEach((char, x) => {
      if (char == "v") {
        const dest_y = y < max_y - 1 ? y + 1 : 0;
        if (stage1[dest_y][x] == ".") {
          stuck = false;
          stage2[y][x] = ".";
          stage2[dest_y][x] = "v";
        }
      }
    })
  );
  if (!stuck) return stage2;
  else return;
}

const puzzle = await promises.readFile("input25");
sample = puzzle.toString();

const input = sample
  .split("\n")
  .filter((e) => Boolean(e))
  .map((row) => row.split(""));
const max_y = input.length;
const max_x = input[0].length;
//console.log(max_x, max_y);
const grid = new Array(max_y).fill().map((_) => new Array(max_x));
input.forEach((row, y) => row.forEach((char, x) => (grid[y][x] = char)));

let state = grid;
for (let i = 0; i < 1000; i++) {
  state = march(state);
  if (!state) {
    console.log("#1:", i + 1);
    break;
  }
}
