# github.com/zeittresor
import pygame as p,math,os,random,tempfile,wave,struct
from math import sin as sn,cos as co,pi
rr=random.random;ru=random.uniform
CO=[rr()*6.28 for _ in range(3)]
SW1=ru(-0.3,0.3);SW2=ru(-0.3,0.3)
CBV=[(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]
CBF=[(0,1,2,3),(4,5,6,7),(0,1,5,4),(2,3,7,6),(0,3,7,4),(1,2,6,5)]
THV=[(1,1,1),(-1,-1,1),(-1,1,-1),(1,-1,-1)]
THF=[(0,1,2),(0,1,3),(0,2,3),(1,2,3)]
OCV=[(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]
OCF=[(0,2,4),(2,1,4),(1,3,4),(3,0,4),(0,2,5),(2,1,5),(1,3,5),(3,0,5)]
PYV=[(1,1,1),(-1,1,1),(-1,-1,1),(1,-1,1),(0,0,-1)]
PYF=[(0,1,2,3),(0,1,4),(1,2,4),(2,3,4),(3,0,4)]
def sh(sf,t,vs,fs):
    ang=t*0.6;ca=co(ang);sa=sn(ang);cbg=co(ang*0.5);sbg=sn(ang*0.5)
    ps=[]
    sfactor=350*(1+0.3*sn(t*0.4))
    for vx,vy,vz in vs:
        x1=vx*ca-vz*sa;z1=vx*sa+vz*ca;y1=vy*cbg-z1*sbg;z2=vy*sbg+z1*cbg;sc=sfactor/(z2+3)
        ps.append((int(W/2+x1*sc),int(H/2+y1*sc),z2))
    sf.fill((0,0,0))
    for face in fs:
        z=sum(ps[i][2] for i in face)/len(face)
        col=int(max(0,min(255,200+z*40)))
        pg=[ps[i][:2] for i in face]
        p.draw.polygon(sf,(col,int(col*0.6),int(col*0.3)),pg)
def g():
    try:
        sr=22050
        bt=0.5;bar=2.0;bars=4;length=bar*bars
        fn=os.path.join(tempfile.gettempdir(),'m.wav')
        wv=wave.open(fn,'wb');wv.setnchannels(1);wv.setsampwidth(2);wv.setframerate(sr)
        tones=[131,147,165,175,196,220,247]
        prog=[[0,4,5,3],[0,5,3,4],[0,5,4,1]][int(rr()*3)]
        chords=[];bass=[];mel=[]
        for c in prog:
            root=tones[c];chords.append((root,tones[(c+2)%len(tones)],tones[(c+4)%len(tones)]));bass.append(root*0.5)
        for j,c in enumerate(prog):
            for _ in range(4):
                mel.append(tones[(c+int(rr()*6))%len(tones)]*2)
        total=int(sr*length)
        for i in range(total):
            t=i/sr
            b=int(t/bar)
            pos=t-b*bar
            q=int(pos/bt)
            bp=pos-q*bt
            r,th,fi=chords[b]
            chord=(sn(2*pi*r*t)+sn(2*pi*th*t)+sn(2*pi*fi*t))*0.2
            bas=sn(2*pi*bass[b]*t)*0.5
            melv=sn(2*pi*mel[b*4+q]*t)*0.3
            k_amp=(0.1-bp)/0.1 if bp<0.1 else 0
            kick=sn(2*pi*55*t)*k_amp*0.8
            s_amp=(0.05-bp)/0.05 if q in (1,3) and bp<0.05 else 0
            snare=sn(2*pi*2000*t)*s_amp*0.4
            hh=int(pos/(bt/2))
            hh_bp=pos-hh*(bt/2)
            h_amp=(0.02-hh_bp)/0.02 if hh_bp<0.02 else 0
            hat=sn(2*pi*3000*t)*h_amp*0.2
            v=chord+bas+melv+kick+snare+hat
            if v>1:v=1
            if v<-1:v=-1
            wv.writeframes(struct.pack('<h',int(v*32767)))
        wv.close()
        return fn
    except Exception:
        return None
p.init();p.mixer.init(22050,-16,1)
info=p.display.Info();W,H=info.current_w,info.current_h
S=p.display.set_mode((W,H),p.FULLSCREEN);p.mouse.set_visible(False)
F=p.font.Font(None,int(H*0.12))
txt=F.render('wait',1,(220,220,240))
S.fill((0,0,0));S.blit(txt,(W//2-txt.get_width()//2,H//2-txt.get_height()//2));p.display.flip()
mp=g()
try:
    p.mixer.music.load(mp);p.mixer.music.play(-1)
except:pass
u=p.Surface((W,H));v=p.Surface((W,H))
st=[];P=p.Surface((80,80))
C=p.time.Clock();tm=0
sd=8;fd=2
GD=0
IMS=[]
for _ in range(6):
    m=p.Surface((64,64))
    r1=rr()*pi*2;r2=rr()*pi*2
    for x in range(32):
        for y in range(32):
            val=int(128+127*sn(x*0.15+r1)+127*sn(y*0.15+r2))
            val=max(0,min(255,val))
            col=(val,val//2,255-val)
            m.set_at((x,y),col);m.set_at((63-x,y),col);m.set_at((x,63-y),col);m.set_at((63-x,63-y),col)
    IMS.append(m)
def lc(sf,t):
    sf.fill((0,0,0))
    for x in range(0,W,4):
        h=int(H*0.4+sn(x*0.01+t*0.3)*H*0.1+sn(x*0.05+t*0.4)*H*0.05)
        sky=(0,0,int(120+100*sn(t*0.5)));ground=(20,int(100+80*sn(t*0.3)),20)
        p.draw.line(sf,sky,(x,0),(x,h));p.draw.line(sf,ground,(x,h),(x,H))
def cld(sf,t):
    for x in range(80):
        for y in range(80):
            v=int(128+127*sn(x*0.07+t)+127*sn(y*0.07-t)+127*sn((x+y)*0.03+t*0.4))
            v=max(0,min(255,v));g=int(v*0.4+127*sn(t*0.2));g=max(0,min(255,g))
            P.set_at((x,y),(v,g,255-v))
    Q=p.transform.smoothscale(P,(W,H));Q.set_alpha(100);sf.blit(Q,(0,0))
def cp(sf,t):
    idx=int((t*0.2)%len(IMS));surf=IMS[idx]
    R=p.transform.rotate(surf,t*10)
    Q=p.transform.smoothscale(R,(W,H))
    Q.set_alpha(140);sf.blit(Q,(0,0))
def th(sf,t):sh(sf,t,THV,THF)
def oc(sf,t):sh(sf,t,OCV,OCF)
def py(sf,t):sh(sf,t,PYV,PYF)
def s1(sf,t):ss(sf,SW1,GD)
def s2(sf,t):ss(sf,SW2,GD)
def s0(sf,t):ss(sf,0,GD)
def tx(sf,t):
    idx=int((t*0.15)%len(IMS))
    r=p.transform.smoothscale(IMS[idx],(W//2,H//2))
    sf.blit(r,(0,0));sf.blit(p.transform.flip(r,1,0),(W//2,0));sf.blit(p.transform.flip(r,0,1),(0,H//2));sf.blit(p.transform.flip(r,1,1),(W//2,H//2))
def spn(sf,t):
    sf.fill((0,0,0))
    R=min(W,H)/2
    for i in range(60):
        ang=i*0.10472+t*0.5
        x=int(W/2+co(ang)*R);y=int(H/2+sn(ang)*R)
        c=int((sn(ang*4)+1)*127)
        p.draw.line(sf,(c,255-c,c//2),(W//2,H//2),(x,y),2)
def bars(sf,t):
    sf.fill((0,0,0))
    sh=int((t*100)%40)
    for x in range(-sh,W,40):
        c=int(128+127*sn(t*0.5+x*0.05))
        p.draw.rect(sf,(c,int(c*0.5),255-c),(x,0,20,H))
def fld(sf,t):
    sf.fill((0,0,0))
    for i in range(30):
        z=i/30
        y=int(H-((t*200)%H+z*H))
        c=int(255*(1-z))
        p.draw.line(sf,(c,int(c*0.6),int(c*0.3)),(0,y),(W,y))
def bw(sf,t):
    sf.fill((0,0,0))
    br=int(128+127*sn(t*0.1+CO[0]));bg=int(128+127*sn(t*0.1+2+CO[1]));bb=int(128+127*sn(t*0.1+4+CO[2]))
    CO[0]+=0.001;CO[1]+=0.0015;CO[2]+=0.002
    for y in range(0,H,4):
        h=int(128*(sn(y*0.03+t*0.4)+1))
        p.draw.line(sf,(br*h//255,bg*h//255,bb*h//255),(0,y),(W,y))
def ss(sfce,sw,d):
    global st
    sfce.fill((0,0,0))
    for s in st:
        x,y,vx,vy,r,sh=s
        if sw:
            dx=x-W/2;dy=y-H/2;vx+=sw*dy*d;vy-=sw*dx*d
        x+=vx*d;y+=vy*d;r+=d*50
        s[0]=x;s[1]=y;s[2]=vx;s[3]=vy;s[4]=r
    st=[s for s in st if 0<=s[0]<W and 0<=s[1]<H]
    cx=W/2+sn(tm*0.2)*W*0.25;cy=H/2+co(tm*0.17)*H*0.25
    for _ in range(5):
        a=rr()*2*pi;sp=ru(50,200);sh=int(rr()*3)
        st.append([cx,cy,co(a)*sp,sn(a)*sp,1,sh])
    for s in st:
        c=min(255,int(s[4]*10))
        rad=max(1,int(s[4]*0.05))
        sh=s[5]
        if sh==0:
            p.draw.circle(sfce,(c,c,c),(int(s[0]),int(s[1])),rad)
        elif sh==1:
            p.draw.rect(sfce,(c,c,c),(int(s[0])-rad,int(s[1])-rad,rad*2,rad*2))
        else:
            x0=int(s[0]);y0=int(s[1])
            pts=[(x0,y0-rad),(x0+rad,y0+rad),(x0-rad,y0+rad)]
            p.draw.polygon(sfce,(c,c,c),pts)
def cb(sf,t):sh(sf,t,CBV,CBF)
def pl(t):
    for x in range(80):
        for y in range(80):
            v=int(128+127*sn(0.13*x+t*0.5)+127*sn(0.14*y-t*0.5));v=max(0,min(255,v));P.set_at((x,y),(v,v//2,v))
    Q=p.transform.smoothscale(P,(W,H));Q.set_alpha(80);S.blit(Q,(0,0))
def tn(sf,t):
    sf.fill((0,0,0))
    for i in range(30):
        r=i/30;rad=int((1-r)*(W if W<H else H)/2)
        xo=int(sn(t*2+i*0.1)*60);yo=int(co(t*2+i*0.1)*60)
        c=int(255*(1-r));p.draw.circle(sf,(c,int(c*0.7),int(c*0.4)),(W//2+xo,H//2+yo),rad,1)
def hx(sf,t):
    sf.fill((0,0,0))
    m=max(W,H)/3
    for i in range(100):
        z=i/100;a=t*1.2+i*0.15;r=(1-z)*m;x=int(W/2+co(a)*r);y=int(H/2+sn(a)*r);
        c=int(255*z);p.draw.circle(sf,(c,int(c*0.7),int(c*0.4)),(x,y),4)
def np(sf,t):
    for x in range(80):
        for y in range(80):
            v=int(128+127*sn(x*0.08+t)+127*sn(y*0.08-t)+127*sn((x+y)*0.04+t*0.5));v=max(0,min(255,v))
            g=int(v*0.5+127*sn(t*0.2))
            g=max(0,min(255,g))
            P.set_at((x,y),(v,g,255-v))
    Q=p.transform.smoothscale(P,(W,H));Q.set_alpha(90);sf.blit(Q,(0,0))
def mg(sf,t):
    sf.fill((0,0,0))
    for x in range(0,W,20):
        for y in range(0,H,20):
            if ((x//20+y//20+int(t*3))%2)==0:
                c=int(100+155*sn(0.1*x+0.1*y+t))
                c=max(0,min(255,c))
                p.draw.rect(sf,(c,int(c*0.5),255-c),(x,y,20,20))
def wk(sf,t):
    sf.fill((0,0,0))
    for i in range(30):
        z=i/30;col=int(200*(1-z))
        y=int(H/2+sn(t*0.7+i)*H*0.1+z*z*H*0.5)
        wv=int(W*(1-z)*0.6)
        x=int(W/2-wv/2)
        p.draw.rect(sf,(col,int(col*0.6),int(col*0.3)),(x,y,wv,H-y))
def cp2(sf,t):
    idx=int((t*0.17)%len(IMS));surf=IMS[idx]
    for i in range(3):
        rot=p.transform.rotate(surf,t*10+i*60)
        sc=p.transform.smoothscale(rot,(W,H))
        sc.set_alpha(60)
        sf.blit(sc,(0,0))
def pp(sf,t):
    sf.fill((0,0,0))
    for i in range(50):
        x=int(i/50*W+sn(t*0.3+i)*40)
        wv=int(W/50+sn(t*0.5+i)*5)
        c=int(128+127*sn(t*0.7+i))
        p.draw.rect(sf,(c,int(c*0.5),255-c),(x,0,wv,H))
def rg(sf,t):
    sf.fill((0,0,0))
    mn=min(W,H)/2
    for i in range(40):
        z=i/40
        rad=int(z*mn)
        ang=t*0.3+i*0.2
        x=int(W/2+co(ang)*rad);y=int(H/2+sn(ang)*rad)
        col=int(128+127*sn(ang*2))
        p.draw.circle(sf,(col,int(col*0.5),255-col),(x,y),int(3+rad*0.03),1)
def mz(sf,t):
    sf.fill((0,0,0))
    sp=25
    for x in range(0,W,sp):
        col=int(128+127*sn(t*0.5+x*0.02))
        p.draw.line(sf,(col,int(col*0.5),255-col),(x,0),(x,H))
    for y in range(0,H,sp):
        col=int(128+127*sn(t*0.5+y*0.02))
        p.draw.line(sf,(col,int(col*0.5),255-col),(0,y),(W,y))
def sc2(sf,t):
    sf.fill((0,0,0))
    for y in range(0,H,6):
        xoff=int(W/2+sn(t*0.4+y*0.05)*W*0.4)
        col=int(128+127*sn(t*0.3+y*0.02))
        p.draw.rect(sf,(col,int(col*0.5),255-col),(0,y,xoff,4))
def r3d(sf,t):
    idx=int((t*0.4)%3)
    if idx==0:th(sf,t)
    elif idx==1:oc(sf,t)
    else:py(sf,t)
def ld2(sf,t):
    sf.fill((0,0,0))
    for x in range(0,W,3):
        h=int(H*0.3+sn(x*0.01+t*0.2)*H*0.15+sn(x*0.05-t*0.3)*H*0.08)
        col=(int(100+80*sn(t*0.2+x*0.02)),int(60+50*sn(t*0.1+x*0.03)),int(150+80*sn(t*0.15+x*0.04)))
        p.draw.line(sf,col,(x,0),(x,h))
        g=int(50+40*sn(t*0.25+x*0.05))
        p.draw.line(sf,(g,int(g*0.5),255-g),(x,h),(x,H))
def rings2(sf,t):
    sf.fill((0,0,0))
    m=min(W,H)/2
    for i in range(50):
        z=i/50;rad=int((1-z)*m)
        off=sn(t*0.6+i*0.3)*50
        col=int(128+127*sn(i*0.2+t*0.3))
        p.draw.circle(sf,(col,int(col*0.5),255-col),(int(W/2+off),int(H/2+off)),rad,1)
def swp(sf,t):
    sf.fill((0,0,0))
    for i in range(70):
        ang=i*0.1+t*0.5
        x=int(W/2+co(ang)*W*0.6)
        y=int(H/2+sn(ang)*H*0.6)
        col=int(128+127*sn(i*0.2+t*0.3))
        p.draw.circle(sf,(col,int(col*0.5),255-col),(x,y),int(i*0.1+2))
def vr(sf,t):
    sf.fill((0,0,0))
    m=min(W,H)/2
    for i in range(80):
        z=i/80;r=z*m;a=t*0.8+z*10
        x=int(W/2+co(a)*r)
        y=int(H/2+sn(a)*r)
        col=int(128+127*sn(t*0.5+i*0.1))
        p.draw.circle(sf,(col,int(col*0.5),255-col),(x,y),2)
def ln2(sf,t):
    sf.fill((0,0,0))
    for i in range(120):
        y=int(i/120*H)
        length=int(W*0.5+sn(t*0.5+i*0.3)*W*0.5)
        col=int(128+127*sn(i*0.15+t*0.25))
        p.draw.line(sf,(col,int(col*0.5),255-col),(0,y),(length,y))
def frc(sf,t):
    for x in range(80):
        for y in range(80):
            v=int(128+127*sn(x*0.09+t*0.5)+127*sn(y*0.09-t*0.5)+127*sn((x+y)*0.06+t*0.3))
            v=max(0,min(255,v))
            g=int(v*0.6+127*sn(t*0.2));g=max(0,min(255,g))
            P.set_at((x,y),(v,g,255-v))
    Q=p.transform.smoothscale(P,(W,H));Q.set_alpha(100);sf.blit(Q,(0,0))
def pxl(sf,t):
    sf.fill((0,0,0))
    step=15
    for x in range(0,W,step):
        for y in range(0,H,step):
            c=int(128+127*sn(0.05*x+0.05*y+t*0.4))
            p.draw.rect(sf,(c,int(c*0.5),255-c),(x,y,step,step))
def spin2(sf,t):
    sf.fill((0,0,0))
    for i in range(90):
        ang=i*0.2+t*0.5
        r=i*5
        x=int(W/2+co(ang)*r)
        y=int(H/2+sn(ang)*r)
        col=int(128+127*sn(ang))
        p.draw.circle(sf,(col,int(col*0.5),255-col),(x,y),3)
def wall(sf,t):
    sf.fill((0,0,0))
    for i in range(40):
        x=int(W*i/40+sn(t*0.4+i)*20)
        col=int(128+127*sn(i*0.1+t*0.3))
        p.draw.rect(sf,(col,int(col*0.5),255-col),(x,0,5,H))
def wave3(sf,t):
    sf.fill((0,0,0))
    for y in range(0,H,5):
        col=int(128+127*sn(t*0.3+y*0.04))
        off=int(sn(y*0.05+t*0.5)*W*0.3)
        p.draw.line(sf,(col,int(col*0.5),255-col),(off,y),(off+W,y))
def tube(sf,t):
    sf.fill((0,0,0))
    rX=W*0.5;rY=H*0.5
    for i in range(100):
        a=t*0.6+i*0.2
        x1=int(W/2+co(a)*rX)
        y1=int(H/2+sn(a)*rY)
        x2=int(W/2+co(a+pi)*rX)
        y2=int(H/2+sn(a+pi)*rY)
        col=int(128+127*sn(i*0.15+t*0.4))
        p.draw.line(sf,(col,int(col*0.5),255-col),(x1,y1),(x2,y2))
FS=[bw,s0,s1,s2,cb,tn,hx,lc,th,oc,py,cld,cp,tx,spn,bars,fld,mg,wk,cp2,pp,rg,mz,sc2,r3d,ld2,rings2,swp,vr,ln2,frc,pxl,spin2,wall,wave3,tube]
random.shuffle(FS)
running=True
while running:
    for e in p.event.get():
        if e.type==p.QUIT or (e.type==p.KEYDOWN and e.key==27):running=False
    d=C.tick(60)/1000;tm+=d;GD=d
    sg=tm%sd;i=int(tm/sd)%len(FS);j=(i+1)%len(FS);a=0
    if sg>sd-fd:a=(sg-(sd-fd))/fd
    FS[i](u,tm);FS[j](v,tm)
    u.set_alpha(int(255*(1-a)));v.set_alpha(int(255*a))
    S.blit(u,(0,0));S.blit(v,(0,0))
    pl(tm);np(S,tm)
    p.display.flip()
p.quit()
