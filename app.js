// This is an editorial example from previous conversation—not verified AA or OpenAI scores.
// No redistribution of third-party benchmark datasets; no false claims of live updates.
(() => {
  'use strict';
  const rows = [["6 Astra Max",53,326,"极复杂研究、旗舰级交付"],["6.1 Sol Max",52,72,"高难推理、复杂项目终稿"],["6 Astra 极高",52,231,"疑难研究、复杂方案复核"],["6.1 Sol 极高",51,39,"复杂项目、精细终稿"],["6 Astra 高",51,173,"重要决策、复杂交付"],["6.1 Sol 高",50,32,"专业交付、复杂材料"],["6 Astra 中",50,154,"跨工具项目、长期规划"],["6.1 Sol 中",48,21,"日常办公、开发研究"],["6 Sol Max",48,104,"深度代码、系统设计"],["5.6 Sol Max",47,199,"旧项目深度审查"],["6 Astra 轻度",46,82,"高质量改写、快速审稿"],["6 Sol 极高",44,52,"复杂代码、严格校验"],["5.6 Sol 极高",44,118,"深度代码审查、旧项目"],["6.1 Sol 轻度",42,13,"快速改写、重点检查"],["6 Sol 高",42,37,"专业开发、复杂文档"],["5.6 Sol 高",42,81,"专业写作、旧项目维护"],["5.6 Terra Max",42,140,"大型资料整合、深度分析"],["6 Sol 中",40,25,"日常编程、研究整理"],["5.6 Sol 中",39,50,"文档撰写、常规开发"],["5.6 Terra 极高",38,63,"多文件资料分析"],["6 Luna Max",38,7,"高性价比批量分析"],["5.6 Luna Max",37,18,"批量摘要、内容整理"],["6 Luna 极高",35,4,"明确约束下的推理"],["5.6 Luna 极高",35,9,"结构化摘要、批处理"],["6 Sol 轻度",34,13,"小改动、重点检查"],["5.6 Terra 高",34,34,"长文归纳、一般分析"],["5.6 Sol 轻度",33,26,"简单代码、小篇写作"],["6 Luna 高",33,3,"批量总结、日常整理"],["5.6 Luna 高",32,4,"结构化摘要、批处理"],["5.6 Terra 中",30,18,"常规资料整理"],["6 Luna 中",30,2,"清晰指令下的改写"],["5.6 Terra 轻度",27,14,"基础归纳、简单问答"],["5.6 Luna 中",25,2,"批量分类、格式转换"],["6 Luna 轻度",22,0.45,"关键词提取、任务分流"],["5.6 Luna 轻度",21,1,"简单提取、格式整理"]];
  const catalog = rows.map(([name,score,cost,purpose],id) => {
    const family=name.startsWith('6.1 ')?'6.1':name.startsWith('5.6 ')?'5.6':'6';
    const type=/Astra/.test(name)?'astra':/Terra/.test(name)?'terra':/Luna/.test(name)?'luna':'sol';
    const badge=name==='6 Astra Max'?'旗舰质量':name==='6.1 Sol 高'?'质量甜点位':name==='6.1 Sol 中'?'日常甜点位':name==='6 Luna 高'?'省钱甜点位':'';
    return {id,name,score,cost,purpose,family,type,badge};
  });
  const icon={astra:'◉',sol:'☀',terra:'◈',luna:'☾'};
  const $ = selector => document.querySelector(selector);
  const $$ = selector => [...document.querySelectorAll(selector)];
  let family='all',sort='score',search='';
  const escapeHtml=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  function filtered(){
    const q=search.trim().toLocaleLowerCase();
    return catalog.filter(r=>(family==='all'||r.family===family)&&(!q||[r.name,r.purpose,r.badge].some(s=>s.toLocaleLowerCase().includes(q))))
      .sort((a,b)=>sort==='score'?b.score-a.score||a.cost-b.cost:sort==='cost'?a.cost-b.cost||b.score-a.score:a.name.localeCompare(b.name,'zh-CN'));
  }
  function render(){
    const items=filtered(),table=$('#rankingRows'),mobile=$('#mobileCards');
    $('#resultInfo').textContent='显示 '+items.length+' / '+catalog.length+' 项';
    $('#heroCount').textContent=catalog.length;
    $('#empty').hidden=items.length!==0;
    table.innerHTML=items.map((r,i)=>`<tr class="${r.type}"><td>${i+1}</td><td><span class="model-icon"><span>${icon[r.type]}</span></span><span class="model-name">${escapeHtml(r.name)}</span>${r.badge?`<span class="pill"><span>${escapeHtml(r.badge)}</span></span>`:''}</td><td>${r.score}</td><td>≈ ${r.cost}</td><td>${escapeHtml(r.purpose)}</td></tr>`).join('');
    mobile.innerHTML=items.map((r,i)=>`<article class="model-card ${r.type}"><div class="model-card-head"><div class="model-card-name"><span class="model-icon"><span>${icon[r.type]}</span></span>${escapeHtml(r.name)}</div><strong>#${i+1}</strong></div>${r.badge?`<span class="pill"><span>${escapeHtml(r.badge)}</span></span>`:''}<div class="model-card-stat"><div><small>参考智能指数</small><strong>${r.score}</strong></div><div><small>参考相对消耗</small><strong>≈ ${r.cost}</strong></div></div><div class="model-card-note">${escapeHtml(r.purpose)}</div></article>`).join('');
  }
  $$('.filter').forEach(btn=>btn.addEventListener('click',()=>{
    family=btn.dataset.family;
    $$('.filter').forEach(b=>{b.classList.toggle('active',b===btn);b.setAttribute('aria-pressed',String(b===btn));});
    render();
  }));
  $('#sort').addEventListener('change',e=>{sort=e.target.value;render();});
  $('#search').addEventListener('input',e=>{search=e.target.value;render();});
  let toastTimer;
  function toast(text){const t=$('#toast');t.textContent=text;t.hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>t.hidden=true,2400);}
  $('#shareBtn').addEventListener('click',async()=>{
    const url=location.href.split('#')[0];
    try{if(navigator.share)await navigator.share({title:'MODEL ATLAS 模式选用参考表',url});
    else if(navigator.clipboard) {await navigator.clipboard.writeText(url);toast('链接已复制，可以分享给朋友');}
    else{toast('请复制浏览器地址栏中的网址');}}
    catch(e){if(e?.name!=='AbortError')toast('请复制浏览器地址栏中的网址');}
  });
  render();
})();
