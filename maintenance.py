from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/<path:path>')
def maintenance():
    return '''
    <html dir="rtl"><head><meta charset="UTF-8"><style>
        body{background:#0d1117;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;font-family:sans-serif}
        .box{text-align:center;color:#e6edf3;padding:40px;background:#161b22;border-radius:20px;border:2px solid #d2991d}
        h1{color:#d2991d;font-size:3em} p{color:#8b949e;font-size:1.2em}
        .icon{font-size:5em} @keyframes spin{100%{transform:rotate(360deg)}} .gear{animation:spin 4s linear infinite;display:inline-block}
    </style></head><body><div class="box">
        <div class="icon"><span class="gear">⚙️</span> 🔧</div>
        <h1>قيد الصيانة</h1><p>نعمل على تحسين الموقع 😊</p><p>سنعود قريباً 💛</p>
    </div></body></html>'''
app.run(host='0.0.0.0', port=9000)
