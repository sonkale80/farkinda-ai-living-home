import unittest, tempfile, pathlib, json
import app, mcp
class TestFarkinda(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.original=app.DB;app.DB=pathlib.Path(self.temp.name)/'test.db';app.init()
 def tearDown(self):app.DB=self.original;self.temp.cleanup()
 def test_brief(self):
  a=app.analyze();self.assertTrue(a['alerts']);self.assertEqual(len(a['pets']),1)
 def test_tools(self):
  r=mcp.handle({'jsonrpc':'2.0','id':1,'method':'tools/list'},app.analyze,app.record_meal,app.prepare_action)
  self.assertEqual(len(r['result']['tools']),5)
 def test_initialize(self):
  r=mcp.handle({'jsonrpc':'2.0','id':1,'method':'initialize'},app.analyze,app.record_meal,app.prepare_action)
  self.assertEqual(r['result']['serverInfo']['name'],'farkinda-living-home')
 def test_meal_requires_consent(self):
  with self.assertRaises(ValueError):app.record_meal({'pet':'Pamuk','grams':100})
 def test_meal_rejects_nan(self):
  with self.assertRaises(ValueError):app.record_meal({'pet':'Pamuk','grams':float('nan'),'confirmed':True})
 def test_meal_record(self):self.assertTrue(app.record_meal({'pet':'Pamuk','grams':120,'confirmed':True})['ok'])
 def test_proposal_no_execution(self):self.assertFalse(app.prepare_action({'kind':'shopping'})['external_action_executed'])
 def test_mcp_call(self):
  r=mcp.handle({'jsonrpc':'2.0','id':2,'method':'tools/call','params':{'name':'get_household_brief','arguments':{}}},app.analyze,app.record_meal,app.prepare_action)
  self.assertIn('alerts',json.loads(r['result']['content'][0]['text']))
 def test_unknown_tool(self):
  r=mcp.handle({'jsonrpc':'2.0','id':2,'method':'tools/call','params':{'name':'bad'}},app.analyze,app.record_meal,app.prepare_action)
  self.assertIn('error',r)
if __name__=='__main__':unittest.main()
