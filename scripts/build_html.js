// Assembles the root index.html from html/index.html (template) +
// html/partials/*.html — mirrors the scss/ -> css/main.css build (see
// package.json's build:css/watch:css), just for HTML instead of CSS.
// Include directive: a line containing exactly
//   <!-- include:relative/path/from/html/dir.html -->
// (leading/trailing whitespace on that line is ignored) gets replaced by
// that file's contents, recursively (partials may include partials).
const fs = require('fs');
const path = require('path');

const root = path.join(__dirname, '..');
const htmlDir = path.join(root, 'html');
const templatePath = path.join(htmlDir, 'index.html');
const outputPath = path.join(root, 'index.html');

const INCLUDE_RE = /^(\s*)<!--\s*include:(\S+)\s*-->\s*$/;

function resolveIncludes(filePath, seen) {
  if (seen.has(filePath)) {
    throw new Error(
      `Circular include detected: ${[...seen, filePath].join(' -> ')}`,
    );
  }
  const lines = fs
    .readFileSync(filePath, 'utf8')
    .replace(/\n$/, '')
    .split('\n');
  const nextSeen = new Set(seen).add(filePath);

  return lines
    .map((line) => {
      const match = line.match(INCLUDE_RE);
      if (!match) return line;

      const [, indent, includePath] = match;
      const resolvedPath = path.join(htmlDir, includePath);
      if (!fs.existsSync(resolvedPath)) {
        throw new Error(
          `Included file not found: ${includePath} (referenced from ${path.relative(htmlDir, filePath)})`,
        );
      }

      // Partials are written at their own natural (zero-based)
      // indentation; the include directive's indentation is what places
      // them in the page. Keeps partials formatter-safe — re-indenting a
      // partial in an editor can no longer break the output.
      const included = resolveIncludes(resolvedPath, nextSeen);
      return included
        .split('\n')
        .map((included_line) =>
          included_line.trim() === '' ? '' : indent + included_line,
        )
        .join('\n');
    })
    .join('\n');
}

function build() {
  const header =
    '<!-- AUTO-GENERATED from html/index.html + html/partials/ via `npm run build:html`' +
    ' (or `npm run watch:html`) — never edit this file directly. -->\n';
  const body = resolveIncludes(templatePath, new Set());
  fs.writeFileSync(outputPath, header + body);
  console.log(`Built index.html from ${path.relative(root, templatePath)}`);
}

function watch() {
  build();
  console.log('Watching html/ for changes...');
  fs.watch(htmlDir, { recursive: true }, (_event, filename) => {
    try {
      build();
    } catch (err) {
      console.error(`Build failed (${filename}):`, err.message);
    }
  });
}

try {
  if (process.argv.includes('--watch')) {
    watch();
  } else {
    build();
  }
} catch (err) {
  console.error('Build failed:', err.message);
  process.exit(1);
}
