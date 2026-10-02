"""Render the original UnvibeCode workflow report using the website's design."""
from pathlib import Path
from html.parser import HTMLParser
import re
import html
import json
DEST=Path(__file__).resolve().parent.parent
ROOT=DEST.parents[2]
source=(DEST/'original/02_business_workflow_map.html').read_text(encoding='utf-8')
home=(ROOT/'docs/index.html').read_text(encoding='utf-8')
class Groups(HTMLParser):
    def __init__(self,text):
        super().__init__(convert_charrefs=False)
        self.offsets=[0]
        for line in text.splitlines(keepends=True):self.offsets.append(self.offsets[-1]+len(line))
        self.text=text;self.depth=0;self.start=None;self.groups=[];self.feed(text)
    def position_offset(self):
        line,col=self.getpos();return self.offsets[line-1]+col
    def handle_starttag(self,tag,attrs):
        if tag=='section':
            if self.start is None and dict(attrs).get('class')=='workflow-group':self.start=self.position_offset();self.depth=0
            if self.start is not None:self.depth+=1
    def handle_endtag(self,tag):
        if tag=='section' and self.start is not None:
            self.depth-=1
            if self.depth==0:
                self.groups.append(self.text[self.start:self.position_offset()+len('</section>')]);self.start=None
areas=Groups(source).groups
assert len(areas)==12
links=[];rendered=[]
for n,group in enumerate(areas,1):
    title=re.search(r'<h2>(.*?)</h2>',group,re.S).group(1)
    count=len(re.findall(r'<article class="workflow-card">',group))
    links.append(f'<a href="#area-{n}">{title}<span>{count:02d}</span></a>')
    rendered.append(group.replace('<section class="workflow-group">',f'<section class="workflow-group" id="area-{n}">',1))
