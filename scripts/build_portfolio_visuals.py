"""Generate README tables, browser data and animated summaries from recorded CSVs.

No models are fitted and no metrics are invented by this presentation script.
"""
from pathlib import Path
import csv,json,math,re
from PIL import Image, ImageDraw, ImageFont
ROOT=Path(__file__).resolve().parents[1]
METRICS=['Accuracy','Precision','Recall','F1','ROC-AUC']
INK='#102f43';PAPER='#f3f7f8';TEAL='#087f8c';SOFT='#dcebed';MUTED='#587685';CORAL='#ce856c'

def load(name):
    with (ROOT/'results'/name).open() as f:
        return [{k:(v if k=='Model' else float(v)) for k,v in row.items()} for row in csv.DictReader(f)]

def font(size,bold=False):
    names=[('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if bold else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'),
           ('/System/Library/Fonts/Supplemental/Arial Bold.ttf' if bold else '/System/Library/Fonts/Supplemental/Arial.ttf'),
           ('arialbd.ttf' if bold else 'arial.ttf')]
    for name in names:
        try:return ImageFont.truetype(name,size)
        except OSError:pass
    return ImageFont.load_default(size=size)

def line(draw,xy,text,size=16,fill=INK,bold=False):draw.text(xy,text,font=font(size,bold),fill=fill)

def save_gif(frames,name,durations):
    palette=frames[0].quantize(colors=48)
    frames=[im.quantize(palette=palette) for im in frames]
    frames[0].save(ROOT/'docs'/name,save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=True,disposal=1)
    frames[0].convert('RGB').save(ROOT/'docs'/name.replace('.gif','.png'))

def frame():
    im=Image.new('RGB',(1100,380),PAPER);d=ImageDraw.Draw(im)
    d.rectangle((0,0,1099,379),outline='#ccdfe5',width=2)
    return im,d

def workflow():
    frames=[]
    steps=[('01','CLEAN','70,000 → 68,627','Fixed plausibility rules'),('02','SPLIT','80% / 20%','Stratified · seed 42'),('03','COMPARE','7 classifiers','5-fold development CV'),('04','EVALUATE','5 metrics','Shared held-out test')]
    foot=['Check measurements before modelling. 1,373 source records were removed.','Keep the evaluation split consistent: 54,901 training and 13,726 test records.','Compare seven algorithms; Random Forest and KNN use tuned configurations.','Read accuracy, precision, recall, F1 and ROC-AUC together.']
    for active in range(4):
        im,d=frame();line(d,(35,25),'THE EXPERIMENT / FOUR CONTROLLED STEPS',13,TEAL,True)
        line(d,(35,61),'Follow the data, not just the score.',31,INK,True)
        for i,(num,title,value,detail) in enumerate(steps):
            x=35+i*263;y=135
            d.rounded_rectangle((x,y,x+240,y+141),radius=6,fill=INK if i==active else '#e4eef1',outline=TEAL if i==active else '#ccdde4',width=2)
            line(d,(x+17,y+13),num,12,'#80d6c9' if i==active else MUTED)
            line(d,(x+17,y+39),title,15,'#ffffff' if i==active else INK,True)
            line(d,(x+17,y+69),value,21,'#80d6c9' if i==active else TEAL,True)
            line(d,(x+17,y+108),detail,10,'#accbd4' if i==active else MUTED)
            if i<3:line(d,(x+244,y+56),'›',22,TEAL,True)
        d.line((35,305,1065,305),fill='#ccdde4',width=1)
        line(d,(35,325),foot[active],13,MUTED)
        frames.append(im)
    save_gif(frames,'experiment-flow.gif',[2700]*4)

def leaders(reported):
    frames=[]
    for metric in METRICS:
        ordered=sorted(reported,key=lambda row:row[metric],reverse=True)
        im,d=frame();line(d,(35,22),'REPORTED DISSERTATION RESULTS / '+metric.upper(),13,TEAL,True)
        line(d,(35,53),'Different metrics. Different leaders.',28,INK,True)
        for i,row in enumerate(ordered):
            y=107+i*30
            name=row['Model'].replace('Gaussian Naive Bayes','Gaussian NB').replace(' (Tuned)',' *')
            line(d,(35,y),name,12,INK,i==0)
            d.rectangle((280,y+2,1000,y+19),fill='#e1ecef')
            d.rectangle((280,y+2,280+int(720*row[metric]),y+19),fill=TEAL if i==0 else '#80acb6')
            line(d,(1016,y),f'{row[metric]:.4f}',12,INK,i==0)
        line(d,(280,324),'0.00',8,MUTED);line(d,(620,324),'0.50',8,MUTED);line(d,(970,324),'1.00',8,MUTED)
        line(d,(35,350),'Table 3.2 / Appendix A · recorded point estimates · * tuned model · not a live training run',10,MUTED)
        frames.append(im)
    save_gif(frames,'metric-leaders.gif',[3200]*5)

def table(rows):
    best={m:max(r[m] for r in rows) for m in METRICS}
    out=['| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |','| --- | ---: | ---: | ---: | ---: | ---: |']
    for row in rows:
        vals=[f'**{row[m]:.4f}**' if row[m]==best[m] else f'{row[m]:.4f}' for m in METRICS]
        out.append('| '+row['Model']+' | '+' | '.join(vals)+' |')
    return '\n'.join(out)

def main():
    reported=load('final_model_comparison.csv');rerun=load('reproduced_model_comparison.csv')
    by_name={r['Model']:r for r in rerun}
    delta=[{'Model':r['Model'],**{m:by_name[r['Model']][m]-r[m] for m in METRICS}} for r in reported]
    (ROOT/'dist/explorer-data.js').write_text('window.TABLE_DATA = '+json.dumps({'reported':reported,'rerun':rerun,'delta':delta},indent=2)+';\n')
    readme=(ROOT/'README.md').read_text()
    summaries=['| Metric | Leading model | Reported score |','| --- | --- | ---: |']
    for metric in METRICS:
        best=max(reported,key=lambda r:r[metric]);summaries.append(f'| {metric} | {best["Model"]} | **{best[metric]:.4f}** |')
    comparison=['| Model | Reported accuracy | Rerun accuracy | Reported ROC-AUC | Rerun ROC-AUC |','| --- | ---: | ---: | ---: | ---: |']
    for a in reported:
        b=by_name[a['Model']];comparison.append(f'| {a["Model"]} | {a["Accuracy"]:.4f} | {b["Accuracy"]:.4f} | {a["ROC-AUC"]:.4f} | {b["ROC-AUC"]:.4f} |')
    for key,value in [('RESULTS',table(reported)),('LEADERS','\n'.join(summaries)),('RERUN','\n'.join(comparison))]:
        pattern=f'<!-- BEGIN {key} -->.*?<!-- END {key} -->'
        readme,n=re.subn(pattern,f'<!-- BEGIN {key} -->\n{value}\n<!-- END {key} -->',readme,flags=re.S)
        if n!=1:raise ValueError(f'Expected one {key} region, found {n}')
    (ROOT/'README.md').write_text(readme)
    workflow();leaders(reported)
    print('Updated CSV-backed tables, explorer data and two animated summaries.')

if __name__=='__main__':main()
