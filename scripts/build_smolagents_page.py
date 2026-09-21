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
extra += '''
.site-header{position:sticky;top:0;z-index:10;background:var(--paper,#f7f6f2)}.site-header nav a[aria-current]{border-bottom:2px solid var(--ink);padding-bottom:6px}.area-nav{top:90px;max-height:calc(100vh - 90px)}html{scroll-behavior:smooth;scroll-padding-top:110px}.journey-section{padding:40px 48px;border-top:1px solid var(--line)}.journey-section h2{font-size:32px}.journey-section textarea{display:block;width:100%;min-height:180px;padding:16px;background:var(--soft);color:var(--ink);border:1px solid var(--line);font:14px/1.6 var(--mono);margin:16px 0}.journey-section select{max-width:100%;padding:12px;background:var(--paper,#f7f6f2);color:var(--ink);border:1px solid var(--line)}.workflow-ask{margin-top:18px}.journey-section .actions{flex-wrap:wrap}.copy-status{min-height:24px}.repo-link{display:inline-block;margin-top:12px}.journey-help{max-width:780px}@media(max-width:850px){.area-nav{max-height:none}.journey-section{padding:28px 24px}.site-header{position:static}html{scroll-padding-top:20px}}@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
'''
journey = """
<section class="journey-section" id="ask" aria-labelledby="ask-title"><p class="eyebrow">02 / ASK</p><h2 id="ask-title">Ask an LLM with the right context</h2><p class="journey-help">Choose a workflow, then copy its question and evidence into your preferred LLM. You can edit the question before copying. For a broader investigation, download the repository context and attach the relevant JSON or JSONL files from the ZIP.</p><noscript><p>Enable JavaScript to select a workflow and prepare prompts. You can still read every workflow and download repository context below.</p></noscript><label for="workflow-choice">Which workflow do you want to understand?</label><br><select id="workflow-choice"></select><label for="ask-prompt"><p>Your question and workflow context</p></label><textarea id="ask-prompt" spellcheck="false"></textarea><div class="actions"><button class="button primary" type="button" data-copy="ask-prompt">Copy question + context</button><a class="button secondary" href="original/complete_repository_context_for_llm.zip" download>Download repository context</a><a id="return-workflow" href="#main">Return to this workflow ↑</a></div><p class="copy-status" role="status" id="copy-status"></p><p class="journey-help">Keep the downloaded context for future conversations. Attach it again when starting a new chat, and ask the model to cite the files and functions behind its answer.</p><a href="#build">Ready to apply it? Build on this workflow →</a></section>
<section class="journey-section" id="build" aria-labelledby="build-title"><p class="eyebrow">03 / BUILD</p><h2 id="build-title">Build on what you understand</h2><p class="journey-help">Start with a workflow you have explored. Describe your application and use the prompt below with that workflow’s context to plan an implementation.</p><label for="build-prompt">Your implementation prompt</label><textarea id="build-prompt" spellcheck="false"></textarea><div class="actions"><button class="button primary" type="button" data-copy="build-prompt">Copy build prompt</button><a class="button secondary" href="#ask">Get workflow context ↑</a><a href="https://github.com/huggingface/smolagents/tree/main/examples">Explore smolagents examples ↗</a></div><p class="journey-help">Use the agent-execution checkpoints in your plan: termination, state persistence, error recovery, tool validation and execution restrictions. Ask for tests and confirm the implementation against the version you install.</p><a href="#understand">Return to Understand ↑</a></section>
"""
interaction = r"""<script>
const cards = Array.from(document.querySelectorAll('.workflow-card'));
const choice = document.getElementById('workflow-choice');
const ask = document.getElementById('ask-prompt');
const build = document.getElementById('build-prompt');
const context = [];
cards.forEach((card, i) => {
  card.id = 'workflow-' + (i + 1);
  const title = card.querySelector('.workflow-title').textContent.trim();
  context.push({title, evidence: card.textContent.trim(), id: card.id});
  choice.add(new Option(title, String(i)));
  const action = document.createElement('a');
  action.href = '#ask'; action.className = 'button secondary workflow-ask';
  action.textContent = 'Ask about this workflow →';
  action.addEventListener('click', () => { choice.value = String(i); selectWorkflow(); });
  (card.querySelector('.workflow-content') || card).append(action);
});
function selectWorkflow() {
  const item = context[Number(choice.value)];
  ask.value = 'Explain "' + item.title + '" in smolagents. Trace the entry point, actions, tools, memory or state, execution boundaries, failure paths and termination wherever the supplied evidence supports them. Cite files and functions. Separate observed behaviour from suggestions and identify any extra code needed to answer.\n\nRepository: https://github.com/huggingface/smolagents\nAnalysis snapshot: smolagents-main (commit not recorded in export).\nSource: UnvibeCode workflow output.\n\n' + item.evidence;
  build.value = 'I want to build [describe your application] in Python using smolagents. Use the attached UnvibeCode context for "' + item.title + '". First ask for my installed smolagents version and requirements. Explain the relevant workflow, then propose the smallest useful implementation with explicit tools, state ownership, termination, failure handling and execution restrictions. Cite the supplied code for existing behaviour; label new design choices. Include setup instructions, an example input and expected output, and tests for success and failure. Do not assume a successful demo proves production readiness.';
  document.getElementById('return-workflow').href = '#' + item.id;
}
choice.addEventListener('change', selectWorkflow); if (context.length) selectWorkflow();
document.querySelectorAll('[data-copy]').forEach(button => button.addEventListener('click', async () => {
 const field = document.getElementById(button.dataset.copy);
 try { await navigator.clipboard.writeText(field.value); button.textContent = 'Copied'; setTimeout(() => { button.textContent = button.dataset.copy === 'ask-prompt' ? 'Copy question + context' : 'Copy build prompt'; }, 2000); }
 catch (_) { field.focus(); field.select(); document.getElementById('copy-status').textContent = 'Text selected. Copy it with Ctrl+C or Command+C.'; }
}));
function highlightJourney() {
 const hash = location.hash;
 const active = hash === '#ask' || hash === '#build' ? hash : '#understand';
 document.querySelectorAll('.site-header nav a').forEach(link => { if (link.getAttribute('href') === active) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current'); });
}
window.addEventListener('hashchange', highlightJourney); highlightJourney();
</script>"""
page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Understand Smol Agents workflows | UnvibeCode</title><meta name="description" content="Explore 26 smolagents workflows in 12 areas, directly from UnvibeCode's analysis, with purposes, outcomes and supporting code."><style>{css}{extra}</style></head><body><a class="skip" href="#main">Skip to workflows</a><div class="frame"><header class="site-header"><a class="brand" href="../../index.html">Unvibe<span>Code</span></a><nav aria-label="Main navigation"><a href="#understand" aria-current="location">Understand</a><a href="#ask">Ask</a><a href="#build">Build</a></nav></header><section class="analysis-intro" id="understand"><p class="eyebrow">Understand → Ask → Build / Smolagents</p><h1>Understand Smol Agents workflows</h1><p class="eyebrow">Repository analysis by UnvibeCode</p><p class="lede">Explore how smolagents handles agent execution, tools, models and more. Follow the workflow areas discovered by UnvibeCode, from entry points to outcomes.</p><div class="analysis-stats"><span>26 workflows</span><span>12 workflow areas</span><span>Supporting code included</span></div><div class="actions"><a class="button primary" href="#area-1">Explore the workflows ↓</a></div><a class="repo-link" href="https://github.com/huggingface/smolagents">View smolagents on GitHub ↗</a></section><div class="analysis-layout"><aside class="area-nav" aria-label="Workflow areas"><p class="eyebrow">Workflow areas</p>{''.join(links)}</aside><main id="main">{''.join(rendered)}<div class="source-note">Content reproduced from the supplied UnvibeCode report. Original wording and evidence are preserved; this page adds navigation and website styling. Analysis snapshot: smolagents-main.</div></main></div><section class="bottom"><div><h2>Ask an LLM with the right context.</h2><p>Take what you have learned into your next question, with the workflow and supporting code alongside it.</p></div><a class="button primary" href="#ask">Ask about Smol Agents →</a></section>{journey}<footer><a class="brand" href="../../index.html">Unvibe<span>Code</span></a><div class="links"><a href="#understand">Understand</a><a href="#ask">Ask</a><a href="#build">Build</a><a href="https://github.com/FinanceFlash/unvibecode">UnvibeCode on GitHub ↗</a><a href="original/complete_repository_context_for_llm.zip" download>Repository context ZIP</a></div></footer></div>{interaction}</body></html>'''
(DEST/'index.html').write_text(page)
# Exact original group content is retained apart from added navigation IDs.
for n,group in enumerate(areas,1):assert group.replace('<section class="workflow-group">',f'<section class="workflow-group" id="area-{n}">',1) in page
print(f'Rendered {len(areas)} original workflow areas; all 26 original cards retained.')
