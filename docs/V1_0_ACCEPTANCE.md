# RANalyzer v1.0 — acceptance and QA guide

## Changes
- R1: Callback-safe journey navigation; selected case and story reset.
- R2: Replay controls and timed presentation colocated within one Streamlit fragment.
- R3: Specialist `evidence_refs` rendered as recorded source families.
- R4: Recorded operational stages presented distinctly from nested validators; full observations inspectable.
- R5: RAN-02 investigation TX/RX/loss indicators; RAN-03 presence/absence interval strip (not reconstructed rates).
- R6: Original spans in optional trace table with monotonic start offsets and subsecond duration formatting.
- R7: Case switching stops replay and resets scene; Story→Flow starts Ready.
- R8: Story puts engineering brief before next investigation; independent Judge is optional.
- R9: Expanded JSON brief with curated observations, references, trace IDs, hypotheses and uncertainty.

## Required browser acceptance
1. The Challenge: test each of six scenario navigation shortcuts; verify proper destination and selected case without StreamlitWidgetAlreadyInstantiatedError.
2. Service Experience → Case Stories; final story → Agent Flow; Agent Flow → Evidence Room; return to case selection.
3. Run RAN-02 story scenes 0–6, verify TX=60.016, RX=4.979 and RX UDP loss=0.02165% together, and separate independent comparison.
4. Confirm RAN-01 SP04 RACH/HARQ/RLC/radio material inspectable; RAN-02 RSRP 0 + zero samples described as missing; RAN-03 three nonzero plus seven zero-reception positions, no implied aligned radio event.
5. Agent Flow: Play/Pause/Next/Previous/Restart/speed; verify completed state and controls, separately for all three cases. Confirm return to another case does not resume without user action.
6. Confirm nested validators only appear in technical trace inspection, with correct classification; independent Judge separate.
7. Results & Value: download JSON and inspect source families, original recorded observations, trace ID, uncertainty and hypotheses. Check no private raw logs or prompts.
8. Check mobile and desktop readability, and Streamlit Cloud deployed version after publication.

## Limits
Automated static validation does not establish live Streamlit Cloud acceptance. Recorded fixture content must remain byte-identical to v0.9.
