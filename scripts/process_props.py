import json
from datetime import datetime,timezone
D=json.load(open("data/raw/events.json")).get("data",[]); R=[]
M={"goal":"Goals","assist":"Assists","point":"Points","shot":"Shots on Goal","block":"Blocked Shots","hit":"Hits","power":"Power Play Points","save":"Goalie Saves","against":"Goalie Goals Allowed"}
def n(v):
 try:return float(v)
 except:return None
def a(v):
 try:return int(float(v))
 except:return None
def name(stat):
 s=(stat or "").lower()
 for k,v in M.items():
  if k in s:return v
def team_info(x):
 if not isinstance(x,dict): return "",""
 names=x.get("names") or {}
 label=(names.get("short") or names.get("medium") or names.get("long") or x.get("teamID") or "")
 return str(x.get("teamID") or ""),str(label)
for e in D:
 teams=e.get("teams") or {}
 away_id,away=team_info(teams.get("away"))
 home_id,home=team_info(teams.get("home"))
 matchup=f"{away} @ {home}" if away and home else ""
 players=e.get("players") or {}
 for oid,o in (e.get("odds") or {}).items():
  market=name(o.get("statID")); pid=o.get("statEntityID"); side=(o.get("sideID") or "").lower()
  if not market or pid in (None,"all","home","away") or side not in ("over","under"):continue
  pdata=players.get(pid,{}) if isinstance(players,dict) else {}
  player=pdata.get("name") or pdata.get("displayName") or str(pid)
  team_id=o.get("teamID") or pdata.get("teamID") or ""
  team=away if team_id==away_id else home if team_id==home_id else str(team_id)
  opponent=home if team_id==away_id else away if team_id==home_id else ""
  for book,b in (o.get("byBookmaker") or {}).items():
   if not isinstance(b,dict) or b.get("available") is False:continue
   line=n(b.get("overUnder",b.get("line",o.get("bookOverUnder",o.get("overUnder"))))); price=a(b.get("odds",b.get("bookOdds",o.get("bookOdds"))))
   if line is None or price is None:continue
   R.append({"id":f"{e.get('eventID')}|{oid}|{book}","gameId":e.get("eventID"),"matchup":matchup,"awayTeam":away,"homeTeam":home,"player":player,"playerId":pid,"team":team,"teamId":team_id,"opponent":opponent,"market":market,"side":side.title(),"line":line,"odds":price,"book":book,"openOdds":a(b.get("openOdds")),"closeOdds":a(b.get("closeOdds")),"openLine":n(b.get("openOverUnder")),"closeLine":n(b.get("closeOverUnder")),"l5":None,"l10":None,"l20":None,"season":None,"gap":None,"result":n(o.get("score"))})
json.dump({"mode":"live","updated":datetime.now(timezone.utc).isoformat(),"props":R},open("data/props.json","w"),indent=2)
print("Processed",len(R),"prop book-lines")
print("Matchups:",sorted(set(x["matchup"] for x in R if x["matchup"])))
