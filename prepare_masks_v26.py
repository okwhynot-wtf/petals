from pathlib import Path
import json
import numpy as np
import trimesh
import bake_fields

ROOT=Path(__file__).parent
OUT=ROOT/'assets/pop/new_masks_v26'; bake_fields.OUT=OUT
FILES=['african_tribal_mask_model_03.glb','maskround.glb','tribal_mask.glb','walu_antelope_mask.glb']
def order(p,d=0):
    if len(p)<=32:return p[np.argsort(p[:,d%3],kind='stable')]
    p=p[np.argsort(p[:,[1,0,2][d%3]],kind='stable')];mid=len(p)//2
    return np.concatenate([order(p[:mid],d+1),order(p[mid:],d+1)])
meta=[]
for i,file in enumerate(FILES,13):
    bake_fields.ORIENTATIONS[file]=([0,1,2],0)
    bake_fields.bake(file)
    m=trimesh.load(Path('C:/Users/matts/Pictures/masks')/file,skip_materials=True,process=False).to_mesh()
    v=m.vertices-m.bounds.mean(0);v*=3.8/np.ptp(v[:,1]);m.vertices=v
    p,_=trimesh.sample.sample_surface(m,524288,seed=41)
    stem=Path(file).stem.replace(' ','_').replace('(','').replace(')','')
    field=np.load(ROOT/'assets/pop/new_masks_v26'/f'{stem}.npy')
    xy=np.clip(np.rint((p[:,:2]/5+.5)*1023).astype(int),0,1023)
    good=p[(field[xy[:,1],xy[:,0],3]>.4)&(p[:,2]>=field[xy[:,1],xy[:,0],0]-.028)]
    rng=np.random.default_rng(81);p=order(good[rng.choice(len(good),65536,replace=len(good)<65536)])
    with (OUT/f'mask_{i}.obj').open('w') as f:
        for v in p:f.write('v %.6f %.6f %.6f\n'%tuple(v))
        for j in range(len(p)):f.write('p %d\n'%(j+1))
    meta.append(dict(index=i,file=file,halfwidth=float(np.max(np.abs(p[:,0]))),points=len(p)))
    print(meta[-1],flush=True)
(ROOT/'assets/pop/new_masks_v26/added_sources.json').write_text(json.dumps(meta,indent=2))

