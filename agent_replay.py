"""Offline, trace-backed, interactive RANalyzer replay.
No calls to agents, LangSmith or networks; display progression is not execution time.
"""
from datetime import datetime
from html import escape
import streamlit as st

NAMES={'SP03':'Measurement specialist','SP04':'Radio/protocol specialist','SUPERVISOR':'Evidence synthesis'}

def parse(t): return datetime.fromisoformat(t.replace('Z','+00:00'))
def fmt(sec): return f'{int(sec)//60:02d}:{sec%60:04.1f}'
def clean(s):return escape(str(s),quote=True)

def events_for(data):
    events=[dict(e) for e in data.get('timeline',[]) if e.get('start') and e.get('end')]
    events.sort(key=lambda e:(parse(e['start']), 0 if e['type']=='chain' else 1))
    return events

def render(data,case):
    events=events_for(data)
    if not events:
        st.warning('No timeline recorded for this case.');return
    key='ra_replay_'+case
    ixkey=key+'_step';runkey=key+'_playing';speedkey=key+'_speed'
    st.session_state.setdefault(ixkey,0)
    st.session_state.setdefault(runkey,False)
    st.session_state.setdefault(speedkey,'Normal')
    st.markdown('''<style>
    .ra-replay-shell{border:1px solid #cad8e9;background:#f6f9ff;border-radius:16px;padding:16px;margin:12px 0;color:#173052}
    .ra-replay-flow{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;align-items:center}
    .ra-replay-node{border:2px solid #d2ddeb;border-radius:12px;background:white;padding:16px 12px;min-height:96px;text-align:center;color:#274262}
    .ra-replay-node strong{display:block;font-size:1rem;color:#182e4b;margin-bottom:7px}
    .ra-replay-node small{color:#5b6f88}
    .ra-replay-node.active{background:#e2f6f1;border-color:#038b80;box-shadow:0 0 0 3px #c6ebe3}
    .ra-replay-node.done{background:#e8effb;border-color:#8cb1e9}
    .ra-replay-stage{padding:13px 15px;background:white;border:1px solid #cedce9;border-radius:11px;margin:10px 0;color:#203956}
    .ra-replay-stage .k{color:#4161a6;font-size:.74rem;font-weight:750;letter-spacing:.08em}
    .ra-replay-stage h4{margin:5px 0;color:#142f51}
    .ra-replay-stage p{color:#415b72;margin:5px 0;line-height:1.55}
    @media(max-width:670px){.ra-replay-flow{grid-template-columns:1fr}.ra-replay-node{min-height:60px}}
    </style>''',unsafe_allow_html=True)
    def move(delta):
        st.session_state[runkey]=False
        st.session_state[ixkey]=max(0,min(len(events),st.session_state[ixkey]+delta))
    def go_start():
        st.session_state[runkey]=False
        st.session_state[ixkey]=0
    def toggle():
        if st.session_state[ixkey]>=len(events):st.session_state[ixkey]=0
        st.session_state[runkey]=not st.session_state[runkey]
    a,b,c,d,e=st.columns([1,1,1,1,1.5])
    a.button('▶ Play' if not st.session_state[runkey] else '⏸ Pause',key=key+'_toggle',on_click=toggle,use_container_width=True)
    b.button('← Previous',key=key+'_prev',on_click=move,args=(-1,),disabled=st.session_state[ixkey]==0,use_container_width=True)
    c.button('Next step →',key=key+'_next',on_click=move,args=(1,),disabled=st.session_state[ixkey]>=len(events),use_container_width=True)
    d.button('↺ Restart',key=key+'_reset',on_click=go_start,use_container_width=True)
    e.selectbox('Playback speed (presentation only)',['Slow','Normal','Fast'],key=speedkey)
    # Auto-refresh a fragment, not the whole app. Display frames are paced for reading;
    # durations shown to users are from original UTC trace, never from this animation.
    interval={'Slow':'3s','Normal':'2s','Fast':'1s'}[st.session_state[speedkey]]
    @st.fragment(run_every=interval)
    def frame():
        if st.session_state[runkey] and st.session_state[ixkey]<len(events):
            st.session_state[ixkey]+=1
            if st.session_state[ixkey]>=len(events):st.session_state[runkey]=False
        idx=st.session_state[ixkey]
        visible=events[:idx]
        current=visible[-1] if visible else None
        owner=current.get('agent') if current else None
        start=parse(events[0]['start'])
        finish=max(parse(e['end']) for e in events)
        total=(finish-start).total_seconds()
        offset=(parse(current['end'])-start).total_seconds() if current else 0
        st.caption(f'RECORDED EXECUTION · EVENT {idx}/{len(events)} · {fmt(max(0,offset))} / {fmt(total)} observed timeline')
        st.progress(idx/len(events))
        st.markdown('<div class="ra-replay-shell"><div class="ra-replay-flow">'+''.join(
            '<div class="ra-replay-node '+('active' if agent==owner else 'done' if any(e.get('agent')==agent for e in visible) else '')+'"><strong>'+agent+'</strong><small>'+clean(NAMES[agent])+'</small></div>'
            for agent in ('SP03','SP04','SUPERVISOR'))+'</div></div>',unsafe_allow_html=True)
        if current:
            dur=(parse(current['end'])-parse(current['start'])).total_seconds()
            st.markdown('<div class="ra-replay-stage"><div class="k">LATEST RECORDED EVENT · '+clean(current.get('type',''))+'</div><h4>'+clean(current.get('name',''))+'</h4><p>Agent: '+clean(owner)+' · '+clean(current.get('status',''))+' · <b>'+f'{dur:.2f}s'+'</b> recorded span</p></div>',unsafe_allow_html=True)
            info=data.get(owner,{}) if owner else {}
            output=info.get('output',{})
            if owner=='SUPERVISOR' and current.get('type')=='chain':
                st.write(output.get('final_assessment',''))
            elif owner in ('SP03','SP04') and current.get('type')=='chain':
                obs=output.get('observations',[])
                for item in obs[:2]:
                    st.write('• '+(item.get('claim','') if isinstance(item,dict) else str(item)))
            elif current.get('type')=='llm': st.caption('Recorded model invocation; no new inference is performed during playback.')
            else: st.caption('Recorded deterministic validation or source-grounding step.')
        else:
            st.info('Ready. Press Play or Next step to reveal the actual recorded execution in order.')
        if idx==len(events):
            st.success('Operational sequence completed. Independent Judge reviewed the completed outputs separately.')
    frame()
    with st.expander('Recorded event details and assurance'):
        st.dataframe([{'Agent':e.get('agent'),'Event':e['name'],'Type':e['type'],'Duration (s)':round((parse(e['end'])-parse(e['start'])).total_seconds(),2),'Status':e['status']} for e in events],use_container_width=True,hide_index=True)
        judge=data.get('judge',{})
        st.write('Independent semantic Judge:',f"{judge.get('score','—')}/{judge.get('max_score','—')}")
        st.caption('Judge is outside LangGraph. Its score does not establish verified causal RCA. Timeline replay reveals recorded stages, not agent thought processes. Playback speed is not investigation runtime.')
    st.caption('Run ID: '+str(data.get('run_id','—'))+' · Trace ID: '+str(data.get('operational_trace_id','—')))
