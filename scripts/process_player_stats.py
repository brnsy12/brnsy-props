import json
from datetime import datetime,timezone
D=json.load(open("data/nhl_history.json"))
def n(v):
 try:return float(v)
 except:return 0
def val(g,*ks):
 for k in ks:
  if g.get(k) is not None:return g[k]
 return 0
def agg(gs):
 a={"gp":len(gs),"goals":0,"assists":0,"points":0,"shots":0,"hits":0,"blocks":0,"ppp":0,"saves":0,"goalsAgainst":0}
 for g in gs:
  for out,keys in {"goals":("goals",),"assists":("assists",),"points":("points",),"shots":("shots","shotsOnGoal"),"hits":("hits",),"blocks":("blockedShots","blocks"),"ppp":("powerPlayPoints",),"saves":("saves",),"goalsAgainst":("goalsAgainst",)}.items():a[out]+=n(val(g,*keys))
 if a["gp"]:
  for k in ("goals","assists","points","shots","hits","blocks","ppp","saves","goalsAgainst"):a[k+"PerGame"]=round(a[k]/a["gp"],2)
 return a
rows=[];versus=[]
for p in D["players"]:
 for season in D["seasons"]:
  gs=D["logs"].get(str(p["playerId"]),{}).get(season,[])
  if not gs:continue
  team=val(gs[0],"teamAbbrev","team") or (p["teams"][-1] if p["teams"] else "")
  r={"playerId":p["playerId"],"player":p["name"],"position":p["position"],"team":team,"season":season};r.update(agg(gs));rows.append(r)
  buckets={}
  for g in gs:
   o=val(g,"opponentAbbrev","opponent")
   if o:buckets.setdefault(o,[]).append(g)
  for o,og in buckets.items():
   v={"playerId":p["playerId"],"player":p["name"],"position":p["position"],"team":team,"opponent":o,"season":season};v.update(agg(og));versus.append(v)
with open("data/player_stats.json","w") as f:json.dump({"updated":datetime.now(timezone.utc).isoformat(),"seasons":D["seasons"],"players":rows,"versus":versus},f,separators=(",",":"))
print("Built",len(rows),"player-season rows and",len(versus),"opponent splits")
