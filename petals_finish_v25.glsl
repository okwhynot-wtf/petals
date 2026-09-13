uniform float uFade;
uniform vec4 uAtmosphere; // scene seconds (other legacy values unused)
uniform vec4 uPetals; // amount, wind, phrase activity, reserved
out vec4 fragColor;
float hash1(float n){return fract(sin(n*127.1+311.7)*43758.5453);}
float faceClear(vec2 uv){
 float d=10.;
 for(int j=0;j<3;j++){
  vec2 q=(uv-vec2(.18+float(j)*.32,.5))/vec2(.135,.39);
  d=min(d,length(q));
 }
 return smoothstep(.85,1.18,d);
}
void main(){
 vec2 uv=vUV.st;float t=uAtmosphere.x;
 vec3 c=max(texture(sTD2DInputs[0],uv).rgb,vec3(0));
 float peak=max(max(c.r,c.g),c.b);float q=peak<=.72?peak:.72+.23*(1.-exp(-(peak-.72)/.23));c*=q/max(peak,1e-6);
 float reveal=smoothstep(4.,7.,t);
 c=mix(texture(sTD2DInputs[1],uv).rgb,c,reveal);
 float activity=clamp(.36+.50*uPetals.z+.24*(1.-smoothstep(6.,14.,t)),0.,1.);
 if(uPetals.x>.001){
  for(int i=0;i<24;i++){
   float id=float(i);float seed=hash1(id+1.);float speed=mix(.038,.075,hash1(id+8.));
   float life=t*speed+hash1(id+30.);float cycle=floor(life);float age=fract(life);
   float presence=1.-smoothstep(activity-.08,activity+.08,hash1(id+50.));
   float lane=mod(id,4.);float x=.035+lane*.31;
   x+=.025*sin(t*.38+seed*25.)+uPetals.y*(.065*sin(t*.16+seed*6.)+.035*sin(t*.51+seed*14.));
   x+=.025*sin(age*6.28+cycle*.73+seed*8.);
   float y=1.13-age*1.30;
   vec2 delta=(uv-vec2(x,y))*vec2(1.7777778,1.);
   float size=mix(.008,.019,hash1(id+80.));
   if(length(delta)>size*2.)continue;
   float angle=t*(.6+seed*.55)+seed*30.;float ca=cos(angle),sa=sin(angle);
   vec2 p=mat2(ca,-sa,sa,ca)*delta/size;
   float fold=.18+.82*abs(cos(t*.95+seed*15.));p.x/=fold;
   // Cupped, irregular petal: rounded tip, narrowing attachment, curled rim.
   float width=.58+.22*p.y+.06*sin(p.y*8.+seed*8.);
   float shape=length(vec2(p.x/max(.15,width),p.y));
   float alpha=(1.-smoothstep(.87,1.03,shape))*presence;
   float edge=smoothstep(.65,.95,shape);
   float vein=.5+.5*sin(p.y*16.+p.x*5.+seed*12.);
   float light=.35+.65*max(0.,sin(angle+1.));
   vec3 petal=mix(vec3(.11,.022,.029),vec3(.42,.17,.085),edge*.55+light*.30);
   petal*=.70+.25*vein+.35*light;
   float clear=mix(1.,.10+.90*faceClear(uv),reveal);
   alpha*=clear*uPetals.x*smoothstep(0.,.04,age)*(1.-smoothstep(.91,1.,age));
   c=mix(c,petal,clamp(alpha,0.,.9));
  }
 }
 fragColor=TDOutputSwizzle(vec4(c*uFade,1));
}
