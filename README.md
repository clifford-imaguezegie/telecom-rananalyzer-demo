# RANalyzer v0.9 — Why Watch / Engineering Deliverable

The v0.9 presentation adds an explicit bridge between each operational problem, the guided investigation, its engineering deliverable, and the optional agent-trace replay. No fixture, recorded agent result, judge output or source notebook was changed.

# RANalyzer — AI-Powered RAN Service Assurance

**v0.7 · Interactive Agent Replay (19 October 2026)**

A seven-workspace, executive-to-engineering Streamlit demonstration based on three frozen v2.3.10 non-RAG RANalyzer investigations and curated LangSmith traces. The presentation approach was informed by the source implementation of TEAD AI `feature/network-observatory-ux` (clarity-first hierarchy, case stories, progressive disclosure and trace-inspectable evidence). RANalyzer retains its own service-assurance proposition and interface. No TEAD AI proprietary code or assets have been copied into this project.

## Journey

1. **The Challenge** — operational problem, opportunity and introduction.
2. **Service Experience** — real recorded UDP test metrics and measurement interpretation.
3. **Architecture** — agent roles, technologies and the difference between experiment and replay.
4. **Case Stories** — Ready → measurements → protocol → synthesis → Judge → missing evidence.
5. **Agent Flow** — interactive Play/Pause, Previous/Next, Restart, speed controls, active agent highlighting and original LangSmith event durations, provenance and structured outputs.
6. **Evidence Room** — claims, supporting reference families, uncertainty and trace IDs.
7. **Results & Value** — observed rubric scores versus hypothesised operator KPIs.

## Running

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

No API keys or internet access are required. All case records are read locally from `data/RAN-01.json` etc. `python -m compileall -q app.py` validates Python syntax but does not replace browser usability testing.

## Evidence limits

Three synthetic cases, each independently reassessed with 40/40 semantic Judge results; not verified causal accuracy. Approximately ten-second UDP tests are not 15-minute production PM counters. UE-to-flow and endpoint-to-gNB timestamps are not verified aligned. Comparison executions do not constitute recovery. Judge and Supervisor share model family. The demo contains selected summaries and source families, not private complete evidence or B3 reference.

**No** network commands, agent calls, LangSmith access, RAG queries, remediation, or site acceptance occurs through the demo. Operational savings or first-time-right improvements require operator pilot validation.

See `docs/TEAD_UX_ALIGNMENT.md` for design adaptation and `docs/DEMO_SCOPE.md` for boundaries.


## v0.6 accessibility and navigation fixes
- Consistent light canvas with readable secondary text, while retaining a navy hero for emphasis.
- Flexible header/navigation layout with wrapping on smaller viewports.
- Revised service-assurance message focused on ongoing service performance investigation rather than site pre-acceptance.
- Case Stories Next / Previous now use Streamlit widget callbacks; no same-run mutation of `st.session_state.scene` after slider creation.
- Frozen scenario JSON and recorded outputs are unchanged.

## v0.7 interactive replay

The Agent Flow workspace displays nine saved trace events for each case, in their recorded chronological order. Active node highlighting follows the real SP03 → SP04 → Supervisor sequence. Play speed controls presentation pacing only; displayed durations are measured trace timings. The independent semantic Judge is shown after the operational sequence, not as a fourth LangGraph agent.

Uses `st.fragment(run_every=...)` (requires Streamlit >=1.39) to refresh only the replay area while playing. No JavaScript, live model inference, LangSmith credentials, or network access required.

Validation performed: Python syntax, fixture and archive integrity. Live browser interactivity and responsive QA are still required.


## v0.9 customer-journey acceptance review

This revision focuses on three customer questions rather than introducing new model capabilities:

1. **What is being offered?** A repeatable RAN performance investigation brief combining service observations, qualified radio/protocol evidence, missing proof and recommended next tests. The opening page displays a selected example deliverable.
2. **What does each guided step add?** Each Case Stories scene now states the engineering reason for that step, culminating in the deliverable.
3. **Why inspect Agent Flow?** Its entry explains the distinct specialist roles, recorded orchestration and limitations, and previews the relevant customer deliverable.

No experimental input, trace fixture, evaluation result or source notebook is modified. Operational savings remain hypotheses for a future pilot. Live browser acceptance is still pending.
