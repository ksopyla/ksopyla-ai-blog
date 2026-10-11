// Headless preview check for a locally served Hugo page (used from Claude Code,
// which has no Cursor browser). Prints one line per viewport: H1, horizontal
// overflow, tables wider than the content column, CSS responses and console
// errors; saves top-of-page and full-page screenshots.
//
// Usage: node preview_check.js <url> <out_dir>
// Needs Playwright: set NODE_PATH to the global node_modules if `require` fails,
// e.g. NODE_PATH=$(npm root -g) node preview_check.js ...
const { chromium } = require('playwright');
const fs = require('fs');

const url = process.argv[2];
const out = process.argv[3] || '.';
if (!url) { console.error('usage: node preview_check.js <url> <out_dir>'); process.exit(1); }
fs.mkdirSync(out, { recursive: true });

const VIEWPORTS = [
  ['desktop', { width: 1280, height: 800 }, 'light'],
  ['desktop-dark', { width: 1280, height: 800 }, 'dark'],
  ['mobile', { width: 390, height: 844 }, 'light'],
];
// Third-party widgets that may be blocked in sandboxes; not a page problem.
const IGNORE = /giscus|umami|ERR_TUNNEL_CONNECTION_FAILED/;

(async () => {
  const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
  for (const [name, viewport, colorScheme] of VIEWPORTS) {
    const ctx = await browser.newContext({ viewport, colorScheme });
    const page = await ctx.newPage();
    const errors = [];
    const css = [];
    page.on('console', m => { if (m.type() === 'error' && !IGNORE.test(m.text())) errors.push(m.text()); });
    page.on('response', r => { if (r.url().endsWith('.css')) css.push(`${r.status()} ${r.url()}`); });
    await page.goto(url, { waitUntil: 'networkidle' });
    const report = await page.evaluate(() => ({
      h1: document.querySelector('h1')?.innerText,
      overflowPx: document.documentElement.scrollWidth - window.innerWidth,
      wideTables: [...document.querySelectorAll('table')].filter(t => t.scrollWidth > t.parentElement.clientWidth).length,
    }));
    console.log(`${name} | h1: ${report.h1} | overflow px: ${report.overflowPx} | wide tables: ${report.wideTables} | css: ${css.join(' ') || 'NONE'} | errors: ${errors.length ? errors.join(' ; ') : 'none'}`);
    await page.screenshot({ path: `${out}/${name}-top.png` });
    await page.screenshot({ path: `${out}/${name}-full.png`, fullPage: true });
    await ctx.close();
  }
  await browser.close();
})();
