from flask import Flask, render_template_string, request, jsonify, redirect, send_from_directory
import json, os, random
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs('uploads', exist_ok=True)

SYRIATEL = "23659879"
ADMIN_PASS = "09627300780962"
DOLLAR_RATE = 13500
PRICE_WA = 5
PRICE_TG = 4

DB_ORDERS = "orders.json"
DB_CHATS = "chats.json"
DB_USERS = "users.json"
DB_NOTIF = "notifications.json"

def load(f):
    if not os.path.exists(f): return {}
    with open(f, "r") as fp: return json.load(fp)

def save(f, data):
    with open(f, "w") as fp: json.dump(data, fp)

def get_uid():
    while True:
        uid = str(random.randint(10000000, 99999999))
        users = load(DB_USERS)
        if uid not in users:
            users[uid] = {"balance": 0, "created": datetime.now().strftime("%Y-%m-%d %H:%M")}
            save(DB_USERS, users)
            return uid

WELCOME = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SMSGate ⚡</title>
    <style>
        :root{--bg:#0d1117;--card:#161b22;--text:#e6edf3;--blue:#58a6ff;--gold:#d2991d}
        *{margin:0;padding:0;box-sizing:border-box}
        body{background:linear-gradient(135deg,#0d1117,#1a0a2e,#0a1a2e,#1a0a2e,#0d1117);background-size:400% 400%;animation:bgMove 10s ease infinite;color:var(--text);font-family:'Segoe UI',sans-serif;min-height:100vh;display:flex;justify-content:center;align-items:center;overflow:hidden}
        @keyframes bgMove{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
        .stars{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:0}
        .star{position:absolute;background:#fff;border-radius:50%;animation:twinkle 3s infinite}
        @keyframes twinkle{0%,100%{opacity:0.2;transform:scale(1)}50%{opacity:1;transform:scale(1.5)}}
        .welcome-box{position:relative;z-index:1;text-align:center;padding:50px 30px;max-width:550px;animation:pop 0.6s}
        @keyframes pop{0%{transform:scale(0.8);opacity:0}100%{transform:scale(1);opacity:1}}
        .welcome-box .logo{font-size:5em;animation:bounce 2s infinite}
        @keyframes bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-20px)}}
        .welcome-box h1{font-size:3em;background:linear-gradient(135deg,#58a6ff,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin:15px 0}
        .welcome-box .subtitle{font-size:1.2em;color:#8b949e;margin-bottom:40px;line-height:1.8}
        .choice-card{background:var(--card);border-radius:20px;padding:25px;margin:20px 0;border:1px solid #30363d;cursor:pointer;transition:0.3s;text-decoration:none;display:block;color:var(--text)}
        .choice-card:hover{transform:translateY(-5px);box-shadow:0 0 40px rgba(88,166,255,0.4);border-color:var(--blue)}
        .choice-card .icon{font-size:3em}
        .choice-card h2{font-size:1.5em;margin:10px 0;color:var(--blue)}
        .choice-card p{color:#8b949e;font-size:1em}
        .choice-card.visa:hover{box-shadow:0 0 40px rgba(210,153,29,0.4);border-color:var(--gold)}
        .choice-card.visa h2{color:var(--gold)}
    </style>
</head>
<body>
    <div class="stars" id="starsContainer"></div>
    <div class="welcome-box">
        <div class="logo">⚡</div>
        <h1>SMSGate</h1>
        <p class="subtitle">نحن هنا لخدمتك! ماذا تحتاج اليوم؟<br>اختر الخدمة اللي تناسبك وابدأ فوراً! 🔥</p>
        <a href="/numbers" class="choice-card">
            <div class="icon">📱</div>
            <h2>شراء أرقام تفعيل</h2>
            <p>أرقام افتراضية لتفعيل واتساب وتلجرام</p>
        </a>
        <a href="/visa" class="choice-card visa">
            <div class="icon">💳</div>
            <h2>شراء بطاقات Visa</h2>
            <p>بطاقات للشراء أونلاين بكل سهولة</p>
        </a>
    </div>
    <script>
        for(let i=0;i<70;i++){const s=document.createElement("div");s.className="star";s.style.left=Math.random()*100+"%";s.style.top=Math.random()*100+"%";s.style.width=Math.random()*3+1+"px";s.style.height=s.style.width;s.style.animationDelay=Math.random()*3+"s";document.getElementById("starsContainer").appendChild(s)}
    </script>
</body>
</html>
"""

HTML = r"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SMSGate - أرقام ⚡</title>
    <style>
        :root{--bg:#0d1117;--card:#161b22;--text:#e6edf3;--blue:#58a6ff;--green:#3fb950;--gold:#d2991d;--red:#f85149;--msg-user:#1a5c2a;--msg-admin:#1a3a5c}
        *{margin:0;padding:0;box-sizing:border-box}
        body{background:linear-gradient(135deg,#0d1117,#1a0a2e,#0a1a2e,#1a0a2e,#0d1117);background-size:400% 400%;animation:bgMove 10s ease infinite;color:var(--text);font-family:'Segoe UI',sans-serif;min-height:100vh;overflow-x:hidden}
        @keyframes bgMove{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
        .lightning{position:fixed;width:2px;background:linear-gradient(to bottom,#58a6ff,transparent);animation:strike 4s infinite;opacity:0;z-index:0;pointer-events:none}
        @keyframes strike{0%,92%,100%{opacity:0;transform:scaleY(0)}93%{opacity:1;transform:scaleY(1)}94%{opacity:0.5}95%{opacity:1;transform:scaleY(1.1)}96%{opacity:0}}
        .rocket{position:fixed;font-size:50px;z-index:10;pointer-events:none;animation:fly 6s ease-in-out infinite}
        @keyframes fly{0%{left:-100px;top:15%;opacity:0}10%{opacity:1}90%{opacity:1}100%{left:110%;top:70%;opacity:0}}
        .container{max-width:700px;margin:0 auto;padding:20px;position:relative;z-index:1}
        .header{text-align:center;padding:40px 20px 20px}
        .logo{font-size:70px;animation:bounce 2s infinite}
        @keyframes bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-20px)}}
        .header h1{font-size:3.5em;font-weight:900;background:linear-gradient(135deg,#58a6ff,#8b5cf6);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
        .id-bar{background:var(--card);border-radius:12px;padding:10px 20px;text-align:center;border:1px solid var(--blue);margin:10px 0;font-size:1.1em}
        .balance-bar{background:var(--card);border-radius:12px;padding:12px 20px;text-align:center;border:1px solid var(--gold);margin:10px 0;font-size:1.2em}
        .notif-bar{background:var(--card);border-radius:12px;padding:10px 20px;text-align:center;border:1px solid var(--green);margin:10px 0;cursor:pointer;position:relative}
        .notif-dot{position:absolute;top:8px;right:15px;width:12px;height:12px;background:var(--red);border-radius:50%;display:none}
        .card{background:var(--card);border-radius:16px;padding:25px;text-align:center;border:1px solid #30363d;margin:15px 0}
        select,input,textarea{width:100%;padding:14px;margin:8px 0;border-radius:10px;border:1px solid #30363d;background:var(--bg);color:var(--text);font-size:1em}
        .btn{width:100%;padding:18px;border:none;border-radius:14px;font-size:1.2em;font-weight:700;cursor:pointer;color:#fff;margin:8px 0;transition:0.3s}
        .btn:hover{box-shadow:0 0 30px rgba(88,166,255,0.6)!important;transform:scale(1.03)!important}
        .btn-primary{background:linear-gradient(135deg,#1a6b9c,#58a6ff)}
        .btn-gold{background:linear-gradient(135deg,#9a6b00,#d2991d)}
        .btn-green{background:#25D366}
        .grid2{display:grid;grid-template-columns:1fr 1fr;gap:15px}
        .mode-btn{position:fixed;top:20px;right:20px;width:50px;height:50px;border-radius:50%;border:2px solid var(--blue);background:var(--card);color:var(--text);font-size:1.4em;cursor:pointer;z-index:100}
        .modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.85);z-index:200;justify-content:center;align-items:center}
        .modal-content{background:var(--card);border-radius:20px;padding:30px;max-width:500px;width:95%;text-align:center}
        .chat-box{background:var(--card);border-radius:20px;padding:20px;height:350px;overflow-y:auto;margin:15px 0;border:1px solid #30363d;display:flex;flex-direction:column;gap:10px}
        .msg{max-width:80%;padding:12px 16px;border-radius:15px;word-wrap:break-word;animation:pop .3s}
        @keyframes pop{0%{transform:scale(.8);opacity:0}100%{transform:scale(1);opacity:1}}
        .msg-user{align-self:flex-end;background:var(--msg-user);text-align:right;border-bottom-right-radius:5px}
        .msg-admin{align-self:flex-start;background:var(--msg-admin);text-align:left;border-bottom-left-radius:5px}
        .msg-name{font-size:0.8em;font-weight:bold;margin-bottom:5px}
        .msg-time{font-size:0.7em;color:#8b949e;margin-top:5px}
        .chat-input{display:flex;gap:10px}
        .chat-input input{flex:1;margin:0}
        .chat-input button{width:auto;padding:14px 20px;margin:0}
        .notif-item{padding:15px;border-radius:10px;margin:8px 0;text-align:right}
        .notif-accepted{background:#0d3320;border:1px solid var(--green)}
        .notif-rejected{background:#330d0d;border:1px solid var(--red)}
        .notif-pending{background:#332a0d;border:1px solid var(--gold)}
        .alert-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.85);z-index:9999;display:flex;justify-content:center;align-items:center}
        .alert-box{background:linear-gradient(145deg,#1a1a2e,#16213e);border:2px solid #58a6ff;border-radius:20px;padding:30px;text-align:center;max-width:400px;width:90%;box-shadow:0 0 40px rgba(88,166,255,0.4),0 0 80px rgba(88,166,255,0.2);animation:glow 2s infinite;color:#e6edf3}
        @keyframes glow{0%,100%{box-shadow:0 0 40px rgba(88,166,255,0.4),0 0 80px rgba(88,166,255,0.2)}50%{box-shadow:0 0 60px rgba(88,166,255,0.6),0 0 100px rgba(88,166,255,0.4)}}
        .alert-icon{font-size:3em;margin-bottom:15px}
        .alert-msg{font-size:1.3em;margin:10px 0;line-height:1.6}
        .alert-btn{background:linear-gradient(135deg,#1a6b9c,#58a6ff);border:none;padding:12px 30px;border-radius:25px;color:#fff;font-size:1.1em;cursor:pointer;margin-top:15px}
        .back-link{display:block;text-align:center;color:var(--blue);margin-top:20px;text-decoration:none;font-size:1em}
    </style>
</head>
<body>
    <div id="lightningContainer"></div>
    <div class="rocket" id="rocketShip">🚀</div>
    <button class="mode-btn" onclick="toggleMode()" id="modeToggle">☀️</button>
    <div class="container">
        <div class="header"><div class="logo">⚡</div><h1>SMSGate</h1><p>🔐 أرقام حقيقية لتفعيل واتساب وتلجرام</p></div>
        <div class="id-bar">🆔 معرفك: <b id="myId">---</b></div>
        <div class="balance-bar">💰 رصيدك: <span id="balanceDisplay">$0.00</span></div>
        <div class="notif-bar" onclick="openNotifications()">🔔 الإشعارات <span class="notif-dot" id="notifDot"></span></div>
        <div class="grid2">
            <div class="card"><label>🌍 الدولة</label><select id="country"><option value="syria">🇸🇾 سوريا</option><option value="usa">🇺🇸 أمريكا</option><option value="uk">🇬🇧 بريطانيا</option><option value="turkey">🇹🇷 تركيا</option><option value="egypt">🇪🇬 مصر</option><option value="iraq">🇮🇶 العراق</option><option value="saudi">🇸🇦 السعودية</option><option value="jordan">🇯🇴 الأردن</option></select></div>
            <div class="card"><label>📲 التطبيق</label><select id="service" onchange="updatePrice()"><option value="whatsapp">واتساب (5$)</option><option value="telegram">تلجرام (4$)</option></select></div>
        </div>
        <button class="btn btn-primary" onclick="submitOrder()">⚡ احصل على رقم الآن</button>
        <div class="grid2">
            <button class="btn btn-gold" onclick="openDeposit()">💳 شحن رصيد</button>
            <button class="btn btn-green" onclick="openChat()">💬 الدردشة مع الدعم</button>
        </div>
        <a href="/" class="back-link">🔙 رجوع للصفحة الرئيسية</a>
    </div>
    <div class="modal" id="notifModal"><div class="modal-content"><h2>🔔 الإشعارات</h2><div id="notifList" style="max-height:400px;overflow-y:auto;"></div><button class="btn" style="background:#6e7681;margin-top:15px;" onclick="closeNotifications()">إغلاق</button></div></div>
    <div class="modal" id="depositModal"><div class="modal-content"><h2>💳 شحن رصيد</h2><p style="color:var(--gold);">🏦 سيريتيل كاش: {{ syriatel }}</p><p style="color:#8b949e;">💱 1$ = {{ rate }} ل.س</p><input id="depAmount" type="number" placeholder="المبلغ بالدولار"><p>المبلغ بالليرة: <span id="liraspan">0</span> ل.س</p><p>📸 صورة إثبات التحويل:</p><input type="file" id="depProof" accept="image/*"><button class="btn btn-gold" onclick="submitDeposit()">🚀 إرسال</button><button class="btn" style="background:#6e7681;" onclick="closeDeposit()">إلغاء</button></div></div>
    <div class="modal" id="chatModal"><div class="modal-content" style="max-width:600px;"><h2>💬 الدردشة مع الدعم</h2><div class="chat-box" id="chatBox"></div><div class="chat-input"><input id="chatInput" placeholder="اكتب رسالتك..."><button class="btn btn-primary" onclick="sendChat()" style="width:auto;">📨</button></div><button class="btn" style="background:#6e7681;margin-top:10px;" onclick="closeChat()">إغلاق</button></div></div>
    <script>
        const RATE={{ rate }};
        let uid=localStorage.getItem('sms_uid');
        if(!uid){uid=Math.floor(10000000+Math.random()*90000000);localStorage.setItem('sms_uid',uid)}
        document.getElementById('myId').textContent=uid;
        function showAlert(msg,icon){icon=icon||'⚡';let overlay=document.createElement('div');overlay.className='alert-overlay';overlay.innerHTML='<div class="alert-box"><div class="alert-icon">'+icon+'</div><div class="alert-msg">'+msg+'</div><button class="alert-btn" onclick="this.closest(\'.alert-overlay\').remove()">حسناً 👍</button></div>';document.body.appendChild(overlay)}
        function clickFx(){try{const a=new AudioContext(),o=a.createOscillator(),g=a.createGain();o.connect(g);g.connect(a.destination);o.frequency.value=900;o.type='sine';g.gain.setValueAtTime(0.15,a.currentTime);g.gain.exponentialRampToValueAtTime(0.001,a.currentTime+0.08);o.start();o.stop(a.currentTime+0.08)}catch(e){}}
        document.addEventListener('click',e=>{if(['BUTTON','A','SELECT'].includes(e.target.tagName))clickFx()});
        const lc2=document.getElementById('lightningContainer');
        for(let i=0;i<8;i++){const b=document.createElement('div');b.className='lightning';b.style.left=(Math.random()*90+5)+'%';b.style.height=(Math.random()*50+30)+'%';b.style.animationDelay=(Math.random()*5)+'s';lc2.appendChild(b)}
        for(let i=0;i<70;i++){const s=document.createElement("div");s.className="star";s.style.left=Math.random()*100+"%";s.style.top=Math.random()*100+"%";s.style.width=Math.random()*3+1+"px";s.style.height=s.style.width;s.style.animationDelay=Math.random()*3+"s";document.body.appendChild(s)}
        const ship=document.getElementById('rocketShip');
        function launch(){ship.style.animation='none';ship.offsetHeight;ship.style.animation='fly 6s ease-in-out';setTimeout(launch,6000)}launch();
        let dark=true;
        function toggleMode(){dark=!dark;const r=document.documentElement;r.style.setProperty('--bg',dark?'#0d1117':'#f6f8fa');r.style.setProperty('--card',dark?'#161b22':'#fff');r.style.setProperty('--text',dark?'#e6edf3':'#24292f');document.getElementById('modeToggle').textContent=dark?'☀️':'🌙'}
        let price=5;
        function updatePrice(){price=document.getElementById('service').value==='whatsapp'?5:4}
        document.getElementById('depAmount').addEventListener('input',function(){document.getElementById('liraspan').textContent=(this.value*RATE).toLocaleString()})
        async function loadBalance(){const r=await fetch(`/api/balance?uid=${uid}`);const d=await r.json();document.getElementById('balanceDisplay').textContent='$'+d.balance.toFixed(2)}
        async function checkNotif(){const r=await fetch(`/api/notifications?uid=${uid}`);const d=await r.json();document.getElementById('notifDot').style.display=d.unread?'block':'none'}
        async function submitOrder(){await loadBalance();if(parseFloat(document.getElementById('balanceDisplay').textContent.replace('$',''))<price){showAlert('❌ عذراً، ليس هنالك رصيد كافٍ لإتمام عملية الشراء','💰');return}const b=event.target;b.textContent='⏳';b.disabled=true;const r=await fetch(`/api/order?uid=${uid}&country=${document.getElementById('country').value}&service=${document.getElementById('service').value}&price=${price}`);const d=await r.json();if(d.ok){await loadBalance();showAlert('✅ تم تقديم طلبك!<br><br>انتظر الموافقة 🔔','🎉')}else{showAlert('❌ '+d.error,'⚠️')}b.textContent='⚡ احصل على رقم الآن';b.disabled=false}
        function openDeposit(){document.getElementById('depositModal').style.display='flex'}
        function closeDeposit(){document.getElementById('depositModal').style.display='none'}
        function openChat(){document.getElementById('chatModal').style.display='flex';loadChat()}
        function closeChat(){document.getElementById('chatModal').style.display='none'}
        function openNotifications(){document.getElementById('notifModal').style.display='flex';loadNotifications()}
        function closeNotifications(){document.getElementById('notifModal').style.display='none';checkNotif()}
        async function loadNotifications(){const r=await fetch(`/api/notifications?uid=${uid}`);const d=await r.json();const list=document.getElementById('notifList');list.innerHTML=d.notifications.length?d.notifications.reverse().map(n=>`<div class="notif-item notif-${n.status}"><b>طلب #${n.oid}</b><br>${n.status==='accepted'?'✅ تم القبول: '+n.number+' | 🎯 '+n.code:n.status==='rejected'?'❌ تم الرفض':'⏳ قيد الانتظار'}</div>`).join(''):'<p>لا توجد إشعارات</p>';fetch(`/api/notifications/read?uid=${uid}`)}
        async function loadChat(){const r=await fetch(`/api/chat?uid=${uid}`);const d=await r.json();const box=document.getElementById('chatBox');box.innerHTML='';d.messages.forEach(m=>{const div=document.createElement('div');div.className='msg '+(m.from=='user'?'msg-user':'msg-admin');div.innerHTML=`<div class="msg-name">${m.from=='user'?'أنت':'📢 إدارة الموقع'}</div>${m.text}<div class="msg-time">${m.time}</div>`;box.appendChild(div)});box.scrollTop=box.scrollHeight}
        async function sendChat(){const text=document.getElementById('chatInput').value;if(!text)return;await fetch('/api/chat/send',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({uid:uid,text:text})});document.getElementById('chatInput').value='';loadChat()}
        async function submitDeposit(){const amt=document.getElementById('depAmount').value;const file=document.getElementById('depProof').files[0];if(!amt||!file){showAlert('⚠️ املأ جميع الحقول','📋');return}const fd=new FormData();fd.append('uid',uid);fd.append('amount',amt);fd.append('proof',file);await fetch('/api/deposit',{method:'POST',body:fd});showAlert('✅ تم الإرسال!','📤');closeDeposit()}
    </script>
</body>
</html>
"""

VISA = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SMSGate - Visa 💳</title>
    <style>
        :root{--bg:#0d1117;--card:#161b22;--text:#e6edf3;--blue:#58a6ff;--gold:#d2991d;--green:#3fb950}
        *{margin:0;padding:0;box-sizing:border-box}
        body{background:linear-gradient(135deg,#0d1117,#1a0a2e,#0a1a2e,#1a0a2e,#0d1117);background-size:400% 400%;animation:bgMove 10s ease infinite;color:var(--text);font-family:'Segoe UI',sans-serif;min-height:100vh;overflow-x:hidden}
        @keyframes bgMove{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
        .container{max-width:700px;margin:0 auto;padding:20px;position:relative;z-index:1}
        .header{text-align:center;padding:40px 20px 20px}
        .header .logo{font-size:4em}
        .header h1{font-size:3em;font-weight:900;background:linear-gradient(135deg,#d2991d,#f0c040);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
        .card-visa{background:var(--card);border-radius:20px;padding:30px;text-align:center;border:2px solid var(--gold);margin:20px 0;animation:pop 0.5s}
        @keyframes pop{0%{transform:scale(0.8);opacity:0}100%{transform:scale(1);opacity:1}}
        .card-visa h2{color:var(--gold);font-size:2em;margin:10px 0}
        .card-visa .price{font-size:2.5em;color:var(--gold);font-weight:900;margin:15px 0}
        .card-visa .price span{font-size:0.5em;color:#8b949e}
        .btn{width:100%;padding:18px;border:none;border-radius:14px;font-size:1.2em;font-weight:700;cursor:pointer;color:#fff;margin:8px 0;transition:0.3s}
        .btn:hover{box-shadow:0 0 30px rgba(210,153,29,0.6)!important;transform:scale(1.03)!important}
        .btn-gold{background:linear-gradient(135deg,#9a6b00,#d2991d)}
        .back-link{display:block;text-align:center;color:var(--gold);margin-top:20px;text-decoration:none;font-size:1.1em}
        .alert-overlay{position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.85);z-index:9999;display:flex;justify-content:center;align-items:center}
        .alert-box{background:linear-gradient(145deg,#1a1a2e,#16213e);border:2px solid var(--gold);border-radius:20px;padding:30px;text-align:center;max-width:400px;width:90%;box-shadow:0 0 40px rgba(210,153,29,0.4);color:#e6edf3}
        .alert-icon{font-size:3em;margin-bottom:15px}
        .alert-msg{font-size:1.3em;margin:10px 0}
        .alert-btn{background:linear-gradient(135deg,#9a6b00,#d2991d);border:none;padding:12px 30px;border-radius:25px;color:#fff;font-size:1.1em;cursor:pointer;margin-top:15px}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">💳</div>
            <h1>Visa Cards</h1>
            <p style="color:#8b949e;font-size:1.2em;">بطاقات فيزا للشراء أونلاين</p>
        </div>
        <div class="card-visa"><h2>💳 بطاقة 10$</h2><div class="price">10$ <span>({{ rate * 10 }} ل.س)</span></div><button class="btn btn-gold" onclick="orderVisa('10$', 10)">🛒 اطلب الآن</button></div>
        <div class="card-visa"><h2>💳 بطاقة 25$</h2><div class="price">25$ <span>({{ rate * 25 }} ل.س)</span></div><button class="btn btn-gold" onclick="orderVisa('25$', 25)">🛒 اطلب الآن</button></div>
        <div class="card-visa"><h2>💳 بطاقة 50$</h2><div class="price">50$ <span>({{ rate * 50 }} ل.س)</span></div><button class="btn btn-gold" onclick="orderVisa('50$', 50)">🛒 اطلب الآن</button></div>
        <div class="card-visa"><h2>💳 بطاقة 100$</h2><div class="price">100$ <span>({{ rate * 100 }} ل.س)</span></div><button class="btn btn-gold" onclick="orderVisa('100$', 100)">🛒 اطلب الآن</button></div>
        <a href="/" class="back-link">🔙 رجوع للصفحة الرئيسية</a>
    </div>
    <script>
        function showAlert(msg,icon){icon=icon||'💳';let overlay=document.createElement('div');overlay.className='alert-overlay';overlay.innerHTML='<div class="alert-box"><div class="alert-icon">'+icon+'</div><div class="alert-msg">'+msg+'</div><button class="alert-btn" onclick="this.closest(\'.alert-overlay\').remove()">حسناً 👍</button></div>';document.body.appendChild(overlay)}
        function orderVisa(name, price){
            let uid=localStorage.getItem('sms_uid');
            if(!uid){uid=Math.floor(10000000+Math.random()*90000000);localStorage.setItem('sms_uid',uid)}
            fetch(`/api/visa_order?uid=${uid}&name=${name}&price=${price}`).then(r=>r.json()).then(d=>{
                if(d.ok){showAlert('✅ تم تقديم طلبك لبطاقة '+name+'!<br><br>انتظر الموافقة 💳','🎉')}
                else{showAlert('❌ '+d.error,'⚠️')}
            });
        }
    </script>
</body>
</html>
"""

ADMIN_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة SMSGate</title>
    <style>
        body{background:#0d1117;color:#e6edf3;font-family:sans-serif;padding:20px}
        .card{background:#161b22;border-radius:16px;padding:25px;margin:15px 0;border:1px solid #30363d}
        input,textarea{width:100%;padding:12px;margin:5px 0;border-radius:10px;border:1px solid #30363d;background:#0d1117;color:#fff;font-size:1em}
        button{padding:15px;background:#58a6ff;border:none;border-radius:10px;color:#fff;font-weight:bold;cursor:pointer;width:100%;margin:5px 0}
        .green{background:#3fb950}.gold{background:#d2991d}.red{background:#f85149}
        .tabs{display:flex;gap
