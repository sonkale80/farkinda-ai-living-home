import json, sqlite3, datetime, math, os, secrets
import mcp
from planner import build_plan
from simulator import simulate
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
ROOT=Path(__file__).parent
DB=ROOT/'home.db'
def connect():
 c=sqlite3.connect(DB);c.row_factory=sqlite3.Row;return c
def init():
 with connect() as c:
  c.executescript('CREATE TABLE IF NOT EXISTS inventory(id INTEGER PRIMARY KEY,name TEXT UNIQUE,qty REAL,unit TEXT,daily REAL,expires TEXT);CREATE TABLE IF NOT EXISTS pets(id INTEGER PRIMARY KEY,name TEXT UNIQUE,baseline REAL);CREATE TABLE IF NOT EXISTS meals(id INTEGER PRIMARY KEY,pet TEXT,grams REAL,day TEXT);CREATE TABLE IF NOT EXISTS actions(id INTEGER PRIMARY KEY,kind TEXT,detail TEXT,status TEXT);CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY,kind TEXT,subject TEXT,quantity REAL,created_at TEXT);')
  if not c.execute('SELECT count(*) FROM inventory').fetchone()[0]:
   c.executemany('INSERT INTO inventory(name,qty,unit,daily,expires) VALUES(?,?,?,?,?)',[('Köpek maması',1200,'g',300,None),('Ispanak',450,'g',150,(datetime.date.today()+datetime.timedelta(days=2)).isoformat()),('Süt',900,'ml',300,(datetime.date.today()+datetime.timedelta(days=5)).isoformat())])
  if not c.execute('SELECT count(*) FROM pets').fetchone()[0]:
   c.execute('INSERT INTO pets(name,baseline) VALUES(?,?)',('Pamuk',300))
   for i,grams in enumerate([190,180,160]):c.execute('INSERT INTO meals(pet,grams,day) VALUES(?,?,?)',('Pamuk',grams,(datetime.date.today()-datetime.timedelta(days=2-i)).isoformat()))
def analyze():
 today=datetime.date.today();alerts=[]
 with connect() as c:
  items=[dict(r) for r in c.execute('SELECT * FROM inventory')]
  pets=[dict(r) for r in c.execute('SELECT * FROM pets')]
  for p in pets:
   meals=[r['grams'] for r in c.execute('SELECT grams FROM meals WHERE pet=? ORDER BY id DESC LIMIT 3',(p['name'],))]
   if len(meals)==3 and sum(meals)/3 < p['baseline']*.8:
    alerts.append(dict(type='pet',level='attention',title=f"{p['name']} daha az mama tüketiyor",reason=f"Son 3 kayıt ortalaması {sum(meals)/3:.0f} g; olağan referans {p['baseline']:.0f} g.",suggestion='Ölçümleri doğrula, iştah ve davranışı gözlemle; değişim sürerse veterinerle görüş.',confidence='recorded'))
  for it in items:
   if it['daily']>0 and it['qty']/it['daily']<=5:
    alerts.append(dict(type='stock',level='attention',title=f"{it['name']} azalıyor",reason=f"Kalan {it['qty']:g} {it['unit']}; yaklaşık {it['qty']/it['daily']:.1f} gün.",suggestion='Alışveriş listesine eklemeyi değerlendir.',confidence='estimated'))
   if it['expires']:
    days=(datetime.date.fromisoformat(it['expires'])-today).days
    if days<=3:alerts.append(dict(type='waste',level='attention',title=f"{it['name']} için tarih yaklaşıyor",reason=f"Kayıtlı son tüketim tarihine {days} gün kaldı.",suggestion='Ürün güvenliyse zamanında kullan; son tüketim tarihini aşmış riskli gıdaları tüketme.',confidence='recorded'))
 return {'inventory':items,'pets':pets,'alerts':alerts,'note':'Demo verileri; tıbbi değerlendirme değildir.'}
