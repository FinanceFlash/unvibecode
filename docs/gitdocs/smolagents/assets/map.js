/* Uses the nodes and edges from the original UnvibeCode export. */
(() => {
  const defaults = {background:'#e9e8e1',border:'#575750',highlight:{background:'#171714',border:'#171714'},hover:{background:'#d4d3ca',border:'#171714'}};
  nodes.update(nodes.get().map(n => ({id:n.id,color:defaults,font:{color:'#171714',face:'Arial'},borderWidth:1})));
  edges.update(edges.get().map(e => ({id:e.id,color:'#b2b2a6'})));
  network.setOptions({interaction:{hover:true},physics:{stabilization:{iterations:200}},nodes:{font:{face:'Arial'}}});
  function send(type, file) { parent.postMessage({type,file},location.origin); }
  network.on('click', p => { if(p.nodes.length) send('unvibecode-file',String(p.nodes[0])); });
  window.addEventListener('message', event => {
    if(event.origin !== location.origin || event.source !== parent || event.data?.type !== 'unvibecode-selection') return;
    const file=event.data.file, included=new Set(event.data.files || []);
    nodes.update(nodes.get().map(n => { const id=String(n.id); const selected=id===file, inside=included.has(id) || [...included].some(f=>id.startsWith('symbol::'+f+'::')); return {id:n.id,color:selected?{background:'#171714',border:'#171714'}:defaults,font:{color:selected?'#ffffff':'#171714',face:'Arial'},opacity:selected||inside?1:0.22,borderWidth:selected?4:inside?3:1}; }));
    network.selectNodes(nodes.get(file)?[file]:[],false);
  });
  send('unvibecode-map-ready');
})();
