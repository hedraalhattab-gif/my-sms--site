with open('index.py', 'r') as f:
    c = f.read()

old1 = "document.getElementById('totalPrice').textContent"
new1 = "document.getElementById('totalPrice').innerHTML"
c = c.replace(old1, new1)

old2 = "document.getElementById('totalBtn').textContent"
new2 = "document.getElementById('totalBtn').innerHTML"
c = c.replace(old2, new2)

old3 = 'onclick="buyEmpty()"'
new3 = 'onclick="buyEmpty();document.getElementById(\'amountSection\').style.display=\'none\'"'
c = c.replace(old3, new3)

with open('index.py', 'w') as f:
    f.write(c)

print("تم الإصلاح")
