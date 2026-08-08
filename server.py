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
"""HTML = r"""
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
"""VISA = """
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
        
        <div class="card-visa">
            <h2>💳 بطاقة 10$</h2>
            <div class="price">10$ <span>({{ rate * 10 }} ل.س)</span></div>
            <button class="btn btn-gold" onclick="orderVisa('10$', 10)">🛒 اطلب الآن</button>
        </div>
        
        <div class="card-visa">
            <h2>💳 بطاقة 25$</h2>
            <div class="price">25$ <span>({{ rate * 25 }} ل.س)</span></div>
            <button class="btn btn-gold" onclick="orderVisa('25$', 25)">🛒 اطلب الآن</button>
        </div>
        
        <div class="card-visa">
            <h2>💳 بطاقة 50$</h2>
            <div class="price">50$ <span>({{ rate * 50 }} ل.س)</span></div>
            <button class="btn btn-gold" onclick="orderVisa('50$', 50)">🛒 اطلب الآن</button>
        </div>
        
        <div class="card-visa">
            <h2>💳 بطاقة 100$</h2>
            <div class="price">100$ <span>({{ rate * 100 }} ل.س)</span></div>
            <button class="btn btn-gold" onclick="orderVisa('100$', 100)">🛒 اطلب الآن</button>
        </div>
        
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
        .tabs{display:flex;gap:10px;margin-bottom:20px;flex-wrap:wrap}
        .tab{padding:10px 20px;background:#161b22;border-radius:10px;cursor:pointer;border:1px solid #30363d}
        .tab.active{background:#58a6ff}
        .section{display:none}
        .section.active{display:block}
        .chat-box{max-height:300px;overflow-y:auto;padding:15px;background:#0d1117;border-radius:10px;margin:10px 0}
        .msg{margin:8px 0;padding:10px;border-radius:10px;max-width:80%}
        .msg-user{background:#1a5c2a;margin-right:auto}
        .msg-admin{background:#1a3a5c;margin-left:auto;text-align:right}
    </style>
</head>
<body>
    <h1>📋 لوحة تحكم SMSGate</h1>
    <div class="tabs">
        <div class="tab active" onclick="showTab('orders')">📝 طلبات الأرقام</div>
        <div class="tab" onclick="showTab('visa')">💳 طلبات Visa</div>
        <div class="tab" onclick="showTab('deposits')">💳 الشحن</div>
        <div class="tab" onclick="showTab('chats')">💬 الدردشات</div>
    </div>
    <div id="orders" class="section active"><h2>📝 طلبات الأرقام</h2>
        {% for o in orders %}
        <div class="card" style="border-color:{% if o.status == 'accepted' %}#3fb950{% elif o.status == 'rejected' %}#f85149{% else %}#d2991d{% endif %};">
            <b>🆔 {{ o.id }}</b> | {{ o.time }}<br>👤 {{ o.uid }} | 🌍 {{ o.country }} | 📲 {{ o.service }} | 💰 {{ o.price }}$
            {% if o.status == 'pending' %}
            <div style="display:flex;gap:10px;">
                <form method="POST" action="/admin/accept" style="flex:1;"><input type="hidden" name="id" value="{{ o.id }}"><input name="number" placeholder="الرقم" required><input name="code" placeholder="الكود" required><button class="green">✅ قبول</button></form>
                <form method="POST" action="/admin/reject" style="flex:1;"><input type="hidden" name="id" value="{{ o.id }}"><button class="red">❌ رفض</button></form>
            </div>
            {% elif o.status == 'accepted' %}<p class="green">✅ {{ o.number }} | 🎯 {{ o.code }}</p>
            {% else %}<p class="red">❌ مرفوض</p>{% endif %}
        </div>{% endfor %}
    </div>
    <div id="visa" class="section"><h2>💳 طلبات Visa</h2>
        {% for v in visa_orders %}
        <div class="card" style="border-color:{% if v.status == 'accepted' %}#3fb950{% elif v.status == 'rejected' %}#f85149{% else %}#d2991d{% endif %};">
            <b>🆔 {{ v.id }}</b> | {{ v.time }}<br>👤 {{ v.uid }} | 💳 {{ v.name }} | 💰 {{ v.price }}$
            {% if v.status == 'pending' %}
            <div style="display:flex;gap:10px;">
                <form method="POST" action="/admin/visa_accept" style="flex:1;"><input type="hidden" name="id" value="{{ v.id }}"><button class="green">✅ قبول</button></form>
                <form method="POST" action="/admin/visa_reject" style="flex:1;"><input type="hidden" name="id" value="{{ v.id }}"><button class="red">❌ رفض</button></form>
            </div>
            {% elif v.status == 'accepted' %}<p class="green">✅ تم التسليم</p>
            {% else %}<p class="red">❌ مرفوض</p>{% endif %}
        </div>{% endfor %}
    </div>
    <div id="deposits" class="section"><h2>💳 طلبات الشحن</h2>
        {% for d in deposits %}<div class="card"><b>{{ d.time }}</b><br>👤 {{ d.uid }} | 💰 {{ d.amount }}$<br>{% if d.file %}<img src="/uploads/{{ d.file }}" width="200">{% endif %}<form method="POST" action="/admin/approve"><input type="hidden" name="uid" value="{{ d.uid }}"><input type="hidden" name="amount" value="{{ d.amount }}"><button class="gold">✅ تأكيد الشحن</button></form></div>{% endfor %}
    </div>
    <div id="chats" class="section"><h2>💬 الدردشات</h2>
        {% for uid, msgs in chats.items() %}<div class="card"><b>👤 {{ uid }}</b><div class="chat-box">{% for m in msgs %}<div class="msg {% if m.from == 'user' %}msg-user{% else %}msg-admin{% endif %}"><small>{% if m.from == 'user' %}مستخدم{% else %}أنت{% endif %} | {{ m.time }}</small><br>{{ m.text }}</div>{% endfor %}</div><form method="POST" action="/admin/reply"><input type="hidden" name="uid" value="{{ uid }}"><textarea name="reply" rows="2" placeholder="ردك..."></textarea><button type="submit">📨 إرسال رد</button></form></div>{% endfor %}
    </div>
    <p style="margin-top:30px;"><a href="/" style="color:#58a6ff;">🔙 الموقع</a></p>
    <script>function showTab(t){document.querySelectorAll('.section').forEach(s=>s.classList.remove('active'));document.getElementById(t).classList.add('active');document.querySelectorAll('.tab').forEach(tb=>tb.classList.remove('active'));event.target.classList.add('active')}</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(WELCOME, syriatel=SYRIATEL, rate=DOLLAR_RATE)

@app.route('/numbers')
def numbers():
    return render_template_string(HTML, syriatel=SYRIATEL, rate=DOLLAR_RATE)

@app.route('/visa')
def visa():
    return render_template_string(VISA, syriatel=SYRIATEL, rate=DOLLAR_RATE)

@app.route('/api/new_user')
def api_new_user():
    return jsonify({"uid": get_uid()})

@app.route('/api/balance')
def api_balance():
    uid = request.args.get('uid')
    users = load(DB_USERS)
    return jsonify({"balance": users.get(uid, {}).get("balance", 0)})

@app.route('/api/order')
def api_order():
    uid = request.args.get('uid')
    price = int(request.args.get('price', 5))
    users = load(DB_USERS)
    if uid not in users: users[uid] = {"balance": 0}
    if users[uid]["balance"] < price: return jsonify({"ok": False, "error": "رصيد غير كاف"})
    users[uid]["balance"] -= price
    save(DB_USERS, users)
    oid = datetime.now().strftime("%H%M%S")
    orders = load(DB_ORDERS)
    orders.append({"id": oid, "uid": uid, "country": request.args.get('country'), "service": request.args.get('service'), "price": price, "time": datetime.now().strftime("%H:%M"), "number": None, "code": None, "status": "pending"})
    save(DB_ORDERS, orders)
    notif = load(DB_NOTIF)
    if uid not in notif: notif[uid] = []
    notif[uid].append({"oid": oid, "status": "pending", "read": False})
    save(DB_NOTIF, notif)
    return jsonify({"ok": True})

@app.route('/api/visa_order')
def api_visa_order():
    uid = request.args.get('uid')
    name = request.args.get('name')
    price = int(request.args.get('price', 10))
    visa_orders = load("visa_orders.json")
    oid = datetime.now().strftime("%H%M%S")
    visa_orders.append({"id": oid, "uid": uid, "name": name, "price": price, "time": datetime.now().strftime("%H:%M"), "status": "pending"})
    save("visa_orders.json", visa_orders)
    return jsonify({"ok": True})

@app.route('/api/notifications')
def api_notifications():
    uid = request.args.get('uid')
    notif = load(DB_NOTIF)
    user_notif = notif.get(uid, [])
    unread = any(not n.get('read', False) for n in user_notif)
    orders = load(DB_ORDERS)
    enriched = []
    for n in user_notif:
        for o in orders:
            if o['id'] == n['oid']:
                enriched.append({**n, "number": o.get('number'), "code": o.get('code')})
    return jsonify({"notifications": enriched, "unread": unread})

@app.route('/api/notifications/read')
def api_notifications_read():
    uid = request.args.get('uid')
    notif = load(DB_NOTIF)
    if uid in notif:
        for n in notif[uid]: n['read'] = True
        save(DB_NOTIF, notif)
    return jsonify({"ok": True})

@app.route('/api/chat')
def api_chat():
    chats = load(DB_CHATS)
    return jsonify({"messages": chats.get(request.args.get('uid'), [])})

@app.route('/api/chat/send', methods=['POST'])
def api_chat_send():
    data = request.json
    uid = data['uid']
    chats = load(DB_CHATS)
    if uid not in chats: chats[uid] = []
    chats[uid].append({"from": "user", "text": data['text'], "time": datetime.now().strftime("%H:%M")})
    save(DB_CHATS, chats)
    return jsonify({"ok": True})

@app.route('/api/deposit', methods=['POST'])
def api_deposit():
    uid = request.form.get('uid')
    amt = request.form.get('amount')
    file = request.files.get('proof')
    fn = None
    if file:
        fn = secure_filename(uid + "_" + datetime.now().strftime("%H%M%S") + ".jpg")
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], fn))
    deposits = load("deposits.json")
    deposits.append({"uid": uid, "amount": amt, "file": fn, "time": datetime.now().strftime("%H:%M")})
    save("deposits.json", deposits)
    return jsonify({"ok": True})

@app.route('/admin')
def admin():
    return '<form method="POST" action="/admin/login" style="text-align:center;margin-top:100px;background:#0d1117;color:#fff;padding:50px;"><h2>🔑 دخول المشرف</h2><input type="password" name="pass" placeholder="كلمة المرور" style="padding:15px;font-size:1.2em;width:80%;margin:20px 0;border-radius:10px;"><br><button type="submit" style="padding:15px 40px;background:#58a6ff;border:none;border-radius:10px;color:#fff;font-size:1.2em;">دخول</button></form>'

@app.route('/admin/login', methods=['POST'])
def admin_login():
    if request.form.get('pass') == ADMIN_PASS:
        orders = load(DB_ORDERS)
        deposits = load("deposits.json")
        chats = load(DB_CHATS)
        visa_orders = load("visa_orders.json")
        return render_template_string(ADMIN_HTML, orders=orders, deposits=deposits, chats=chats, visa_orders=visa_orders)
    return '<h1>❌ خطأ</h1>'

@app.route('/admin/accept', methods=['POST'])
def admin_accept():
    oid = request.form.get('id')
    orders = load(DB_ORDERS)
    for o in orders:
        if o['id'] == oid:
            o['number'] = request.form.get('number')
            o['code'] = request.form.get('code')
            o['status'] = 'accepted'
    save(DB_ORDERS, orders)
    return redirect('/admin/login')

@app.route('/admin/reject', methods=['POST'])
def admin_reject():
    oid = request.form.get('id')
    orders = load(DB_ORDERS)
    for o in orders:
        if o['id'] == oid:
            o['status'] = 'rejected'
    save(DB_ORDERS, orders)
    return redirect('/admin/login')

@app.route('/admin/visa_accept', methods=['POST'])
def admin_visa_accept():
    oid = request.form.get('id')
    visa_orders = load("visa_orders.json")
    for v in visa_orders:
        if v['id'] == oid:
            v['status'] = 'accepted'
    save("visa_orders.json", visa_orders)
    return redirect('/admin/login')

@app.route('/admin/visa_reject', methods=['POST'])
def admin_visa_reject():
    oid = request.form.get('id')
    visa_orders = load("visa_orders.json")
    for v in visa_orders:
        if v['id'] == oid:
            v['status'] = 'rejected'
    save("visa_orders.json", visa_orders)
    return redirect('/admin/login')

@app.route('/admin/approve', methods=['POST'])
def admin_approve():
    uid = request.form.get('uid')
    amt = float(request.form.get('amount', 0))
    users = load(DB_USERS)
    if uid not in users: users[uid] = {"balance": 0}
    users[uid]["balance"] += amt
    save(DB_USERS, users)
    return redirect('/admin/login')

@app.route('/admin/reply', methods=['POST'])
def admin_reply():
    uid = request.form.get('uid')
    reply = request.form.get('reply')
    chats = load(DB_CHATS)
    if uid not in chats: chats[uid] = []
    chats[uid].append({"from": "admin", "text": reply, "time": datetime.now().strftime("%H:%M")})
    save(DB_CHATS, chats)
    return redirect('/admin/login')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
