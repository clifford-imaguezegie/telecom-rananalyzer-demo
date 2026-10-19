"""RANalyzer v0.9 — operational-value-led clarity-first offline demonstration built from frozen v2.3.10 replay fixtures.
Presentation only. No external inference, network action, or LangSmith API access.
"""
import json
from pathlib import Path
from html import escape
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from agent_replay import render as render_agent_replay

ROOT=Path(__file__).resolve().parent
CASES={
 'RAN-01':{'title':'Severe service impairment','rx':0.39140933,'comparison':29.87555144,'sender':35.39936212,'loss':98.4299,'hook':'Near-total packet loss and four zero-reception intervals','lesson':'Serious degradation can be established without claiming its unverified cause.'},
 'RAN-02':{'title':'Throughput disparity','rx':4.97887422,'comparison':57.88308126,'sender':60.01608528,'loss':0.02165,'hook':'Large sender/receiver gap despite low receiver-reported packet loss','lesson':'A throughput deficit must not be mislabelled as receiver UDP loss.'},
 'RAN-03':{'title':'Intermittent service interruption','rx':2.4369,'comparison':29.9002,'sender':30.006,'loss':62.515,'hook':'Seven consecutive intervals of zero reception','lesson':'Radio observations and throughput collapse are not proven causally linked.'},
}
PAGES=['The Challenge','Service Experience','Architecture','Case Stories','Agent Flow','Evidence Room','Results & Value']
TECH=[('Measurement evidence','iPerf JSON / interval CSV','Observed sender/receiver rates, packet loss and interval behaviour'),('Protocol evidence','Selected gNB logs','RACH, MAC/HARQ, RLC, PDCP, RRC and radio-quality observations'),('Orchestration','LangGraph / Python','Runs SP03, SP04 and Supervisor in frozen engineering experiment'),('SP03 + SP04','GPT-6 Luna','Specialist measurement and protocol analysis'),('Supervisor','Gemma 4 31B IT','Evidence synthesis, hypotheses and uncertainty'),('Assurance','Independent Gemma 4 Judge / B3','Ten-criterion semantic assessment outside the operational graph'),('Observability','LangSmith','Recorded model, validation and stage traces'),('Presentation','Streamlit / Plotly / Pandas','Local, offline, curated replay; no inference')]
VALUE=[('Accelerate diagnosis','Potential reduction in evidence interpretation effort','Median time to engineer-reviewed assessment'),('Support service assurance','Surface performance gaps and unresolved engineering evidence','First-time-right acceptance and repeat visits'),('Increase engineering productivity','Standardise measurements, protocol review and findings','Engineer-minutes per completed investigation'),('Strengthen assurance','Traceable claims, independent semantic checks, explicit abstention','Unsupported findings and evidence completeness')]
# Business-to-evidence storytelling. These are editorial prompts and possible operational
# opportunities, not new measurements or independently verified root causes.
STORY={
 'RAN-01':{
  'question':'How do we investigate a service that is nearly unusable?',
  'problem':'Receiver throughput fell to about 0.39 Mbps with 98.43% receiver packet loss. A team needs to separate the measured impairment from possible protocol explanations.',
  'promise':'Watch measurements and sampled RAN logs become an evidence-qualified engineering assessment.',
  'finding':'Severe receiver-side impairment is established. Sampled random-access, retransmission and radio-link indicators warrant examination, but their causal connection is unverified.',
  'next':'Acquire synchronized per-UE radio, HARQ/RLC counters and verified UE-to-test-flow mapping.',
  'value':'Structured triage and a defensible list of follow-up checks; shorter manual diagnostic effort is a pilot hypothesis.'},
 'RAN-02':{
  'question':'The sender transmits around 60 Mbps. Why does the receiver see only about 5 Mbps?',
  'problem':'A large sender/receiver throughput gap coexists with very low receiver-reported packet loss. That combination can lead to the wrong interpretation.',
  'promise':'See how measurement semantics and sampled RACH/RLC evidence are examined without equating the throughput gap to UDP loss.',
  'finding':'The throughput deficit is real, but it is not accurately described by the receiver-reported loss percentage alone; several protocol mechanisms remain possible, not proven.',
  'next':'Verify aligned flow and UE identity, full protocol logs, bearer counters and relevant time-correlated throughput records.',
  'value':'Avoid misleading diagnosis and focus the engineer on discriminating evidence; improved review effort must be measured in a pilot.'},
 'RAN-03':{
  'question':'Why does service reception stop after the first three measurement intervals?',
  'problem':'The receiver has seven consecutive zero-reception intervals despite an independent comparison run with much better performance.',
  'promise':'Follow the measured traffic interruption alongside sampled radio-quality observations and see where causal confidence stops.',
  'finding':'A reception interruption is observed. RSRP and A2 observations raise questions but cannot be connected causally without validated timeline and UE correlation.',
  'next':'Obtain time-aligned complete gNB logs, per-UE counters and verified UE-to-iPerf flow attribution.',
  'value':'Make uncertainty and missing validation data explicit so the next diagnostic action is purposeful.'},
}

