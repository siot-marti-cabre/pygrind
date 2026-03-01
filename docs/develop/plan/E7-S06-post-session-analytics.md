# E7-S06: Post-Session Analytics

## Status
To Do

## Epic
E7 - Learning Features & Analytics

## Priority
High

## Estimate
M

## Description
[PCT] Analyze session results and historical data to generate actionable improvement recommendations. Shows topic performance breakdown, tier solve rates, time management analysis, and comparison to previous sessions. Helps users focus their practice where it matters most.

## Acceptance Criteria
- [ ] Topic performance: per-topic solve percentage across last N sessions
- [ ] Tier performance: solve rate per tier for current session
- [ ] Time analysis: average time vs estimate per tier
- [ ] Comparison to previous sessions if history exists (score trend)
- [ ] Top 3 specific recommendations (e.g., 'Focus on tier-3 dynamic programming')
- [ ] Analytics section displayed in ResultsScreen below score summary

## Tasks
- **T1: Implement analytics queries** -- Add analytics methods to Database or create core/analytics.py. Query: per-topic solve rate (GROUP BY topic), per-tier performance, time averages.
- **T2: Implement recommendation engine** -- Rank topics by weakness (lowest solve rate with >=3 data points). Generate 3 text recommendations combining topic + tier suggestions.
- **T3: Integrate with results UI** -- Add collapsible 'Analytics' section to ResultsScreen. Show topic breakdown as a simple table/list, recommendations as bullet points.

## Technical Notes
- Minimum data threshold: only recommend topics with >=3 attempted problems across sessions. Score trend: simple list of last 5 session scores. Keep analytics simple -- no charts in Phase 2 (charts come in Phase 3).

## Dependencies
- E7-S05 (SQLite Persistence) -- provides Database.get_topic_stats() and historical data.