css=re.search(r'<style>(.*?)</style>',home,re.S).group(1)
extra='''
.analysis-intro{padding:44px 48px;border-bottom:1px solid var(--line)}.analysis-intro h1{font-size:clamp(36px,4vw,62px)}.analysis-intro .lede{max-width:780px}.analysis-stats{display:flex;gap:30px;font:14px var(--mono);margin:20px 0}.analysis-layout{display:grid;grid-template-columns:270px minmax(0,1fr)}.area-nav{border-right:1px solid var(--line);padding:24px 20px;align-self:start;position:sticky;top:0;max-height:100vh;overflow:auto}.area-nav .eyebrow{margin-bottom:16px}.area-nav a{display:flex;justify-content:space-between;gap:10px;padding:10px 0;text-decoration:none;font-size:14px;border-bottom:1px solid #d4d3ca}.area-nav a:hover{background:var(--soft)}.area-nav span{font:12px var(--mono);color:var(--muted)}.workflow-group{padding:30px;border-bottom:1px solid var(--line);scroll-margin-top:20px}.group-header{padding:0 0 22px;min-height:0;border-bottom:0;align-items:start}.group-header h2{font-size:30px;margin:8px 0}.group-count{font:12px var(--mono);white-space:nowrap;border:1px solid var(--line);padding:5px 9px}.workflow-card{padding:26px 0;border-top:1px solid #bbbbae;display:flex;gap:18px}.workflow-number{font:16px var(--mono);color:var(--muted);padding-top:5px}.workflow-content{min-width:0;flex:1}.workflow-title{font-size:23px;line-height:1.35;overflow-wrap:anywhere}.workflow-summary{border-left:2px solid var(--ink);padding:8px 18px;margin:20px 0}.workflow-summary h3,.context-panel h3,.value-section h3{font-size:13px;font-family:var(--mono);letter-spacing:0;color:var(--muted)}.workflow-summary p{margin:0}.context-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;padding:20px 0;border-top:1px solid #d4d3ca}.context-panel p{font-size:14px}.value-section{margin:16px 0}.value-section ul{padding-left:20px}details{margin:16px 0;border:1px solid #b2b2a6;padding:14px 16px}summary{cursor:pointer;font-weight:600;font-size:14px}.evidence-list{margin-top:15px}.evidence-item{margin-bottom:16px}.code-location{font:12px/1.6 var(--mono);overflow-wrap:anywhere}.evidence-item pre{background:var(--soft);padding:16px;white-space:pre-wrap;overflow-wrap:anywhere;font:13px/1.6 var(--mono);max-height:460px;overflow:auto}.journey-label{font:13px var(--mono);color:var(--muted)}.source-note{font-size:13px;color:var(--muted);padding:20px 30px;border-top:1px solid var(--line)}@media(max-width:850px){.analysis-layout{grid-template-columns:1fr}.area-nav{position:static;max-height:none;border-right:0;border-bottom:1px solid var(--line);display:grid;grid-template-columns:1fr 1fr;gap:0 20px}.area-nav .eyebrow{grid-column:1/-1}.context-grid{grid-template-columns:1fr}.analysis-intro{padding:32px 24px}.workflow-group{padding:24px}.group-header{display:block}.group-count{display:inline-block}.analysis-stats{flex-wrap:wrap}}@media(max-width:440px){.area-nav{grid-template-columns:1fr}.workflow-card{gap:10px}.workflow-title{font-size:20px}}'''
extra += '''
.site-header{position:sticky;top:0;z-index:10;background:var(--paper,#f7f6f2)}.site-header nav a[aria-current]{border-bottom:2px solid var(--ink);padding-bottom:6px}.area-nav{top:90px;max-height:calc(100vh - 90px)}html{scroll-behavior:smooth;scroll-padding-top:110px}.journey-section{padding:40px 48px;border-top:1px solid var(--line)}.journey-section h2{font-size:32px}.journey-section textarea{display:block;width:100%;min-height:180px;padding:16px;background:var(--soft);color:var(--ink);border:1px solid var(--line);font:14px/1.6 var(--mono);margin:16px 0}.journey-section select{max-width:100%;padding:12px;background:var(--paper,#f7f6f2);color:var(--ink);border:1px solid var(--line)}.workflow-ask{margin-top:18px}.journey-section .actions{flex-wrap:wrap}.copy-status{min-height:24px}.repo-link{display:inline-block;margin-top:12px}.journey-help{max-width:780px}@media(max-width:850px){.area-nav{max-height:none}.journey-section{padding:28px 24px}.site-header{position:static}html{scroll-padding-top:20px}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
'''
own_repo = '<section class="bottom"><div><p class="eyebrow">YOUR REPOSITORY / YOUR WORKFLOWS</p><h2>Understand your own codebase</h2><p>Run UnvibeCode on your repository to explore its workflows and prepare context for your LLM.</p></div><a class="button primary" href="https://github.com/FinanceFlash/unvibecode#readme">Analyse your own repository →</a></section>'
outputs=(DEST/'design/templates/outputs.html').read_text(encoding='utf-8')
nav='<a href="#business-workflows">Business workflows</a><a href="#connected-map">Connected code map</a><a href="#llm-context">Download LLM context</a>'
page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Smolagents analysis outputs | UnvibeCode</title><meta name="description" content="Explore 26 smolagents business workflows, the connected-code map and downloadable repository context for your LLM."><style>{css}{extra}</style><link rel="stylesheet" href="assets/outputs.css"></head><body><a class="skip" href="#main">Skip to workflows</a><div class="frame"><header class="site-header"><a class="brand" href="../../index.html">Unvibe<span>Code</span></a><nav aria-label="Analysis outputs">{nav}</nav></header><section class="analysis-intro" id="business-workflows"><p class="eyebrow">SAMPLE ANALYSIS / SMOLAGENTS</p><h1>Explore Smol Agents business workflows</h1><p class="eyebrow">Repository analysis by UnvibeCode</p><p class="lede">Explore how smolagents handles agent execution, tools, models and more. Follow the workflow areas discovered by UnvibeCode, from entry points to outcomes.</p><div class="analysis-stats"><span>26 workflows</span><span>12 workflow areas</span><span>Supporting code included</span></div><div class="actions"><a class="button primary" href="#area-1">Explore workflows ↓</a><a class="button secondary" href="#connected-map">Connected code map ↓</a></div><a class="repo-link" href="https://github.com/huggingface/smolagents">View smolagents on GitHub ↗</a></section><div class="analysis-layout"><aside class="area-nav" aria-label="Workflow areas"><p class="eyebrow">Workflow areas</p>{''.join(links)}</aside><main id="main">{''.join(rendered)}<div class="source-note">Content reproduced from the supplied UnvibeCode report. Original wording and evidence are preserved; this page adds navigation and website styling. Analysis snapshot: smolagents-main.</div></main></div>{outputs}{own_repo}<footer><a class="brand" href="../../index.html">Unvibe<span>Code</span></a><div class="links">{nav}<a href="https://github.com/FinanceFlash/unvibecode">UnvibeCode on GitHub ↗</a></div></footer></div><script src="original/_support/fast_lane_context_store.js"></script><script src="assets/outputs.js"></script></body></html>'''
(DEST/'index.html').write_text(page,encoding='utf-8')
for n,group in enumerate(areas,1):
    assert group.replace('<section class="workflow-group">',f'<section class="workflow-group" id="area-{n}">',1) in page
# Keep previous shared Ask URLs useful without retaining a separate experience.
(DEST/'ask.html').write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Smolagents analysis outputs</title><meta http-equiv="refresh" content="0;url=index.html#connected-map"></head><body><p><a href="index.html#connected-map">Explore the connected-code map and download LLM context →</a></p><script>location.replace('index.html'+location.search+'#connected-map');</script></body></html>''',encoding='utf-8')

# Reuse the exported graph's visualization library, nodes, edges and layout.
# The new controller below selects context in Ask instead of auto-downloading on click.
original_map=(DEST/'original/01_connected_code_map_for_llm.html').read_text(encoding='utf-8')
map_scripts=re.findall(r'<script\b[^>]*>(.*?)</script>',original_map,re.S)
vis_script=next(s for s in map_scripts if 'vis-network' in s or 't.Network=' in s)
graph_script=next(s for s in map_scripts if 'function drawGraph()' in s)
# Export retains a loading bar hook; retain its DOM targets without showing a second UI.
graph_page='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Smolagents connected-code map</title><style>html,body{margin:0;width:100%;height:100%;background:#f7f6f2;font-family:Arial,sans-serif}#mynetwork{width:100%;height:100%}#loadingBar{display:none}.vis-tooltip{background:#f7f6f2!important;color:#171714!important;border:1px solid #35352e!important;padding:10px;font:12px Arial;max-width:300px;overflow-wrap:anywhere}canvas:focus{outline:2px solid #171714}</style></head><body><div id="mynetwork" aria-label="Connected code graph"></div><div id="loadingBar"><div id="bar"></div><div id="text"></div></div><script>'''+vis_script+'</script><script>'+graph_script+'</script><script src="assets/map.js"></script></body></html>'
(DEST/'connected-code.html').write_text(graph_page,encoding='utf-8')
print('Rendered business workflows, connected-code map and LLM context downloads.')
