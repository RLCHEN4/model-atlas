// MODEL ATLAS public edition. Editorial recommendations only: no AA scores, rankings, or third-party dataset.
(() => {
  'use strict';
  const $ = s => document.querySelector(s);
  const $$ = s => [...document.querySelectorAll(s)];
  const tasks = [
    {name:'战略课题与高难研究',cat:'研究',difficulty:'非常复杂',tier:'flagship',why:'任务跨度大，需要分阶段拆解并反复核验',tip:'拆成子问题，并逐条验证关键结论'},
    {name:'重大方案与决策复核',cat:'研究',difficulty:'非常复杂',tier:'flagship',why:'假设多、风险高，需要多角度检验',tip:'要求列出反例、边界和证据'},
    {name:'技术架构与复杂重构',cat:'开发',difficulty:'复杂',tier:'high',why:'涉及依赖、接口与维护成本的权衡',tip:'先提供需求、代码结构和限制'},
    {name:'疑难 Bug 与代码审查',cat:'开发',difficulty:'复杂',tier:'high',why:'需要定位根因并验证修复',tip:'附报错、复现步骤及测试'},
    {name:'网页设计与产品原型',cat:'开发',difficulty:'中等',tier:'medium',why:'需求明确时能快速迭代布局和组件',tip:'附参考图和目标设备'},
    {name:'脚本、SQL 与常规开发',cat:'开发',difficulty:'中等',tier:'medium',why:'有可测试结果，适合快速完成',tip:'要求给出可运行样例'},
    {name:'品牌定位与整套营销方案',cat:'创作',difficulty:'复杂',tier:'high',why:'需要兼顾受众、信息结构和品牌一致性',tip:'明确目标用户、风格与预算'},
    {name:'长篇故事与剧本结构',cat:'创作',difficulty:'复杂',tier:'high',why:'要控制人物动机、情节和连贯性',tip:'先确定故事大纲再逐章迭代'},
    {name:'短视频文案与创意选题',cat:'创作',difficulty:'中等',tier:'medium',why:'容易通过风格样例和反馈快速改善',tip:'给出平台、时长、受众'},
    {name:'日常邮件、会议纪要',cat:'办公',difficulty:'轻度',tier:'light',why:'目标明确、格式固定',tip:'提供固定模板提升一致性'},
    {name:'批量摘要与关键词提取',cat:'办公',difficulty:'轻度',tier:'light',why:'规则清楚、重复性高',tip:'定义输出字段和示例'},
    {name:'表格分类与格式转换',cat:'办公',difficulty:'轻度',tier:'light',why:'主要是确定性规则与结构化处理',tip:'抽检边界案例'},
    {name:'多文件资料整理',cat:'研究',difficulty:'中等',tier:'medium',why:'需要统一分类、提炼主题和去重',tip:'保留来源以便追溯'},
    {name:'业务周报与项目复盘',cat:'办公',difficulty:'中等',tier:'medium',why:'需要组织信息并提取行动项',tip:'区分事实、问题与下一步'}
  ];
  const level = {
    flagship:{label:'旗舰深推理',css:'flagship'},
    high:{label:'高推理',css:'high'},
    medium:{label:'中等推理',css:'medium'},
    light:{label:'轻量快速',css:'light'}
  };
  let category='all';
  let search='';
  function escapeHtml(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
  function render(){
    const rows=tasks.filter(t=>(category==='all'||t.cat===category) && [t.name,t.cat,t.difficulty,t.why,t.tip,level[t.tier].label].some(s=>s.toLowerCase().includes(search)));
    $('#visibleCount').textContent=rows.length+' 项';
    $('#tableInfo').textContent='当前展示 '+rows.length+' / '+tasks.length+' 项';
    $('#taskRows').innerHTML=rows.length ? rows.map((t,i)=>`<tr><td>${i+1}</td><td><span class="task-title">${escapeHtml(t.name)}</span><small class="task-cat">${escapeHtml(t.cat)}</small></td><td><span class="difficulty">${escapeHtml(t.difficulty)}</span></td><td><span class="tier-pill ${level[t.tier].css}">${level[t.tier].label}</span></td><td>${escapeHtml(t.why)}</td><td>${escapeHtml(t.tip)}</td></tr>`).join('') : '<tr><td class="empty" colspan="6">没有找到相关任务，请换个关键词。</td></tr>';
  }
  $('#taskCount').innerHTML=tasks.length+' <em>项</em>';
  $$('.tab').forEach(button=>button.addEventListener('click',()=>{
    category=button.dataset.category;
    $$('.tab').forEach(t=>{t.classList.toggle('active',t===button);t.setAttribute('aria-pressed',String(t===button));});
    render();
  }));
  $('#searchInput').addEventListener('input',e=>{search=e.target.value.trim().toLowerCase();render();});
  $('#printPage').addEventListener('click',()=>window.print());
  let toastHandle;
  function toast(message){const el=$('#toast');el.textContent=message;el.hidden=false;clearTimeout(toastHandle);toastHandle=setTimeout(()=>el.hidden=true,2600);}
  $('#copyLink').addEventListener('click',async()=>{
    try{
      if(navigator.clipboard && location.protocol!=='file:')await navigator.clipboard.writeText(location.href.split('#')[0]);
      else {const tmp=document.createElement('textarea');tmp.value=location.href.split('#')[0];document.body.appendChild(tmp);tmp.select();if(!document.execCommand('copy'))throw new Error('Clipboard unavailable');tmp.remove();}
      toast('已复制网站地址，可以发给朋友。');
    }catch(e){toast('复制失败，请从浏览器地址栏复制网址。');}
  });
  function fmtDate(d){const x=new Date(d);return Number.isNaN(x.getTime())?'待首次检查':new Intl.DateTimeFormat('zh-CN',{timeZone:'Asia/Shanghai',year:'numeric',month:'2-digit',day:'2-digit'}).format(x);}
  // These are *link health checks*, not benchmark updates or model scores.
  fetch('./data/source-status.json',{cache:'no-store'}).then(r=>{if(!r.ok)throw new Error('unavailable');return r.json();}).then(meta=>{
    $('#checkDate').textContent=fmtDate(meta.checked_at);
    if(!meta.checked_at){$('#checkStatus').textContent='上线后首次定时检查';return;}
    const ok=(meta.targets||[]).filter(t=>t.ok).length;
    $('#checkStatus').textContent=`来源链接可访问 ${ok} / ${(meta.targets||[]).length}`;
    $('#footerUpdate').textContent='LINK CHECK · '+fmtDate(meta.checked_at);
  }).catch(()=>{$('#checkDate').textContent='未检测';$('#checkStatus').textContent='打开网页后显示链接检查状态';});
  render();
})();

