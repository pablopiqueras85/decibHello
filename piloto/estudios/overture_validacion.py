import json, numpy as np, pandas as pd
from scipy.optimize import nnls
from scipy.spatial import cKDTree
from sklearn.model_selection import LeaveOneGroupOut
from pyproj import Transformer
P='/home/user/Ideas/piloto/cache/'
t=Transformer.from_crs(4326,25831,always_xy=True)
val=pd.read_csv(P+'validacion_sensores.csv')
sens=pd.DataFrame(json.load(open(P+'sensors_todos.json'))); sens['sensor']=sens.Id_Instal.astype(float).astype(int)
sens=sens.drop_duplicates('sensor')[['sensor','Latitud','Longitud','Codi_Districte']]
val=val.merge(sens,on='sensor',how='left')
S=np.array([t.transform(float(a),float(b)) for a,b in zip(val.Longitud,val.Latitud)]); g=val.Codi_Districte.astype(str).values
def cens(n): return np.array([t.transform(float(r['Longitud']),float(r['Latitud'])) for r in json.load(open(P+n+'.json')) if r.get('Latitud')])
def cnt(pts, R=100): return np.log1p(np.array([len(x) for x in cKDTree(pts).query_ball_point(S,R)]))
O=np.load('overture/O.npy'); cat=np.load('overture/cat.npy'); conf=np.load('overture/conf.npy')
noct=np.isin(cat,['dance_club','cocktail_bar','pub','music_venue','lounge','hookah_bar','gay_bar','irish_pub','speakeasy','dive_bar','beer_garden'])
bares_ov=np.isin(cat,['bar','wine_bar','beer_bar','brewery','sports_bar','tapas_bar'])
alta=conf>=0.7
variantes={
 'censo 2024 (actual)': [cnt(cens('cens_solo_bares')), cnt(cens('cens_musicales'))],
 'Overture (todos)': [cnt(O[bares_ov]), cnt(O[noct])],
 'Overture (confianza >= 0,7)': [cnt(O[bares_ov&alta]), cnt(O[noct&alta])],
 'Overture sin tapas (conf >= 0,7)': [cnt(O[bares_ov&alta&(cat!='tapas_bar')]), cnt(O[noct&alta])],
}
for f in 'DEN':
    y=val[f'dif_{f}'].values; base=np.abs(y).mean()
    fila=[f'{f}: solo mapa {base:.2f}']
    for nombre,cols in variantes.items():
        A=np.c_[tuple(cols)]; p=np.zeros(len(y))
        for tr,te in LeaveOneGroupOut().split(A,y,g): p[te]=A[te]@nnls(A[tr],y[tr])[0]
        fila.append(f'{nombre} {np.abs(y-p).mean():.2f}')
    print(' · '.join(fila))
print('sensores', len(y))
