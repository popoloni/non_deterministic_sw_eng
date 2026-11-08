#!/usr/bin/env python3
"""Calibrate from a real pilot CSV. Never substitutes synthetic data for observations.
Usage: python calibrate_from_pilot.py pilot.csv --out calibrated.json
Schema documented in pilot/DATA_DICTIONARY.md.
"""
import csv, json, argparse, math, statistics, random
from collections import defaultdict
REQUIRED=['task_id','mode','assigned_at','accepted','released','developer_minutes','reviewer_minutes','verification_minutes','model_cost_eur','compute_cost_eur','followup_minutes','incident_loss_eur','deployment_outcome','observation_days','risk_class']
NUM=['developer_minutes','reviewer_minutes','verification_minutes','model_cost_eur','compute_cost_eur','followup_minutes','incident_loss_eur']
def load(path):
 with open(path,newline='') as f:
  r=csv.DictReader(f)
  missing=set(REQUIRED)-set(r.fieldnames or [])
  if missing:raise ValueError('Missing columns: '+', '.join(sorted(missing)))
  rows=list(r)
 if not rows:raise ValueError('NO_REAL_PILOT_DATA: empty file; calibration prohibited')
 seen=set()
 for i,row in enumerate(rows,2):
  if not row['task_id'] or row['task_id'] in seen:raise ValueError(f'Invalid or repeated task_id at row {i}')
  seen.add(row['task_id'])
  if row['accepted'] not in ('0','1') or row['released'] not in ('0','1'):raise ValueError(f'Invalid binary flag row {i}')
  if row['released']=='1' and row['accepted']!='1':raise ValueError(f'Release without acceptance row {i}')
  if row['deployment_outcome'] not in ('not_deployed','success','rollback','incident','unknown'):raise ValueError(f'Bad deployment outcome row {i}')
  for k in NUM:
   v=float(row[k]);
   if not math.isfinite(v) or v<0:raise ValueError(f'Invalid {k} row {i}')
   row[k]=v
  row['observation_days']=float(row['observation_days'])
  if row['observation_days']<0:raise ValueError('Negative observation window')
 return rows
def summarize(rows,dev_rate=90,review_rate=110,verify_rate=90):
 modes=defaultdict(list)
 for r in rows:modes[r['mode']].append(r)
 results={}
 for mode,group in modes.items():
  n=len(group); accepted=sum(r['accepted']=='1' for r in group);released=sum(r['released']=='1' for r in group)
  costs=[r['developer_minutes']*dev_rate/60+r['reviewer_minutes']*review_rate/60+r['verification_minutes']*verify_rate/60+r['model_cost_eur']+r['compute_cost_eur']+r['followup_minutes']*dev_rate/60+r['incident_loss_eur'] for r in group]
  total=sum(costs)
  results[mode]={'tasks':n,'accepted':accepted,'released':released,'acceptance_rate':accepted/n,'release_rate':released/n,'observed_cost_eur':round(total,2),'cost_per_assigned_eur':round(total/n,2),'cost_per_accepted_eur':round(total/accepted,2) if accepted else None,'cost_per_released_eur':round(total/released,2) if released else None,'mean_reviewer_minutes':round(statistics.mean(r['reviewer_minutes'] for r in group),2),'mean_developer_minutes':round(statistics.mean(r['developer_minutes'] for r in group),2),'mean_followup_minutes':round(statistics.mean(r['followup_minutes'] for r in group),2),'deployment_outcomes':{k:sum(r['deployment_outcome']==k for r in group) for k in ['not_deployed','success','rollback','incident','unknown']},'min_observation_days':min(r['observation_days'] for r in group)}
 return results
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('csv');p.add_argument('--out',default='calibrated.json');p.add_argument('--developer-rate',type=float,default=90);p.add_argument('--reviewer-rate',type=float,default=110);p.add_argument('--verifier-rate',type=float,default=90)
 a=p.parse_args(); rows=load(a.csv)
 result={'status':'OBSERVED_PILOT_DESCRIPTIVE_ONLY','sample_n':len(rows),'modes':summarize(rows,a.developer_rate,a.reviewer_rate,a.verifier_rate),'limits':['No causal interpretation without assignment/compliance analysis','Observation windows and risk strata must be aligned','Unobserved tail risk and correlated failures remain unestimated','Cost per accepted is descriptive, not geometric-retry expectation']}
 with open(a.out,'w') as f:json.dump(result,f,indent=2)
 print(json.dumps(result,indent=2))
