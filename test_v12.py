import unittest, tempfile
from pathlib import Path
import app, mcp
class UpgradeTests(unittest.TestCase):
 def test_rejects_non_jsonrpc(self):
  r=mcp.handle({'id':1,'method':'ping'},lambda:None,lambda x:None,lambda x:None)
  self.assertEqual(r['error']['code'],-32600)
 def test_rejects_bad_arguments(self):
  r=mcp.handle({'jsonrpc':'2.0','id':1,'method':'tools/call','params':{'name':'get_connected_plan','arguments':{'away_tomorrow':'yes'}}},lambda:None,lambda x:None,lambda x:None,lambda x:None)
  self.assertTrue(r['result']['isError'])
 def test_forecast_tool_listed(self):
  r=mcp.handle({'jsonrpc':'2.0','id':1,'method':'tools/list'},lambda:None,lambda x:None,lambda x:None)
  self.assertIn('get_inventory_forecast',[x['name'] for x in r['result']['tools']])
 def test_forecast_math(self):
  with tempfile.TemporaryDirectory() as d:
   old=app.DB
   try:
    app.DB=Path(d)/'test.db';app.init();data=app.inventory_forecast()
    dog=next(x for x in data['items'] if x['name']=='Köpek maması')
    self.assertEqual(dog['days_of_supply'],4)
   finally:app.DB=old
 def test_meal_requires_confirmation(self):
  with self.assertRaises(ValueError):app.record_meal({'pet':'Pamuk','grams':100,'confirmed':False})
if __name__=='__main__':unittest.main()
