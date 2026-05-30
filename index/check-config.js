// Validate LaTeX index configuration (.sty, .ist, Makefile, .tex)
const fs = require('fs');
const path = require('path');
const { PROJECT_ROOT, formatSection, heading, pass, fail, warn, info } = require('./utils');

function check() {
  const lines = [];
  let passes = 0, failures = 0, warnings = 0;

  lines.push(formatSection('Configuration Validation'));

  // ---- TopologyBook.sty ----
  lines.push(heading('TopologyBook.sty'));
  const styPath = path.join(PROJECT_ROOT, 'TopologyBook.sty');
  const sty = fs.readFileSync(styPath, 'utf8');

  function styCheck(label, pattern, severity) {
    if (pattern.test(sty)) {
      lines.push(pass(label));
      passes++;
    } else {
      if (severity === 'warn') { lines.push(warn(label)); warnings++; }
      else { lines.push(fail(label)); failures++; }
    }
  }

  styCheck('makeidx package loaded', /\\usepackage\{makeidx\}/, 'fail');
  styCheck('\\makeindex present', /\\makeindex/, 'fail');
  styCheck('\\idx defined (L1 bold-slanted)', /\\newcommand\{\\idx\}\[1\]\{\\index\{#1\}/, 'fail');
  styCheck('\\idxsub defined (L2 only)', /\\newcommand\{\\idxsub\}\[2\]\{\\index\{#1!#2\}\}/, 'fail');
  styCheck('\\idxmath defined (math sort-key)', /\\newcommand\{\\idxmath\}\[2\]\{\\index\{#1@#2\}/, 'fail');
  styCheck('\\idxfmt defined (bold slanted formatting)', /\\newcommand\{\\idxfmt\}/, 'fail');
  styCheck('\\lettergroup defined (alphabet headers)', /\\newcommand\{\\lettergroup\}/, 'fail');
  styCheck('hyperindex=false set', /hyperindex\s*=\s*false/, 'warn');

  // ---- Topology_by_Munkres.ist ----
  lines.push(heading('Topology_by_Munkres.ist'));
  const istPath = path.join(PROJECT_ROOT, 'Topology_by_Munkres.ist');
  if (!fs.existsSync(istPath)) {
    lines.push(fail('.ist file missing'));
    failures++;
  } else {
    const ist = fs.readFileSync(istPath, 'utf8');
    const istChecks = [
      ['File exists', true],
      ['heading_prefix uses \\lettergroup', /lettergroup/],
      ['headings_flag = 1', /headings_flag\s+1/],
      ['preamble/postamble present', /preamble.*postamble/s],
    ];
    for (const [label, pattern] of istChecks) {
      if (pattern === true || (typeof pattern === 'object' && pattern.test(ist))) {
        lines.push(pass(label));
        passes++;
      } else {
        lines.push(fail(label));
        failures++;
      }
    }
  }

  // ---- Makefile ----
  lines.push(heading('Makefile'));
  const mkPath = path.join(PROJECT_ROOT, 'Makefile');
  const mk = fs.readFileSync(mkPath, 'utf8');
  const mkChecks = [
    ['makeindex recipe found', /makeindex/],
    ['makeindex has -s flag (style file)', /makeindex\s.*-s/],
    ['Targets .idx file', /\.idx/],
  ];
  for (const [label, pattern] of mkChecks) {
    if (pattern.test(mk)) { lines.push(pass(label)); passes++; }
    else { lines.push(fail(label)); failures++; }
  }

  // ---- Topology_by_Munkres.tex ----
  lines.push(heading('Main file (Topology_by_Munkres.tex)'));
  const mainPath = path.join(PROJECT_ROOT, 'Topology_by_Munkres.tex');
  const main = fs.readFileSync(mainPath, 'utf8');
  if (/\\printindex/.test(main)) {
    lines.push(pass('\\printindex present'));
    passes++;
  } else {
    lines.push(fail('\\printindex missing'));
    failures++;
  }

  return { passes, failures, warnings, lines };
}

if (require.main === module) {
  const r = check();
  console.log(r.lines.join('\n'));
  process.exit(r.failures > 0 ? 1 : 0);
}

module.exports = { check };
