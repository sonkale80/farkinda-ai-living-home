import unittest, tempfile, os
from pathlib import Path
import app
class TestV2(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.old=app.DB;app.DB=Path(self.tmp.name)/'test.db';app.init()
 def tearDown(self):app.DB=self.old;self.tmp.cleanup()
 def test_restock(self):
  r=app.add_event({'kind':'restock','subject':'Süt','quantity':200,'confirmed':True});self.assertEqual(r['new_quantity'],1100)
 def test_consume(self):
  r=app.add_event({'kind':'consume','subject':'Süt','quantity':100,'confirmed':True});self.assertEqual(r['new_quantity'],800)
 def test_no_negative(self):
  with self.assertRaises(ValueError):app.add_event({'kind':'consume','subject':'Süt','quantity':2000,'confirmed':True})
 def test_confirmation(self):
  with self.assertRaises(ValueError):app.add_event({'kind':'restock','subject':'Süt','quantity':1,'confirmed':False})
 def test_nan(self):
  with self.assertRaises(ValueError):app.add_event({'kind':'consume','subject':'Süt','quantity':float('nan'),'confirmed':True})
 def test_history(self):
  app.add_event({'kind':'restock','subject':'Süt','quantity':1,'confirmed':True});self.assertEqual(len(app.history()['events']),1)
 def test_forecast_updated(self):
  app.add_event({'kind':'consume','subject':'Süt','quantity':300,'confirmed':True});self.assertEqual(next(x for x in app.inventory_forecast()['items'] if x['name']=='Süt')['days_of_supply'],2)
if __name__=='__main__':unittest.main()
