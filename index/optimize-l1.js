// Optimize remaining L1 entries — check findability and suggest fixes
const fs = require('fs');
const path = require('path');

const MISSING = [
  ['Ch11','Adjoining a 2-cell'],['Ch9','Antipode-preserving'],['Ch2','Boundary: of a set'],
  ['Ch10','Clockwise loop'],['Ch4','Cofinal'],['Ch9','Commutator subgroup'],
  ['Ch3','Compactness'],['Ch7','Completeness: and Baire condition'],
  ['Ch14','Cone'],['Ch2','Continuity: of algebraic operations in R'],
  ['Ch3','Coset'],['Ch4','Countable dense subset'],['Ch8','Cube in R^n'],
  ['Ch12','CW complex'],['Ch4','Directed set'],['Ch7','Distance from x to A'],
  ['Ch12','Edge: of curved triangle'],['Ch2','First-countability'],['Ch12','First homology group'],
  ['Ch9','Fixed point theorem: for B^n'],['Ch6','Functor'],
  ['Ch9','Functorial properties of h_*'],['Ch1','If ... then, meaning of'],
  ['Ch1','Indexed family of sets'],['Ch1','Infimum'],['Ch1','Intersection'],
  ['Ch3','Intervals in R: compactness'],['Ch12','Labelling scheme'],
  ['Ch1','Least upper bound'],['Ch1','Least upper bound property'],
  ['Ch3','Left coset'],['Ch2','Limit of a sequence'],['Ch8','Locally euclidean'],
  ['Ch1','Logical quantifiers'],['Ch2','Metric space'],['Ch4','Net'],
  ['Ch10','Nonseparation theorem: arc in S^2'],['Ch10','Nulhomotopy lemma'],
  ['Ch4','One-point compactification'],['Ch1','Onto function'],['Ch3','Open covering'],
  ['Ch1','Or, meaning of'],['Ch9','Path connectedness'],['Ch9','Path homotopy'],
  ['Ch9','Path-induced homomorphism'],['Ch7','Peano space'],
  ['Ch8','Plane in R^N'],['Ch2','Positive linear map: of intervals in R'],
  ['Ch1','Principle of recursive definition'],['Ch4','Regular Lindelof space: metrizability'],
  ['Ch12','Scheme'],['Ch4','Separates points from closed sets'],
  ['Ch10','Separation theorem: closed topologists sine curve'],
  ['Ch10','Simple closed curve'],['Ch7','Smirnov metrization theorem'],
  ['Ch2','Standard bounded metric'],['Ch2','Standard topology'],
  ['Ch6','Stone-Cech compactification'],['Ch2','Strictly finer topology'],
  ['Ch1','Strict partial order'],['Ch4','Subnet'],['Ch1','Supremum'],
  ['Ch11','System of free generators'],['Ch2','Topological imbedding'],
  ['Ch12','Torus-type scheme'],['Ch2','Tower'],['Ch8','Translation of R^N'],
  ['Ch13','2-manifold with boundary'],['Ch1','Uncountability'],
  ['Ch4','Vanish precisely on A'],['Ch3','Weak local connectedness'],['Ch11','Wedge of spaces'],
];

