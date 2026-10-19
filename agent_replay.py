"""Frozen LangSmith operational stages presented as a trace-faithful investigation replay."""
from datetime import datetime
import streamlit as st

AGENTS=('SP03','SP04','SUPERVISOR')
ROLE={'SP03':'Service measurement interpretation','SP04':'Sampled RAN protocol review','SUPERVISOR':'Evidence-grounded assessment'}

def parse(t):return datetime.fromisoformat(t.replace('Z','+00:00'))
def duration(e):return max(0,(parse(e['end'])-parse(e['start'])).total_seconds())
def timefmt(s):return f'{s:.3f}s' if 0<s<0.01 else f'{s:.2f}s'
def refs(item):
 v=item.get('evidence_refs') or item.get('source_refs') or []
 return [v] if isinstance(v,str) else v

def render(data,case):
 events=sorted((dict(e) for e in data.get('timeline',[]) if e.get('start') and e.get('end')),key=lambda e:parse(e['start']))
 main={a:next((e for e in events if e.get('agent')==a and e.get('type')=='chain' and e.get('name')==a),None) for a in AGENTS}
 if not all(main.values()):
  st.error('Recorded operational stage missing. Unable to show a faithful replay.');return
 prefix='ra_replay_'+case;step=prefix+'_step';playing=prefix+'_playing';speed=prefix+'_speed';resume=prefix+'_return'
 for k,v in ((step,0),(playing,False),(speed,'Normal'),(resume,0),(prefix+'_tick',0)):st.session_state.setdefault(k,v)
 def move(delta):
  st.session_state[playing]=False;st.session_state[step]=max(0,min(4,st.session_state[step]+delta))
 def toggle():
  if st.session_state[step]>=4:st.session_state[step]=0
  st.session_state[playing]=not st.session_state[playing]
 def restart():st.session_state[playing]=False;st.session_state[step]=0
 @st.fragment(run_every='1s')
 def stage_view():
  # Controls and displayed replay state are in the same fragment: no stale parent controls.
  if st.session_state[playing] and st.session_state[step]<4:
   tick=prefix+'_tick';st.session_state[tick]+=1
   if st.session_state[tick] >= {'Slow':3,'Normal':2,'Fast':1}[st.session_state[speed]]:
    st.session_state[tick]=0;st.session_state[step]+=1
    if st.session_state[step]==4:st.session_state[playing]=False
  a,b,c,d,e=st.columns([1.1,1,1,1,1.3])
  a.button('⏸ Pause' if st.session_state[playing] else '▶ Play',key=prefix+'_toggle',on_click=toggle,use_container_width=True)
  b.button('← Previous',key=prefix+'_prev',on_click=move,args=(-1,),disabled=st.session_state[step]==0,use_container_width=True)
  c.button('Next →',key=prefix+'_next',on_click=move,args=(1,),disabled=st.session_state[step]>=4,use_container_width=True)
  d.button('↺ Restart',key=prefix+'_restart',on_click=restart,use_container_width=True)
  e.selectbox('Replay pace · not runtime',['Slow','Normal','Fast'],key=speed)
  idx=st.session_state[step]
  st.caption(f'PRESENTATION STAGE {idx}/4 · '+('Ready' if idx==0 else AGENTS[idx-1] if idx<4 else 'Engineering brief')+' · Playback pace is not investigation duration')
  st.progress(idx/4)
  cols=st.columns(3)
  for i,agent in enumerate(AGENTS):
   status='Active' if idx==i+1 else 'Reviewed' if idx>i+1 else 'Pending'
   with cols[i]:
    with st.container(border=True):
     st.markdown('**'+agent+'** · '+status)
     st.caption(ROLE[agent])
  if idx==0:
   st.info('Ready. Watch the recorded measurement and protocol specialist assessments, followed by Supervisor synthesis. This is an offline presentation, not a live inference run.')
  elif idx in (1,2):
   agent=AGENTS[idx-1];span=main[agent];obs=data[agent]['output'].get('observations',[])
   st.subheader(agent+' · '+ROLE[agent]);st.caption('Recorded parent span: '+timefmt(duration(span))+' · This is an original operational stage.')
   st.markdown('**Selected findings from recorded output**')
   # Evidence-editorial highlights remain a subset; all original observations are accessible.
   start=0 if agent=='SP03' else max(0,len(obs)-3)
   selected=obs[start:start+3]
   for item in selected:
    st.write('• '+(item.get('claim','') if isinstance(item,dict) else str(item)))
    if isinstance(item,dict) and refs(item):st.caption('Recorded source family: '+', '.join(map(str,refs(item))))
   with st.expander(f'All {len(obs)} original {agent} observations'):
    for item in obs:
     st.write('• '+(item.get('claim','') if isinstance(item,dict) else str(item)))
     if isinstance(item,dict) and refs(item):st.caption('Recorded source family: '+', '.join(map(str,refs(item))))
  elif idx==3:
   span=main['SUPERVISOR'];sup=data['SUPERVISOR']['output']
   st.subheader('Supervisor · Reconcile evidence, retain uncertainty');st.caption('Recorded parent span: '+timefmt(duration(span)))
   st.write(sup.get('final_assessment',''))
   with st.expander('Candidate explanations and evidence gaps'):
    for v in sup.get('candidate_hypotheses',[]):st.write('• '+str(v.get('status','POSSIBLE'))+': '+v.get('claim',''))
    for v in sup.get('missing_discriminating_evidence',[]):st.write('• '+str(v))
  else:
   sup=data['SUPERVISOR']['output'];st.success('Recorded operational investigation completed. Engineering assessment ready for review.')
   st.markdown('**Engineering assessment**');st.write(sup.get('final_assessment',''))
   st.markdown('**Missing discriminating evidence / next investigation**')
   for v in sup.get('missing_discriminating_evidence',[]):st.write('• '+str(v))
   st.caption('Verified causal RCA, remediation and recovery are not established.')
 stage_view()
 st.markdown('**Technical trace inspection · optional**')
 with st.expander('Original nested LangSmith spans, model calls and validators'):
  first=min(parse(e['start']) for e in events)
  rows=[]
  for e in events:
   typ=e.get('type','')
   name=e.get('name','')
   classification='Specialist / Supervisor' if e.get('agent') in AGENTS and typ=='chain' and name==e.get('agent') else 'Model invocation' if typ=='llm' else 'Validator / grounding check'
   rows.append({'Agent':e.get('agent'),'Recorded event':name,'Classification':classification,'Start offset (s)':round((parse(e['start'])-first).total_seconds(),3),'Span duration (s)':round(duration(e),4),'Status':e.get('status')})
  st.dataframe(rows,use_container_width=True,hide_index=True)
  st.caption('Events are nested recorded spans, not nine independent sequential agents. Start offsets describe event starts; durations are not added. No validator is credited with specialist findings.')
 with st.expander('Independent Judge · separate assurance'):
  j=data.get('judge',{});st.write(f"Semantic rubric result: {j.get('score','—')}/{j.get('max_score','—')}")
  st.write(j.get('assessment',''))
  st.caption('Judge is outside the operational LangGraph. Rubric score does not verify causal accuracy.')
 st.caption('Recorded run: '+str(data.get('run_id','—'))+' · Operational trace: '+str(data.get('operational_trace_id','—')))
