from pathlib import Path
p=Path("BlockbusterAutoPlayer/app/src/main/java/com/niyam/blockauto")
sfile=p/"AutoPlayService.java"
s=sfile.read_text()
def rep(a,b):
 global s
 if s.count(a)!=1: raise RuntimeError("v0.6 patch match failure: "+a[:90]+" count="+str(s.count(a)))
 s=s.replace(a,b,1)
rep("private long nextAllowed=0,lastStatusUpdate=0,gestureCompletedAt=0,lastScreenshotAt=0;",
"private long nextAllowed=0,lastStatusUpdate=0,gestureCompletedAt=0,lastScreenshotAt=0,busySince=0,lastEnableEpoch=-1;\n    private int recoveryAttempts=0;")
rep("            long now=System.currentTimeMillis();\n            if(prefs!=null && prefs.getBoolean(\"enabled\",false) && !busy",
"""            long now=System.currentTimeMillis();
            if(prefs!=null){
                long epoch=prefs.getLong("enableEpoch",0L);
                if(epoch!=lastEnableEpoch){
                    lastEnableEpoch=epoch;busy=false;busySince=0;consecutiveErrors=0;
                    action="";lockedMove=null;stableSignature="";stableFrames=0;
                    nextAllowed=now+150;recoveryAttempts=0;
                }
            }
            if(busy && busySince>0 && now-busySince>7000)
                retry("Android request timed out",950);
            if(prefs!=null && prefs.getBoolean("enabled",false) && !busy""")
rep("busy=true;lastScreenshotAt=System.currentTimeMillis();","busy=true;busySince=lastScreenshotAt=System.currentTimeMillis();")
rep('busy=false;nextAllowed=System.currentTimeMillis()+360;\n                        status("Android screenshot cooldown…");',
'busy=false;busySince=0;nextAllowed=System.currentTimeMillis()+550;\n                        status("Screenshot cooldown: automatic retry");')
rep('if(!prefs.getBoolean("enabled",false)||!isGameForeground()){busy=false;return;}',
'if(!prefs.getBoolean("enabled",false)||!isGameForeground()){busy=false;busySince=0;return;}')
rep('busy=false;nextAllowed=System.currentTimeMillis()+1100;\n            if(tryAccessibleReplay())return;',
'busy=false;busySince=0;nextAllowed=System.currentTimeMillis()+520;\n            if(tryAccessibleReplay())return;')
rep('        consecutiveErrors=0;\n        String signature=frameSignature(f);',
'        consecutiveErrors=0;busySince=0;\n        String signature=frameSignature(f);')
rep('stop("Drag not registered. Check calibration / speed.");return;',
'retry("Drag not confirmed; rescanning",580);return;')
rep('''            if(!proved && !signature.equals(stableSignature)){
                stableSignature=signature;stableFrames=1;busy=false;
                return;
            }
            if(!proved && stableFrames<1){stableFrames=1;busy=false;return;}
            placed++;''',
'''            if(!proved){
                if(!signature.equals(stableSignature)){stableSignature=signature;stableFrames=1;}
                else stableFrames++;
                if(gestureCompletedAt>0 && System.currentTimeMillis()-gestureCompletedAt>2800){
                    retry("Move result uncertain; rescanning",720);
                    return;
                }
                busy=false;busySince=0;nextAllowed=System.currentTimeMillis()+350;
                return;
            }
            placed++;''')
rep('busy=false;nextAllowed=System.currentTimeMillis()+1500;\n            status("No fitting placement. Waiting for round-end/replay (safe mode).");',
'busy=false;busySince=0;nextAllowed=System.currentTimeMillis()+950;\n            status("No fitting placement; waiting for safe replay.");')
rep('private void dispatch(Path path,int ms,String type){\n        try{',
'private void dispatch(Path path,int ms,String type){\n        busy=true;busySince=System.currentTimeMillis();\n        try{')
rep('busy=false;stableCaptures=0;gestureCompletedAt=System.currentTimeMillis();',
'busy=false;busySince=0;stableCaptures=0;gestureCompletedAt=System.currentTimeMillis();')
rep('onCancelled(GestureDescription g){stop("Touch cancelled. Paused for safety.");}',
'onCancelled(GestureDescription g){retry("Touch cancelled by Android",700);}')
rep('if(!sent)stop("Android rejected gesture; check Accessibility permission");',
'if(!sent)retry("Android rejected gesture",1200);')
rep('}catch(Exception ex){stop("Gesture failure: "+ex.getMessage());}',
'}catch(Exception ex){retry("Gesture failure: "+ex.getMessage(),1200);}')
rep('''    private void fault(String s){
        busy=false;consecutiveErrors++;
        if(consecutiveErrors>=5)stop("Auto-paused after errors: "+s);
        else status("Retry "+consecutiveErrors+"/5: "+s);
    }
    private void stop(String s){
        busy=false;action="";lockedMove=null;stableSignature="";stableFrames=0;
        if(prefs!=null)prefs.edit().putBoolean("enabled",false).putString("status",s).apply();
    }''',
'''    private void fault(String s){
        consecutiveErrors++;
        long pause=Math.min(6500L,450L*(1L<<Math.min(4,consecutiveErrors-1)));
        retry("Screen read: "+s,pause);
    }
    private void retry(String why,long pause){
        busy=false;busySince=0;action="";lockedMove=null;
        stableSignature="";stableFrames=0;stableCaptures=0;
        recoveryAttempts++;
        nextAllowed=System.currentTimeMillis()+Math.max(250,pause);
        status("AUTO ON | Recovering #"+recoveryAttempts+": "+why);
    }
    private void stop(String s){retry(s,1250);}
''')
rep('@Override public void onInterrupt(){busy=false;}',
'@Override public void onInterrupt(){retry("Accessibility interrupted; reconnecting",1300);}')
sfile.write_text(s)
activity=p/"MainActivity.java"
s=activity.read_text()
assert "ULTRA SPEED V0.5" in s
s=s.replace("ULTRA SPEED V0.5 • No root • Android 11+","STABLE ULTRA V0.6 • Auto-recovery • Android 11+")
s=s.replace('putBoolean("enabled",true).putString("status","Armed. Open the puzzle game.")',
            'putBoolean("enabled",true).putLong("enableEpoch",System.currentTimeMillis()).putString("status","Armed. Auto-recovery ON. Open the puzzle game.")')
s=s.replace("Ultra checks roughly every 360 ms and drags in 300 ms. Confirmed board updates can skip a redundant screenshot. If Android rate-limits screenshots, it retries instead of stopping. Game data and rewards are untouched. Rotations and automatic replays need live-device testing. If the puzzle or replay screen cannot be verified, automation waits or stops instead of tapping randomly.",
"Stable Ultra checks screenshots and drags in 300 ms. If touch is cancelled or a screenshot fails, it remains ON and retries. Manual ON resets the process. Auto replay still needs game-over testing. No game data or rewards are modified.")
activity.write_text(s)
g=Path("BlockbusterAutoPlayer/app/build.gradle")
s=g.read_text()
assert "versionCode 5" in s
g.write_text(s.replace("versionCode 5","versionCode 6").replace("versionName '0.5.0-ultra'","versionName '0.6.0-stable-ultra'"))
print("V0.6 stable patch applied")
