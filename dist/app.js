(() => {
  'use strict';
  const results = window.RESEARCH_RESULTS;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const metricDescriptions = {
    'ROC-AUC': 'ROC-AUC measures how well scores rank positive cases above negative cases across thresholds.',
    Accuracy: 'Accuracy is the proportion of all held-out cases classified correctly.',
    Precision: 'Precision asks: of the cases predicted positive, how many were actually positive?',
    Recall: 'Recall asks: of all the actual positive cases, how many did the classifier identify?',
    F1: 'F1 is the harmonic mean of precision and recall, balancing the two at the chosen decision rule.'
  };
  const insights = {
    'ROC-AUC': 'Random Forest leads on ROC-AUC at 0.8062. The closest competitors remain close; statistical significance was not established.',
    Accuracy: 'Random Forest leads on accuracy at 73.89%. KNN follows at 73.47% — a small difference of 0.42 percentage points.',
    Precision: 'AdaBoost leads on precision at 0.7699, only 0.0001 ahead of Random Forest. This narrow gap should not be overstated.',
    Recall: 'KNN leads on recall at 0.6885, identifying a larger share of positive cases in this comparison than the other six models.',
    F1: 'KNN leads on F1 at 0.7197, versus 0.7185 for Random Forest. Neither is a universal winner across all five metrics.'
  };
  const metrics = ['Accuracy', 'Precision', 'Recall', 'F1', 'ROC-AUC'];
  const shortName = name => name.replace(' (Tuned)', '').replace('Gaussian Naive Bayes', 'Gaussian NB');
  const element = (tag, className, value) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (value !== undefined) node.textContent = value;
    return node;
  };
  function renderRanking(metric) {
    const target = document.querySelector('#ranking');
    target.replaceChildren();
    target.setAttribute('aria-label', 'Model ranking by ' + metric);
    const ranked = [...results].sort((a,b) => b[metric] - a[metric]);
    ranked.forEach((model, index) => {
      const row = element('div', 'ranking-row');
      row.setAttribute('role', 'listitem');
      row.setAttribute('aria-label', `${index + 1}. ${model.Model}: ${model[metric].toFixed(4)} ${metric}`);
      const label = element('div', 'model-label');
      label.append(element('span', '', String(index + 1).padStart(2,'0')));
      label.append(document.createTextNode(shortName(model.Model)));
      if (model.Model.includes('(Tuned)')) label.append(element('small', '', ' (tuned)'));
      const track = element('div', 'bar-track');
      track.setAttribute('aria-hidden', 'true');
      const bar = element('div', 'bar-fill');
      track.append(bar);
      row.append(label, track, element('div', 'bar-value', model[metric].toFixed(4)));
      target.append(row);
      // Two animation frames ensure the zero-width initial state is painted.
      requestAnimationFrame(() => requestAnimationFrame(() => { bar.style.width = (model[metric]*100) + '%'; }));
    });
    document.querySelector('#chart-title').textContent = 'Ranking by ' + (metric === 'F1' ? 'F1 score' : metric);
    document.querySelector('#metric-description').textContent = metricDescriptions[metric];
    document.querySelector('#winner-note').textContent = insights[metric];
    document.querySelectorAll('[data-metric]').forEach(btn => btn.setAttribute('aria-pressed', String(btn.dataset.metric === metric)));
  }
  document.querySelectorAll('[data-metric]').forEach(btn => btn.addEventListener('click', () => renderRanking(btn.dataset.metric)));

  const selects = [document.querySelector('#model-a'), document.querySelector('#model-b')];
  selects.forEach(select => results.forEach(model => {
    const option = element('option', '', model.Model);
    option.value = model.Model;
    select.append(option);
  }));
  selects[0].value = 'Random Forest (Tuned)';
  selects[1].value = 'KNN (Tuned)';
  function renderComparison() {
    const [a,b] = selects.map(select => results.find(model => model.Model === select.value));
    const target = document.querySelector('#comparison');
    target.replaceChildren();
    metrics.forEach(metric => {
      const row = element('div', 'compare-row');
      row.setAttribute('aria-label', `${metric}: ${a.Model} ${a[metric].toFixed(4)}; ${b.Model} ${b[metric].toFixed(4)}`);
      const track = element('div', 'duo-track');
      track.setAttribute('aria-hidden', 'true');
      [a,b].forEach(model => { const bar=element('span');bar.style.width=(model[metric]*100)+'%';track.append(bar); });
      const values = element('div','duo-values');
      [a,b].forEach(model => values.append(element('span','',model[metric].toFixed(4))));
      row.append(element('span','label',metric),track,values);
      target.append(row);
    });
    const winsA=metrics.filter(metric=>a[metric]>b[metric]).length;
    const winsB=metrics.filter(metric=>b[metric]>a[metric]).length;
    const note=a.Model===b.Model ? 'The same model is selected twice. Choose a different model to explore the trade-offs.' : `${shortName(a.Model)} leads on ${winsA} of 5 metrics; ${shortName(b.Model)} on ${winsB}. These are rounded point estimates, not evidence of statistically significant differences.`;
    document.querySelector('#comparison-note').textContent=note;
  }
  selects.forEach(select=>select.addEventListener('change',renderComparison));

  const methods = [
    ['DATA QUALITY','Start with the measurements.','The source had no missing values, but that did not make every measurement plausible. Fixed rules removed extreme height, weight, blood-pressure and BMI values before modelling.','Cleaning rules are included in the analysis notebook and preparation script.'],
    ['FEATURE ENGINEERING','Make assumptions testable.','Age was converted from days to years. BMI and pulse pressure were engineered, then examined through correlation, statistical checks and feature ablation. The final comparison used ten input features.','Ablation analysis did not find a material predictive gain from the engineered feature sets.'],
    ['EXPERIMENTAL CONTROL','Use the same held-out split.','Models shared an 80/20 stratified train–test split with random_state=42. Numerical scaling stayed inside the pipeline. Five-fold stratified cross-validation supported model development.','Random Forest and KNN used tuned configurations; the other five retained their documented baseline settings.'],
    ['EVALUATION','Let more than one metric speak.','Accuracy, precision, recall, F1 and ROC-AUC were considered together. Additional threshold analysis was kept separate from the seven-model primary comparison.','The report discusses overfitting, dataset provenance, calibration and the limits of one test split.']
  ];
  document.querySelectorAll('[data-method]').forEach(btn=>btn.addEventListener('click',()=>{
    const index=Number(btn.dataset.method), info=methods[index];
    document.querySelector('#method-number').textContent=String(index+1).padStart(2,'0');
    ['kicker','title','body','foot'].forEach((key,i)=>document.querySelector('#method-'+key).textContent=info[i]);
    document.querySelectorAll('[data-method]').forEach(other=>other.setAttribute('aria-pressed',String(other===btn)));
    const detail=document.querySelector('.method-detail');detail.classList.remove('refresh');
    requestAnimationFrame(()=>detail.classList.add('refresh'));
  }));
  let paused=reduceMotion.matches;
  const motion=document.querySelector('#motion');
  function setMotion(){
    document.body.classList.toggle('motion-paused',paused);
    document.documentElement.style.scrollBehavior=paused?'auto':'';
    motion.setAttribute('aria-pressed',String(paused));
    document.querySelector('#motion-label').textContent=paused?'Motion paused':'Pause motion';
  }
  motion.addEventListener('click',()=>{paused=!paused;setMotion();});
  reduceMotion.addEventListener('change',e=>{paused=e.matches;setMotion();});
  setMotion();renderRanking('ROC-AUC');renderComparison();
  if(!reduceMotion.matches && 'IntersectionObserver' in window){
    const observer=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('revealed');observer.unobserve(entry.target);}}),{threshold:.06});
    document.querySelectorAll('.intro-grid,.dataset-flow,.method,.results-panel,.takeaways,.compare-layout,.findings-grid,.resource-list').forEach(node=>{node.classList.add('reveal-ready');observer.observe(node);});
  }
})();
