/* 67858.com core script — nav, theme, consent, hidden-contact routing, forms, video facades */
(function(){
  'use strict';
  // ---- Contact routing: the address is never present as plain text in HTML or JS ----
  var _k=__EMAILCODES__;
  function _r(){return _k.map(function(c){return String.fromCharCode(c-7)}).join('')}
  window.S67={
    endpoint:function(){return 'https://formsubmit.co/ajax/'+_r()},
    donate:function(amount,purpose){
      var u='https://www.paypal.com/donate?business='+encodeURIComponent(_r())+'&currency_code=USD&no_recurring=0&item_name='+encodeURIComponent('67858.com support — '+(purpose||'General operations'));
      if(amount)u+='&amount='+encodeURIComponent(amount);
      window.open(u,'_blank','noopener');
    }
  };
  document.addEventListener('click',function(e){
    var a=e.target.closest('[data-mail]');
    if(!a)return;
    e.preventDefault();
    var subj=a.getAttribute('data-mail')||'Inquiry from 67858.com';
    window.location.href='mai'+'lto:'+_r()+'?subject='+encodeURIComponent(subj);
  });

  // ---- Theme ----
  var root=document.documentElement;
  try{var t=localStorage.getItem('t67');if(t)root.setAttribute('data-theme',t)}catch(e){}
  var tb=document.getElementById('themeBtn');
  if(tb)tb.addEventListener('click',function(){
    var dark=root.getAttribute('data-theme')==='dark'||(!root.getAttribute('data-theme')&&matchMedia('(prefers-color-scheme: dark)').matches);
    var n=dark?'light':'dark';root.setAttribute('data-theme',n);
    try{localStorage.setItem('t67',n)}catch(e){}
  });

  // ---- Mobile menu ----
  var bg=document.getElementById('burger'),mn=document.getElementById('menu');
  if(bg&&mn)bg.addEventListener('click',function(){var o=mn.classList.toggle('open');bg.setAttribute('aria-expanded',o)});

  // ---- Footer year ----
  document.querySelectorAll('[data-year]').forEach(function(el){el.textContent=new Date().getFullYear()});

  // ---- Cookie consent (pair with Google CMP in AdSense > Privacy & messaging for EEA/UK) ----
  var cb=document.getElementById('consent');
  var seen=null;try{seen=localStorage.getItem('c67')}catch(e){}
  if(cb&&!seen){cb.classList.add('show')}
  document.querySelectorAll('[data-consent]').forEach(function(b){b.addEventListener('click',function(){
    try{localStorage.setItem('c67',b.getAttribute('data-consent'))}catch(e){}
    cb.classList.remove('show');
  })});

  // ---- Forms: all submissions go to one hidden inbox via FormSubmit AJAX ----
  document.querySelectorAll('form[data-form]').forEach(function(f){
    f.addEventListener('submit',function(e){
      e.preventDefault();
      var msg=f.querySelector('.form-msg');
      if(f.querySelector('.hp input')&&f.querySelector('.hp input').value){return}
      if(!f.checkValidity()){f.reportValidity();return}
      var data={};new FormData(f).forEach(function(v,k){data[k]=data[k]?data[k]+', '+v:v});
      data._subject='[67858.com] '+(f.getAttribute('data-form')||'Form')+' submission';
      data._template='table';data._captcha='false';
      data.page=location.href;
      var btn=f.querySelector('[type=submit]');if(btn){btn.disabled=true;btn.dataset.t=btn.textContent;btn.textContent='Sending…'}
      fetch(S67.endpoint(),{method:'POST',headers:{'Content-Type':'application/json','Accept':'application/json'},body:JSON.stringify(data)})
        .then(function(r){return r.json()})
        .then(function(){
          if(msg){msg.className='form-msg ok';msg.textContent=f.getAttribute('data-ok')||'Thank you — we received your submission and will reply within 1–2 business days.'}
          f.reset();
          if(window.gtag)gtag('event','generate_lead',{form:f.getAttribute('data-form')});
        })
        .catch(function(){if(msg){msg.className='form-msg err';msg.textContent='Network issue — please try again in a moment.'}})
        .finally(function(){if(btn){btn.disabled=false;btn.textContent=btn.dataset.t}});
    });
  });

  // ---- YouTube facades (load iframe only on click: faster pages, better Core Web Vitals) ----
  document.querySelectorAll('.video[data-yt]').forEach(function(v){
    v.addEventListener('click',function(){
      var id=v.getAttribute('data-yt');
      v.innerHTML='<iframe src="https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0" title="'+(v.getAttribute('data-title')||'Video')+'" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>';
    },{once:true});
  });

  // ---- Sticky CTA after scroll; one-time exit-intent offer (desktop only) ----
  var sc=document.getElementById('stickyCta');
  if(sc&&!document.body.hasAttribute('data-nocta'))addEventListener('scroll',function(){sc.classList.toggle('show',scrollY>900)},{passive:true});
  var md=document.getElementById('exitModal');
  if(md&&matchMedia('(min-width:900px)').matches&&!document.body.hasAttribute('data-nocta')){
    var shown=false;try{shown=sessionStorage.getItem('x67')}catch(e){}
    document.addEventListener('mouseout',function(e){
      if(shown||e.relatedTarget||e.clientY>10)return;
      shown=true;try{sessionStorage.setItem('x67','1')}catch(e){}
      md.classList.add('show');
    });
    md.addEventListener('click',function(e){if(e.target===md||e.target.closest('.x'))md.classList.remove('show')});
  }

  // ---- Site-wide quick search (hero + hub) ----
  var qs=document.getElementById('quickSearch');
  if(qs)qs.addEventListener('submit',function(e){
    e.preventDefault();var q=qs.querySelector('input').value.trim();
    if(/^\d[\d\s-]*$/.test(q)){location.href=qs.getAttribute('data-lab')+'?n='+encodeURIComponent(q.replace(/\D/g,''))}
    else location.href=qs.getAttribute('data-hub')+'?q='+encodeURIComponent(q);
  });
})();
