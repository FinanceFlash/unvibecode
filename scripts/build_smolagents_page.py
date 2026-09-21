"""Render the original UnvibeCode workflow report using the website's design."""
from pathlib import Path
from html.parser import HTMLParser
import re
import html
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'docs/gitdocs/smolagents'
source=(DEST/'original/02_business_workflow_map.html').read_text()
home=(ROOT/'docs/index.html').read_text()
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
page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Understand Smol Agents workflows | UnvibeCode</title><meta name="description" content="Explore 26 smolagents workflows in 12 areas, directly from UnvibeCode's analysis, with purposes, outcomes and supporting code."><style>{css}{extra}</style></head><body><a class="skip" href="#main">Skip to workflows</a><div class="frame"><header><a class="brand" href="../../index.html">Unvibe<span>Code</span></a><nav aria-label="Main navigation"><a href="#main" aria-current="page">Understand</a><a href="original/01_connected_code_map_for_llm.html">Connected code</a><a href="original/00_unvibecode_results.html">All outputs</a><a class="star" href="https://github.com/FinanceFlash/unvibecode">GitHub ↗</a></nav></header><section class="analysis-intro"><p class="eyebrow">Understand → Ask → Build / Smolagents</p><h1>Understand Smol Agents workflows.</h1><p class="lede">Explore how smolagents handles agent execution, tools, models and more. Follow the workflow areas discovered by UnvibeCode, from entry points to outcomes.</p><div class="analysis-stats"><span>26 workflows</span><span>12 workflow areas</span><span>Supporting code included</span></div><div class="actions"><a class="button primary" href="#area-1">Explore the workflows ↓</a><a class="button secondary" href="original/02_business_workflow_map.html">Open original report ↗</a></div></section><div class="analysis-layout"><aside class="area-nav" aria-label="Workflow areas"><p class="eyebrow">Workflow areas</p>{''.join(links)}</aside><main id="main">{''.join(rendered)}<div class="source-note">Content reproduced from the supplied UnvibeCode report. Original wording and evidence are preserved; this page adds navigation and website styling. Analysis snapshot: smolagents-main.</div></main></div><section class="bottom"><div><h2>Take the connected code into your AI.</h2><p>Choose a file and download the relevant context for your next question.</p></div><a class="button primary" href="original/01_connected_code_map_for_llm.html">Explore connected code ↗</a></section><footer><a class="brand" href="../../index.html">Unvibe<span>Code</span></a><div class="links"><a href="original/03_business_risk_findings.html">Risk findings</a><a href="original/complete_repository_context_for_llm.zip" download>Repository context ZIP</a></div></footer></div></body></html>'''
(DEST/'index.html').write_text(page)
# Exact original group content is retained apart from added navigation IDs.
for n,group in enumerate(areas,1):assert group.replace('<section class="workflow-group">',f'<section class="workflow-group" id="area-{n}">',1) in page
print(f'Rendered {len(areas)} original workflow areas; all 26 original cards retained.')
