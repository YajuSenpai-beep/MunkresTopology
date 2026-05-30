// Shared utilities for index-checking scripts
const fs = require('fs');
const path = require('path');

const PROJECT_ROOT = path.resolve(__dirname, '..');

function loadJSON(filePath) {
  const fullPath = path.resolve(PROJECT_ROOT, filePath);
  try {
    const raw = fs.readFileSync(fullPath, 'utf8');
    const data = JSON.parse(raw);
    return { data, error: null };
  } catch (e) {
    return { data: null, error: e.message };
  }
}

function braceMatch(str, openPos) {
  // str[openPos] must be '{'
  let depth = 1;
  let i = openPos + 1;
  while (i < str.length && depth > 0) {
    if (str[i] === '\\') { i += 2; continue; }
    if (str[i] === '{') depth++;
    if (str[i] === '}') depth--;
    i++;
  }
  return depth === 0 ? i - 1 : -1;
}

function extractCommands(content) {
  const idx = [];
  const idxmath = [];
  const idxsub = [];

  function findAll(prefix) {
    const results = [];
    let i = 0;
    const pattern = '\\' + prefix + '{';
    while ((i = content.indexOf(pattern, i)) !== -1) {
      const argStart = i + pattern.length - 1; // position of opening '{'
      const argEnd = braceMatch(content, argStart);
      if (argEnd === -1) { i += pattern.length; continue; }
      const arg1 = content.slice(argStart + 1, argEnd);
      results.push({ arg: arg1, pos: i });
      i = argEnd + 1;
    }
    return results;
  }

  function findAll2(prefix) {
    const results = [];
    let i = 0;
    const pattern = '\\' + prefix + '{';
    while ((i = content.indexOf(pattern, i)) !== -1) {
      const arg1Start = i + pattern.length - 1;
      const arg1End = braceMatch(content, arg1Start);
      if (arg1End === -1) { i += pattern.length; continue; }
      const arg1 = content.slice(arg1Start + 1, arg1End);
      // find second arg: skip whitespace, expect '{'
      let j = arg1End + 1;
      while (j < content.length && content[j] !== '{') {
        if (content[j] !== ' ' && content[j] !== '\n' && content[j] !== '\t' && content[j] !== '\r') break;
        j++;
      }
      if (j >= content.length || content[j] !== '{') { i = arg1End + 1; continue; }
      const arg2End = braceMatch(content, j);
      if (arg2End === -1) { i = arg1End + 1; continue; }
      const arg2 = content.slice(j + 1, arg2End);
      results.push({ arg1, arg2, pos: i });
      i = arg2End + 1;
    }
    return results;
  }

  findAll('idx{').forEach(m => idx.push(m.arg));
  findAll2('idxmath').forEach(m => idxmath.push({ sort: m.arg1, display: m.arg2 }));
  findAll2('idxsub').forEach(m => idxsub.push({ parent: m.arg1, term: m.arg2 }));

  return { idx, idxmath, idxsub };
}

function normalizeTerm(term) {
  return term
    .replace(/\\textbf\{([^}]*)\}/g, '$1')
    .replace(/\\textsl\{([^}]*)\}/g, '$1')
    .replace(/\\text\{([^}]*)\}/g, '$1')
    .replace(/\\emph\{([^}]*)\}/g, '$1')
    .replace(/\\\\/g, '\\')
    .replace(/\s+/g, ' ')
    .trim();
}

function formatSection(title) {
  const line = '='.repeat(Math.min(title.length + 8, 60));
  return `\n  ${line}\n  === ${title} ===\n  ${line}\n`;
}

function heading(title) {
  return `\n${title}`;
}

function pass(label, detail) {
  return `  [PASS] ${label}${detail ? ': ' + detail : ''}`;
}

function fail(label, detail) {
  return `  [FAIL] ${label}${detail ? ': ' + detail : ''}`;
}

function warn(label, detail) {
  return `  [WARN] ${label}${detail ? ': ' + detail : ''}`;
}

function info(label, detail) {
  return `  [INFO] ${label}${detail ? ': ' + detail : ''}`;
}

function summaryLine(label, passCount, failCount, warnCount) {
  const parts = [];
  if (passCount > 0) parts.push(`${passCount} PASS`);
  if (failCount > 0) parts.push(`${failCount} FAIL`);
  if (warnCount > 0) parts.push(`${warnCount} WARN`);
  const status = failCount > 0 ? 'FAIL' : (warnCount > 0 ? 'WARN' : 'PASS');
  return `  ${label} ${status}  (${parts.join(', ')})`;
}

function exitCode(results) {
  return results.failures > 0 ? 1 : 0;
}

module.exports = {
  PROJECT_ROOT,
  loadJSON,
  braceMatch,
  extractCommands,
  normalizeTerm,
  formatSection,
  heading,
  pass,
  fail,
  warn,
  info,
  summaryLine,
  exitCode,
};
