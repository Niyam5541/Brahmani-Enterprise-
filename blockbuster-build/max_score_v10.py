from pathlib import Path
root=Path("BlockbusterAutoPlayer/app")
q=root/"src/main/java/com/niyam/blockauto/QuickSolver.java"
s=q.read_text()
anchor="    // Strongly prefer multi-line clears in one drop (2x/3x/4x), not just several single clears."
assert s.count(anchor)==1, "Expected v0.9 combo scorer"
setup="""    // Colors do not appear in strategy: only occupied 8x8 cells and piece shapes.
    // Prepare multiple nearly full lines with compatible gaps for the next large clear.
    private static double comboSetup(long board){
        int[] rowHoles=new int[8],colHoles=new int[8];
        int used=Long.bitCount(board);
        double score=0;
        for(int i=0;i<8;i++){
            rowHoles[i]=8-Long.bitCount(board & ROW[i]);
            colHoles[i]=8-Long.bitCount(board & COL[i]);
            if(rowHoles[i]==1)score+=70;
            else if(rowHoles[i]==2)score+=43;
            else if(rowHoles[i]==3)score+=15;
            if(colHoles[i]==1)score+=70;
            else if(colHoles[i]==2)score+=43;
            else if(colHoles[i]==3)score+=15;
        }
        for(int r=0;r<8;r++)if(rowHoles[r]<=3){
            for(int c=0;c<8;c++)if(colHoles[c]<=3 && (board & (1L<<(r*8+c)))==0)
                score+=(4-rowHoles[r])*(4-colHoles[c])*7;
        }
        // Do not choke the board merely to prepare a theoretical multiplier.
        if(used>43)score*=Math.max(.15,1.-(used-43)*.075);
        return score;
    }
"""
s=s.replace(anchor,setup+anchor,1)
for a,b in [('case 1:return 180;','case 1:return 120;'),('case 2:return 550;','case 2:return 620;'),('case 3:return 1220;','case 3:return 1650;'),('case 4:return 2150;','case 4:return 3100;'),('case 5:return 3500;','case 5:return 4400;')]:
    assert s.count(a)==1, "missing combo value "+a
    s=s.replace(a,b,1)
old="""double score=n.score+comboValue(lines)+boardScore(nextBoard)*.42 -orientCost
                                    + (nextBoard==0 && tmp!=0 ? 3200:0);"""
new="""double score=n.score+comboValue(lines)
                                    + (boardScore(nextBoard)-boardScore(n.board))*.50
                                    + (comboSetup(nextBoard)-comboSetup(n.board))*.55
                                    -orientCost + (nextBoard==0 && tmp!=0 ? 3200:0);"""
assert s.count(old)==1, "Expected v0.9 scoring expression"
s=s.replace(old,new,1)
q.write_text(s)
a=root/"src/main/java/com/niyam/blockauto/MainActivity.java"
t=a.read_text().replace("MAX COMBO V0.9","MAX SCORE V1.0")
t=t.replace("MAX COMBO v0.9 fixes false waiting on pale tiles, prioritizes multi-line clears (2x/3x/4x), and keeps fast ~195 ms adaptive drags.",
'''MAX SCORE v1.0 ignores block colors for strategy, plans future 3x/4x line clears, and protects board space. Keeps adaptive ~195ms gestures and scanner recovery.''')
a.write_text(t)
b=root/"build.gradle"
t=b.read_text()
assert "versionCode 9" in t
t=t.replace("versionCode 9","versionCode 10").replace("versionName '0.9.0-max-combo'","versionName '1.0.0-max-score'")
b.write_text(t)
print("V1.0 color-agnostic combo setup enabled")
