> Historical supporting note retained from RANalyzer v0.4. The v0.5 README and `TEAD_UX_ALIGNMENT.md` define the current interface.

# Operational value and pilot measurement — v0.3

## Positioning
RANalyzer is an AI-powered RAN service-assurance demonstration built around frozen v2.3.10 evidence, not a production site acceptance system. It complements TEAD AI incident investigation by focusing on service validation and evidence completeness before handover.

## Four potential operational outcomes

| Pillar | Shown through | Proposed KPI | Not yet proven |
|---|---|---|---|
| Faster diagnosis | SP03 measurement and SP04 protocol reports + Supervisor | Median elapsed diagnosis review time | MTTD reduction |
| Better acceptance quality | Performance evidence, gap review, illustrative thresholds | First-time-right acceptance, repeat visits | Site acceptance efficacy |
| Engineering productivity | Standardised multi-agent output and evidence brief | Engineer-minutes per evidence pack | Labour/cost savings |
| Operational assurance | Evidence references, validation and Judge | Source-verifiable claim rate, rework | Deployment-scale assurance gains |

## Pilot test design
1. Select representative operational cases and formal acceptance expectations.
2. Record engineer baseline: time, manual actions, review accuracy and evidence gaps.
3. Use the same evidence in RANalyzer-assisted review, with independent engineers verifying results.
4. Record efficiency and quality metrics; do not infer causal accuracy without verified labels.
5. Report both strengths and limitations, including the shared model family used by Supervisor and Judge.

## Scientific boundaries
- Three synthetic cases and approximately 10-second UDP executions; not 15-minute PM counters.
- Investigation and comparison are independent; not an intervention/recovery.
- UE-to-flow mapping and temporal alignment to sampled gNB logs remain unverified.
- The Judge's 100% rubric does not demonstrate causal root-cause accuracy.
- No production policy for site acceptance has been implemented.
