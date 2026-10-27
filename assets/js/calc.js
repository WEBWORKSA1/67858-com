/* 67858.com calculator engine: instant results, shareable URLs, charts, recent history */
(function(){
  'use strict';
  var C=window.CALC;if(!C)return;
  var form=document.getElementById('calcForm'),out=document.getElementById('results'),chart=document.getElementById('chart'),steps=document.getElementById('steps');
  var cur=(function(){try{return localStorage.getItem('cur67')||'$'}catch(e){return '$'}})();
  document.querySelectorAll('.cur').forEach(function(s){s.textContent=cur});
  var csel=document.getElementById('curSel');
  if(csel){csel.value=cur;csel.addEventListener('change',function(){cur=csel.value;try{localStorage.setItem('cur67',cur)}catch(e){}document.querySelectorAll('.cur').forEach(function(s){s.textContent=cur});run()})}

  function fmt(v,f){
    if(v===null||v===undefined||(typeof v==='number'&&!isFinite(v)))return '—';
    if(typeof v==='string')return v;
    switch(f){
      case 'money':return (v<0?'-':'')+cur+Math.abs(v).toLocaleString(undefined,{minimumFractionDigits:2,maximumFractionDigits:2});
      case 'money0':return (v<0?'-':'')+cur+Math.abs(Math.round(v)).toLocaleString();
      case 'pct':return v.toLocaleString(undefined,{maximumFractionDigits:2})+'%';
      case 'int':return Math.round(v).toLocaleString();
      case 'months':return v.toLocaleString(undefined,{maximumFractionDigits:1})+' months';
      case 'years':return v.toLocaleString(undefined,{maximumFractionDigits:1})+' years';
      case 'x':return v.toLocaleString(undefined,{maximumFractionDigits:2})+'×';
      default:return v.toLocaleString(undefined,{maximumFractionDigits:4});
    }
  }
  function vals(){
    var v={};
    form.querySelectorAll('[data-k]').forEach(function(i){
      var k=i.getAttribute('data-k');
      v[k]=i.tagName==='SELECT'?(isNaN(parseFloat(i.value))?i.value:parseFloat(i.value)):parseFloat(String(i.value).replace(/,/g,''));
      if(i.tagName!=='SELECT'&&isNaN(v[k]))v[k]=0;
    });
    return v;
  }
  function drawChart(s){
    if(!chart)return;
    if(!s||!s.data||!s.data.length){chart.style.display='none';return}
    chart.style.display='block';
    var W=640,H=220,P=34,n=s.data.length,max=0;
    s.data.forEach(function(d){max=Math.max(max,(d.a||0)+(d.b||0))});
    if(max<=0){chart.style.display='none';return}
    var bw=(W-P*2)/n,svg='<svg viewBox="0 0 '+W+' '+(H+24)+'" role="img" aria-label="'+(s.title||'Chart')+'">';
    for(var g=0;g<=4;g++){var y=P/2+(H-P)*(g/4);svg+='<line x1="'+P+'" x2="'+(W-8)+'" y1="'+y+'" y2="'+y+'" stroke="#273048"/>'}
    s.data.forEach(function(d,i){
      var ha=(H-P)*(d.a||0)/max,hb=(H-P)*(d.b||0)/max,x=P+i*bw+bw*.15,w=bw*.7,base=H-P/2;
      svg+='<rect x="'+x+'" y="'+(base-ha)+'" width="'+w+'" height="'+ha+'" fill="#0f9d8a" rx="2"><title>'+d.l+': '+fmt(d.a,'money0')+'</title></rect>';
      if(hb)svg+='<rect x="'+x+'" y="'+(base-ha-hb)+'" width="'+w+'" height="'+hb+'" fill="#e8a317" rx="2"><title>'+d.l+': '+fmt(d.b,'money0')+'</title></rect>';
      if(n<=12||i%Math.ceil(n/10)===0)svg+='<text x="'+(x+w/2)+'" y="'+(H+10)+'" fill="#9aa3b5" font-size="11" text-anchor="middle">'+d.l+'</text>';
    });
    svg+='</svg><div style="display:flex;gap:16px;font-size:.8rem;color:#b9c0cf;margin-top:6px"><span>■ <span style="color:#0f9d8a">'+(s.a||'Principal')+'</span></span>'+(s.b?'<span>■ <span style="color:#e8a317">'+s.b+'</span></span>':'')+'</div>';
    chart.innerHTML=svg;
  }
  var last=null;
  function run(){
    var v=vals(),r;
    try{r=C.compute(v)}catch(e){r={results:[{l:'Check inputs',v:'—'}]}}
    last=r;
    out.innerHTML=r.results.map(function(x,i){return '<div class="res'+(i===0?' main':'')+'"><small>'+x.l+'</small><b>'+fmt(x.v,x.f)+'</b></div>'}).join('');
    drawChart(r.series);
    if(steps)steps.innerHTML=r.steps||'';
  }
  form.addEventListener('input',run);form.addEventListener('change',run);
  form.addEventListener('submit',function(e){e.preventDefault();run();save()});

  // Prefill from shared URL
  var q=new URLSearchParams(location.search);
  form.querySelectorAll('[data-k]').forEach(function(i){var k=i.getAttribute('data-k');if(q.has(k))i.value=q.get(k)});
  run();

  function shareUrl(){var p=new URLSearchParams();form.querySelectorAll('[data-k]').forEach(function(i){p.set(i.getAttribute('data-k'),i.value)});return location.origin+location.pathname+'?'+p.toString()}
  function save(){
    try{var h=JSON.parse(localStorage.getItem('h67')||'[]');h=h.filter(function(x){return x.u!==shareUrl()});
      h.unshift({t:C.title,u:shareUrl(),r:last&&last.results[0]?fmt(last.results[0].v,last.results[0].f):''});localStorage.setItem('h67',JSON.stringify(h.slice(0,8)))}catch(e){}
  }
  function flash(b,t){var o=b.textContent;b.textContent=t;setTimeout(function(){b.textContent=o},1600)}
  var bs=document.getElementById('btnShare'),bc=document.getElementById('btnCopy'),bp=document.getElementById('btnPrint');
  if(bs)bs.addEventListener('click',function(){save();var u=shareUrl();if(navigator.share){navigator.share({title:C.title,url:u}).catch(function(){})}else{navigator.clipboard&&navigator.clipboard.writeText(u);flash(bs,'Link copied ✓')}});
  if(bc)bc.addEventListener('click',function(){save();var t=C.title+'\n'+(last?last.results.map(function(x){return x.l+': '+fmt(x.v,x.f)}).join('\n'):'')+'\n'+shareUrl();navigator.clipboard&&navigator.clipboard.writeText(t);flash(bc,'Copied ✓')});
  if(bp)bp.addEventListener('click',function(){save();print()});

  // Pass result into the lead form so the inquiry arrives with context
  var lf=document.getElementById('resultLead');
  if(lf)lf.addEventListener('submit',function(){var h=lf.querySelector('[name=calculation]');if(h&&last)h.value=C.title+' | '+last.results.map(function(x){return x.l+': '+fmt(x.v,x.f)}).join(' | ')+' | '+shareUrl()},true);

  // Was this helpful
  document.querySelectorAll('[data-vote]').forEach(function(b){b.addEventListener('click',function(){
    var w=document.getElementById('voteWrap');if(w)w.innerHTML='<p class="muted">Thanks for the feedback — it helps us improve this calculator.</p>';
    try{localStorage.setItem('v67-'+C.id,b.getAttribute('data-vote'))}catch(e){}
  })});
})();
