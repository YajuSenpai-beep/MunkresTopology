// Audit skipped L1 entries — check if they can be found in .tex with better search
const fs = require('fs');
const path = require('path');

const SKIPPED = [
  ['Ch1','Counterimage'],['Ch1','Inf A'],['Ch1','Infimum'],['Ch1','m-tuple'],['Ch1','omega-tuple'],
  ['Ch1','R^n'],['Ch1','S_bar_Omega'],['Ch1','Sup A'],['Ch1','Supremum'],['Ch1','Zermelo'],
  ['Ch2','Ball, unit'],['Ch2','Bd A'],['Ch2','epsilon-ball'],['Ch2','First-countability'],
  ['Ch2','Hilbert cube'],['Ch2','Int A'],['Ch2','ell-two topology'],['Ch2','T1 axiom'],['Ch2','Tower'],
  ['Ch3','Bicompactness'],['Ch3','Coset'],['Ch3','epsilon-neighborhood'],['Ch3','Left coset'],
  ['Ch3','Perfect map'],['Ch3','R^n - 0'],['Ch3','S^n (unit sphere)'],
  ['Ch4','Cofinal'],['Ch4','Curve'],['Ch4','Directed set'],['Ch4','G_delta set'],
  ['Ch4','Line with two origins'],['Ch4','Net'],['Ch4','Second-countability'],['Ch4','Subnet'],
  ['Ch4','T_i axioms'],['Ch4','2-manifold'],
  ['Ch6','F_sigma set'],['Ch6','Functor'],['Ch6','sigma-locally discrete'],
  ['Ch6','sigma-locally finite'],['Ch6','Stone-Cech compactification'],
  ['Ch7','sigma-compact'],
  ['Ch8','Cube in R^n'],['Ch8','k-plane'],
  ['Ch9','widehat_alpha'],['Ch9','[f]'],['Ch9','k-fold covering'],['Ch9','Star-convex set'],
  ['Ch11','Clockwise loop'],['Ch11','2-cell'],
  ['Ch12','CW complex'],['Ch12','m-fold projective plane'],['Ch12','n-fold torus'],
  ['Ch13','Normalizer'],['Ch13','2-manifold with boundary'],
  ['Ch14','Cone'],
];

const ALIASES = {
  'Counterimage': ['counterimage', 'counter-image', 'preimage', 'inverse image'],
  'Inf A': ['infimum', 'greatest lower bound', 'inf a'],
  'Infimum': ['infimum', 'greatest lower bound'],
  'Sup A': ['supremum', 'least upper bound', 'sup a'],
  'Supremum': ['supremum', 'least upper bound'],
  'Bd A': ['boundary of', 'bd a', 'boundary'],
  'Int A': ['interior of', 'int a', 'interior'],
  'First-countability': ['first-countable', 'first countable', 'first axiom'],
  'Second-countability': ['second-countable', 'second countable', 'second axiom'],
  'Hilbert cube': ['hilbert cube'],
  'Bicompactness': ['bicompact', 'bicompactness'],
  'Perfect map': ['perfect map'],
  'Cofinal': ['cofinal'],
  'Curve': ['curve', 'simple closed curve', 'peano curve'],
  'Directed set': ['directed set'],
  'Line with two origins': ['two origins', 'line with two'],
  'Net': ['a net ', 'convergent net', 'directed set'],
  'Subnet': ['subnet'],
  'Stone-Cech compactification': ['stone-cech', 'cech compact', 'stone-Čech'],
  'Functor': ['functor'],
  'Normalizer': ['normalizer', 'normaliser'],
  'Cone': ['mapping cone', 'cone over'],
  'CW complex': ['cw complex', 'cw-complex'],
  'Clockwise loop': ['clockwise', 'clock-wise'],
  'k-fold covering': ['k-fold', 'k fold cover'],
  'Star-convex set': ['star-convex', 'star convex'],
  'Zermelo': ['zermelo'],
  'Tower': ['tower'],
  'T1 axiom': ['t_1 axiom', 't_1', 't1 space'],
  'T_i axioms': ['separation axioms', 't_i axioms', 't_i'],
  'G_delta set': ['g_delta', 'g-delta', 'g_δ', 'gδ'],
  'F_sigma set': ['f_sigma', 'f-sigma', 'f_σ', 'fσ'],
  'sigma-locally discrete': ['locally discrete', 'countably locally'],
  'sigma-locally finite': ['locally finite', 'countably locally'],
  'sigma-compact': ['sigma-compact', 'σ-compact', 'sigma compact'],
  'epsilon-ball': ['epsilon-ball', 'epsilon ball', 'ε-ball', 'e-ball'],
  'epsilon-neighborhood': ['epsilon-neighborhood', 'epsilon neighbourhood'],
  'ell-two topology': ['ell-two', 'l^2', 'little ell'],
  'R^n - 0': ['punctured', 'r^n - 0', 'r^n minus'],
  'S^n (unit sphere)': ['unit sphere', 's^n '],
  'Cube in R^n': ['cube in', 'n-dimensional cube'],
  'k-plane': ['k-plane', 'k plane'],
  '[f]': ['[f]', 'homotopy class', 'path-homotopy class'],
  'm-tuple': ['m-tuple', 'm tuple'],
  'omega-tuple': ['omega-tuple', 'ω-tuple'],
  'R^n': ['r^n', 'n-tuple', 'n dimensional euclidean', 'n-space'],
  'S_bar_Omega': ['bar s', 'overline s'],
  'widehat_alpha': ['widehat{\\\\alpha}', 'widehat', 'alpha'],
  'm-fold projective plane': ['m-fold', 'm fold projective', 'projective plane'],
  'n-fold torus': ['n-fold', 'n fold torus'],
  '2-cell': ['2-cell', 'two-cell', 'adjoining a 2-cell'],
  '2-manifold': ['2-manifold', 'two-manifold', '2 dimensional manifold', '2-manifold'],
  '2-manifold with boundary': ['2-manifold with boundary', 'surface with boundary'],
  'Ball, unit': ['unit ball', 'unit ball'],
};

const chaptersDir = path.join(__dirname, '..', 'chapters');
let totalFound = 0, totalMissing = 0;

for (const [chLabel, term] of SKIPPED) {
  const chNum = parseInt(chLabel.replace('Ch', ''));
  const files = fs.readdirSync(chaptersDir).filter(f =>
    f.startsWith('Chapter_' + chNum + '_') && f.endsWith('.tex')
  );
  if (!files.length) continue;
  const content = fs.readFileSync(path.join(chaptersDir, files[0]), 'utf8');
  const lc = content.toLowerCase();

  const toTry = [term.toLowerCase(), ...(ALIASES[term] || [])];
  let found = false;
  let matched = '';
  for (const t of toTry) {
    if (lc.includes(t.toLowerCase())) { found = true; matched = t; break; }
  }

  console.log((found ? '✓  ' : '✗  ') + chLabel + ' ' + term.padEnd(40) + (found ? '→ "' + matched + '"' : ''));
  if (found) totalFound++; else totalMissing++;
}

console.log('\nFound: ' + totalFound + ' / Missing: ' + totalMissing + ' / Total: ' + SKIPPED.length);
