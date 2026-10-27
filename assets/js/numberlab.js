/* 67858 Number Lab — math properties, cultural symbolism and a memorability score for any number */
(function(){
  'use strict';
  var inp=document.getElementById('labNum'),btn=document.getElementById('labGo');
  if(!inp)return;
  var CN={0:['líng','Completeness / a fresh start; neutral-positive'],1:['yī','Unity, being first; neutral'],2:['èr','Pairs and harmony — “good things come in pairs”'],3:['sān','Sounds like “birth/life” (shēng) in some dialects; positive'],4:['sì','Sounds like “death” (sǐ); widely avoided in phone numbers, floors and prices'],5:['wǔ','Five elements and five blessings; can also echo “wú” (nothing); mixed'],6:['liù','Sounds like “smooth/flowing” (liú); very positive for business'],7:['qī','Mixed: tied to togetherness, but also read as “gone”; often avoided in plates/phones'],8:['bā','Sounds like “prosper/fortune” (fā); the most sought-after digit'],9:['jiǔ','Sounds like “long-lasting” (jiǔ); longevity, endurance']};
  var COMBOS=[['168','“Prosperity all the way” (yī lù fā)'],['518','“I will prosper” (wǒ yào fā)'],['58','Often read as “I prosper” (wǒ fā)'],['88','Double fortune'],['888','Triple fortune — premium in plates and phone numbers'],['666','“Everything goes smoothly”; also slang for “awesome”'],['520','“I love you” (wǔ èr líng)'],['1314','“For a lifetime” (yī shēng yī shì)'],['99','Long-lasting'],['67','2025 viral slang “6-7”, Dictionary.com Word of the Year'],['678','Rising run 6-7-8: smooth → momentum → prosperity']];
  var NUM={1:'Leadership, independence, new beginnings',2:'Partnership, diplomacy, balance',3:'Creativity, expression, communication',4:'Structure, discipline, building foundations',5:'Change, freedom, adventure',6:'Responsibility, care, community',7:'Analysis, introspection, research',8:'Ambition, business, material success',9:'Compassion, completion, global outlook',11:'Master number — intuition and inspiration',22:'Master number — the “master builder”',33:'Master number — teaching and service'};
  function words(n){
    var a=['','one','two','three','four','five','six','seven','eight','nine','ten','eleven','twelve','thirteen','fourteen','fifteen','sixteen','seventeen','eighteen','nineteen'],t=['','','twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety'],sc=['','thousand','million','billion','trillion'];
    if(n===0)return 'zero';
    function h(x){var s='';if(x>=100){s+=a[Math.floor(x/100)]+' hundred';x%=100;if(x)s+=' '}if(x>=20){s+=t[Math.floor(x/10)];if(x%10)s+='-'+a[x%10]}else if(x)s+=a[x];return s}
    var out=[],i=0;while(n>0){var c=n%1000;if(c)out.unshift(h(c)+(sc[i]?' '+sc[i]:''));n=Math.floor(n/1000);i++}
    return out.join(' ');
  }
  function roman(n){if(n<1||n>3999)return 'n/a (1–3,999 only)';var m=[[1000,'M'],[900,'CM'],[500,'D'],[400,'CD'],[100,'C'],[90,'XC'],[50,'L'],[40,'XL'],[10,'X'],[9,'IX'],[5,'V'],[4,'IV'],[1,'I']],r='';m.forEach(function(p){while(n>=p[0]){r+=p[1];n-=p[0]}});return r}
  function factor(n){var f=[],d=2;while(d*d<=n){while(n%d===0){f.push(d);n/=d}d+=d===2?1:2}if(n>1)f.push(n);return f}
  function reduce(n){var s=String(n);while(s.length>1&&!['11','22','33'].includes(s)){s=String(s.split('').reduce(function(a,b){return a+ +b},0))}return +s}
  function memo(s){
    var sc=50,why=[];
    var uniq=new Set(s).size;
    if(s.length<=5){sc+=12;why.push('Short ('+s.length+' digits)')}else if(s.length>=9){sc-=12;why.push('Long ('+s.length+' digits)')}
    if(uniq<=2){sc+=18;why.push('Only '+uniq+' distinct digit(s)')}else if(uniq===3){sc+=9;why.push('3 distinct digits')}
    if(s===s.split('').reverse().join('')&&s.length>1){sc+=12;why.push('Palindrome')}
    var runs=(s.match(/(\d)\1+/g)||[]);if(runs.length){sc+=6*runs.length;why.push('Repeated digits: '+runs.join(', '))}
    var asc=0;for(var i=1;i<s.length;i++){if(+s[i]===+s[i-1]+1||+s[i]===+s[i-1]-1)asc++}
    if(asc>=2){sc+=asc*3;why.push('Sequential steps: '+asc)}
    var half=s.length/2;if(s.length%2===0&&s.slice(0,half)===s.slice(half)){sc+=10;why.push('Repeating halves')}
    var e8=(s.match(/8/g)||[]).length,e6=(s.match(/6/g)||[]).length,e4=(s.match(/4/g)||[]).length;
    if(e8){sc+=e8*3;why.push('Contains 8 ×'+e8+' (premium in East-Asian markets)')}
    if(e6){sc+=e6*2}
    if(e4){sc-=e4*4;why.push('Contains 4 ×'+e4+' (avoided in East-Asian markets)')}
    return {score:Math.max(1,Math.min(99,Math.round(sc))),why:why};
  }
  function render(raw){
    var s=String(raw||'').replace(/\D/g,'').replace(/^0+(?=\d)/,'');
    var res=document.getElementById('labOut');
    if(!s){res.innerHTML='<p class="muted">Type any whole number above — a phone number, a domain like 67858, a price or a date.</p>';return}
    if(s.length>15){s=s.slice(0,15)}
    var n=Number(s),big=n>1e12;
    var f=big?null:factor(n),prime=!big&&n>1&&f.length===1;
    var ds=s.split('').reduce(function(a,b){return a+ +b},0),dr=reduce(n);
    var m=memo(s);
    var combos=COMBOS.filter(function(c){return s.indexOf(c[0])>-1});
    var html='<div class="grid g2">'+
      '<div class="card"><span class="tag">Math profile</span><h3 class="mono">'+n.toLocaleString()+'</h3><dl class="kv">'+
      '<dt>In words</dt><dd>'+words(n)+'</dd>'+
      '<dt>Parity</dt><dd>'+(n%2?'Odd':'Even')+'</dd>'+
      '<dt>Prime?</dt><dd>'+(big?'Too large for instant test':(prime?'Yes — prime':'No'))+'</dd>'+
      '<dt>Prime factors</dt><dd>'+(big?'—':(n<2?'—':f.join(' × ')))+'</dd>'+
      '<dt>Digit sum</dt><dd>'+ds+'</dd>'+
      '<dt>Reversed</dt><dd>'+s.split('').reverse().join('')+'</dd>'+
      '<dt>Square root</dt><dd>'+Math.sqrt(n).toFixed(4)+'</dd>'+
      '<dt>Binary</dt><dd class="mono">'+n.toString(2)+'</dd>'+
      '<dt>Hex</dt><dd class="mono">'+n.toString(16).toUpperCase()+'</dd>'+
      '<dt>Roman</dt><dd>'+roman(n)+'</dd>'+
      '</dl></div>'+
      '<div class="card"><span class="tag">Memorability score</span><div class="score">'+m.score+'<small style="font-size:1rem" class="muted">/99</small></div>'+
      '<p>How easy this number is to recall, say and type — useful when choosing phone numbers, domains, product codes or prices.</p><ul>'+m.why.map(function(w){return '<li>'+w+'</li>'}).join('')+'</ul>'+
      '<p class="muted" style="font-size:.85rem">Heuristic based on length, repetition, symmetry and cultural digit preferences. For comparison only.</p></div>'+
      '</div>'+
      '<div class="card" style="margin-top:16px"><span class="tag">Digit-by-digit symbolism (Chinese homophones)</span><div class="digit-row">'+
      s.split('').map(function(d){return '<div class="dchip"><b>'+d+'</b><small><i>'+CN[d][0]+'</i> — '+CN[d][1]+'</small></div>'}).join('')+'</div>'+
      (combos.length?'<h3>Patterns found</h3><ul>'+combos.map(function(c){return '<li><b class="mono">'+c[0]+'</b>: '+c[1]+'</li>'}).join('')+'</ul>':'')+
      '</div>'+
      '<div class="card" style="margin-top:16px"><span class="tag">Numerology reduction</span><p><b class="mono">'+s.split('').join(' + ')+' = '+ds+'</b> → reduces to <b>'+dr+'</b>.</p><p>In Pythagorean numerology tradition, '+dr+' is associated with: <b>'+(NUM[dr]||'—')+'</b>.</p><p class="muted" style="font-size:.85rem">Numerology and number symbolism are cultural traditions shared here for interest and entertainment, not predictions or advice.</p></div>';
    res.innerHTML=html;
    try{history.replaceState(null,'','?n='+s)}catch(e){}
  }
  btn.addEventListener('click',function(){render(inp.value)});
  inp.addEventListener('keydown',function(e){if(e.key==='Enter')render(inp.value)});
  document.querySelectorAll('[data-try]').forEach(function(b){b.addEventListener('click',function(){inp.value=b.getAttribute('data-try');render(inp.value);inp.scrollIntoView({behavior:'smooth',block:'center'})})});
  var q=new URLSearchParams(location.search).get('n');
  inp.value=q||inp.value||'67858';render(inp.value);
})();
