#!/usr/bin/env node
/* Render local HTML to PNG/JPEG and a contact sheet. Requires Playwright. */
const fs=require('fs'),path=require('path'),{pathToFileURL}=require('url');
const args=process.argv.slice(2),at=args.indexOf('--input');
if(at<0){console.error('Usage: node render.cjs --input /path/to/manifest.json');process.exit(2)}
let pw;try{pw=require(process.env.PLAYWRIGHT_MODULE_PATH||'playwright')}catch(e){console.error('Playwright not found. Use an available runtime or npm install playwright, then set PLAYWRIGHT_MODULE_PATH.');process.exit(2)}
(async()=>{const file=path.resolve(args[at+1]),dir=path.dirname(file),manifest=JSON.parse(fs.readFileSync(file));
const chrome=process.env.CHROME_PATH;const browser=await pw.chromium.launch({headless:true,...(chrome?{executablePath:chrome}:{})});
try{const page=await browser.newPage({viewport:{width:1080,height:1000},deviceScaleFactor:1});const checks=[];
for(const s of manifest.styles){const errors=[];page.on('pageerror',e=>errors.push(String(e)));await page.goto(pathToFileURL(path.join(dir,s.html)).href);await page.evaluate(()=>document.fonts.ready);await page.locator('img').evaluateAll(imgs=>Promise.all(imgs.map(i=>i.decode().catch(()=>{}))));
const check=await page.evaluate(()=>({brokenImages:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.getAttribute('src')),horizontalOverflow:document.documentElement.scrollWidth>1080,caseCount:document.querySelectorAll('[data-case]').length,height:document.querySelector('#poster').scrollHeight}));
check.style=s.style;check.errors=errors;checks.push(check);if(check.brokenImages.length||check.horizontalOverflow||errors.length)throw Error('Render check failed: '+JSON.stringify(check));
await page.locator('#poster').screenshot({path:path.join(dir,s.png)});await page.locator('#poster').screenshot({path:path.join(dir,s.jpg),type:'jpeg',quality:92});console.log('Rendered '+s.style);}
fs.writeFileSync(path.join(dir,'checks.json'),JSON.stringify(checks,null,2));await page.setViewportSize({width:2400,height:1200});await page.goto(pathToFileURL(path.join(dir,'index.html')).href);await page.locator('img').evaluateAll(imgs=>Promise.all(imgs.map(i=>i.decode().catch(()=>{}))));await page.screenshot({path:path.join(dir,'overview.jpg'),fullPage:true,type:'jpeg',quality:90});console.log('Complete: '+dir);
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exit(1)});
