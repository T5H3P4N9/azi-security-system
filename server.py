from flask import Flask, request, render_template_string, jsonify
from openai import OpenAI
import time
import math

app = Flask(__name__)

# ================= CONFIG =================
client = OpenAI(api_key="API key here")

# ================= STATE =================
sensor_ai_enabled = True
event_voice_enabled = True

sensor_data = {
    "distance": 0,
    "state": "CLEAR",
    "angle": 90,
    "x": 0,
    "y": 0,
    "last_message": ""
}

# ================= ANTI-SPAM =================
last_trigger_time = {
    "INTRUDER": 0,
    "WARNING": 0,
    "FINAL_WARNING": 0
}

COOLDOWN = 6

# ================= UI =================
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>AZI AI</title>

<style>
body{
    background:#050b12;
    color:#00ffee;
    font-family:Arial;
    margin:0;
}

.container{
    display:flex;
    gap:20px;
    padding:20px;
}

.panel{
    background:#111927;
    border:1px solid #00ffee44;
    border-radius:15px;
    padding:15px;
    flex:1;
}

#chat{
    height:450px;
    overflow-y:auto;
}

.msg{
    margin:10px;
    padding:10px;
    border-radius:10px;
}

.user{background:#333;color:white;}
.ai{background:#004466;}
.sensor{background:#331100;}

button{
    padding:10px;
    margin:5px;
    border:none;
    border-radius:10px;
    cursor:pointer;
}

#radar{
    width:100%;
    height:350px;
    background:black;
    border-radius:15px;
}
</style>
</head>

<body>

<h1 style="padding-left:20px;">🧠 JARVIS SECURITY SYSTEM</h1>

<div class="container">

<!-- CHAT -->
<div class="panel">
<h2>🎤 Voice AI</h2>

<button onclick="startListening()">START TALKING</button>

<div id="chat"></div>
</div>

<!-- RADAR -->
<div class="panel">
<h2>📡 Radar System</h2>

<canvas id="radar"></canvas>

<h3 id="distance">Distance: -- cm</h3>
<h3 id="threat">Threat: CLEAR</h3>
<h3 id="coords">X: 0 | Y: 0</h3>

<button onclick="toggleSensorAI()" id="sensorBtn">
SENSOR AI: ON
</button>

<button onclick="toggleEventVoice()" id="voiceBtn">
EVENT VOICE: ON
</button>

<div id="sensorLog"></div>
</div>

</div>

<script>

let recognition;
let sensorAI = true;
let eventVoice = true;
let lastEvent = "";

// ================= UI =================
function addMsg(text, cls){
    let div = document.createElement("div");
    div.className = "msg " + cls;
    div.innerText = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

function addSensor(text){
    sensorLog.innerHTML = "";
    let div = document.createElement("div");
    div.className = "msg sensor";
    div.innerText = text;
    sensorLog.prepend(div);
}

// ================= FIXED SPEECH SYSTEM =================
function speak(text){

    // ONLY stop mic (NOT event gating)
    if(recognition){
        recognition.stop();
    }

    speechSynthesis.cancel();

    let s = new SpeechSynthesisUtterance(text);

    s.onend = () => {
        if(recognition){
            recognition.start();
        }
    };

    speechSynthesis.speak(s);
}

// ================= TOGGLES =================
function toggleSensorAI(){

    sensorAI = !sensorAI;

    fetch("/toggle_sensor_ai",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({enabled:sensorAI})
    });

    sensorBtn.innerText =
        "SENSOR AI: " + (sensorAI ? "ON" : "OFF");
}

function toggleEventVoice(){

    eventVoice = !eventVoice;

    fetch("/toggle_event_voice",{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({enabled:eventVoice})
    });

    voiceBtn.innerText =
        "EVENT VOICE: " + (eventVoice ? "ON" : "OFF");

    if(!eventVoice){
        sensorLog.innerHTML = "";
        lastEvent = "";
    }
}

// ================= VOICE INPUT =================
function startListening(){

    recognition =
    new(window.SpeechRecognition || window.webkitSpeechRecognition)();

    recognition.lang = "en-US";
    recognition.continuous = true;

    recognition.onresult = async (e)=>{

        let text = e.results[e.results.length-1][0].transcript;

        addMsg("YOU: "+text,"user");

        let res = await fetch("/chat",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({text})
        });

        let data = await res.json();

        addMsg("JARVIS: "+data.reply,"ai");

        // 🔥 AI ALWAYS SPEAKS (FIXED)
        speak(data.reply);
    };

    recognition.start();
}

// ================= SENSOR LOOP =================
async function updateSensor(){

    let res = await fetch("/sensor_data");
    let d = await res.json();

    distance.innerText = "Distance: " + d.distance + " cm";
    threat.innerText = "Threat: " + d.state;
    coords.innerText = "X: " + d.x + " | Y: " + d.y;

    drawRadar(d.distance, d.angle);

    // 🔥 SENSOR SPEECH ONLY IF EVENT VOICE ON
    if(d.last_message && d.last_message !== lastEvent){

        lastEvent = d.last_message;

        addSensor(d.last_message);

        if(eventVoice){
            speak(d.last_message);
        }
    }
}

setInterval(updateSensor, 500);

// ================= RADAR =================
const canvas = document.getElementById("radar");
const ctx = canvas.getContext("2d");

canvas.width = 400;
canvas.height = 350;

let sweep = 0;

function drawRadar(dist, angle){

    ctx.clearRect(0,0,400,350);

    ctx.strokeStyle="#00ff00";

    for(let r=50;r<200;r+=50){
        ctx.beginPath();
        ctx.arc(200,300,r,Math.PI,2*Math.PI);
        ctx.stroke();
    }

    // cross
    ctx.beginPath();
    ctx.moveTo(200,300);
    ctx.lineTo(200,50);
    ctx.stroke();

    ctx.beginPath();
    ctx.moveTo(50,300);
    ctx.lineTo(350,300);
    ctx.stroke();

    // sweep
    sweep += 3;
    if(sweep > 180) sweep = 0;

    let rad = sweep * Math.PI / 180;

    ctx.strokeStyle = "lime";
    ctx.beginPath();
    ctx.moveTo(200,300);
    ctx.lineTo(
        200 + Math.cos(Math.PI - rad) * 200,
        300 - Math.sin(rad) * 200
    );
    ctx.stroke();

    // target
    if(dist > 0 && dist < 40){

        let a = angle * Math.PI / 180;

        let x = 200 - Math.cos(a) * (dist * 5);
        let y = 300 - Math.sin(a) * (dist * 5);

        ctx.fillStyle = "red";
        ctx.beginPath();
        ctx.arc(x,y,8,0,Math.PI*2);
        ctx.fill();

        ctx.strokeStyle = "red";
        ctx.strokeRect(x-12,y-12,24,24);
    }
}

</script>

</body>
</html>
"""

# ================= ROUTES =================
@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    return jsonify({"reply": ask_ai(request.json["text"])})

# ================= AI =================
def ask_ai(text):
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":"""
                                    You are AZI Security AI, an advanced AI-powered security and monitoring assistant.

                                    Your purpose is to assist the user with:
                                    - Home security monitoring
                                    - Smart surveillance systems
                                    - ESP32 sensor monitoring
                                    - Threat detection
                                    - Device status reporting
                                    - AI automation
                                    - Emergency alerts
                                    - Robotics and IoT control systems

                                    Rules:
                                    - Be concise, intelligent, and professional.
                                    - Respond like a real AI operating system similar to JARVIS.
                                    - Prioritize safety and security awareness.
                                    - If suspicious activity is mentioned, respond seriously and recommend security actions.
                                    - Help explain sensor readings, device states, and automation logic clearly.
                                    - Support Python, Flask, ESP32, networking, and robotics questions.
                                    - Never pretend to perform real-world actions unless connected to hardware.
                                    - Never generate harmful, illegal, or dangerous instructions.
                                    - Speak confidently and technically when needed.
                                    - Keep responses futuristic but realistic.

                                    Personality:
                                    - Calm
                                    - Intelligent
                                    - Helpful
                                    - Technical
                                    - Slightly futuristic

                                    System Name:
                                    AZI Security System

                                    Creator:
                                    Tshepang Oliver
                                    """},
                {"role":"user","content":text}
            ]
        )
        return res.choices[0].message.content
    except:
        return "System error."

# ================= SENSOR =================
@app.route("/sensor")
def sensor():

    global sensor_data

    if not sensor_ai_enabled:
        return "OFF"

    dist = request.args.get("dist", type=int)
    state = request.args.get("state")
    angle = request.args.get("angle", type=int)

    rad = math.radians(angle)
    x = int(dist * math.cos(rad))
    y = int(dist * math.sin(rad))

    sensor_data.update({
        "distance": dist,
        "state": state,
        "angle": angle,
        "x": x,
        "y": y
    })

    now = time.time()
    msg = None

    if event_voice_enabled:

        if state == "INTRUDER" and now-last_trigger_time["INTRUDER"] > COOLDOWN:
            msg = f"Intruder detected at {dist} centimeters"
            last_trigger_time["INTRUDER"] = now

        elif state == "WARNING" and now-last_trigger_time["WARNING"] > COOLDOWN:
            msg = "Warning. Target approaching."
            last_trigger_time["WARNING"] = now

        elif state == "FINAL_WARNING" and now-last_trigger_time["FINAL_WARNING"] > COOLDOWN:
            msg = "Final warning. Leave immediately."
            last_trigger_time["FINAL_WARNING"] = now

    sensor_data["last_message"] = msg if msg else ""

    return "OK"

# ================= DATA =================
@app.route("/sensor_data")
def sensor_data_route():
    return jsonify(sensor_data)

# ================= TOGGLES =================
@app.route("/toggle_sensor_ai", methods=["POST"])
def toggle_sensor():
    global sensor_ai_enabled
    sensor_ai_enabled = request.json["enabled"]
    return jsonify({"ok":True})

@app.route("/toggle_event_voice", methods=["POST"])
def toggle_voice():
    global event_voice_enabled
    event_voice_enabled = request.json["enabled"]
    return jsonify({"ok":True})

# ================= RUN =================
if __name__ == "__main__":
    print("🚀 JARVIS FULL SYSTEM ONLINE")
    app.run(host="0.0.0.0", port=8000)