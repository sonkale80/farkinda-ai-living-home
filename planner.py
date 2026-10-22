"""Deterministic cross-domain planning for an explainable demo."""
def build_plan(brief, away_tomorrow=False):
    alerts=brief['alerts']; kinds={a['type'] for a in alerts}; actions=[]
    if 'pet' in kinds:
        actions.append({'id':'check-pet','title':'Check pet wellbeing','reason':'Recorded intake differs from baseline; verify actual consumption.','requires_approval':True})
    if 'stock' in kinds:
        actions.append({'id':'review-shopping','title':'Review shopping list','reason':'One or more supplies are projected to run low.','requires_approval':True})
    if 'waste' in kinds:
        actions.append({'id':'reduce-waste','title':'Plan a safe meal','reason':'An item has an approaching recorded expiry date.','requires_approval':True})
    if away_tomorrow and 'pet' in kinds:
        actions.insert(0,{'id':'arrange-care','title':'Arrange pet care before leaving','reason':'Tomorrow’s absence overlaps with an unusual recorded feeding pattern.','requires_approval':True})
    return {'headline':'A connected household plan' if len(kinds)>1 else 'Household status', 'signal_categories':sorted(kinds),'combined':len(kinds)>1,'away_tomorrow':bool(away_tomorrow),'actions':actions,'evidence':[{'type':a['type'],'title':a['title'],'reason':a['reason'],'confidence':a['confidence']} for a in alerts], 'limitations':['Sample or manually recorded data; no live sensors','Not a veterinary diagnosis','No external action is performed automatically']}
