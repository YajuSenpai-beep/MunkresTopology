// Orchestrator: run all index checks and produce unified report
const { summaryLine, heading } = require('./utils');

const MODULES = [
  { name: 'Master JSON Validation',              path: './validate/master-json' },
  { name: 'Chapter JSON Validation',             path: './validate/chapter-jsons' },
  { name: 'Chapter-Master Cross-Reference',       path: './validate/crossref' },
  { name: 'Index Command Scan',                  path: './scan/commands' },
  { name: 'Coverage Analysis',                   path: './scan/coverage' },
  { name: 'Configuration Validation',            path: './check/config' },
  { name: 'Build Artifact Validation',           path: './check/build' },
];

if (require.main === module) {
  const args = process.argv.slice(2);
  const quick = args.includes('--quick');
  const jsonOut = args.includes('--json');

  const excluded = quick ? ['Index Command Scan', 'Coverage Analysis'] : [];

  const results = [];

  console.log('╔══════════════════════════════════════════════════════════════╗');
  console.log('║        MUNKRES TOPOLOGY — INDEX CHECKING SYSTEM             ║');
  console.log('╚══════════════════════════════════════════════════════════════╝\n');

  for (const mod of MODULES) {
    if (excluded.includes(mod.name)) continue;

    const script = require(mod.path);
    const r = script.check();

    results.push({ name: mod.name, ...r });

    const num = results.length;
    const status = r.failures > 0 ? 'FAIL' : (r.warnings > 0 ? 'WARN' : 'PASS');
    console.log(`  ${num}. ${mod.name} ${'.'.repeat(Math.max(2, 48 - mod.name.length))} ${status}  (${r.passes}P / ${r.failures}F / ${r.warnings}W)`);

    // Print details for failures only
    if (r.failures > 0 || (r.warnings > 0 && r.warnings < 20)) {
      for (const line of r.lines) {
        if (line.includes('[FAIL]') || (line.includes('[WARN]') && r.warnings < 10)) {
          console.log(line);
        }
      }
    }
  }

  // Summary
  console.log('\n  ' + '═'.repeat(65));
  const totalPasses = results.reduce((s, r) => s + r.passes, 0);
  const totalFailures = results.reduce((s, r) => s + r.failures, 0);
  const totalWarnings = results.reduce((s, r) => s + r.warnings, 0);
  const passCount = results.filter(r => r.failures === 0 && r.warnings === 0).length;
  const failCount = results.filter(r => r.failures > 0).length;
  const warnCount = results.filter(r => r.failures === 0 && r.warnings > 0).length;

  console.log(summaryLine('OVERALL:', passCount, failCount, warnCount));
  console.log(`  (${totalPasses} checks passed, ${totalFailures} failed, ${totalWarnings} warnings)`);

  if (totalFailures === 0 && totalWarnings > 0) {
    const allWarn = results.every(r => r.failures === 0) && results.some(r => r.warnings > 0);
    if (allWarn && totalFailures === 0) {
      console.log(`\n  Note: Most warnings are expected — the index has not been implemented yet.`);
    }
  }

  console.log('  ' + '═'.repeat(65));

  if (jsonOut) {
    console.log(JSON.stringify(results.map(r => ({
      name: r.name,
      passes: r.passes,
      failures: r.failures,
      warnings: r.warnings,
    })), null, 2));
  }

  process.exit(totalFailures > 0 ? 1 : 0);
} else {
  module.exports = { MODULES };
}
