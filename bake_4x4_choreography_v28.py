import numpy as np
beat=60/72.; phase=20.10
centers=np.array([20.,38.,56.,74.,92.,110.,128.,146.,164.,182.,200.,218.,236.,254.])
raw=np.asarray(e.fetch('baked_envelopes'),dtype=float);curves=np.zeros((17020,3,3));bars=[]
for number,start in enumerate(np.arange(phase,280,4*beat)):
    phrase=int(np.searchsorted(centers,start,side='right'));leader=phrase%3
    angle=[.20,2.85,-.25,3.35][phrase%4];direction=np.array([np.cos(angle),np.sin(angle)]);normal=np.array([-direction[1],direction[0]])
    energy=float(np.mean(raw[max(0,int(start/.05)-8):min(len(raw),int(start/.05)+8),0]));amp=.42+.42*energy;bars.append((float(start),leader+1))
    for j in range(3):
        rank=0 if j==leader else (1 if (j-leader)%3==1 else 2);strength=[1.,.52,.40][rank]
        for beat_index,weight in [(0,1.0),(1,.34),(2,.20),(3,.52)]:
            begin=start+beat_index*beat+rank*.11*beat;duration=.92*beat
            for f in range(max(0,int(begin*60)),min(len(curves),int((begin+duration)*60)+1)):
                u=(f/60-begin)/duration
                if u<.25:q=u/.25;advance=q*q*(3-2*q)
                else:q=(u-.25)/.75;advance=1-q*q*(3-2*q)
                bend=.30*(1 if phrase%2==0 else -1)*np.sin(np.pi*u)**2
                curves[f,j,:2]+=amp*strength*weight*(direction*advance+normal*bend)
                curves[f,j,2]+=amp*strength*weight*(.32*direction[0]*advance+.16*bend)
kernel=np.array([1,4,6,4,1],float)/16
for j in range(3):
    for k in range(3):curves[:,j,k]=np.convolve(curves[:,j,k],kernel,'same')
assert np.isfinite(curves).all() and np.max(np.abs(curves))<1.2
e.store('dance_curves_v28',curves.tolist())
e.store('choreography_v28',dict(bpm=72,time_signature='4/4',phase=phase,bars=bars))
print('4/4 choreography:',len(bars),'bars; leaders:',sorted(set(x[1] for x in bars)))