def inventory_forecast():
 today=datetime.date.today();out=[]
 with connect() as c:
  for item in c.execute("SELECT name,qty,unit,daily,expires FROM inventory ORDER BY name"):
   days=round(item["qty"]/item["daily"],1) if item["daily"] and item["daily"]>0 else None
   expiry=(datetime.date.fromisoformat(item["expires"])-today).days if item["expires"] else None
   out.append({"name":item["name"],"quantity":item["qty"],"unit":item["unit"],"days_of_supply":days,"days_to_expiry":expiry,"confidence":"estimated from manually entered consumption"})
 return {"items":out,"sensor_connected":False}
def record_meal(body):
 pet=str(body['pet']); grams=float(body['grams'])
 if not math.isfinite(grams) or not 0<=grams<=5000:raise ValueError('Invalid grams')
 if body.get('confirmed') is not True:raise ValueError('Explicit confirmation required')
 with connect() as c:
  if not c.execute('SELECT 1 FROM pets WHERE name=?',(pet,)).fetchone():raise ValueError('Unknown pet')
  c.execute('INSERT INTO meals(pet,grams,day) VALUES(?,?,?)',(pet,grams,datetime.date.today().isoformat()))
 return {'ok':True,'note':'Recorded; consumption is user-reported, not sensor measured.'}
def prepare_action(body):
 kind=body['kind']
 if kind not in ('shopping','pet-check','meal-plan'):raise ValueError('Invalid action')
 return {'kind':kind,'status':'proposed','requires_user_approval':True,'external_action_executed':False}
def add_event(body):
 kind=body.get('kind');subject=body.get('subject');quantity=body.get('quantity')
 if kind not in ('consume','restock') or not isinstance(subject,str) or not subject.strip():raise ValueError('Invalid event')
 if isinstance(quantity,bool):raise ValueError('Invalid quantity')
 try:quantity=float(quantity)
 except (ValueError,TypeError):raise ValueError('Invalid quantity')
 if not math.isfinite(quantity) or quantity<=0 or quantity>100000:raise ValueError('Invalid quantity')
 if body.get('confirmed') is not True:raise ValueError('Explicit confirmation required')
 with connect() as c:
  row=c.execute('SELECT qty FROM inventory WHERE name=?',(subject,)).fetchone()
  if row is None:raise ValueError('Unknown inventory item')
  new_qty=row['qty']+quantity*(1 if kind=='restock' else -1)
  if new_qty<0:raise ValueError('Insufficient stock')
  c.execute('UPDATE inventory SET qty=? WHERE name=?',(new_qty,subject))
  cur=c.execute('INSERT INTO events(kind,subject,quantity,created_at) VALUES(?,?,?,?)',(kind,subject,quantity,datetime.datetime.now(datetime.timezone.utc).isoformat()))
 return {'ok':True,'event_id':cur.lastrowid,'new_quantity':new_qty,'unit':'recorded','sensor_connected':False}
def history():
 with connect() as c:
  return {'events':[dict(r) for r in c.execute('SELECT * FROM events ORDER BY id DESC LIMIT 50')], 'actions':[dict(r) for r in c.execute('SELECT * FROM actions ORDER BY id DESC LIMIT 50')]}
