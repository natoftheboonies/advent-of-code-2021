import { promises } from "fs";

const sample = `0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2`;

let puzzle = sample;
const dataBuf = await promises.readFile("input5");
puzzle = dataBuf.toString();
const input = puzzle.split("\n").filter((line) => Boolean(line));

const lines = input.map((line) =>
  Array.from(line.match(/(\d+)/g)).map((n) => Number(n))
);

/*
const bar = lines.reduce((m, cur) => {
  const [x1, y1, x2, y2] = cur;
  return [
    m ? Math.min(x1, x2, m[0]) : Math.min(x1, x2),
    m ? Math.min(y1, y2, m[1]) : Math.min(y1, y2),
    m ? Math.max(x1, x2, m[2]) : Math.max(x1, x2),
    m ? Math.max(y1, y2, m[3]) : Math.max(y1, y2),
  ];
}, null);
console.log(bar);
*/

const grid = new Map();

for (const [x1, y1, x2, y2] of lines) {
  if (x1 == x2 || y1 == y2) {
    for (let x = Math.min(x1, x2); x <= Math.max(x1, x2); x++) {
      for (let y = Math.min(y1, y2); y <= Math.max(y1, y2); y++) {
        const key = `${x},${y}`;
        grid.set(key, grid.get(key) + 1 || 1);
      }
    }
  }
}
console.log("#1:", Array.from(grid.values()).filter((i) => i > 1).length);

// diagonals
for (const [x1, y1, x2, y2] of lines) {
  if (x1 != x2 && y1 != y2) {
    const xDir = x2 > x1 ? 1 : -1;
    const yDir = y2 > y1 ? 1 : -1;
    for (let d = 0; d <= Math.abs(x2 - x1); d++) {
      const x = x1 + d * xDir;
      const y = y1 + d * yDir;
      const key = `${x},${y}`;
      grid.set(key, grid.get(key) + 1 || 1);
    }
  }
}
console.log("#2:", Array.from(grid.values()).filter((i) => i > 1).length);
