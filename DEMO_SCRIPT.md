# TripWise: 90-second judge demo

## 0–15 sec — Problem
“Tourists don't just need a list of attractions. They need to know which attraction makes sense right now, given limited time, queues, travel time, and their interests.”

## 15–35 sec — Live interaction
Open the dashboard. Show Jaipur and the current demo recommendations. Point out the clear demo-data disclaimer. Change the crowd tolerance and budget, then click **Find my next stop**.

## 35–55 sec — Explainability
Open the recommendation cards. Explain that the ranking combines crowd score, travel time, interest match, budget fit, time fit, and weather suitability. The numeric rank is deterministic; AI is optional and only rewrites the summary.

## 55–70 sec — Resilience
Show the `/api/health` endpoint and Swagger docs at `/docs`. Explain that the UI has a fallback dataset so a provider outage does not destroy the live demo.

## 70–90 sec — Roadmap and differentiation
“Our next step is replacing illustrative crowd and traffic values with attributable live provider data, freshness timestamps, route optimization, and event-aware recommendations. We deliberately separate the ranking engine from optional AI so every recommendation is explainable and testable.”

## Judge-ready honesty notes
- Do not call the included crowd scores live.
- Do not claim AI controls the ranking.
- Do not claim location is detected automatically; this MVP uses selected city and preferences.
- Mention the real-time data adapters as integration points, not as already verified live crowd feeds.
