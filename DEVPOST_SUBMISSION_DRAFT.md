# FARKINDA AI — Your Home Notices What You Miss

## Inspiration
Households use separate apps for groceries, pet feeding, and expiry reminders. Important signals remain disconnected.

## What it does
FARKINDA combines manually entered or synthetic inventory, pet feeding, and food expiry signals into one explainable household action plan. It can show why a recommendation was made and requires user approval for local demo actions.

## How we built it
Python standard library HTTP server, SQLite, deterministic planning engine, JSON-RPC MCP-style local demo endpoint, and a browser-based English voice-intent simulator.

## Challenges
Combining unrelated signals without pretending uncertain records are live sensor observations, and preventing suggestions from silently becoming purchases or messages.

## Accomplishments
Working local demonstration, evidence-based planning, inventory forecasts, user-approval records, automated tests, and a simulated natural-language interface.

## What we learned
Cross-domain context is more useful than isolated low-stock notifications, but explanations and explicit approvals are necessary.

## What's next
Validate Streamable HTTP MCP conformance, HTTPS and authentication; integrate approved Alexa+ surfaces and optional real sensor feeds.

## Important disclosure
This submission is a LOCAL PROTOTYPE. It does not connect to Alexa+, does not use a live LLM, and does not contain real sensors. The /mcp endpoint is an MCP-style JSON-RPC demonstration, not a verified Streamable HTTP deployment. No veterinary diagnosis or external purchases.

## Demo video outline (under 3 minutes)
0:00 Problem: three disconnected household signals.
0:25 Launch English dashboard and explain sample records.
0:50 Ask the simulator: Nobody will be home tomorrow. What should I take care of?
1:20 Show the combined plan and supporting evidence.
1:50 Ask about food stock and pet feeding.
2:15 Approve one LOCAL action and show the explicit no-external-action notice.
2:35 Show MCP tool list, tests and limitations.
