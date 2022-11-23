import { readFile } from "fs";

const fuel = (crabs, goto) =>
  crabs.reduce((acc, crab) => acc + Math.abs(crab - goto), 0);

const fuel2 = (crabs, goto) =>
  crabs.reduce((acc, crab) => {
    const n = Math.abs(crab - goto);
    return acc + Math.round((n * (n + 1)) / 2);
  }, 0);

function solve(input) {
  const crabs = input
    .split(",")
    .map((e) => Number(e))
    .sort((a, b) => a - b);
  const [min, max] = [crabs[0], crabs[crabs.length - 1]];

  function solveLoop(fuelFunc) {
    let bestFuel;
    let best;

    for (let i = min; i <= max; i++) {
      const iFuel = fuelFunc(crabs, i);
      if (!bestFuel || iFuel < bestFuel) {
        bestFuel = iFuel;
        best = i;
      }
    }
    return bestFuel;
  }

  console.log(`1: ${solveLoop(fuel)}`);
  console.log(`2: ${solveLoop(fuel2)}`);
}

const sample = "16,1,2,0,4,2,7,1,2,14";
console.log("# sample");
solve(sample);

readFile("input7", "utf8", (err, data) => {
  if (err) {
    console.error(err);
    return;
  }
  console.log("# puzzle");
  solve(data);
});
