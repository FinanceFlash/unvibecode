/* All context selections and code come from the original UnvibeCode store. */
(() => {
  'use strict';
  const store=window.SHIPREADY_CONTEXT_STORE, workflows=window.UNVIBECODE_WORKFLOWS;
  const $=id=>document.getElementById(id);
  const choice=$('workflow-choice'), file=$('file-choice'), scope=$('scope-choice'), question=$('question');
  const map=$('code-map');
  if(!store || !workflows) { $('action-status').textContent='Context could not load. Reload this page or download the full ZIP below.'; return; }
  const files=Object.keys(store.files).sort();
  for(const name of files) file.add(new Option(name,name));
  let current, payload;
  function remember() { try { sessionStorage.setItem('unvibecode-smolagents-selection',JSON.stringify({workflow:choice.value,file:file.value,scope:scope.value,question:question.value})); } catch {} }
  function queryState() {
    const url=new URL(location.href); url.searchParams.set('workflow',choice.value);url.searchParams.set('file',file.value);url.searchParams.set('scope',scope.value);history.replaceState(null,'',url);
    document.querySelectorAll('[data-understand]').forEach(a=>a.href='index.html?workflow='+choice.value+'#workflow-'+choice.value);
    document.querySelectorAll('[data-build]').forEach(a=>a.href='index.html?workflow='+choice.value+'#build');remember();
  }
  function highlight() { map.contentWindow?.postMessage({type:'unvibecode-selection',file:file.value,files:payload?.context_scope.included_files||[]},location.origin); }
  function pack() {
    const selection=store.files[file.value]?.scopes[scope.value]; if(!selection) return null;
    const ids=new Set(selection.chunk_ids);
    return {schema_version:'shipreadyv2.connected_code_context.v1',repository:store.repository,repository_url:'https://github.com/huggingface/smolagents',repository_commit:null,source:'UnvibeCode supplied analysis export',workflow:{id:current.id,title:current.title},selected_file:file.value,context_scope:{size:scope.value,name:['Narrow connection context','Optimal connection context','Wider connection context'][Number(scope.value)],estimated_tokens:selection.estimated_tokens,maximum_tokens:selection.maximum_tokens,included_files:selection.included_files,connected_files_not_included:selection.connected_files_not_included,selected_file_sections_not_included:selection.selected_file_sections_not_included},instructions:['Use the ordered code chunks as one connected context.','Cite original filenames and line numbers.','Treat only verified_cross_file_connections as established links.','Separate observed code behaviour from proposed designs.','If required evidence is absent, identify the missing file or function.'],question:question.value,included_code_chunks:selection.chunk_ids.map(id=>store.chunks[id]).filter(Boolean),verified_cross_file_connections:store.verified_cross_file_connections.filter(link=>ids.has(link.source_chunk)&&ids.has(link.target_chunk))};
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
  function updateWorkflow(resetFile=true) {
    current=workflows.find(w=>String(w.id)===choice.value)||workflows[0];
    $('workflow-summary').textContent=current.summary;
    $('workflow-evidence').href='index.html?workflow='+current.id+'#workflow-'+current.id;
    document.querySelectorAll('.faq').forEach(el=>el.hidden=Number(el.dataset.workflow)!==current.id);
    document.querySelectorAll('[data-area]').forEach(el=>{if(Number(el.dataset.area)===current.area)el.setAttribute('aria-current','true');else el.removeAttribute('aria-current');});
    if(resetFile) file.value=current.files.find(f=>store.files[f])||files[0];
    question.value='Explain "'+current.title+'" from entry point to result. Describe actions, state, termination and failure handling where the code provides evidence. Cite files and functions, and identify any additional code needed.';
    updateContext();
  }
  let saved={};try{saved=JSON.parse(sessionStorage.getItem('unvibecode-smolagents-selection')||'{}');}catch{}
  const params=new URLSearchParams(location.search), requested=params.get('workflow')||saved.workflow;
  choice.value=workflows.some(w=>String(w.id)===requested)?requested:'1';
  const requestedScope=params.get('scope')||saved.scope;if(['0','1','2'].includes(requestedScope))scope.value=requestedScope;
  updateWorkflow();
  const requestedFile=params.get('file')||(!params.has('workflow') || params.get('workflow')===saved.workflow ? saved.file:null);
  if(requestedFile && store.files[requestedFile])file.value=requestedFile;
  if(saved.question && saved.workflow===choice.value)question.value=saved.question;
  updateContext();
  choice.addEventListener('change',()=>updateWorkflow());file.addEventListener('change',updateContext);scope.addEventListener('change',updateContext);
  question.addEventListener('input',()=>{payload=pack();$('context-preview').textContent=JSON.stringify(payload,null,2);remember();});
  document.querySelectorAll('[data-area]').forEach(a=>a.addEventListener('click',event=>{event.preventDefault();choice.value=String(workflows.find(w=>w.area===Number(a.dataset.area)).id);updateWorkflow();location.hash='questions';}));
  document.querySelectorAll('[data-question]').forEach(button=>button.addEventListener('click',()=>{question.value=button.dataset.question+' Explain using the attached code, cite files and functions, and identify any missing evidence.';updateContext();location.hash='connected-map';}));
  async function copy(text) {
    const fallback=$('copy-fallback');fallback.value=text;
    try{await navigator.clipboard.writeText(text);$('action-status').textContent='Copied. Paste into your preferred LLM.';fallback.hidden=true;$('copy-fallback-label').hidden=true;}
    catch{fallback.hidden=false;$('copy-fallback-label').hidden=false;fallback.focus();fallback.select();$('action-status').textContent='Text selected below. Press Ctrl+C or Command+C to copy, or download the JSON.';}
  }
  $('copy-question').addEventListener('click',()=>copy(question.value));
  $('copy-context').addEventListener('click',()=>copy(JSON.stringify(pack(),null,2)));
  $('download-context').addEventListener('click',()=>{const blob=new Blob([JSON.stringify(pack(),null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=file.value.replace(/[^A-Za-z0-9._-]/g,'_')+'_context_'+scope.value+'.json';document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);$('action-status').textContent='Downloaded. Attach this JSON to your LLM with your question.';});
  window.addEventListener('message',event=>{if(event.origin!==location.origin||event.source!==map.contentWindow)return;if(event.data?.type==='unvibecode-map-ready')highlight();if(event.data?.type==='unvibecode-file'&&store.files[event.data.file]){file.value=event.data.file;updateContext();}});
})();
