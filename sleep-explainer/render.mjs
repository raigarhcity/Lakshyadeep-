// Frame-exact capture: serve the folder, call render(t) per frame, pipe JPEGs to ffmpeg.
// usage: node render.mjs [out.mp4] [--stills 1,5,10]
import { chromium } from "playwright";
import { spawn } from "node:child_process";
import http from "node:http";
import fs from "node:fs";
import path from "node:path";

const root = path.dirname(new URL(import.meta.url).pathname);
const args = process.argv.slice(2);
const stillsArg = args.indexOf("--stills");
const stills = stillsArg >= 0 ? args[stillsArg + 1].split(",").map(Number) : null;
const out = args.find(a => a.endsWith(".mp4")) || path.join(root, "out", "silent.mp4");

const types = { ".html": "text/html", ".woff2": "font/woff2" };
const server = http.createServer((req, res) => {
  const f = path.join(root, decodeURIComponent(req.url.split("?")[0]));
  fs.readFile(f, (e, d) => { if (e) { res.writeHead(404); res.end(); return; } res.writeHead(200, { "content-type": types[path.extname(f)] || "application/octet-stream" }); res.end(d); });
}).listen(0);
const port = server.address().port;

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
await page.goto(`http://127.0.0.1:${port}/index.html?capture`);
await page.evaluate(() => window.ready);
const grab = t => page.evaluate(t => { render(t); return document.getElementById("c").toDataURL("image/jpeg", 0.95).split(",")[1]; }, t);

fs.mkdirSync(path.join(root, "out"), { recursive: true });
if (stills) {
  for (const t of stills) fs.writeFileSync(path.join(root, "out", `still-${t}.jpg`), Buffer.from(await grab(t), "base64"));
} else {
  const { DURATION, FPS } = await page.evaluate(() => ({ DURATION, FPS }));
  const ff = spawn("ffmpeg", ["-y", "-loglevel", "error", "-f", "image2pipe", "-framerate", String(FPS), "-c:v", "mjpeg", "-i", "-",
    "-c:v", "libx264", "-preset", "slow", "-crf", "18", "-pix_fmt", "yuv420p", out], { stdio: ["pipe", "inherit", "inherit"] });
  const n = Math.round(DURATION * FPS);
  for (let i = 0; i < n; i++) {
    const buf = Buffer.from(await grab(i / FPS), "base64");
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once("drain", r));
    if (i % 150 === 0) console.log(`frame ${i}/${n}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on("close", r));
  console.log("wrote", out);
}
await browser.close();
server.close();
