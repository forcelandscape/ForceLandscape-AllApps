// Exercise the real out() implementation with a mocked bridge.
const assert = require('assert');
const fs = require('fs');
const vm = require('vm');
const html = fs.readFileSync('webroot/index.html', 'utf8');
const body = html.slice(html.indexOf('async function out(args){'), html.indexOf('function kvParse(txt)'));
const context = { SHELL: 'sh', SCRIPT: 'webui.sh', result: null };
context.execRaw = async () => context.result;
vm.createContext(context);
vm.runInContext(body, context);
(async () => {
  context.result = {errno: 1, stdout: 'HATA|reddedildi', stderr: ''};
  await assert.rejects(context.out('mode smart'), /reddedildi/);
  context.result = {errno: 2, stdout: 'ADIM|test\nSONUC|KANIT-YOK|okunamadi', stderr: ''};
  assert.match(await context.out('kesin com.example.app'), /KANIT-YOK/);
  context.result = {errno: 0, stdout: 'OK|smart', stderr: ''};
  assert.strictEqual(await context.out('mode smart'), 'OK|smart');
  console.log('webui bridge regression tests passed');
})().catch(e => { console.error(e); process.exit(1); });
