"""Run inside TouchDesigner. Set retire_source to 7 (Yoruba) or 9 (paired Chokwe)."""
from pathlib import Path
import json,re
import numpy as np
base=Path('C:/Users/matts/Documents/ChatGPT/particle mask')
e=op('/project1/nine_mask_cloud')
assert not e.op('recorder').par.record.eval()
e.par.Play=False
old=[0,10,2,12,3,11,4,9,5,6,7,1,8]
names={0:'Wooden',1:'Narrow',2:'Hare',3:'Round',4:'Five prongs',5:'Ritual',6:'Royal',7:'Yoruba',8:'Paired masks',9:'Chokwe',10:'Horned oval',11:'Carved face',12:'Crescent horns',13:'Oval face',14:'Ornate round',15:'Long face',16:'Walu antelope'}
widths=dict(zip(old,[.66,.99,.84,.95,1.14,1.18,.69,1.447,1.12,1.53,1.19,.63,1.03]))
for item in json.loads((base/'assets/pop/new_masks_v26/added_sources.json').read_text()):widths[item['index']]=item['halfwidth']
# Interleave new silhouettes and replace the retired mask with the narrow Walu.
order=[0,13,10,2,12,15,3,11,14,4,9,5,6,7,1,8]
order=[16 if n==retire_source else n for n in order]
assert len(order)==len(set(order))==16
beat=60/88.;phase=20.425%beat
centers=[round(phase+round((t-phase)/beat)*beat,6) for t in np.linspace(20,265,15)]
source=(base/'thirteen_mask_runtime_v25.py').read_text()
source=re.sub(r'^ORDER=.*$',f'ORDER={order!r}',source,flags=re.M)
source=re.sub(r'^NAMES=.*$',f'NAMES={[names[n] for n in order]!r}',source,flags=re.M)
source=re.sub(r'^WIDTHS=.*$',f'WIDTHS={[widths[n] for n in order]!r}',source,flags=re.M)
source=re.sub(r'^CENTERS=.*$',f'CENTERS={centers!r}',source,flags=re.M)
source=source.replace('dance_curves_v19','dance_curves_v26').replace('thirteen_mask_audit_v25.json','sixteen_mask_audit_v26.json')
source=source.replace('-14*((1-blend) if a%COUNT==10 else (blend if (a+1)%COUNT==10 else 0))', '-14*((1-blend) if ORDER[a%COUNT]==7 else (blend if ORDER[(a+1)%COUNT]==7 else 0))')
(base/'sixteen_mask_runtime_v26.py').write_text(source)
for j in range(3):
    c=e.op('actor_'+str(j+1))
    for n in range(13,17):
        shape=c.op('shape_'+str(n)) or c.create(fileinPOP,'shape_'+str(n))
        shape.par.file=str(base/f'assets/pop/new_masks_v26/mask_{n}.obj');shape.cook(force=True)
        assert shape.numPoints()==65536
    for k,n in enumerate(order+[order[0]]):c.op('morph').inputConnectors[k].connect(c.op('shape_'+str(n)))
choreo=(base/'bake_choreography_v19.py').read_text()
choreo=re.sub(r'^centers=.*$',f'centers=np.array({centers!r})',choreo,flags=re.M)
choreo=choreo.replace('dance_curves_v19','dance_curves_v26').replace('choreography_v19','choreography_v26')
(base/'bake_choreography_v26.py').write_text(choreo)
exec(choreo)
e.op('ensemble_clock').text=source
e.op('recorder').par.file=str(base/'petals_sixteen_masks_v26_video.mov')
e.store('mask_sequence_v26',dict(retired=names[retire_source],order=order,names=[names[n] for n in order],centers=centers))
print('Installed 16-mask sequence; retired',names[retire_source])