def proposition(cid,mode='story'):
    item=STORY[cid]
    st.markdown(f'<div class="ra-kicker">WHY WATCH THIS INVESTIGATION?</div><div class="ra-question">{html(item["question"])}</div>',unsafe_allow_html=True)
    a,b=st.columns([1,1.05],gap='medium')
    with a:
        st.markdown('**The engineering challenge**')
        st.write(item['problem'])
    with b:
        st.markdown('**What you will see RANalyzer deliver**')
        st.write(item['promise'])
    st.caption('All case facts refer to frozen synthetic network recordings. Expected operational savings have not been measured.')

# Customer journey prompts: editorial interpretations of recorded findings, not new test results.
SCENE_VALUE={
 'RAN-01':[
  'Decide which service symptom deserves attention first.',
  'Establish the degree of throughput impairment and measured loss.',
  'Receive a repeatable quantitative account of the impaired service.',
  'See relevant radio/access indicators without treating samples as causal proof.',
  'Convert separate observations into a qualified engineering assessment.',
  'Check whether the recorded explanation is faithful to the benchmark rubric.',
  'Leave with specific verification tasks rather than an unsupported RCA.'
 ],
 'RAN-02':[
  'Understand why the large throughput gap demands more than a packet-loss check.',
  'See the 60 Mbps versus 5 Mbps discrepancy in its proper measurement context.',
  'Distinguish receiver-reported UDP loss from the sender/receiver rate gap.',
  'Inspect possible RACH/RLC contributors without assigning causation.',
  'Receive a reconciled assessment that preserves competing explanations.',
  'Review the semantic quality of the measurement and protocol interpretation.',
  'Know which correlated UE, bearer and time-series evidence to request next.'
 ],
 'RAN-03':[
  'See why an abrupt reception stop calls for a structured evidence review.',
  'Establish that seven consecutive intervals received no traffic.',
  'Characterise the interruption without guessing the missing packets or cause.',
  'Review radio-quality observations and their correlation limitations.',
  'Separate observed interruption from unverified radio causation.',
  'Inspect whether the agent ensemble maintained appropriate uncertainty.',
  'Request time-aligned UE/flow evidence before a causal conclusion.'
 ]
}

def customer_takeaway(cid,scene):
    st.markdown('**Why this step matters to an engineering team**')
    st.info(SCENE_VALUE[cid][scene])

def buyer_bridge(cid):
    story=STORY[cid]
    with st.container(border=True):
        st.markdown('**What an operator receives — for this specific investigation**')
        st.markdown('**Observed:** '+story['finding'])
        st.markdown('**Recommended evidence to collect:** '+story['next'])
        st.markdown('**Operational opportunity to validate:** '+story['value'])
        st.caption('An engineering review output, not a verified causal diagnosis or a measured productivity saving.')

