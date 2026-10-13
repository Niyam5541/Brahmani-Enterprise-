from pathlib import Path
import re
root=Path('BlockbusterAutoPlayer/app')
p=root/'src/main/java/com/niyam/blockauto/AutoPlayService.java'
s=p.read_text()
def change(old,new,mandatory=True):
    global s
    if old not in s:
        if mandatory: raise RuntimeError('expected service code not found: '+old[:90])
        return
    s=s.replace(old,new,1)
s,n=re.subn(r'(FRAME_INTERVAL_MS\s*=\s*)165(\s*;)',r'\g<1>70\g<2>',s,count=1)
if n!=1:
    s,n=re.subn(r'handler\.postDelayed\(this,\s*165\);','handler.postDelayed(this,70);',s,count=1)
if n!=1: raise RuntimeError('Could not locate Ultra loop interval')
change('private int recoveryAttempts=0;', '''private int recoveryAttempts=0;
    private int failedDragStreak=0;
    private long lastGoodMoveAt=0;''')
change('placed++;transformTries=0;orientationActions=0;',
       'placed++;failedDragStreak=0;lastGoodMoveAt=System.currentTimeMillis();transformTries=0;orientationActions=0;')
change('private void retry(String why,long pause){\n        busy=false;', '''private void retry(String why,long pause){
        if(why.startsWith("Drag") || why.startsWith("Move result")){
            failedDragStreak=Math.min(6,failedDragStreak+1);
            if(failedDragStreak>=4)pause=Math.max(pause,2400);
        }
        busy=false;''')
change('float fingerY=startY+(targetY-anchorY+lift)/factor;', '''float fingerY=startY+(targetY-anchorY+lift)/factor;
        // Retry near the same cell center after a failed gesture.
        if(failedDragStreak>0){
            float nudge=Math.min(failedDragStreak,3)*.055f*f.cell;
            fingerX+=(failedDragStreak%2==0 ? nudge : -nudge);
            fingerY-=nudge;
        }''')
change('dispatch(path,300,"drag");', 'dispatch(path,failedDragStreak>0?Math.min(430,225+55*failedDragStreak):225,"drag");')
change('dispatch(path,55,kind);', 'dispatch(path,45,kind);',False)
change('boolean b=GAME.contentEquals(p);\n                    return b;', '''boolean b=GAME.contentEquals(p);
                    if(b){foreground=true;return true;}
                    String pkg=p.toString();
                    if(("android".equals(pkg)||"com.android.systemui".equals(pkg)) && foreground)
                        return true;
                    return false;''')
p.write_text(s)
sp=root/'src/main/java/com/niyam/blockauto/GameSolver.java'
g=sp.read_text()
assert 'if(pruned.size()>=180)break;' in g
g=g.replace('if(pruned.size()>=180)break;','if(pruned.size()>=52)break;')
g=g.replace('double transformCost=(o.turns+(o.mirrored?2:0))*.20;',
            'double transformCost=(o.turns+(o.mirrored?2:0))*2.0;')
sp.write_text(g)
act=root/'src/main/java/com/niyam/blockauto/MainActivity.java'
a=act.read_text().replace('STABLE ULTRA V0.6','ULTRA FAST STABLE V0.7')
a=a.replace('Stable Ultra checks screenshots and drags in 300 ms.','Ultra V0.7 drags in about 225 ms when stable.')
act.write_text(a)
b=root/'build.gradle'
t=b.read_text()
assert 'versionCode 6' in t
t=t.replace('versionCode 6','versionCode 7').replace("versionName '0.6.0-stable-ultra'","versionName '0.7.0-ultra-fast-stable'")
b.write_text(t)
print('V0.7 Ultra Fast Stable patch applied; solver beam=52')
