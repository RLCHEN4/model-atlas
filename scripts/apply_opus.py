"""Extend the approved MODEL ATLAS homepage; never rewrite the GPT snapshot."""
from pathlib import Path
import hashlib
import json
import re

BASE = '0614f0258ce4d6d93f44c463a9d54bcb631be00a35ad77f43cd437ca0c9bae09'
CSS = '''
/* Opus addition: retain the approved layout, colors and centered SVG icons. */
.opus-section{margin-top:60px}.opus-section .section-kicker{color:#b6664a}.opus-section h2 em{color:#bd674b}
.opus-model-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}
.opus-model-card{border:1px solid #eeddd5;border-radius:18px;background:linear-gradient(120deg,#fffaf7,#fcf1eb);padding:23px}
.opus-card-head{display:flex;gap:13px;align-items:center}.opus-model-card h3{margin:0;color:#95533e;font-size:20px}.opus-model-card .model-icon,.family-opus .model-icon{background:#bf7055}
.opus-version-badge{font-size:10px;padding:3px 7px;background:#f2dfd4;border-radius:5px;color:#8f5744;display:inline-block;margin-top:4px}
.opus-price-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:20px 0 16px;padding-bottom:16px;border-bottom:1px solid #eeddd5}
.opus-price-grid small{display:block;font-size:11px;color:#997c70}.opus-price-grid strong{font-size:25px;letter-spacing:-.7px;color:#975b43;white-space:nowrap}.opus-price-grid strong span{font-size:11px;margin-left:3px}
.opus-meta{font-size:12px;color:#866e66;line-height:1.8;margin:0 0 15px}.opus-actions{display:flex;align-items:center;justify-content:space-between;gap:12px}
.opus-compare-btn{background:#ac6048;color:#fff;padding:10px 14px;border:0;border-radius:9px;font-size:12px;font-weight:750}.opus-source{font-size:11px;color:#975a46;text-decoration:underline;white-space:nowrap}
.opus-disclosure{font-size:11px;line-height:1.85;color:#8f7a72;margin:13px 0 0}.filter-tab.opus-tab.active{color:#a65e45}
.ranking-table tbody tr.family-opus{background:#fff6ef}.family-opus .model-name{color:#9d583f}.family-opus .model-badge{background:#ac6c52}
.cell-note{display:block;font-size:10px;font-weight:500;color:#8d97a9;margin-top:3px;line-height:1.5}.missing-val{font-size:12px;font-weight:600;color:#8793a6;white-space:nowrap}.unranked{font-size:10px;font-weight:600;color:#8c97a9}
.model-api-note{font-size:10px;color:#9e7a69;margin-top:4px;line-height:1.5}.model-api-note a{text-decoration:underline}
.benchmark-divider td{background:#f4f6fa!important;color:#6b7d99;font-size:11px;font-weight:650;padding:11px 20px!important;text-align:left!important}
.compare-cards{grid-template-columns:repeat(var(--compare-cols,3),minmax(0,1fr))}.compare-cards .comparison-field{min-height:70px}.compare-cards .comparison-field:last-of-type{min-height:100px}
.comparison-field .spec-text{font-size:14px;line-height:1.6;display:block;color:#536d91;margin-top:4px}.comparison-field .price-value{font-size:19px}
.compare-card .source-detail{font-size:11px;line-height:1.7;margin-bottom:8px;min-height:3.4em}.compare-card.family-opus{border-color:#e6cabc;background:#fff9f5}.compare-card.family-opus .comparison-field{border-color:#eeddd5}.compare-card.family-opus .comparison-field b{color:#9f6047}
.compare-card-top{display:flex;align-items:center;gap:9px;margin-bottom:5px}.comparison-source{font-size:11px;color:#93614c;text-decoration:underline;display:inline-block;margin-top:12px}
.comparison-caveat{padding:11px 14px;border-radius:9px;background:#fff4e6;color:#936a35;font-size:12px;line-height:1.7;margin:0 0 16px}
.opus-compare-btn:focus-visible,.opus-source:focus-visible{outline:2px solid #a95f47;outline-offset:3px}
@media(max-width:800px){.opus-section{margin-top:48px}.opus-model-card{padding:18px}.opus-model-card h3{font-size:18px}}
@media(max-width:540px){.opus-model-grid{grid-template-columns:1fr}.compare-cards{grid-template-columns:1fr}.compare-cards .comparison-field:last-of-type{min-height:0}.opus-model-card{padding:19px}.tab-group{justify-content:flex-start;gap:2px}.filter-tab{padding:8px 10px}.status-banner .status-right{width:100%}.compare-card .source-detail{min-height:0}}
@media print{.opus-actions{display:none}.opus-section{margin-top:20px}.opus-model-grid{grid-template-columns:repeat(2,1fr)}.opus-model-card{padding:12px}.opus-price-grid{margin:10px 0}}
'''
PANEL = '''<section class="opus-section" aria-labelledby="opus-title">
<div class="section-top"><div><span class="section-kicker">NEW / CLAUDE OPUS</span><h2 id="opus-title">加入 Opus，<em>一起看差异。</em></h2></div><p>Anthropic 官方规格与费率 · 核对于 2026-10-09</p></div>
<div class="opus-model-grid" id="opusModels"></div>
<p class="opus-disclosure">同一型号的五档 effort 共用 token 单价，但消耗量不同；Max 不等于固定任务费用。评分与每任务成本尚未接入的 Opus 不参与排名，可照常勾选对比。</p>
</section>
'''
SPECS = {
    'verified_on': '2026-10-09',
    'effort_source': 'https://platform.claude.com/docs/en/build-with-claude/effort',
    'price_basis': 'USD / 1M tokens; standard API, excluding cache, batch, fast mode and regional modifiers',
    'models': [
        {'api_id':'claude-opus-5-5','name':'Claude Opus 5.5','status':'本次核对最新 Opus','input_mtok_usd':4,'output_mtok_usd':20,'context_tokens':1000000,'max_output_tokens':128000,'default_effort':'medium','source_url':'https://platform.claude.com/docs/en/models/opus-5-5/overview'},
        {'api_id':'claude-opus-5','name':'Claude Opus 5','status':'上一代 Opus','input_mtok_usd':5,'output_mtok_usd':25,'context_tokens':1000000,'max_output_tokens':128000,'default_effort':'high','source_url':'https://platform.claude.com/docs/en/models/opus-5/overview'}
    ]
}
JS = r'''(() => {
'use strict';
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const meta=window.MODEL_ATLAS_OPUS_DATA, selected=new Set();
let data={models:[]}, family='all', sort='score', search='';
const finite=n=>typeof n==='number'&&Number.isFinite(n);
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const num=n=>finite(n)?n.toLocaleString('en-US',{maximumFractionDigits:2}):'—';
const money=n=>finite(n)?'$'+n.toLocaleString('en-US',{minimumFractionDigits:n<.01?3:2,maximumFractionDigits:4}):'—';
const glyph=p=>`<svg class="icon-glyph" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">${p}</svg>`;
const icons={
astra:glyph('<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="5.2"/><circle cx="12" cy="12" r="1.9"/>'),
sol:glyph('<circle cx="12" cy="12" r="4.5"/><path d="M12 2.5v2M12 19.5v2M2.5 12h2M19.5 12h2M5.28 5.28l1.42 1.42M17.3 17.3l1.42 1.42M5.28 18.72l1.42-1.42M17.3 6.7l1.42-1.42"/>'),
terra:glyph('<path d="m12 3 9 9-9 9-9-9Z"/><path d="m12 8 4 4-4 4-4-4Z" fill="currentColor" stroke="none"/>'),
luna:glyph('<path d="M20.9 13A9 9 0 1 1 11 3.1 7 7 0 0 0 20.9 13Z"/>'),
opus:glyph('<path d="M12 3v18M3 12h18M5.64 5.64l12.72 12.72M5.64 18.36 18.36 5.64M8.56 3.69l6.88 16.62M3.69 8.56l16.62 6.88M3.69 15.44l16.62-6.88M8.56 20.31l6.88-16.62"/>')};
const effortLabels={max:'Max',xhigh:'极高',high:'高',medium:'中',low:'轻度'};
const mode=m=>Object.hasOwn(icons,m.mode)?m.mode:'sol';
function effort(m){if(m.effort)return m.effort;const n=m.name.toLowerCase();return n.includes('max')?'max':/xhigh|极高/.test(n)?'xhigh':/high|高/.test(n)?'high':/medium|中/.test(n)?'medium':'low';}
function best(m){
 const texts={astra:{max:'复杂研究 · 关键成果复核',xhigh:'深度研究 · 疑难方案',high:'重要决策 · 复杂交付',medium:'跨工具项目 · 长期规划',low:'高质量改写 · 专业审稿'},sol:{max:'高难推理 · 单项深度任务',xhigh:'复杂项目 · 精细终稿',high:'专业交付 · 复杂材料',medium:'日常研究 · 开发项目',low:'快速改写 · 重点校对'},luna:{max:'批量分析 · 规模化处理',xhigh:'明确约束 · 快速推理',high:'批量总结 · 内容整理',medium:'结构化输出 · 日常改写',low:'关键词提取 · 任务分流'},terra:{max:'大型文档 · 深度分析',xhigh:'多文件资料分析',high:'长文归纳 · 内容分析',medium:'常规资料整理',low:'基础归纳 · 简单问答'},opus:{max:'建议：高难分析 · 深入复核',xhigh:'建议：长程开发 · 多步骤代理',high:'建议：复杂编码 · 技术研究',medium:'建议：日常开发 · 质量成本平衡',low:'建议：简单任务 · 快速子任务'}};
 return texts[mode(m)][effort(m)];
}
function metric(m,k){return k==='cost'?m.cost_usd:k==='value'?(finite(m.score)&&finite(m.cost_usd)?m.score/(m.cost_usd+.05):null):m.score;}
function sorted(rows,k='score'){return [...rows].sort((a,b)=>{const x=metric(a,k),y=metric(b,k);if(!finite(x)||!finite(y))return Number(finite(y))-Number(finite(x));const d=k==='cost'?x-y:y-x;return d||(k==='cost'?(b.score??0)-(a.score??0):(a.cost_usd??Infinity)-(b.cost_usd??Infinity));});}
function picks(){
 const rows=sorted(data.models.filter(m=>finite(m.score)));
 const find=(type,lev)=>rows.find(m=>m.mode===type&&effort(m)===lev&&(type!=='sol'||m.family==='6.1')&&(type!=='luna'||m.family==='6'));
 return [{title:'旗舰质量',sub:'关键研究 / 疑难方案复核',tag:'FLAGSHIP QUALITY',model:rows[0]},
 {title:'质量甜点位',sub:'专业交付 / 复杂材料',tag:'HIGH QUALITY',model:find('sol','high')},
 {title:'日常甜点位',sub:'办公研究 / 开发任务',tag:'EVERYDAY SWEET SPOT',model:find('sol','medium')},
 {title:'省钱甜点位',sub:'批量总结 / 常规整理',tag:'BUDGET PICK',model:find('luna','high')}];
}
function overview(){
 const scored=sorted(data.models.filter(m=>finite(m.score))), costs=sorted(data.models.filter(m=>finite(m.cost_usd)),'cost');
 $('#modelCount').innerHTML=num(data.models.length)+' <small>个</small>';
 $('#topScore').innerHTML=num(scored[0]?.score)+' <small>pts</small>';$('#topModel').textContent=scored[0]?.name||'暂无数据';
 $('#minCost').innerHTML=money(costs[0]?.cost_usd)+' <small>USD</small>';$('#minCostModel').textContent=costs[0]?.name||'暂无数据';
 $('#lastCheck').textContent=meta.verified_on;$('#versionLabel').textContent='仅 Opus 规格 / 费率 · 非测评分数更新';
 $('#statusBanner').className='status-banner status-demo';
 $('#statusBanner').innerHTML='<div class="status-left"><span class="status-icon">ⓘ</span><span><strong>GPT：35 条未核验示例　/　Opus：官方规格与费率已核对</strong><br>Opus 同口径评分与每任务成本未接入，不参与数值排名；本站未启用实时测评更新。</span></div><span class="status-right">Opus 规格核对 · '+esc(meta.verified_on)+'</span>';
 $('#footerFreshness').textContent='OPUS SPECS · '+meta.verified_on+' / NOT LIVE';
 const max=Math.max(1,...scored.map(m=>m.score));
 $('#heroBars').innerHTML=scored.slice(0,5).map(m=>`<div class="barline"><span class="bar-label" title="${esc(m.name)}">${esc(m.name)}</span><div class="bar-track"><div class="bar-fill ${{astra:'purple',sol:'orange',terra:'green',luna:'blue'}[mode(m)]}" style="width:${m.score/max*100}%"></div></div><span class="bar-number">${num(m.score)}</span></div>`).join('');
 $('#picks').innerHTML=picks().filter(p=>p.model).map(p=>{const m=p.model,c=mode(m);return `<article class="pick ${c}"><div class="pick-symbol" aria-hidden="true">${icons[c]}</div><div class="pick-tag">${p.tag}</div><h3 title="${esc(m.name)}">${esc(m.name)}</h3><p>${p.title} · ${p.sub}</p><span class="pick-letter" aria-hidden="true">${c[0].toUpperCase()}</span></article>`;}).join('');
 $('#opusModels').innerHTML=meta.models.map(m=>`<article class="opus-model-card"><div class="opus-card-head"><span class="model-icon" aria-hidden="true">${icons.opus}</span><div><h3>${esc(m.name)}</h3><span class="opus-version-badge">${esc(m.status)} · Anthropic</span></div></div><div class="opus-price-grid"><div><small>输入 / 百万 token</small><strong>$${num(m.input_mtok_usd)}</strong></div><div><small>输出 / 百万 token</small><strong>$${num(m.output_mtok_usd)}</strong></div><div><small>上下文窗口</small><strong>1M <span>tokens</span></strong></div></div><p class="opus-meta">Low / Medium / High / Xhigh / Max · 默认 ${esc(m.default_effort)}<br>最大常规输出 128K tokens · 标准 API 单价，不含缓存、批量、Fast 模式与区域加价。</p><div class="opus-actions"><button class="opus-compare-btn" type="button" data-opus-compare="${esc(m.api_id+':'+m.default_effort)}">与 GPT 对比 ↗</button><a class="opus-source" href="${esc(m.source_url)}" target="_blank" rel="noopener noreferrer">官方规格 ↗</a></div></article>`).join('');
}
function render(){
 const rows=sorted(data.models.filter(m=>(family==='all'||m.family===family)&&(m.name+' '+(effortLabels[m.effort]||'')).toLowerCase().includes(search)),sort);
 $('#filteredCount').textContent=rows.length+' 个模式';$('#tableFoot').textContent={score:'按参考指数降序',cost:'按参考任务成本升序',value:'按参考指数 / 成本的启发式排序'}[sort]+' · 空缺项不排名';
 let rank=0,separator=false;
 $('#rankingRows').innerHTML=rows.length?rows.map(m=>{
  const op=m.mode==='opus',c=mode(m),ranked=finite(metric(m,sort));let before='';
  if(!ranked&&!separator){separator=true;before='<tr class="benchmark-divider"><td colspan="7">Claude Opus · 官方规格 / 费率已核对 · 同口径评分与每任务成本未接入，以下不排名</td></tr>';}
  if(ranked)rank++;
  const badge=op?'规格已核对'+(m.effort===m.default_effort?' · 默认档':''):(picks().find(p=>p.model?.id===m.id)?.title||'');
  return before+`<tr class="family-${c}" data-model-id="${esc(m.id)}"><td>${ranked?`<span class="rank-number ${rank<=3?'top3':''}">${rank}</span>`:'<span class="unranked">未排</span>'}</td><td><div class="model-cell"><span class="model-icon" aria-hidden="true">${icons[c]}</span><div><div class="model-name">${esc(m.name)}</div>${badge?`<span class="model-badge">${esc(badge)}</span>`:''}${op?`<div class="model-api-note"><a href="${esc(m.source_url)}" target="_blank" rel="noopener noreferrer">API 输入 $${num(m.input_mtok_usd)} / 输出 $${num(m.output_mtok_usd)} · 每百万 token ↗</a></div>`:''}</div></div></td><td>${finite(m.score)?`<span class="score-val">${num(m.score)}</span>`:'<span class="missing-val">待接入</span>'}</td><td>${finite(m.cost_usd)?`<span class="usd-cell">${money(m.cost_usd)}</span>`:'<span class="missing-val">—</span><small class="cell-note">不是 token 单价</small>'}</td><td>${finite(m.relative_cost)?`<span class="relative-cell">≈ ${num(m.relative_cost)}</span>`:'<span class="missing-val">—</span>'}</td><td class="best-cell">${esc(best(m))}</td><td><input type="checkbox" class="compare-checkbox" aria-label="选择 ${esc(m.name)} 用于对比" data-id="${esc(m.id)}" ${selected.has(m.id)?'checked':''}></td></tr>`;
 }).join(''):'<tr><td colspan="7" class="empty-row">没有找到匹配的模式，可以换个关键词或版本。</td></tr>';
}
function dock(){$('#compareNum').textContent=selected.size;$('#compareDock').hidden=!selected.size;}
function compare(){
 const rows=[...selected].map(id=>data.models.find(m=>m.id===id)).filter(Boolean);if(!rows.length)return;
 const mixed=rows.some(m=>m.mode==='opus'), field=(label,value,cls='')=>`<div class="comparison-field"><small>${label}</small><b class="${cls}">${value}</b></div>`;
 $('#compareResults').innerHTML=(mixed?'<p class="comparison-caveat">Opus 的规格与 API 费率已核对；GPT 数值仍为演示。未接入的测评项留空，不能据此认定谁更强或更便宜。</p>':'')+`<div class="compare-cards" style="--compare-cols:${rows.length}">`+rows.map(m=>{
  const op=m.mode==='opus';
  return `<article class="compare-card family-${mode(m)}"><div class="compare-card-top"><span class="model-icon" aria-hidden="true">${icons[mode(m)]}</span><strong>${esc(m.name)}</strong></div><p class="source-detail">${op?'Anthropic 官方规格 · '+esc(meta.verified_on):'原始参考示例 · 名称 / 数值未核验'}<br>${esc(best(m))}</p>`+
  field('智能指数 ↑',finite(m.score)?num(m.score):'待接入同口径评测',finite(m.score)?'':'spec-text')+
  field('每任务成本 · USD',finite(m.cost_usd)?money(m.cost_usd):'未接入',finite(m.cost_usd)?'':'spec-text')+
  field('相对消耗 · 每 $0.01 为 1',finite(m.relative_cost)?'≈ '+num(m.relative_cost):'—',finite(m.relative_cost)?'':'spec-text')+
  (mixed?field('标准 API 输入 / 百万 token',op?money(m.input_mtok_usd):'未核验，暂不提供',op?'price-value':'spec-text')+
  field('标准 API 输出 / 百万 token',op?money(m.output_mtok_usd):'未核验，暂不提供',op?'price-value':'spec-text')+
  field('上下文 / 最大常规输出',op?'1M / 128K tokens':'未核验，暂不提供','spec-text')+
  field('推理档位',op?esc(m.effort)+'（默认 '+esc(m.default_effort)+'）':esc(effort(m))+' · 参考名称','spec-text')+
  field('计费与设置说明',op?'标准 API；不含缓存、批量、Fast 与区域加价。effort 控制 token 消耗，不改变本表单价。':'仅演示任务成本，不能作为 API 预算。','spec-text'):'')+
  (op?`<a class="comparison-source" href="${esc(m.source_url)}" target="_blank" rel="noopener noreferrer">官方规格 ↗</a> · <a class="comparison-source" href="${esc(meta.effort_source)}" target="_blank" rel="noopener noreferrer">档位说明 ↗</a>`:'')+'</article>';
 }).join('')+'</div>';
 $('#compareDialog').showModal();
}
function exportCsv(){
 let rank=0;
 const rows=[['参考排名','模型','模型家族','参考智能指数','参考单任务成本USD','参考相对消耗','适用任务（编辑建议）','数据状态','API输入USD/百万token','API输出USD/百万token','上下文tokens','最大常规输出tokens','effort','规格核对日期','规格来源','档位来源','价格口径'],...sorted(data.models).map(m=>[finite(m.score)?++rank:'',m.name,m.family,m.score,m.cost_usd,m.relative_cost,best(m),m.mode==='opus'?'仅官方规格/费率已核对；测评未接入':'GPT原始示例；名称/数值未核验',m.input_mtok_usd,m.output_mtok_usd,m.context_tokens,m.max_output_tokens,m.effort,m.mode==='opus'?meta.verified_on:'',m.source_url,m.mode==='opus'?meta.effort_source:'',m.mode==='opus'?meta.price_basis:'未核验参考任务成本'])];
 const cell=v=>{let t=String(v??'');if(/^[=+@\t\r]/.test(t)||(/^[-]/.test(t)&&typeof v!=='number'))t="'"+t;return '"'+t.replaceAll('"','""')+'"';};
 const text='\ufeff'+rows.map(row=>row.map(cell).join(',')).join('\r\n');
 const url=URL.createObjectURL(new Blob([text],{type:'text/csv;charset=utf-8'})),a=document.createElement('a');a.href=url;a.download='MODEL-ATLAS-GPT-REFERENCE-OPUS-SPECS.csv';document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
}
$$('.filter-tab').forEach(b=>b.addEventListener('click',()=>{family=b.dataset.family;$$('.filter-tab').forEach(t=>{t.classList.toggle('active',t===b);t.setAttribute('aria-pressed',String(t===b));});render();}));
$('#search').addEventListener('input',e=>{search=e.target.value.trim().toLowerCase();render();});
$('#sort').addEventListener('change',e=>{sort=e.target.value;render();});
$('#downloadCsv').addEventListener('click',exportCsv);$('#printPage').addEventListener('click',()=>window.print());
$('#rankingRows').addEventListener('change',e=>{if(!e.target.matches('.compare-checkbox'))return;const id=e.target.dataset.id;if(e.target.checked){if(selected.size>=3){e.target.checked=false;alert('最多同时对比 3 个模式');return;}selected.add(id);}else selected.delete(id);dock();});
$('#opusModels').addEventListener('click',e=>{const b=e.target.closest('[data-opus-compare]');if(!b)return;selected.clear();selected.add(b.dataset.opusCompare);const gpt=data.models.find(m=>m.family==='6.1'&&m.mode==='sol'&&effort(m)==='high');if(gpt)selected.add(gpt.id);dock();render();compare();});
$('#clearCompare').addEventListener('click',()=>{selected.clear();dock();render();});$('#openCompare').addEventListener('click',compare);$('#closeCompare').addEventListener('click',()=>$('#compareDialog').close());
$('#compareDialog').addEventListener('click',e=>{const d=$('#compareDialog'),r=d.getBoundingClientRect();if(e.target===d&&(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom))d.close();});
try{
 const snap=window.MODEL_ATLAS_INLINE_DATA;if(!Array.isArray(snap?.models)||!snap.models.length)throw new Error('没有有效参考记录');
 const extra=meta.models.flatMap(m=>['max','xhigh','high','medium','low'].map(e=>({...m,id:m.api_id+':'+e,name:m.name+' ('+effortLabels[e]+')',family:'opus',mode:'opus',effort:e,score:null,cost_usd:null,relative_cost:null,score_delta:null})));
 data={...snap,models:[...snap.models,...extra]};overview();render();
}catch(e){$('#statusBanner').className='status-banner status-error';$('#statusBanner').textContent='页面数据读取失败：'+e.message;$('#rankingRows').innerHTML='<tr><td colspan="7" class="empty-row">无法加载数据</td></tr>';}
})();'''

