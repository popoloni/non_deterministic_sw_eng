import unittest, tempfile, csv, os, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from calibrate_from_pilot import load,summarize,REQUIRED
class Tests(unittest.TestCase):
 def make(self, rows):
  f=tempfile.NamedTemporaryFile('w',newline='',suffix='.csv',delete=False)
  w=csv.DictWriter(f,fieldnames=REQUIRED);w.writeheader();w.writerows(rows);f.close();self.addCleanup(lambda:os.unlink(f.name));return f.name
 def row(self,**kwargs):
  r=dict(task_id='t1',mode='pair',assigned_at='2026-10-01',accepted='1',released='1',developer_minutes='30',reviewer_minutes='20',verification_minutes='10',model_cost_eur='2',compute_cost_eur='1',followup_minutes='0',incident_loss_eur='0',deployment_outcome='success',observation_days='30',risk_class='low');r.update(kwargs);return r
 def test_empty_fails_closed(self):
  with self.assertRaisesRegex(ValueError,'NO_REAL_PILOT_DATA'):load(self.make([]))
 def test_released_requires_acceptance(self):
  with self.assertRaises(ValueError):load(self.make([self.row(accepted='0')]))
 def test_negative_cost_rejected(self):
  with self.assertRaises(ValueError):load(self.make([self.row(model_cost_eur='-2')]))
 def test_duplicate_task_rejected(self):
  with self.assertRaises(ValueError):load(self.make([self.row(),self.row()]))
 def test_calculation(self):
  d=summarize(load(self.make([self.row()])))['pair'];self.assertEqual(d['accepted'],1);self.assertAlmostEqual(d['observed_cost_eur'],99.67,places=2)
if __name__=='__main__':unittest.main()
