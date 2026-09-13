"""Thirteen front-facing POP masks, musical motion, and restrained camera parallax."""
import math,time,json
DURATION=283.65
OFFSET=0.
ORDER=[0, 13, 10, 2, 12, 15, 3, 11, 14, 4, 16, 5, 6, 7, 1]
NAMES=['Wooden', 'Oval face', 'Horned oval', 'Hare', 'Crescent horns', 'Long face', 'Round', 'Carved face', 'Ornate round', 'Five prongs', 'Walu antelope', 'Ritual', 'Royal', 'Yoruba', 'Narrow']
WIDTHS=[0.66, 1.089771588874651, 0.99, 0.84, 0.95, 0.6977035028103191, 1.14, 1.18, 1.5444561680890154, 0.69, 0.723328873662088, 1.12, 1.53, 1.19, 0.63]
CENTERS=[20.0, 38.0, 56.0, 74.0, 92.0, 110.0, 128.0, 146.0, 164.0, 182.0, 200.0, 218.0, 236.0, 254.0]
COUNT=len(NAMES)
def smooth(x):
    x=max(0.,min(1.,x));return x*x*(3-2*x)
def state(t):
    for i,center in enumerate(CENTERS):
        if t<center+4:return i,smooth((t-center+4)/8)
    return COUNT-1,0.
def focus(t):
    return [float(parent().op('actor_'+str(j+1)+'/morph').par.index) for j in range(3)]

def dance(e,t,j):
    data=e.fetch('dance_curves_v28');x=max(0.,t)*60.
    a=min(int(x),len(data)-1);b=min(a+1,len(data)-1);w=x-int(x)
    return [data[a][j][k]*(1-w)+data[b][j][k]*w for k in range(3)]
def snare_turn(e,t,j):
    data=e.fetch('snare_turns_v28');x=max(0.,t)*60.
    a=min(int(x),len(data)-1);b=min(a+1,len(data)-1);w=x-int(x)
    return data[a][j]*(1-w)+data[b][j]*w

def apply(t):
    e=parent();e.par.Time=t;e.par.Cliptime=t;e.store('scene_seconds',t)
    i,w=state(t);m=i+w
    e.par.Feature=NAMES[i]+(' to '+NAMES[(i+1)%COUNT] if w>0 else '')
    e.op('score_envelopes').cook(force=True)
    audio=e.op('score_envelopes')
    low=float(audio['low'][0]);mid=float(audio['mid'][0]);high=float(audio['high'][0]);onset=float(audio['onset'][0])
    am=float(e.par.Audiomotion);rot=float(e.par.Rotationamount);cm=float(e.par.Cameramotion)
    appearance=smooth(t/7)*(1-smooth((t-276)/7.65))
    phrase_times=[43.55,88.9,151.,194.9,239.]
    mist=sum(math.exp(-.5*((t-p)/4.5)**2) for p in phrase_times)
    e.store('atmosphere_envelope',min(1.,mist)*appearance)
    cue=min(phrase_times,key=lambda p:abs(t-p))
    e.store('atmosphere_progress',smooth((t-cue+9)/18))
    if e.par.Mistpreview:
        e.store('atmosphere_envelope',appearance)
        e.store('atmosphere_progress',.5+.45*math.sin(t*.18))
    cx=.24*cm*math.sin(t*.035);cy=.075*cm*math.sin(t*.027)
    cz=8.5+.16*cm*math.sin(t*.031+.7)
    camera=e.op('ensemble_camera');camera.par.tx=cx;camera.par.ty=cy;camera.par.tz=cz
    camera.par.ry=math.degrees(math.atan2(cx,cz))
    camera.par.rx=-math.degrees(math.atan2(cy,math.hypot(cx,cz)))
    projection=camera.projection(e.op('OUT').width,e.op('OUT').height)
    distance=math.sqrt(cx*cx+cy*cy+cz*cz);horizontal=math.hypot(cx,cz)
    forward=(-cx/distance,-cy/distance,-cz/distance)
    right=(cz/horizontal,0.,-cx/horizontal)
    up=(-cx*cy/(horizontal*distance),horizontal/distance,-cz*cy/(horizontal*distance))
    for j in range(3):
        c=e.op('actor_'+str(j+1));c.store('scene_seconds',t+j*23)
        ri,rw=state(t-(4 if j==1 else -4))
        index=m if j==0 else (ri+rw+(-2 if j==1 else 2))%COUNT
        a=int(index);blend=index-a;transition=math.sin(math.pi*blend)**2
        width=WIDTHS[a%COUNT]*(1-blend)+WIDTHS[(a+1)%COUNT]*blend
        strength=am*(1 if j==0 else .75)
        # Equal-size trio in one row, on the former centre actor's Z plane.
        c.par.Posx=[0.,-3.15,3.15][j]
        c.par.Posy=0.
        c.par.Posz=.25
        dx,dy,dz=dance(e,t,j);turn=dz
        # One diagonal gesture: lateral travel carries a related depth arc,
        # while the baked vertical channel adds lift or dip.
        c.par.Posx=float(c.par.Posx)+.30*dx*strength*appearance
        c.par.Posy=float(c.par.Posy)+.25*dy*strength*appearance
        depth_mix=.72*dz+.28*dx-.10*dy
        c.par.Posz=float(c.par.Posz)+.46*depth_mix*strength*appearance
        c.par.Scale=1.12
        c.par.Tilt=4.5*rot*math.sin(t*.071+j*1.9)+4*turn*strength*appearance
        c.par.Yaw=math.degrees(math.atan2(cx-float(c.par.Posx),cz-float(c.par.Posz)))+6*snare_turn(e,t,j)*min(rot,1.0)*min(am,1.0)*appearance
        for geo in ['intact_geo','cloud_geo']:
            c.op(geo).par.rx=math.degrees(math.atan2(float(c.par.Posy)-cy,cz-float(c.par.Posz)))+3.5*rot*math.sin(t*.065+j*1.7)-14*((1-blend) if ORDER[a%COUNT]==7 else (blend if ORDER[(a+1)%COUNT]==7 else 0))
        c.op('morph').par.index=index;c.op('gather_morph').par.index=appearance
        c.op('surface_breath').par.amp0=.008+(.075 if j==0 else .04)*transition+.032*mid*strength+.018*onset*strength+.22*math.sin(math.pi*appearance)**2
        # This edge selection only emits drifting particles; the full face remains visible.
        c.par.Cut=width*((.72 if j==0 else .92)-.14*mid*strength-.1*transition)
        c.par.Brightness=(.21 if j==0 else .105)*(.9+.14*low)*(.08+.92*appearance)
        c.par.Birthrate=((8500 if j==0 else 2200)+(14000 if j==0 else 4000)*transition+(15000*mid+9000*onset)*strength)*appearance
        c.par.Drift=(.002 if j==0 else .0027)+.0015*transition+.001*mid*strength
        c.par.Pointsize=.85+.20*high*strength+.12*onset*strength
        c.par.Postglow=.48+.28*high;c.par.Ghostmix=.35 if j==0 else .25
        c.par.Chromatic=.2;c.par.Postexposure=1.5
    e.op('actor_1/dust_material').par.alpha=.135+.045*low
    e.par.Fade=smooth(t/2)*(1-smooth((t-281)/2.65))

