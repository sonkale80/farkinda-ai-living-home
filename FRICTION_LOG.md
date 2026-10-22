# FARKINDA AI — Development Friction Log

**Project:** FARKINDA AI — Living Home Intelligence  
**Repository:** https://github.com/sonkale80/farkinda-ai-living-home

## Issue 1 — Local Browser Connectivity

**Task:** Launch and access the interactive household dashboard.

**Steps Taken:** Started the Python HTTP server, tested local ports, opened the dashboard in a browser, and inspected HTTP responses using PowerShell.

**Expected Result:** The dashboard should load successfully and display household recommendations.

**Actual Result:** Some browser requests returned `{"error":"not found"}` even though PowerShell HTTP requests returned status 200 and valid HTML.

**Severity:** Important

**Workaround:** Used `http://localhost:8877/`, which successfully loaded the application.

**Actionable Recommendation:** Add automated endpoint validation, clearer routing diagnostics, and documented localhost configuration.

## Issue 2 — Frontend-to-Backend Communication

**Task:** Load the Connected Household Planner with live local application data.

**Steps Taken:** Opened the frontend directly as an HTML file, attempted to retrieve household data, and compared the behavior with the server-hosted version.

**Expected Result:** The planner should retrieve household data and generate actionable recommendations.

**Actual Result:** The standalone HTML page displayed `Failed to fetch` because the expected backend connection was unavailable.

**Severity:** Important

**Workaround:** Served the frontend and backend together through the Python application. The planner subsequently displayed three household categories and three recommended actions.

**Actionable Recommendation:** Provide configurable API endpoints, connection health checks, and clearer network error messages.

## Issue 3 — Conversational Assistant Integration

**Task:** Prepare reusable household tools for future conversational assistant integration.

**Steps Taken:** Separated planning logic into modular components, developed MCP-oriented tool interfaces, and implemented a local voice-intent simulator.

**Expected Result:** A structured tool architecture suitable for conversational household workflows.

**Actual Result:** Local tool-oriented workflows were developed, but live Alexa+ integration and production remote MCP deployment were not completed.

**Severity:** Important

**Workaround:** Demonstrated the intended interaction flow through a local simulator without representing it as a live Alexa+ integration.

**Actionable Recommendation:** Provide end-to-end examples covering remote MCP deployment, authentication, tool discovery, testing, and assistant integration.

## Issue 4 — Reproducible Testing and Demonstration

**Task:** Validate application behavior and prepare a reliable hackathon demonstration.

**Steps Taken:** Used isolated demonstration data, exercised household planning workflows, generated demonstration materials, and ran automated tests.

**Expected Result:** A reproducible demonstration with passing tests and no impact on real household records.

**Actual Result:** Demo preparation required a Windows-specific test-environment adjustment. The local preparation report subsequently recorded 32 passing tests.

**Severity:** Moderate

**Workaround:** Applied a temporary test-environment adjustment and used isolated sample data.

**Actionable Recommendation:** Provide cross-platform test automation, deterministic fixtures, and one-command demo setup.

## Key Takeaways

The primary development friction points involved browser routing, frontend-backend communication, conversational integration readiness, and cross-platform test reproducibility.

Addressing
