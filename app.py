from flask import Flask, request, jsonify
import requests, os

app = Flask(__name__)

# ===== ARIA CONFIG - LOCKED =====
FACE = "Polished Long Hair - No Freckles - LOCKED 🔒"
ACADEMY = "Aria Forge Academy"
CEO = "Nkiru"
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "") # You will set this on Render

def aria_brain(message):
    msg = message.lower().strip()
    welcome = f"👋 Hello! I'm Aria from {ACADEMY}! 🎓\nPowered by CEO {CEO}\nFace: {FACE}\n\n"
    if msg in ["hi","hello","hey","start","menu","/start"]:
        return welcome + "📋 MENU:\n1️⃣ Academy Info\n2️⃣ Build AI Agent\n3️⃣ Sharp Video (MBG Quality)\n4️⃣ Talk to CEO Nkiru\n\nReply with number!"
    if "1" in msg: return f"🎓 {ACADEMY} by CEO Nkiru - We teach you to build AI Agents like me & create sharp MBG videos!"
    if "2" in msg: return "🤖 To build your AI Agent, tell me your business name and what you want it to do!"
    if "3" in msg: return "🎬 Sharp Video ACTIVE! Tell me your video script and I'll make it 4K!"
    if "4" in msg: return "👩‍💼 CEO Nkiru will reply soon! Your message has been forwarded. 💌"
    return welcome + "I didn't get that. Type MENU"

# ===== ROUTES =====
@app.route("/")
def home():
    return f"✅ ARIA IS LIVE 24/7 - {ACADEMY} - Face: {FACE}"

@app.route("/test/<msg>")
def test(msg):
    return aria_brain(msg)

# ===== TELEGRAM WEBHOOK =====
@app.route("/telegram", methods=["POST"])
def telegram():
    data = request.json
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]
        reply = aria_brain(text)
        if TELEGRAM_TOKEN:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            requests.post(url, json={"chat_id": chat_id, "text": reply})
    return jsonify({"status": "ok"})

# ===== WHATSAPP WEBHOOK =====
@app.route("/whatsapp", methods=["GET","POST"])
def whatsapp():
    if request.method == "GET":
        return request.args.get("hub.challenge", "Aria verification")
    data = request.json
    # Meta will send messages here - you can process later
    print("WhatsApp message:", data)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

