import unittest
from planner import build_plan
from mcp import handle
SAMPLE={'alerts':[{'type':t,'title':t,'reason':'sample','confidence':'estimated'} for t in ('pet','stock','waste')]}
class PlanTests(unittest.TestCase):
 def test_combines_domains(self):
  p=build_plan(SAMPLE);self.assertTrue(p['combined']);self.assertEqual(len(p['actions']),3)
 def test_away_adds_care(self):
  p=build_plan(SAMPLE,True);self.assertEqual(p['actions'][0]['id'],'arrange-care')
 def test_no_signals(self):
  self.assertFalse(build_plan({'alerts':[]})['combined'])
 def test_mcp_tool(self):
  r=handle({'jsonrpc':'2.0','id':1,'method':'tools/list'},lambda:None,lambda a:None,lambda a:None,lambda a:None)
  self.assertIn('get_connected_plan',[t['name'] for t in r['result']['tools']])
 def test_mcp_plan(self):
  r=handle({'jsonrpc':'2.0','id':2,'method':'tools/call','params':{'name':'get_connected_plan','arguments':{'away_tomorrow':True}}},lambda:None,lambda a:None,lambda a:None,lambda a:build_plan(SAMPLE,a['away_tomorrow']))
  self.assertIn('arrange-care',str(r))
if __name__=='__main__':unittest.main()
