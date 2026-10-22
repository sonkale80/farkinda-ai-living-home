import unittest
from simulator import simulate
class SimulatorTests(unittest.TestCase):
 def setUp(self):
  self.brief={'alerts':[{'type':'pet','reason':'Less food','title':'Feeding change','confidence':'recorded'},{'type':'waste','reason':'Near expiry','title':'Expiring food','confidence':'recorded'}]}
  self.forecast={'items':[{'name':'Dog food','days_of_supply':4}]}
 def test_brief(self):
  r=simulate('What should I do tomorrow?',self.brief,self.forecast,True)
  self.assertEqual(r['intent'],'connected_brief');self.assertTrue(r['plan']['away_tomorrow'])
 def test_inventory(self):self.assertEqual(simulate('How long until food supply runs out?',self.brief,self.forecast)['intent'],'inventory_forecast')
 def test_pet(self):self.assertEqual(simulate('How is my dog feeding?',self.brief,self.forecast)['intent'],'pet_welfare')
 def test_waste(self):self.assertEqual(simulate('Any fridge waste?',self.brief,self.forecast)['intent'],'food_waste')
 def test_protected(self):
  r=simulate('Buy now',self.brief,self.forecast);self.assertTrue(r['requires_approval']);self.assertFalse(r['external_action_executed'])
 def test_empty(self):
  with self.assertRaises(ValueError):simulate('',self.brief,self.forecast)
if __name__=='__main__':unittest.main()
