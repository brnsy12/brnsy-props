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
for e in D:
 for oid,o in (e.get("odds") or {}).items():
  market=name(o.get("statID")); pid=o.get("statEntityID"); side=(o.get("sideID") or "").lower()
  if not market or pid in (None,"all","home","away") or side not in ("over","under"):continue
  player=str(pid)
  for c in ("players","participants","entities"):
   z=e.get(c,{})
   if isinstance(z,dict) and pid in z: player=z[pid].get("name") or z[pid].get("displayName") or player
  for book,b in (o.get("byBookmaker") or {}).items():
   if not isinstance(b,dict) or b.get("available") is False:continue
   line=n(b.get("overUnder",b.get("line",o.get("bookOverUnder",o.get("overUnder"))))); price=a(b.get("odds",b.get("bookOdds",o.get("bookOdds"))))
   if line is None or price is None:continue
   R.append({"id":f"{e.get('eventID')}|{oid}|{book}","gameId":e.get("eventID"),"player":player,"playerId":pid,"team":o.get("teamID") or "","opponent":"","market":market,"side":side.title(),"line":line,"odds":price,"book":book,"openOdds":a(b.get("openOdds")),"closeOdds":a(b.get("closeOdds")),"openLine":n(b.get("openOverUnder")),"closeLine":n(b.get("closeOverUnder")),"l5":None,"l10":None,"l20":None,"season":None,"gap":None,"result":n(o.get("score"))})
json.dump({"mode":"live","updated":datetime.now(timezone.utc).isoformat(),"props":R},open("data/props.json","w"),indent=2)
print("Processed",len(R),"prop book-lines")
