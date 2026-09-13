import numpy as np
raw=np.asarray(e.fetch('baked_envelopes'),dtype=float);rise=np.maximum(0,np.diff(raw,axis=0,prepend=raw[:1]));score=rise[:,2]+.5*rise[:,1]
beat=60/72.;phase=20.10;curves=np.zeros((17020,3));rng=np.random.default_rng(2828);events=[]
for bar in np.arange(phase,280,4*beat):
    for beat_index in [1,3]:
        tick=bar+beat_index*beat;lo=max(0,int((tick-.10)/.05));hi=min(len(score),int((tick+.10)/.05)+1);n=lo+int(np.argmax(score[lo:hi]))
        if score[n]<.035:continue
        start=n*.05;sign=float(rng.choice([-1,1]));events.append((start,sign))
        for j in range(3):
            begin=start+j*.03;duration=.55
            for f in range(int(begin*60),min(len(curves),int((begin+duration)*60)+1)):
                u=(f/60-begin)/duration;q=min(1.,u/.25);v=q*q*(3-2*q) if u<.25 else 1-(min(1.,(u-.25)/.75)**2*(3-2*min(1.,(u-.25)/.75)))
                curves[f,j]=sign*v*(1 if j==0 else .8)
e.store('snare_turns_v28',curves.tolist());e.store('snare_events_v28',events);print('4/4 snare turns',len(events))
