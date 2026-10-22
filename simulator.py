"""Deterministic English voice-intent simulator, not an Alexa service."""
import re
from planner import build_plan

def simulate(utterance, brief, forecast, away=False):
    if not isinstance(utterance,str) or not 1 <= len(utterance.strip()) <= 400:
        raise ValueError("Please enter a short question")
    q=utterance.casefold()
    if any(x in q for x in ("buy now", "place order", "purchase now", "contact veterinarian")):
        return {"intent":"protected_action", "speech":"I can prepare a suggestion, but I cannot make purchases or contact anyone. Please review and approve any proposed action.","requires_approval":True,"external_action_executed":False}
    if any(x in q for x in ("how long", "run out", "left", "inventory", "stock", "food supply")):
        lines=[f"{x['name']}: {x['days_of_supply']} days of supply" if x['days_of_supply'] is not None else f"{x['name']}: insufficient consumption data" for x in forecast['items']]
        return {"intent":"inventory_forecast","speech":"Estimated from manually recorded data. "+"; ".join(lines)+".","evidence":forecast['items']}
    if any(x in q for x in ("pet", "dog", "cat", "pamuk", "feeding")):
        matches=[x for x in brief['alerts'] if x['type']=='pet']
        return {"intent":"pet_welfare","speech":("; ".join(x['reason'] for x in matches)+". Verify the records; consult a veterinarian if changes persist." if matches else "No feeding anomaly in the available records. This does not establish pet health."),"evidence":matches}
    if any(x in q for x in ("waste", "expire", "fridge", "food")):
        matches=[x for x in brief['alerts'] if x['type']=='waste']
        return {"intent":"food_waste","speech":("; ".join(x['reason'] for x in matches)+". Check food safety before use." if matches else "No near-expiry alerts in the current records."),"evidence":matches}
    plan=build_plan(brief,away or any(x in q for x in ("away tomorrow","nobody home tomorrow","leaving tomorrow")))
    return {"intent":"connected_brief","speech":f"I found {len(plan['evidence'])} household signals across {len(plan['signal_categories'])} categories and prepared {len(plan['actions'])} suggestions. Nothing has been purchased or sent.","plan":plan,"requires_approval":True}
