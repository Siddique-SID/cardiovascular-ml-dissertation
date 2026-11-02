(() => {
  'use strict';
  const data = window.TABLE_DATA;
  const metrics = ['Accuracy','Precision','Recall','F1','ROC-AUC'];
  const dataset = document.querySelector('#dataset');
  const search = document.querySelector('#search-model');
  const format = document.querySelector('#score-format');
  const rows = document.querySelector('#result-rows');
  const sourceText = {
    reported: 'Historical point estimates from dissertation Table 3.2 / Appendix A, cross-checked against the original working notebook. Small differences were not shown to be statistically significant.',
    rerun: 'Current-environment rerun of the seven primary held-out model fits. Full cross-validation, tuning, ablation and threshold experiments were not rerun. These values remain separate from the historical dissertation figures.',
    delta: 'Rerun minus reported value. Positive means the rerun score was higher; negative means lower. Differences are not confidence intervals or evidence of statistical significance. The causes have not been established.'
  };
  let sortKey = 'ROC-AUC', direction = -1, visible = [];
  const node = (tag, text, cls) => {const n=document.createElement(tag);if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n;};
  function number(value,metric) {
    const delta=dataset.value==='delta';
    const sign=delta && value>0?'+':'';
    if(format.value==='percent' && metric!=='ROC-AUC')return sign+(value*100).toFixed(2)+(delta?' pp':'%');
    return sign+value.toFixed(4);
  }
  function render() {
    const active=data[dataset.value],query=search.value.trim().toLowerCase(),delta=dataset.value==='delta';
    visible=active.filter(row=>row.Model.toLowerCase().includes(query)).sort((a,b)=>{
      const comparison=sortKey==='Model'?a.Model.localeCompare(b.Model):a[sortKey]-b[sortKey];
      return comparison*direction || a.Model.localeCompare(b.Model);
    });
    rows.replaceChildren();
    const leaders=Object.fromEntries(metrics.map(m=>[m,Math.max(...visible.map(r=>r[m]))]));
    visible.forEach(row=>{
      const tr=node('tr'),name=node('th',row.Model);name.scope='row';tr.append(name);
      metrics.forEach(metric=>{
        const cell=node('td',number(row[metric],metric));
        if(!delta && row[metric]===leaders[metric]){cell.className='leader';cell.title='Column leader in current view';}
        if(delta)cell.className=row[metric]>0?'delta-positive':row[metric]<0?'delta-negative':'';
        tr.append(cell);
      });
      rows.append(tr);
    });
    if(!visible.length){const td=node('td','No models match this filter. Clear the search or choose Reset.','empty');td.colSpan=6;const tr=node('tr');tr.append(td);rows.append(tr);}
    document.querySelectorAll('thead th').forEach(th=>{
      const selected=th.dataset.key===sortKey;th.setAttribute('aria-sort',selected?(direction===1?'ascending':'descending'):'none');
      th.querySelector('span').textContent=selected?(direction===1?'↑':'↓'):'↕';
    });
    const metric=sortKey==='Model'?'ROC-AUC':sortKey;
    const best=[...visible].sort((a,b)=>delta?Math.abs(b[metric])-Math.abs(a[metric]):b[metric]-a[metric])[0];
    document.querySelector('#model-count').replaceChildren(document.createTextNode(visible.length+' '),node('small','/ '+active.length));
    document.querySelector('#best-label').textContent=(delta?'LARGEST ABSOLUTE ':'BEST ')+metric+' IN VIEW';
    document.querySelector('#best-score').textContent=best?number(best[metric],metric):'—';
    document.querySelector('#best-model').textContent=best?best.Model:'No matching models';
    const order=sortKey==='Model'?(direction===1?'A–Z':'Z–A'):(direction===1?'lowest first':'highest first');
    document.querySelector('#table-status').textContent=`${visible.length} of ${active.length} models · sorted by ${sortKey}, ${order}`;
    document.querySelector('#table-caption').textContent=dataset.value==='reported'?'Reported dissertation results · Table 3.2 / Appendix A':dataset.value==='rerun'?'Portfolio primary held-out rerun · see environment record':'Difference between rerun and reported scores · rerun minus reported';
    document.querySelector('#source-context').textContent=sourceText[dataset.value];
    document.querySelector('.explorer-key>span').style.visibility=delta?'hidden':'visible';
    document.querySelector('#export-table').disabled=visible.length===0;
  }
  document.querySelectorAll('thead th button').forEach(button=>button.addEventListener('click',()=>{
    const key=button.closest('th').dataset.key;
    direction=key===sortKey?-direction:key==='Model'?1:-1;sortKey=key;render();
  }));
  dataset.addEventListener('change',render);format.addEventListener('change',render);search.addEventListener('input',render);
  document.querySelector('#reset-table').addEventListener('click',()=>{dataset.value='reported';search.value='';format.value='decimal';sortKey='ROC-AUC';direction=-1;render();});
  document.querySelector('#export-table').addEventListener('click',()=>{
    const quote=v=>'"'+String(v).replaceAll('"','""')+'"';
    const csv=[['Model',...metrics].join(','),...visible.map(row=>[quote(row.Model),...metrics.map(m=>row[m])].join(','))].join('\r\n')+'\r\n';
    const blob=new Blob([csv],{type:'text/csv;charset=utf-8;'}),url=URL.createObjectURL(blob),a=document.createElement('a');
    a.href=url;a.download='cardio-'+dataset.value+'-results.csv';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  });
  render();
})();
