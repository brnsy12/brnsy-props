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
MAP={"goals":("goals",),"assists":("assists",),"points":("points",),"shots":("shots","shotsOnGoal"),"hits":("hits",),"blocks":("blockedShots","blocks"),"ppp":("powerPlayPoints",),"saves":("saves",),"goalsAgainst":("goalsAgainst",)}
def agg(gs):
 a={"gp":len(gs),**{k:0 for k in MAP}}
 for g in gs:
  for out,keys in MAP.items():a[out]+=n(val(g,*keys))
 if a["gp"]:
  for k in MAP:a[k+"PerGame"]=round(a[k]/a["gp"],2)
 return a
def compact(g):
 return {"date":g.get("gameDate") or "","opponent":val(g,"opponentAbbrev","opponent"),"homeRoad":g.get("homeRoadFlag") or "","goals":n(val(g,"goals")),"assists":n(val(g,"assists")),"points":n(val(g,"points")),"shots":n(val(g,"shots","shotsOnGoal")),"hits":n(val(g,"hits")),"blocks":n(val(g,"blockedShots","blocks")),"ppp":n(val(g,"powerPlayPoints")),"saves":n(val(g,"saves")),"goalsAgainst":n(val(g,"goalsAgainst"))}
rows=[];versus=[];games={}
for p in D["players"]:
 pid=str(p["playerId"]);games[pid]={}
 for season in D["seasons"]:
  gs=D["logs"].get(pid,{}).get(season,[])
  if not gs:continue
  games[pid][season]=[compact(g) for g in gs]
  team=val(gs[0],"teamAbbrev","team") or (p["teams"][-1] if p["teams"] else "")
  r={"playerId":p["playerId"],"player":p["name"],"position":p["position"],"team":team,"season":season};r.update(agg(gs));rows.append(r)
  buckets={}
  for g in gs:
   o=val(g,"opponentAbbrev","opponent")
   if o:buckets.setdefault(o,[]).append(g)
  for o,og in buckets.items():
   v={"playerId":p["playerId"],"player":p["name"],"position":p["position"],"team":team,"opponent":o,"season":season};v.update(agg(og));versus.append(v)
with open("data/player_stats.json","w") as f:json.dump({"updated":datetime.now(timezone.utc).isoformat(),"seasons":D["seasons"],"players":rows,"versus":versus,"games":games},f,separators=(",",":"))
print("Built",len(rows),"player-season rows,",len(versus),"opponent splits and",sum(len(s) for p in games.values() for s in p.values()),"game logs")
