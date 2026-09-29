import json,time,urllib.request
from datetime import datetime,timezone
BASE="https://api-web.nhle.com/v1"; SEASONS=["20252026","20262027"]
TEAMS=["ANA","BOS","BUF","CAR","CBJ","CGY","CHI","COL","DAL","DET","EDM","FLA","LAK","MIN","MTL","NJD","NSH","NYI","NYR","OTT","PHI","PIT","SEA","SJS","STL","TBL","TOR","UTA","VAN","VGK","WPG","WSH"]
def get(path):
 r=urllib.request.Request(BASE+path,headers={"User-Agent":"BRNSY-PROPS/3.0"})
 with urllib.request.urlopen(r,timeout=30) as x:return json.load(x)
def txt(x):return (x.get("default") or next(iter(x.values()),"")) if isinstance(x,dict) else (x or "")
P={}
for season in SEASONS:
 for team in TEAMS:
  try:
   r=get(f"/roster/{team}/{season}")
   for group in ("forwards","defensemen","goalies"):
    for p in r.get(group,[]):
     pid=str(p.get("id"))
     if pid=="None":continue
     q=P.setdefault(pid,{"playerId":p["id"],"name":(txt(p.get("firstName"))+" "+txt(p.get("lastName"))).strip(),"position":p.get("positionCode") or "","teams":set(),"seasons":set()})
     q["teams"].add(team);q["seasons"].add(season)
  except Exception as e:print("Roster warning",team,season,e)
print("Unique players",len(P)); logs={}
for i,(pid,p) in enumerate(P.items(),1):
 logs[pid]={}
 for season in SEASONS:
  if season not in p["seasons"]:continue
  try:logs[pid][season]=get(f"/player/{pid}/game-log/{season}/2").get("gameLog",[])
  except Exception as e:print("Log warning",pid,season,e);logs[pid][season]=[]
  time.sleep(.02)
 if i%100==0:print("Game logs",i,"/",len(P))
players=[{"playerId":p["playerId"],"name":p["name"],"position":p["position"],"teams":sorted(p["teams"]),"seasons":sorted(p["seasons"])} for p in P.values()]
with open("data/nhl_history.json","w") as f:json.dump({"updated":datetime.now(timezone.utc).isoformat(),"seasons":SEASONS,"players":players,"logs":logs},f,separators=(",",":"))
print("Saved NHL history",len(players),"players")