def build(base):
    if hashlib.sha256(base.encode()).hexdigest() != BASE:
        raise ValueError('Approved source changed; stop instead of overwriting another edit.')
    s=base
    def replace(a,b):
        nonlocal s
        if s.count(a)!=1:
            raise ValueError('Expected one unique anchor: '+a[:80])
        s=s.replace(a,b)
    replace('MODEL ATLAS 原设计视觉还原预览。35 个演示模型模式、筛选排序和对比功能；分数与成本为未经官方核验的参考示例，不是实时榜单。','MODEL ATLAS：GPT 参考模式与 Claude Opus 对比。保留 35 条 GPT 演示数据，新增 Opus 5.5 / 5 的官方规格、API 费率及推理档位；缺少同口径数据的项目不参与排名。')
    replace('<title>MODEL ATLAS · GPT 模型智能选用榜</title>','<title>MODEL ATLAS · GPT × Claude Opus 模型对比</title>')
    replace('DESIGN REFERENCE','MODEL COMPARISON')
    replace('参考快照 · 未核验','GPT 参考 / Opus 官方规格')
    replace('GPT MODEL INTELLIGENCE INDEX','GPT × CLAUDE OPUS')
    replace('GPT-6.1 / GPT-6 / GPT-5.6 的 35 个模式演示参考。<br class="desktop-br">保留原版完整视觉与交互；分数及成本尚未核验。','保留 GPT 全模式参考，加入 Claude Opus 5.5 / 5。<br class="desktop-br">同屏比较推理档位、适用场景与官方 API 费率。')
    replace('导出演示 CSV','导出对比 CSV')
    replace('<p>GPT-6.1 / 6 / 5.6</p>','<p>35 个 GPT 参考 + 10 个 Opus 档位</p>')
    replace('数据核验时间 <span>04 / UPDATE','Opus 规格核对 <span>04 / UPDATE')
    replace('按模型版本筛选','按模型系列筛选')
    replace('<button type="button" class="filter-tab" data-family="5.6" aria-pressed="false">GPT-5.6</button>','<button type="button" class="filter-tab" data-family="5.6" aria-pressed="false">GPT-5.6</button>\n<button type="button" class="filter-tab opus-tab" data-family="opus" aria-pressed="false">Claude Opus</button>')
    replace('展示用模拟参考数字 · 不是官方测评结果','GPT 数值为未核验示例 · Opus 未接入同口径评测，不参与数值排名')
    replace('35 模式设计还原演示版，未连接实时数据。本站非 OpenAI 或 Artificial Analysis 官方产品。','GPT 参考示例 + Opus 官方规格，不是实时测评榜单。本站非 OpenAI、Anthropic 或 Artificial Analysis 官方产品。')
    replace('智能指数越高越好；成本越低越好。仅比较本页未核验的演示数字，不代表 Artificial Analysis 官方测试结果。','数据口径不同：GPT 分数与任务成本为未核验示例；Opus 仅型号、推理档位、规格及标准 API 费率经官方文档核对。空缺项不作优劣判断，token 单价不能替代每任务成本。')
    replace('此处为原参考表中的演示智能指数，未完成官方来源核验。数值高低只用于验证排行榜展示和排序功能。','GPT 指数来自原演示快照，未核验。Opus 暂未接入同一基准版本的分数，用“待接入”表示，不按零分处理，也不参与名次或性价比排序。')
    replace('本页面展示的任务成本为演示值，尚未验证，不可用于预算、API 采购或产品性能比较。','GPT 任务成本为未核验示例。Opus 官方价格按每百万 token 计价，在对比面板单列；未实测的任务成本留空，不能用 token 单价换算代替。')
    replace('<span>HIGHER IS BETTER ↗</span>','<span>GPT DEMO ONLY ↗</span>')
    replace('    <section id="leaderboard" class="board-section"',PANEL+'    <section id="leaderboard" class="board-section"')
    replace('</style>',CSS+'\n</style>')
    start=s.index('<script>\n(() => {');end=s.index('</script>',start)
    s=s[:start]+'<script>window.MODEL_ATLAS_OPUS_DATA='+json.dumps(SPECS,ensure_ascii=False,indent=2)+';</script>\n<script>\n'+JS+'\n'+s[end:]
    snapshot=lambda t:re.search(r'window\.MODEL_ATLAS_INLINE_DATA=(.*?);</script>',t,re.S).group(1)
    assert snapshot(s)==snapshot(base),'Original GPT values changed'
    return s

if __name__=='__main__':
    import sys
    source=Path(sys.argv[1] if len(sys.argv)>1 else 'index.html')
    target=Path(sys.argv[2] if len(sys.argv)>2 else 'index.html')
    result=build(source.read_text(encoding='utf-8'))
    target.write_text(result,encoding='utf-8')
    b=result.encode();print(json.dumps({'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'blob':hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()}))
