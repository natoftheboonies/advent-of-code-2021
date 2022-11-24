import { promises } from "fs";

const sample = `NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C`;

let puzzle = sample;
const dataBuf = await promises.readFile("input14");
puzzle = dataBuf.toString();

let [poly, rules] = puzzle.split("\n\n");
//console.log(poly);
rules = rules
  .split("\n")
  .filter((e) => Boolean(e))
  .map((rule) => rule.split(" -> "));
rules = new Map(rules);
//console.log(rules);

let poly_pairs = new Map();
for (let i = 0; i < poly.length - 1; i++) {
  let pair = poly.slice(i, i + 2);
  poly_pairs.set(pair, (poly_pairs.get(pair) ?? 0) + 1);
}

function evolve(poly_pairs) {
  const prior_pairs = new Map(poly_pairs);
  for (const [pair, insertCount] of prior_pairs) {
    // remove split pairs
    poly_pairs.set(pair, poly_pairs.get(pair) - prior_pairs.get(pair));
    // add replacement pairs
    const left = pair.charAt(0) + rules.get(pair);
    const right = rules.get(pair) + pair.charAt(1);
    poly_pairs.set(left, (poly_pairs.get(left) ?? 0) + insertCount);
    poly_pairs.set(right, (poly_pairs.get(right) ?? 0) + insertCount);
  }
  // trim empty pairs
  for (const pair of poly_pairs.keys()) {
    if (poly_pairs.get(pair) == 0) poly_pairs.delete(pair);
  }
  return poly_pairs;
}

function diffElements(poly_pairs) {
  const elements = new Map();
  for (const [pair, count] of poly_pairs) {
    const element = pair.charAt(0);
    elements.set(element, (elements.get(element) ?? 0) + count);
  }
  const tail = poly.charAt(poly.length - 1);
  elements.set(tail, elements.get(tail) + 1);

  return Math.max(...elements.values()) - Math.min(...elements.values());
}

for (let i = 0; i < 10; i++) {
  poly_pairs = evolve(poly_pairs);
}
console.log("#1:", diffElements(poly_pairs));

for (let i = 10; i < 40; i++) {
  poly_pairs = evolve(poly_pairs);
}
console.log("#2:", diffElements(poly_pairs));
