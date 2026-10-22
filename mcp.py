"""Minimal stateless MCP Streamable HTTP JSON-RPC endpoint (local demonstration)."""
import json
TOOLS=[
 {'name':'get_household_brief','description':'Explain household inventory, pet welfare signals and food waste risks from recorded data.','inputSchema':{'type':'object','properties':{},'additionalProperties':False}},
 {'name':'get_inventory_forecast','description':'Forecast days of supply and expiry for recorded inventory.','inputSchema':{'type':'object','properties':{},'additionalProperties':False}},
 {'name':'get_connected_plan','description':'Create a cross-domain, explainable action plan from household signals.','inputSchema':{'type':'object','properties':{'away_tomorrow':{'type':'boolean'}},'additionalProperties':False}},
 {'name':'record_pet_meal','description':'Record a measured meal for a known pet; requires user confirmation.','inputSchema':{'type':'object','properties':{'pet':{'type':'string'},'grams':{'type':'number'},'confirmed':{'type':'boolean'}},'required':['pet','grams','confirmed']}},
 {'name':'prepare_action','description':'Prepare a proposed action, without executing purchases or contacting third parties.','inputSchema':{'type':'object','properties':{'kind':{'type':'string','enum':['shopping','pet-check','meal-plan']}},'required':['kind']}}
]
def handle(msg, brief, meal, propose, plan=None, forecast=None):
 if not isinstance(msg,dict):return {'jsonrpc':'2.0','id':None,'error':{'code':-32600,'message':'Invalid Request'}}
 mid=msg.get('id');method=msg.get('method');params=msg.get('params') or {}
 if msg.get('jsonrpc')!='2.0' or not isinstance(method,str) or not isinstance(params,dict):return {'jsonrpc':'2.0','id':mid,'error':{'code':-32600,'message':'Invalid Request'}}
 if method=='notifications/initialized':return None
 if method=='initialize':return {'jsonrpc':'2.0','id':mid,'result':{'protocolVersion':'2025-03-26','capabilities':{'tools':{}},'serverInfo':{'name':'farkinda-living-home','version':'1.0.0'}}}
 if method=='ping':return {'jsonrpc':'2.0','id':mid,'result':{}}
 if method=='tools/list':return {'jsonrpc':'2.0','id':mid,'result':{'tools':TOOLS}}
 if method=='tools/call':
  name=params.get('name');args=params.get('arguments') or {}
  if not isinstance(args,dict):return {'jsonrpc':'2.0','id':mid,'error':{'code':-32602,'message':'Invalid arguments'}}
  try:
   if name=='get_household_brief':result=brief()
   elif name=='get_inventory_forecast' and forecast:result=forecast()
   elif name=='get_connected_plan' and plan:
    if type(args.get('away_tomorrow',False)) is not bool:raise ValueError('away_tomorrow must be boolean')
    result=plan(args)
   elif name=='record_pet_meal':result=meal(args)
   elif name=='prepare_action':result=propose(args)
   else:return {'jsonrpc':'2.0','id':mid,'error':{'code':-32602,'message':'Unknown tool'}}
   return {'jsonrpc':'2.0','id':mid,'result':{'content':[{'type':'text','text':json.dumps(result,ensure_ascii=False)}]}}
  except (ValueError,TypeError,KeyError) as exc:
   return {'jsonrpc':'2.0','id':mid,'result':{'content':[{'type':'text','text':str(exc)}],'isError':True}}
 return {'jsonrpc':'2.0','id':mid,'error':{'code':-32601,'message':'Method not found'}}