class Handler(BaseHTTPRequestHandler):
 def authorized(self):
  token=os.environ.get('FARKINDA_WRITE_TOKEN','')
  return not token or secrets.compare_digest(self.headers.get('X-Farkinda-Token',''),token)
 def do_OPTIONS(self):
  self.send_response(204);self.send_header('Allow','GET, POST, OPTIONS');self.send_header('Access-Control-Allow-Methods','GET, POST, OPTIONS');self.send_header('Access-Control-Allow-Headers','Content-Type, Accept, MCP-Protocol-Version, X-Farkinda-Token');self.end_headers()

 def send(self,obj,status=200):
  data=json.dumps(obj,ensure_ascii=False).encode();self.send_response(status);self.send_header('Content-Type','application/json; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
 def do_GET(self):
  if self.path=='/api/health':return self.send({'ok':True,'service':'farkinda-ai','version':'2.0','alexa_connected':False,'sensors_connected':False})
  if self.path=='/api/history':return self.send(history())
  if self.path=='/api/status':return self.send(analyze())
  if self.path=='/api/forecast':return self.send(inventory_forecast())
  if self.path.startswith('/api/plan'):
   from urllib.parse import urlparse, parse_qs
   q=parse_qs(urlparse(self.path).query)
   return self.send(build_plan(analyze(),q.get('away',['0'])[0]=='1'))
  if self.path=='/mcp':return self.send({'error':'Use POST for MCP JSON-RPC'},405)
  if self.path=='/':
   data=(ROOT/'index.html').read_bytes();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.end_headers();return self.wfile.write(data)
  return self.send({'error':'not found'},404)
 def do_POST(self):
  try:n=int(self.headers.get('Content-Length','0'))
  except ValueError:return self.send({'error':'invalid content length'},400)
  if n<=0:return self.send({'error':'empty body'},400)
  if n>10000:return self.send({'error':'too large'},413)
  try:body=json.loads(self.rfile.read(n))
  except Exception:return self.send({'error':'invalid JSON'},400)
  if self.path=='/mcp':
   if not self.authorized() and isinstance(body,dict) and body.get('method')=='tools/call' and body.get('params',{}).get('name') in ('record_pet_meal',):return self.send({'error':'Unauthorized write'},401)
   response=mcp.handle(body,analyze,record_meal,prepare_action,lambda args:build_plan(analyze(),args.get("away_tomorrow",False)),inventory_forecast)
   if response is None:
    self.send_response(202);self.end_headers();return
   return self.send(response)
  if self.path=='/api/simulate':
   try:
    if not isinstance(body,dict):raise ValueError('Invalid payload')
    return self.send(simulate(body.get('utterance',''),analyze(),inventory_forecast(),body.get('away_tomorrow') is True))
   except ValueError as exc:return self.send({'error':str(exc)},400)
  if self.path=='/api/event':
   if not self.authorized():return self.send({'error':'Unauthorized write'},401)
   try:return self.send(add_event(body))
   except (ValueError,TypeError,AttributeError) as exc:return self.send({'error':str(exc)},400)
  if self.path=='/api/meal':
   if not self.authorized():return self.send({'error':'Unauthorized write'},401)
   try:
    pet=str(body['pet']);grams=float(body['grams'])
    if not math.isfinite(grams) or not 0<=grams<=5000 or body.get('confirmed') is not True:raise ValueError('Invalid meal or missing confirmation')
    with connect() as c:
     if not c.execute('SELECT 1 FROM pets WHERE name=?',(pet,)).fetchone():raise ValueError('Unknown pet')
     c.execute('INSERT INTO meals(pet,grams,day) VALUES(?,?,?)',(pet,grams,datetime.date.today().isoformat()))
    return self.send({'ok':True,'status':analyze()})
   except (ValueError,TypeError,KeyError,AssertionError):return self.send({'error':'invalid pet or grams'},400)
  if self.path=='/api/action':
   if not self.authorized():return self.send({'error':'Unauthorized write'},401)
   if body.get('confirmed') is not True:return self.send({'error':'Explicit confirmation required'},400)
   kind=str(body.get('kind',''))
   if kind not in ('shopping','pet-check','meal-plan'):return self.send({'error':'invalid kind'},400)
   with connect() as c:
    cur=c.execute('INSERT INTO actions(kind,detail,status) VALUES(?,?,?)',(kind,'User approved demo action','approved'))
    return self.send({'ok':True,'action_id':cur.lastrowid,'note':'Recorded locally; no external action executed.'})
  return self.send({'error':'not found'},404)
if __name__=='__main__':
 init();port=int(os.environ.get('FARKINDA_PORT','8765'));print(f'Open http://127.0.0.1:{port}');ThreadingHTTPServer(('127.0.0.1',port),Handler).serve_forever()
