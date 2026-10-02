/* Context selections, ordered chunks and connections are preserved from the original export. */
(() => {
  'use strict';
  // Preserve previously shared workflow anchors without changing workflow HTML.
  document.querySelectorAll('.workflow-card').forEach((card,i)=>card.id='workflow-'+(i+1));
  if (/^#workflow-\d+$/.test(location.hash)) requestAnimationFrame(()=>document.getElementById(location.hash.slice(1))?.scrollIntoView());
  if (['#ask','#build'].includes(location.hash)) location.hash='connected-map';
  if (location.hash==='#understand') location.hash='business-workflows';
  const store=window.SHIPREADY_CONTEXT_STORE;
  const $=id=>document.getElementById(id);
  const file=$('file-choice'), scope=$('scope-choice'), question=$('question');
  const map=$('code-map');
  if(!store) { $('action-status').textContent='Context could not load. Reload this page or download the full ZIP below.'; return; }
  const files=Object.keys(store.files).sort();
  for(const name of files) file.add(new Option(name,name));
  let payload;
  function remember() { try { sessionStorage.setItem('unvibecode-smolagents-output-selection',JSON.stringify({file:file.value,scope:scope.value,question:question.value})); } catch {} }
  function queryState() {
    const url=new URL(location.href);url.searchParams.delete('workflow');url.searchParams.set('file',file.value);url.searchParams.set('scope',scope.value);history.replaceState(null,'',url);remember();
  }
  function highlight() { map.contentWindow?.postMessage({type:'unvibecode-selection',file:file.value,files:payload?.context_scope.included_files||[]},location.origin); }
  function pack() {
    const selection=store.files[file.value]?.scopes[scope.value]; if(!selection) return null;
    const ids=new Set(selection.chunk_ids);
    return {schema_version:'shipreadyv2.connected_code_context.v1',repository:store.repository,repository_url:'https://github.com/huggingface/smolagents',repository_commit:null,source:'UnvibeCode supplied analysis export',selected_file:file.value,context_scope:{size:scope.value,name:['Narrow connection context','Optimal connection context','Wider connection context'][Number(scope.value)],estimated_tokens:selection.estimated_tokens,maximum_tokens:selection.maximum_tokens,included_files:selection.included_files,connected_files_not_included:selection.connected_files_not_included,selected_file_sections_not_included:selection.selected_file_sections_not_included},instructions:['Use the ordered code chunks as one connected context.','Cite original filenames and line numbers.','Treat only verified_cross_file_connections as established links.','Separate observed code behaviour from proposed designs.','If required evidence is absent, identify the missing file or function.'],question:question.value,included_code_chunks:selection.chunk_ids.map(id=>store.chunks[id]).filter(Boolean),verified_cross_file_connections:store.verified_cross_file_connections.filter(link=>ids.has(link.source_chunk)&&ids.has(link.target_chunk))};
  }
  function updateContext() {
    payload=pack(); if(!payload) return;
    const c=payload.context_scope;
    $('context-summary').textContent=c.included_files.length+' files · '+payload.included_code_chunks.length+' code sections · about '+Number(c.estimated_tokens).toLocaleString()+' tokens';
    $('included-files').replaceChildren(...c.included_files.map(name=>{const li=document.createElement('li');li.textContent=name;return li;}));
    $('context-preview').textContent=JSON.stringify(payload,null,2);
    $('omissions-text').textContent=(c.connected_files_not_included||[]).length+' connected files and '+(c.selected_file_sections_not_included||[]).length+' sections of the starting file are outside this selection. Choose a wider size or use the full repository ZIP when your question needs more context.';
    $('omissions').hidden=!(c.connected_files_not_included?.length || c.selected_file_sections_not_included?.length);
    queryState();highlight();
  }
  let saved={};try{saved=JSON.parse(sessionStorage.getItem('unvibecode-smolagents-output-selection')||'{}');}catch{}
  const params=new URLSearchParams(location.search);
  const requestedFile=params.get('file')||saved.file;
  file.value=store.files[requestedFile]?requestedFile:(store.files['src/smolagents/agents.py']?'src/smolagents/agents.py':files[0]);
  const requestedScope=params.get('scope')||saved.scope;if(['0','1','2'].includes(requestedScope))scope.value=requestedScope;
  question.value=saved.question||'Explain how this code works. Trace its entry points, actions and failure paths. Cite the files and functions behind your answer.';
  updateContext();
  file.addEventListener('change',updateContext);scope.addEventListener('change',updateContext);
  question.addEventListener('input',()=>{payload=pack();$('context-preview').textContent=JSON.stringify(payload,null,2);remember();});
  async function copy(text) {
    const fallback=$('copy-fallback');fallback.value=text;
    try{await navigator.clipboard.writeText(text);$('action-status').textContent='Copied. Paste into your preferred LLM.';fallback.hidden=true;$('copy-fallback-label').hidden=true;}
    catch{fallback.hidden=false;$('copy-fallback-label').hidden=false;fallback.focus();fallback.select();$('action-status').textContent='Text selected below. Press Ctrl+C or Command+C to copy, or download the JSON.';}
  }
  $('copy-context').addEventListener('click',()=>copy(JSON.stringify(pack(),null,2)));
  $('download-context').addEventListener('click',()=>{const blob=new Blob([JSON.stringify(pack(),null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=file.value.replace(/[^A-Za-z0-9._-]/g,'_')+'_context_'+scope.value+'.json';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);$('action-status').textContent='Downloaded. Attach this JSON to your LLM with your question.';});
  function markOutput() {
    const target=location.hash==='#connected-map'?'#connected-map':location.hash==='#llm-context'?'#llm-context':'#business-workflows';
    document.querySelectorAll('.site-header nav a').forEach(a=>{if(a.getAttribute('href')===target)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');});
  }
  window.addEventListener('hashchange',markOutput);markOutput();
  window.addEventListener('message',event=>{if(event.origin!==location.origin||event.source!==map.contentWindow)return;if(event.data?.type==='unvibecode-map-ready')highlight();if(event.data?.type==='unvibecode-file'&&store.files[event.data.file]){file.value=event.data.file;updateContext();}});
})();