const ALIASES = {
  'Compactness': ['compact', 'compactness'], 'Cofinal': ['cofinal'], 'Coset': ['coset', 'left coset'],
  'Cone': ['mapping cone', 'cone over', 'cone'], 'Clockwise loop': ['clockwise', 'clock-wise'],
  'CW complex': ['cw complex', 'cw-complex'], 'Directed set': ['directed set'],
  'First-countability': ['first-countable', 'first countable'], 'Functor': ['functor'],
  'Infimum': ['infimum', 'greatest lower bound'], 'Intersection': ['intersection'],
  'Indexed family of sets': ['indexed family', 'indexing function'],
  'Least upper bound': ['least upper bound'], 'Least upper bound property': ['least upper bound property'],
  'Left coset': ['left coset'], 'Labelling scheme': ['labelling scheme', 'labeling scheme'],
  'Locally euclidean': ['locally euclidean'], 'Metric space': ['metric space'],
  'Net': ['a net ', 'convergent net'], 'Nulhomotopy lemma': ['nulhomotopy', 'nullhomotopy'],
  'Open covering': ['open covering', 'open cover'], 'One-point compactification': ['one-point compactification'],
  'Path connectedness': ['path connected', 'path-connected'], 'Path homotopy': ['path homotopy'],
  'Path-induced homomorphism': ['path-induced', 'path induced'], 'Peano space': ['peano space', 'peano curve'],
  'Principle of recursive definition': ['recursive definition', 'principle of recursive'],
  'Scheme': ['labelling scheme', 'proper labelling'], 'Separates points from closed sets': ['separates points from closed'],
  'Simple closed curve': ['simple closed curve'], 'Standard bounded metric': ['standard bounded metric'],
  'Strictly finer topology': ['strictly finer', 'finer topology'], 'Strict partial order': ['strict partial order'],
  'Subnet': ['subnet'], 'Supremum': ['supremum', 'least upper bound'],
  'Stone-Cech compactification': ['stone-\\v{C}ech', 'cech compactification', 'stone-cech'],
  'Topological imbedding': ['topological imbedding', 'imbedding theorem'],
  'Tower': ['tower'], 'Torus-type scheme': ['torus-type', 'torus type'],
  'Weak local connectedness': ['weak local connectedness', 'weakly locally connected'],
  'Wedge of spaces': ['wedge of spaces'], 'Standard topology': ['standard topology'],
  'Countable dense subset': ['countable dense', 'countable dense subset'],
  'Boundary: of a set': ['boundary of a set', 'boundary of'],
  'Completeness: and Baire condition': ['baire condition', 'completeness and baire'],
  'Commutator subgroup': ['commutator subgroup', 'commutator'],
  'Continuity: of algebraic operations in R': ['continuity of algebraic', 'algebraic operations in'],
  'Cube in R^n': ['cube in', 'n-dimensional cube'],
  'Distance from x to A': ['distance from', 'd(x,'],
  'Edge: of curved triangle': ['curved triangle', 'edge of'],
  'First homology group': ['first homology group', 'homology group'],
  'Fixed point theorem: for B^n': ['fixed point theorem', 'fixed point'],
  'Functorial properties of h_*': ['functorial properties'],
  'If ... then, meaning of': ['if ... then', 'meaning of'],
  'Intervals in R: compactness': ['intervals in', 'compactness'],
  'Limit of a sequence': ['limit of a sequence', 'convergent sequence'],
  'Logical quantifiers': ['logical quantifiers', 'quantifiers'],
  'Onto function': ['onto function', 'surjective function'],
  'Or, meaning of': ['meaning of or', 'exclusive or'],
  'Plane in R^N': ['plane in', 'k-plane'],
  'Positive linear map: of intervals in R': ['positive linear map', 'positive linear'],
  'Regular Lindelof space: metrizability': ['regular lindelof', 'lindelof space'],
  'Separation theorem: closed topologists sine curve': ['separation theorem', 'separates'],
  'Smirnov metrization theorem': ['smirnov'],
  'System of free generators': ['system of free generators', 'free generators'],
  'Translation of R^N': ['translation of', 'translation'],
  'Uncountability': ['uncountability', 'uncountable'],
  'Vanish precisely on A': ['vanish precisely', 'vanish'],
  '2-manifold with boundary': ['2-manifold with boundary', 'surface with boundary'],
  'Antipode-preserving': ['antipode-preserving', 'antipode preserving'],
  'Adjoining a 2-cell': ['adjoining a 2-cell', 'adjoining'],
};

const chaptersDir = path.join(__dirname, '..', 'chapters');
let foundCount = 0, notFoundCount = 0;

for (const [chLabel, term] of MISSING) {
  const chNum = parseInt(chLabel.replace('Ch', ''));
  const files = fs.readdirSync(chaptersDir).filter(f => f.startsWith('Chapter_' + chNum + '_'));
  if (!files.length) continue;
  const content = fs.readFileSync(path.join(chaptersDir, files[0]), 'utf8');
  const lc = content.toLowerCase();

  // Strip LaTeX but keep plain text
  let search = term.replace(/\\\(|\\\)/g, '').replace(/\\[a-zA-Z]+(\{[^}]*\})?/g, '').replace(/[{}]/g, '').trim().toLowerCase();
  if (search.length < 3) search = term.toLowerCase();

  let found = false, matched = '';
  const toTry = [search, ...(ALIASES[term] || [])];
  for (const t of toTry) {
    if (t && lc.includes(t.toLowerCase())) { found = true; matched = t; break; }
  }

  if (found) foundCount++; else notFoundCount++;
  console.log((found ? '✓  ' : '✗  ') + chLabel.padEnd(5) + '[' + matched.slice(0,30).padEnd(32) + '] ' + term.slice(0,55));
}

console.log('\nFound: ' + foundCount + ' / Not found: ' + notFoundCount + ' / Total: ' + MISSING.length);