def restart(record=False):
    e=parent();e.op('recorder').par.record=False;e.par.Play=False
    e.store('frame',0);e.store('recording',False);e.store('arm',bool(record));e.store('warmup',3)
    e.store('audit',[]);e.store('performance',[]);apply(0)
    for j in range(3):
        c=e.op('actor_'+str(j+1));c.op('particles').par.initializepulse.pulse()
        for name in ['image_feedback','ghost_feedback']:c.op(name).par.resetpulse.pulse()
    root.time.end=max(root.time.end,17030);root.time.frame=1
    root.time.play=True;project.realTime=not record
def onStart():
    e=parent();e.par.Play=False;e.op('recorder').par.record=False
    e.store('frame',0);e.store('recording',False);e.store('warmup',0);e.store('arm',False);apply(0)
def onFrameStart(frame):
    e=parent();warm=e.fetch('warmup',0)
    if warm:
        e.store('warmup',warm-1);e.op('OUT').cook(force=True)
        if warm==1:
            for j in range(3):e.op('actor_'+str(j+1)+'/particles').par.startpulse.pulse()
            e.par.Play=True;e.op('track').par.cuepulse.pulse()
            if e.fetch('arm',False):e.op('recorder').par.record=True;e.store('recording',True)
        return
    if not e.par.Play or not root.time.play:return
    f=e.fetch('frame',0)
    if f>=17019:
        e.op('recorder').par.record=False;e.par.Play=False;e.store('recording',False);project.realTime=True
        with open(e.par.Outputfolder.eval()+'/fifteen_mask_audit_v27.json','w') as out:
            json.dump(dict(frames=f,fps=60,duration=DURATION,errors=e.errors(recurse=True),samples=e.fetch('audit',[])),out,indent=2)
        return
    apply(f/60.)
    if not e.fetch('recording',False):e.op('monitor').cook(force=True)
    for j in range(3):e.op('actor_'+str(j+1)+'/ghost_history').cook(force=True)
    e.op('OUT').cook(force=True)
    if e.fetch('recording',False):e.op('recorder').cook(force=True)
    if f%300==0:
        audit=e.fetch('audit',[]);audit.append(dict(time=f/60.,indices=focus(f/60.),errors=e.errors(recurse=True)));e.store('audit',audit)
    e.store('frame',f+1)
    p=e.fetch('performance',[]);p.append(time.perf_counter());e.store('performance',p[-180:])