def deliverable(cid,sup,compact=False):
    item=STORY[cid]
    st.markdown('<div class="ra-kicker">ENGINEERING DELIVERABLE · NOT JUST AN AGENT COMPLETION</div>',unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown('**01 · Observed problem and engineering finding**')
        st.write(item['finding'])
        st.markdown('**02 · Supporting evidence and causal boundary**')
        st.write(sup.get('final_assessment',''))
        st.caption('The Supervisor did not verify root cause, corrective action or recovery.')
        st.markdown('**03 · What to verify next**')
        for text in sup.get('missing_discriminating_evidence',[])[:(2 if compact else 3)]:
            st.markdown('• '+str(text))
        st.markdown('**04 · Potential operational value**')
        st.write(item['value'])
        st.caption('Supporting evidence and limitations come from the recorded specialists and Supervisor. This summary does not certify a causal root cause, remediation, recovery or operator acceptance.')

TERMS={'iPerf':'A tool used to measure network traffic performance, here in short UDP tests.','gNB':'5G radio base station (next-generation Node B).','RAN':'Radio Access Network, connecting user devices to the mobile network.','RACH':'Random Access Channel procedures used to begin radio access.','HARQ':'Hybrid Automatic Repeat Request, a radio transmission error-recovery mechanism.','RLC':'Radio Link Control, a layer handling radio-link data transfer and retransmission.','PDCP':'Packet Data Convergence Protocol, a layer supporting packet delivery and related functions.','RRC':'Radio Resource Control, signalling used to configure and manage a radio connection.','RSRP':'Reference Signal Received Power, one measure of radio signal strength.','BLER':'Block Error Rate, a measure of radio block decoding errors.','RCA':'Root Cause Analysis; a causal conclusion here is not independently verified.','LangGraph':'A framework for structured execution of agent workflows.','LangSmith':'Observability tooling used to capture investigation execution traces.','Judge':'A separate model assessment against a ten-criterion semantic rubric; not causal ground truth.'}

st.set_page_config(page_title='RANalyzer | Service Assurance',page_icon='📡',layout='wide',initial_sidebar_state='collapsed')
st.markdown("""<style>
:root{--navy:#101b35;--blue:#325bdb;--teal:#008f89;--ink:#162441;--muted:#596d87;--line:#d8e2ef}
.block-container{max-width:1320px;width:100%;padding:1.35rem clamp(1rem,3vw,2.2rem) 4rem;overflow-x:clip}
.ra-brand{display:flex;justify-content:space-between;align-items:center;gap:10px;padding:8px 0 15px;border-bottom:1px solid var(--line);flex-wrap:wrap;max-width:100%;min-width:0;overflow-wrap:anywhere}
.ra-brand b{color:#142448;font-size:1.02rem}.ra-brand span{font-size:.70rem;color:#566783;letter-spacing:.025em;overflow-wrap:anywhere}
.ra-hero{background:radial-gradient(circle at 90% 2%,#245b83,transparent 50%),linear-gradient(115deg,#142744,#1b4460);border-radius:17px;padding:30px clamp(20px,3vw,38px);color:#fff;margin:17px 0 22px;max-width:100%;overflow-wrap:anywhere}
.ra-hero .over{color:#86e3db;font-weight:800;font-size:.71rem;letter-spacing:.15em;text-transform:uppercase}
.ra-hero h1{color:#fff!important;background:transparent!important;font-size:clamp(1.8rem,3vw,2.65rem);line-height:1.2;margin:11px 0;max-width:970px;overflow-wrap:anywhere}.ra-hero p{color:#d9eaf4;max-width:810px;line-height:1.62;font-size:1rem}
.ra-kicker{font-size:.74rem;letter-spacing:.095em;color:#254db8;font-weight:800;text-transform:uppercase;margin-bottom:5px}
.ra-lead{font-size:.96rem;color:#344860;max-width:950px;line-height:1.62}
.ra-card{border:1px solid var(--line);border-radius:13px;background:#f9fbff;padding:17px 19px;height:100%;color:var(--ink)}
.ra-card b{font-size:.95rem;color:#213b63;display:block;margin-bottom:6px}.ra-card p{font-size:.83rem;color:#52647c;line-height:1.52;margin:0}
.ra-journey{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0}.ra-journey span{font-size:.78rem;font-weight:750;color:#244a73;background:#edf3fb;border:1px solid #cbdced;border-radius:9px;padding:8px 11px}
.ra-banner{border-left:4px solid #36849b;background:#eff8fa;border-radius:0 10px 10px 0;padding:12px 16px;font-size:.85rem;color:#36596f;line-height:1.55;margin:14px 0}
.ra-flow{display:grid;grid-template-columns:1fr 36px 1.5fr 36px 1fr;gap:6px;align-items:stretch;margin:20px 0}
.ra-node{border:1px solid #cbd9ea;border-radius:12px;padding:18px;background:#fff;color:#213953}.ra-node b{font-size:.95rem;display:block}.ra-node small{color:#5e7187;line-height:1.5;display:block;margin-top:8px}
.ra-node.focus{background:#e8f5f3;border-color:#93cfc5}.ra-arr{text-align:center;align-self:center;color:#547ca1;font-size:24px}
.ra-agent{background:#f1f5fb;border:1px solid #cddaea;padding:10px;border-radius:8px;margin-bottom:8px;font-size:.81rem;color:#23415f}
.ra-chip{font-size:.74rem;font-weight:750;color:#11776d;border:1px solid #a4d8cf;background:#e7f8f4;border-radius:14px;padding:4px 9px;display:inline-block}
.ra-question{font-size:clamp(1.24rem,2vw,1.75rem);font-weight:800;color:#173757;line-height:1.26;margin:6px 0 15px;overflow-wrap:anywhere}.ra-case-pitch{border:1px solid #cddfeb;background:#f8fbff;border-radius:14px;padding:17px 19px;margin:12px 0}.ra-case-pitch h3{font-size:1.10rem;margin:4px 0 9px;color:#183b5a}.ra-case-pitch p{font-size:.85rem;line-height:1.55;color:#425b70}.ra-proof{background:#eaf7f2;border:1px solid #b9ddcf;border-radius:12px;padding:13px 16px;margin:12px 0;font-size:.84rem;color:#24574d}
[data-testid="stMetric"]{border:1px solid var(--line);background:#fff;border-radius:12px;padding:12px 15px}
/* Streamlit-wide navigation should wrap instead of escaping right viewport. */
[data-testid="stRadio"] [role="radiogroup"]{flex-wrap:wrap!important;row-gap:.25rem!important;column-gap:.45rem!important;max-width:100%!important}
[data-testid="stRadio"] label{max-width:100%;white-space:normal}
[data-testid="stMarkdownContainer"]{overflow-wrap:anywhere}
[data-testid="stAppViewContainer"]{overflow-x:clip}
[data-testid="stMetric"] label{color:#42566f!important}
[data-testid="stMetricValue"]{color:#152e4a!important}
.stCaption, [data-testid="stCaptionContainer"], small{color:#52667e}
@media(max-width:900px){.ra-brand>span{width:100%}.ra-flow{grid-template-columns:1fr;gap:6px}.ra-arr{transform:rotate(90deg);height:24px}.ra-brand{align-items:flex-start}}
@media(max-width:760px){.ra-hero{padding:24px}.block-container{padding-left:1rem;padding-right:1rem}}
""",unsafe_allow_html=True)
@st.cache_data(show_spinner=False)
def load(cid):return json.loads((ROOT/'data'/f'{cid}.json').read_text('utf-8'))
if 'page' not in st.session_state:st.session_state.page=PAGES[0]
if 'case' not in st.session_state:st.session_state.case='RAN-01'
if 'scene' not in st.session_state:st.session_state.scene=0

def step_scene(delta):
    # Called before the scene slider is instantiated on the next Streamlit rerun.
    st.session_state.scene=max(0,min(6,int(st.session_state.scene)+delta))

def navigate(to,case=None):
 st.session_state.page=to
 if case and case!=st.session_state.case:st.session_state.case=case;st.session_state.scene=0
 st.rerun()
def html(x):return escape(str(x),quote=True)
def section(tag,title,desc=''):
 st.markdown(f'<div class="ra-kicker">{html(tag)}</div>',unsafe_allow_html=True)
 st.subheader(title)
 if desc:st.markdown(f'<p class="ra-lead">{html(desc)}</p>',unsafe_allow_html=True)
def case_metrics(c,d):
 cols=st.columns(4)
 for col,title,val in zip(cols,['Investigation RX','Independent comparison RX','Receiver packet loss','Semantic Judge'],[f'{c["rx"]:.3f} Mbps',f'{c["comparison"]:.3f} Mbps',f'{c["loss"]:.3f}%',f'{d["judge"]["score"]}/{d["judge"]["max_score"]}']):col.metric(title,val)
def source_obs(items,limit=8):
 for o in items[:limit]:
  if isinstance(o,dict):
   st.markdown('• '+o.get('claim',''))
   if o.get('source_refs'):st.caption('Sources: '+', '.join(o['source_refs']))
  else:st.markdown('• '+str(o))
def comparison_chart(c):
 fig=go.Figure()
 fig.add_bar(name='Investigation',x=['Measured receiver throughput'],y=[c['rx']],marker_color='#168d86')
 fig.add_bar(name='Independent comparison',x=['Measured receiver throughput'],y=[c['comparison']],marker_color='#4270c8')
 fig.update_layout(barmode='group',height=305,yaxis_title='Mbps',margin=dict(l=10,r=10,b=10,t=10),legend=dict(orientation='h',y=1.15))
 st.plotly_chart(fig,use_container_width=True)

def card(title,text):st.markdown(f'<div class="ra-card"><b>{html(title)}</b><p>{html(text)}</p></div>',unsafe_allow_html=True)

def boundary():st.markdown('<div class="ra-banner"><b>Evidence boundary:</b> Three synthetic cases use approximately ten-second UDP measurements and selected gNB logs. There is no verified UE-to-flow mapping, time alignment, causal RCA, corrective action or recovery. Independent comparisons are not intervention outcomes.</div>',unsafe_allow_html=True)

st.markdown('<div class="ra-brand"><b>📡 RANalyzer <span> / AI-POWERED RAN SERVICE ASSURANCE</span></b><span>PROOF OF CONCEPT · TRACE-GROUNDED REPLAY · 2026</span></div>',unsafe_allow_html=True)
nav=st.radio('Navigate the experience',PAGES,key='page',horizontal=True,label_visibility='collapsed')
with st.sidebar:
 st.subheader('RANalyzer · Case selector')
 st.selectbox('Recorded RAN case',list(CASES),key='case',format_func=lambda x:x+' · '+CASES[x]['title'])
 st.caption('v2.3.10 · frozen non-RAG evidence')
 st.caption('Semantic Judge: 40/40 on each 2026-10-19 rerun')
 st.divider()
 with st.expander('Glossary and definitions'):
  q=st.text_input('Find a term',placeholder='RACH, iPerf, RCA ...')
  for k,v in TERMS.items():
   if q.lower() in (k+' '+v).lower():st.markdown('**'+k+'** — '+v)
 st.divider()
 st.caption('Read-only offline replay · no LLM calls, live telemetry or network commands.')

cid=st.session_state.case;c=CASES[cid];d=load(cid);sup=d['SUPERVISOR']['output'];judge=d['judge'];page=st.session_state.page

if page=='The Challenge':
 st.markdown('<div class="ra-hero"><div class="over">AI-POWERED RAN SERVICE ASSURANCE</div><h1>From service measurements to engineering confidence</h1><p>RANalyzer brings measured service performance and sampled 5G protocol evidence into a structured investigation — showing what is observed, what remains uncertain, and what engineers should investigate next.</p></div>',unsafe_allow_html=True)
 section('01 · Why this matters','Operational challenges','Operational services can suffer throughput degradation, packet loss and intermittent interruptions. Engineers need clear evidence to distinguish observable symptoms from unverified explanations.')
 cc=st.columns(3)
 for co,t,s in zip(cc,['Service confidence','Investigation productivity','Evidence-based handover'],['Expose impaired receiver performance and distinguish measurements from assumptions.','Bring measurement and RAN protocol perspectives into one structured review.','Surface missing verification and support consistent human acceptance processes.']):
  with co:card(t,s)
 section('02 · How it works','An understandable engineering journey')
 st.markdown('<div class="ra-journey"><span>01 · Observe the service</span><span>→ 02 · Interpret the logs</span><span>→ 03 · Reconcile findings</span><span>→ 04 · Review evidence</span></div>',unsafe_allow_html=True)
 section('03 · Choose the problem to investigate','Three operational questions — one diagnostic capability','Each case shows how RANalyzer turns a different service-performance symptom into engineering evidence, uncertainty and a practical next-investigation plan.')
 for k,v in CASES.items():
  t=STORY[k]
  with st.container(border=True):
   l,r=st.columns([4.8,1.3],gap='medium')
   with l:
    st.markdown(f'**{k} · {v["title"]}**')
    st.markdown(f'#### {t["question"]}')
    st.write(t['problem'])
    st.caption('**Why watch:** '+t['promise'])
   with r:
    if st.button('Watch guided story →',key='story_'+k,use_container_width=True):navigate('Case Stories',k)
    if st.button('Inspect agent flow →',key='agent_'+k,use_container_width=True):navigate('Agent Flow',k)
 st.markdown('**The common engineering output:** documented service impairment → qualified hypotheses → missing evidence → recommended next investigation. The operational time or cost benefit remains a pilot hypothesis.')
 section('04 · What the buyer actually gets','An engineering investigation brief, not a black-box score','For each case the product packages measured service symptoms, supported protocol observations, qualified hypotheses and specific missing evidence into a reviewable assessment.')
 buyer_bridge(cid)
 st.markdown('**Two different ways to experience the value:** The Guided Story shows *what the engineering team receives*. Agent Flow shows *how the recorded agents produced it*.')
 st.markdown('<div class="ra-proof"><b>Demonstrated:</b> Three completed multi-agent investigations; all reruns scored 40/40 on the existing semantic rubric. <b>Not demonstrated:</b> verified causal accuracy, production performance improvements or automated site acceptance.</div>',unsafe_allow_html=True)
 boundary()

elif page=='Service Experience':
 section('01 · Measured service','What does the network service evidence show?','Explore recorded sender/receiver performance from the selected synthetic RAN case. Comparison measurements came from a separate execution.')
 proposition(cid);st.subheader(f'{cid} · {c["title"]}');case_metrics(c,d);comparison_chart(c)
 st.info(c['hook'])
 with st.expander('SP03 · detailed measurement interpretation',expanded=True):source_obs(d['SP03']['output'].get('observations',[]),8)
 st.caption('Do not interpret sender–receiver throughput disparity as receiver-reported packet loss. Interval arithmetic loss and packet-weighted summary loss are different metrics.')
 if st.button('Continue to case story →'):navigate('Case Stories')
 boundary()

elif page=='Architecture':
 section('How the system works','A compact, evidence-grounded multi-agent architecture','Source measurements and sampled radio logs are analysed by specialist agents, synthesised by the Supervisor, then independently assessed outside the operational LangGraph.')
 st.markdown("""<div class="ra-flow"><div class="ra-node"><b>Frozen network evidence</b><small>iPerf JSON, interval CSV and selected gNB logs</small></div><div class="ra-arr">→</div><div class="ra-node focus"><div class="ra-agent"><b>SP03 · Measurement specialist</b>GPT-6 Luna · throughput, loss, jitter</div><div class="ra-agent"><b>SP04 · Protocol specialist</b>GPT-6 Luna · RACH/MAC/RLC/PDCP/RRC</div><div class="ra-agent"><b>Supervisor</b>Gemma 4 31B IT · synthesis and uncertainty</div></div><div class="ra-arr">→</div><div class="ra-node"><b>Engineering review</b><small>Judge outside LangGraph; LangSmith trace; source-linked findings; missing evidence</small></div></div>""",unsafe_allow_html=True)
 st.info('Important: the original engineering experiment used LangGraph, OpenRouter-routed models and LangSmith. The current Streamlit app only replays curated JSON; it does not contact these services.')
 section('Technology & implementation','What technology is used?')
 st.dataframe(pd.DataFrame(TECH,columns=['Layer','Technology','Responsibility']),hide_index=True,use_container_width=True)
 st.markdown('**Quality controls:** source-qualified observations, deterministic validation, evaluator-only B3 reference, independent Judge step, causal abstention and no network execution.')
 boundary()

elif page=='Case Stories':
 section('Guided engineering story',f'{cid} · {c["title"]}','Follow the actual recorded engineering outputs through a clear, progressive story. Each scene is a presentation of completed evidence, not simulated inference.')
 proposition(cid)
 stages=['Ready','Observe service','Measurement specialist','Protocol specialist','Supervisor synthesis','Independent evaluation','Decision boundary']
 navcols=st.columns([1,3,1])
 with navcols[0]:
  st.button('← Previous',disabled=st.session_state.scene==0,on_click=step_scene,args=(-1,),key='story_previous')
 with navcols[1]:st.select_slider('Investigation scene',options=list(range(len(stages))),key='scene',format_func=lambda x:f'{x} · {stages[x]}')
 with navcols[2]:
  st.button('Next →',disabled=st.session_state.scene==len(stages)-1,on_click=step_scene,args=(1,),key='story_next')
 scene=st.session_state.scene
 st.progress(scene/(len(stages)-1))
 with st.container(border=True):
  st.caption(f'SCENE {scene} OF {len(stages)-1} · {stages[scene].upper()}')
  if scene==0:st.subheader('The reason to watch');st.write(STORY[cid]['problem']);st.info('What to watch for: '+STORY[cid]['promise'])
  elif scene==1:st.subheader('What the measurements show');case_metrics(c,d);st.write(c['lesson'])
  elif scene==2:st.subheader('SP03 · Measurement analysis');source_obs(d['SP03']['output'].get('observations',[]),6)
  elif scene==3:st.subheader('SP04 · Radio and protocol interpretation');source_obs(d['SP04']['output'].get('observations',[]),6)
  elif scene==4:
   st.subheader('Supervisor · Evidence synthesis');st.write(sup.get('final_assessment',''))
   for h in sup.get('candidate_hypotheses',[]):st.markdown('• **'+h.get('status','POSSIBLE')+'** — '+h.get('claim',''))
   if not sup.get('candidate_hypotheses'):st.info('No sufficiently supported causal hypothesis was asserted in this recorded case.')
  elif scene==5:st.subheader('Independent semantic evaluation');st.success(f'{judge["score"]}/{judge["max_score"]} · existing ten-criterion rubric');st.write(judge.get('assessment',''))
  else:
   st.subheader('Engineering outcome and next action');deliverable(cid,sup);st.warning('A verified causal root cause, verified recovery and site acceptance are outside this experiment.')
 customer_takeaway(cid,scene)
 if scene==6:
  st.success('Delivered: a qualified, source-linked engineering assessment and a focused next-evidence plan — not a verified root cause.')
  st.markdown('**Next: verify the mechanism.** The Agent Flow shows which specialist contributed each type of evidence and how the Supervisor synthesised it.')
 st.caption('Scene progression follows engineering presentation order. The raw LangSmith timeline remains inspectable separately in Agent Flow.')
 st.markdown('**Why inspect the Agent Flow?** See *how* SP03, SP04 and the Supervisor produced and qualified this assessment, with original trace events, independent evaluation and recorded timing.')
 if st.button('See how the AI reached this assessment →',key='story_to_agent'):navigate('Agent Flow')

elif page=='Agent Flow':
 section('Interactive trace-grounded replay',f'{cid} · Follow the agent execution','Play the recorded SP03 → SP04 → Supervisor sequence. Events and timings come from the saved LangSmith trace; animation timing is for presentation only.')
 st.markdown('**Why watch this workflow?** Inspect the engineering process behind the deliverable: SP03 interprets service measurements, SP04 evaluates sampled radio/protocol observations, and the Supervisor reconciles them. Validation and the independent Judge make the work auditable; they do not establish causal ground truth.')
 buyer_bridge(cid)
 st.info(STORY[cid]['question']+'  '+STORY[cid]['promise'])
 render_agent_replay(d,cid)
 deliverable(cid,sup,compact=True)
 if st.button('Inspect supporting evidence →',key='agent_to_evidence'):navigate('Evidence Room')
 boundary()

elif page=='Evidence Room':
 section('Engineering transparency','What supports each conclusion?','Open the recorded observations and source-reference families. Exact raw log-line validation remains in the private original source inventory, not this curated public-style replay.')
 tabs=st.tabs(['Measured observations','RAN protocol findings','Supervisor & uncertainty','Trace provenance'])
 with tabs[0]:source_obs(d['SP03']['output'].get('observations',[]),20)
 with tabs[1]:source_obs(sup.get('supported_protocol_observations',[]),20)
 with tabs[2]:
  st.write(sup.get('final_assessment',''))
  st.markdown('**Missing discriminating evidence**');source_obs(sup.get('missing_discriminating_evidence',[]),15)
  st.markdown('**Recorded uncertainty**');source_obs(sup.get('uncertainty',[]),15)
 with tabs[3]:
  st.json({'case_id':cid,'run_id':d.get('run_id'),'operational_trace_id':d.get('operational_trace_id'),'judge_trace_id':judge.get('trace_id'),'root_cause_verified':sup.get('root_cause_verified',False),'corrective_action_verified':sup.get('corrective_action_verified',False),'recovery_verified':sup.get('recovery_verified',False)})
 boundary()

elif page=='Results & Value':
 section('Experimental results','What has actually been demonstrated?','Every recorded v2.3.10 rerun completed; all achieved 40/40 on the existing role-based semantic evaluation. That is evidence of the rubric outcome, not verified causal root-cause accuracy.')
 rows=[{'Scenario':k,'Investigation RX (Mbps)':round(v['rx'],3),'Independent comparison RX (Mbps)':round(v['comparison'],3),'Receiver loss (%)':round(v['loss'],4),'Judge semantic score':'40/40','Causal RCA':'NOT_SCORABLE'} for k,v in CASES.items()]
 st.dataframe(pd.DataFrame(rows),hide_index=True,use_container_width=True)
 st.info('Measured: recorded packet/throughput values, LangSmith stage timing and semantic Judge criteria. Proposed: reduced manual investigation time, improved site acceptance, engineer productivity and operating-cost effects.')
 section('Operational opportunities','What might this enable for a telecom organisation?')
 cols=st.columns(2)
 for i,(a,b,kpi) in enumerate(VALUE):
  with cols[i%2]:card(a,b+' Pilot KPI: '+kpi+'.')
 section('Operationalisation path','From demonstrated research to operator value')
 st.markdown('<div class="ra-journey"><span>01 · Closed engineering experiment</span><span>→ 02 · Operator benchmark pilot</span><span>→ 03 · Governed integration</span></div>',unsafe_allow_html=True)
 st.markdown('**Pilot measures:** time to engineer-reviewed finding; manual effort per investigation; evidence completeness and unsupported claims; acceptance rework. No measured savings, formal operator acceptance or production SLAs have yet been established.')
 st.markdown('**Independent assurance caveat:** the Judge uses the same model family as the Supervisor, and B3 is evaluator-only rather than a verified causal RCA label.')
 brief={'case':cid,'metrics':c,'supervisor_assessment':sup.get('final_assessment'), 'missing_evidence':sup.get('missing_discriminating_evidence',[]),'semantic_judge':{'score':judge['score'],'max_score':judge['max_score']},'root_cause_verified':False,'recovery_verified':False,'evidence_scope':'Synthetic offline replay, not an operator acceptance decision'}
 st.download_button('Download selected case evidence brief (JSON)',json.dumps(brief,indent=2),file_name=f'RANalyzer_{cid}_evidence_brief.json',mime='application/json')
 boundary()
