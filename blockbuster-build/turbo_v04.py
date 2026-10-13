from pathlib import Path
base=Path('BlockbusterAutoPlayer/app')
src=base/'src/main/java/com/niyam/blockauto/AutoPlayService.java'
s=src.read_text()
def repl(old,new):
    global s
    if old not in s: raise RuntimeError('Cannot apply patch: '+old[:70])
    s=s.replace(old,new,1)
repl('private static final long FRAME_INTERVAL_MS=1550;', '''// Respect Android screenshot rate limit while reducing response time.
    private static final long FRAME_INTERVAL_MS=410;''')
repl('private long nextAllowed=0,lastStatusUpdate=0;', 'private long nextAllowed=0,lastStatusUpdate=0,gestureCompletedAt=0;')
repl('handler.postDelayed(loop,1200);','handler.postDelayed(loop,400);')
repl('@Override public void onFailure(int code){fault("Screen capture denied: "+code);}', '''@Override public void onFailure(int code){
                    if(code==ERROR_TAKE_SCREENSHOT_INTERVAL_TIME_SHORT){
                        busy=false;nextAllowed=System.currentTimeMillis()+500;
                        status("Screen capture cooldown, retrying…");
                    } else fault("Screen capture denied: "+code);
                }''')
repl('busy=false;nextAllowed=System.currentTimeMillis()+3000;', 'busy=false;nextAllowed=System.currentTimeMillis()+1100;')
repl('''        if("drag".equals(action)){
            if(signature.equals(pendingSignature)){
                stableCaptures++;
                if(stableCaptures>=2){stop("Drag not registered twice; inspect touch calibration");return;}
                busy=false;nextAllowed=System.currentTimeMillis()+850;
                status("Waiting for drag animation…");return;
            }
            placed++;transformTries=0;orientationActions=0;transformDisabled=false;stableCaptures=0;lockedMove=null;
            action="";
        }else if("transform".equals(action)){''', '''        if("drag".equals(action)){
            // A changing animation is not enough: confirm the new state twice.
            if(signature.equals(pendingSignature)){
                if(gestureCompletedAt>0 && System.currentTimeMillis()-gestureCompletedAt>1700){
                    stop("Drag not registered. Check calibration / speed.");return;
                }
                busy=false;nextAllowed=System.currentTimeMillis()+250;
                status("Waiting for block to land…");return;
            }
            if(!signature.equals(stableSignature)){
                stableSignature=signature;stableFrames=1;busy=false;
                status("Confirming new board…");return;
            }
            if(stableFrames<1){stableFrames=1;busy=false;return;}
            placed++;transformTries=0;orientationActions=0;transformDisabled=false;
            stableCaptures=0;lockedMove=null;action="";
            // Reuse confirmed frame rather than waiting an additional cycle.
            stableFrames=2;
        }else if("transform".equals(action)){''')
for a,b in [('nextAllowed=System.currentTimeMillis()+3500;', 'nextAllowed=System.currentTimeMillis()+1500;'),('nextAllowed=System.currentTimeMillis()+2600;', 'nextAllowed=System.currentTimeMillis()+1150;'),('dispatch(path,120,"transform");','dispatch(path,105,"transform");'),('dispatch(path,105,kind);','dispatch(path,75,kind);'),('dispatch(path,920,"drag");','dispatch(path,470,"drag");')]:repl(a,b)
repl('busy=false;stableCaptures=0;nextAllowed=System.currentTimeMillis()+("drag".equals(type)?1000:550);', '''busy=false;stableCaptures=0;gestureCompletedAt=System.currentTimeMillis();
                    nextAllowed=gestureCompletedAt+("drag".equals(type)?280:160);''')
src.write_text(s)
activity=base/'src/main/java/com/niyam/blockauto/MainActivity.java'
t=activity.read_text().replace('Auto puzzle testing • No root • Android 11+','HIGH SPEED (Turbo) • No root • Android 11+')
t=t.replace('text(root,"Game data and rewards are untouched.', 'text(root,"Turbo scans near 410 ms and drags near 470 ms. If Android rate-limits screenshots, it retries instead of stopping. Game data and rewards are untouched.')
activity.write_text(t)
build=base/'build.gradle'
b=build.read_text().replace('versionCode 3','versionCode 4').replace("versionName '0.3.0-video-calibrated'", "versionName '0.4.0-turbo'")
build.write_text(b)
print('Applied turbo v0.4 changes')
