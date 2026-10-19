# Interactive Agent Flow — v0.7

- Display only recorded events from the curated v2.3.10 LangSmith trace fixtures.
- Each case has nine ordered trace events across SP03, SP04, and Supervisor.
- Play, Pause, Previous, Next, Restart and pacing options are presentation controls, not operational actions.
- The operator can examine the observed trace durations, model invocation spans, validation and source references.
- The Judge is independent and runs outside LangGraph; it is not an operational stage.
- No raw prompts, B3 evaluator reference, private paths, or complete gNB logs are published.
- Playback timing is illustrative; recorded UTC span durations are shown separately.
- None of the findings prove causal root cause, corrective action, or recovery.

## Manual browser checks

1. On RAN-01, use Play to move from Ready through nine events; check all stage transitions.
2. Pause mid-flow, navigate Previous and Next, and Restart.
3. Change speed, confirm it affects only playback pacing and not displayed recorded timing.
4. Select RAN-02 and RAN-03 and verify independent progression and preserved case identity.
5. Confirm the Judge is labelled independent/outside LangGraph, and no live network or model activity occurs.
6. Check readable contrast, wrapping and smaller viewport layout.
