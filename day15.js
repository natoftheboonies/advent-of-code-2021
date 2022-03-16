"use strict";

const fs = require("fs");

// collect https://github.com/luciopaiva/heapify
const { MinQueue } = require("heapify");
// try my own priority queue?
// https://medium.com/@adriennetjohnson/a-walkthrough-of-dijkstras-algorithm-in-javascript-e94b74192026

const DIRS = [
  [0, 1],
  [1, 0],
  [0, -1],
  [-1, 0],
];

function solve(puzzle) {
  const maze = [];
  for (const line of puzzle) {
    //console.log(line);
    maze.push(line.split("").map((x) => parseInt(x)));
  }

  const dim = { row: maze.length, col: maze[0].length };
  console.log("maze dim", dim);

  function djikstra(mult = 1) {
    const goal = [dim.col * mult - 1, dim.row * mult - 1];
    const shortest = new Map([[0, 0]]);
    console.log("goal is", goal);

    const heap = new MinQueue(1024);
    // need integer keys, so use y*(dim.col*mult)+x
    heap.push(0, 0);

    while (heap.size) {
      const base_cost = heap.peekPriority();
      const last = heap.pop();
      const hy = Math.floor(last / (dim.row * mult));
      const hx = last % (dim.row * mult);
      if (hx == goal[0] && hy == goal[1]) {
        console.log("goal!", heap.size);

        return base_cost;
      }
      for (const [dx, dy] of DIRS) {
        const x = hx + dx;
        const y = hy + dy;
        if (x > goal[0] || x < 0 || y > goal[1] || y < 0) continue;
        const key = y * dim.row * mult + x;
        // compute adjusted cost for nodes beyond maze
        let cost =
          maze[y % dim.row][x % dim.col] +
          Math.floor(x / dim.col) +
          Math.floor(y / dim.row);
        // pt2: wrap cost after 9 to 1
        while (cost > 9) cost -= 9;
        // new cost for this node
        const neighbor_cost = base_cost + cost;
        if ((shortest.get(key) ?? 9999) > neighbor_cost) {
          //console.log("set", key, "priority", neighbor_cost);
          shortest.set(key, neighbor_cost);
          heap.push(key, neighbor_cost);
        }
      }
    }
  }

  console.log("part1", djikstra());
  console.log("part2", djikstra(5));
}

// sample
/*
const puzzle = `1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581`.split("\n");

solve(puzzle);
*/

fs.readFile("input15", "utf8", (err, data) => {
  if (err) {
    console.error(err);
    return;
  }
  const steps = data.split("\n").filter((x) => Boolean(x));
  solve(steps);
});
