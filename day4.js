"use strict";

const fs = require("fs");

const BoardProto = {
  init(rows) {
    this.rows = rows;
    this.cols = rows[0].map((_, i) => rows.map((b) => b[i]).reverse());
  },
  play(draws) {
    const self = this;
    for (const [i, draw] of draws.entries()) {
      // draws.forEach(function (draw, i) {
      // console.log(draw, self);
      self.rows.forEach((row) => {
        const match = row.indexOf(draw);
        if (match > -1) row.splice(match, 1);
      });
      self.cols.forEach((row) => {
        const match = row.indexOf(draw);
        if (match > -1) row.splice(match, 1);
      });
      if (
        self.rows.some((row) => row.length == 0) ||
        self.cols.some((row) => row.length == 0)
      ) {
        // win!
        // console.log("win at index", i, "with draw", draw);
        self.winIndex = i;
        self.winDraw = draw;
        self.score =
          this.rows.flat().reduce((acc, n) => acc + n) * this.winDraw;
        return;
      }
    }
  },
};

function solver(puzzle) {
  const draws = puzzle
    .shift()
    .split(",")
    .map((x) => parseInt(x));
  //console.log("draws", draws);

  const boards = puzzle.map((board) => {
    const lines = board.split("\n").filter((x) => Boolean(x.trim()));
    const next = lines.map((line) =>
      line.match(/\d+/g).map((x) => parseInt(x))
    );
    const newboard = Object.create(BoardProto);
    newboard.init(next);
    return newboard;
    // return new Board(next);
  });
  boards.forEach((board) => {
    board.play(draws);
  });
  const part1 = boards
    .slice(1)
    .reduce(
      (acc, board) => (board.winIndex < acc.winIndex ? board : acc),
      boards[0]
    );
  console.log("#1", part1.score);
  const part2 = boards
    .slice(1)
    .reduce(
      (acc, board) => (board.winIndex > acc.winIndex ? board : acc),
      boards[0]
    );
  console.log("#2", part2.score);
}

const puzzle =
  `7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
 `
    .split("\n\n")
    .filter((x) => Boolean(x));

console.log("# sample");
solver(puzzle);

fs.readFile("input4", "utf8", (err, data) => {
  if (err) {
    console.error(err);
    return;
  }
  const steps = data.split("\n\n").filter((x) => Boolean(x));
  console.log("# puzzle");
  solver(steps);
});
