> Historical supporting note retained from RANalyzer v0.4. The v0.5 README and `TEAD_UX_ALIGNMENT.md` define the current interface.

# RANalyzer — Technology, Architecture and Assurance

**Version:** Demo v0.4 (19 October 2026)  
**Evidence baseline:** frozen v2.3.10 non-RAG rerun, three cases.

## Two systems that must not be confused

### Recorded engineering experiment
1. **iPerf UDP JSON / interval CSV:** separate sender/receiver metrics and ten approximately one-second intervals per execution.
2. **Selected gNB logs:** bounded, sampled protocol and radio messages; not exhaustive logs or a time-correlated production trace.
3. **SP03:** GPT-6 Luna via OpenRouter, measurement interpretation.
4. **SP04:** GPT-6 Luna via OpenRouter, protocol interpretation, sampled evidence handles.
5. **LangGraph:** orchestrated operational specialist calls and Supervisor synthesis.
6. **Supervisor:** Gemma 4 31B IT, synthesises findings and explicitly preserves unsupported causal boundaries.
7. **LangSmith:** recorded model invocation, stages, validations and persistence; six exported traces (three operational and three separate Judge).
8. **Independent Judge:** Gemma 4 31B IT, ten semantic criteria, B3 evaluation reference strictly restricted to Judge. This evaluator shares model family with Supervisor and is not verified causal ground truth.

### Current offline public-facing concept
**Streamlit + Python + Pandas + Plotly + local curated JSON fixtures.** The frontend does not execute LangGraph, models, a live iPerf test, a network change or LangSmith API queries. Hosting and browser QA must be completed before release claims.

## Logical flow

```text
               Frozen synthetic evidence
          /                           \
   iPerf/interval files          Selected gNB logs
          |                            |
   SP03 GPT-6 Luna                SP04 GPT-6 Luna
          \                           /
             Supervisor Gemma 4 31B IT
                    |
            Operational graph END
                    |
         Saved outputs + trace records
                    |
       Separate B3-backed semantic Judge
                    |
       Curated and sanitised replay JSON
                    |
            Streamlit v0.4 demo
```

## Operational opportunities — proposed, not verified

| Technical capability | Potential business value | Pilot measurement |
|---|---|---|
| SP03 structured iPerf analysis | Faster initial measurement review | Manual vs assisted engineer-minutes |
| SP04 evidence-backed protocol interpretation | Less manual log triage | Correctly sourced claims; review time |
| LangGraph + Supervisor synthesis | More repeatable cross-domain assessment | Report quality, engineer-hours, repeated rework |
| Deterministic validation + separate Judge | Improved auditability | Unsupported findings and review agreement |
| Offline replay | Repeatable stakeholder communication | Clarity, usability and understanding in walkthroughs |

## Demonstrated vs not demonstrated

**Demonstrated:** three synthetic service impairments, three successful latest non-RAG case executions, ten-criterion Judge score 40/40 per case, preserved uncertainty and recorded LangSmith tracing.

**Not demonstrated:** independent causal root-cause labels, commercial MTTD reductions, first-time-right acceptance gains, production live AI integration, network remediation or acceptance certification. The independent comparison is not proven recovery.

**Experimental only:** v2.4.1 Supervisor Knowledge RAG is excluded from v0.4. Its incremental benefit is not established; separate RAN-03 validation issue is retained in closure docs.

## Confidentiality and publication

The demonstration must ship **curated fixtures only**. Do not copy raw LangSmith exports, B3 reference, full model prompts, original private Drive paths, API credentials or internal technical records to a public demonstration repository. Review each downloadable evidence brief before enabling public sharing.
