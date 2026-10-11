from flask import Flask, jsonify, request, render_template_string, Response
from camera import get_camera_frame, generate_mjpeg
import numpy as np
import os

app = Flask(__name__)

latest = {
    "max_temp": 0.0,
    "min_temp": 0.0,
    "avg_temp": 0.0,
    "status": "Starting...",
    "fever_risk": 0.0,
    "trend": "Collecting data...",
    "hot_zone": "--",
    "timestamp": "--",
    "frame": [],
    "history": []
}
def compute_correlations(history):
    if len(history) < 5:
        return {"available": False, "reason": "Not enough data yet (need at least 5 readings)"}

    try:
        temps = np.array([h.get("max_temp", 0) for h in history], dtype=float)
        nh3   = np.array([h.get("nh3_ppm", 0) for h in history], dtype=float)
        act   = np.array([h.get("activity_score", 0) for h in history], dtype=float)

        def safe_corr(a, b):
            if np.std(a) == 0 or np.std(b) == 0:
                return 0.0
            val = np.corrcoef(a, b)[0, 1]
            return round(float(val), 3) if not np.isnan(val) else 0.0

        temp_activity_corr = safe_corr(temps, act)
        temp_nh3_corr      = safe_corr(temps, nh3)
        nh3_activity_corr  = safe_corr(nh3, act)

        def interpret(corr, label_a, label_b):
            strength = abs(corr)
            direction = "negative" if corr < 0 else "positive"
            if strength >= 0.6:
                level = "Strong"
            elif strength >= 0.3:
                level = "Moderate"
            else:
                level = "Weak"
            return level + " " + direction + " correlation between " + label_a + " and " + label_b

        return {
            "available": True,
            "sample_size": len(history),
            "temp_activity": {
                "value": temp_activity_corr,
                "insight": interpret(temp_activity_corr, "temperature", "activity")
            },
            "temp_ammonia": {
                "value": temp_nh3_corr,
                "insight": interpret(temp_nh3_corr, "temperature", "ammonia")
            },
            "ammonia_activity": {
                "value": nh3_activity_corr,
                "insight": interpret(nh3_activity_corr, "ammonia", "activity")
            }
        }
    except Exception as e:
        return {"available": False, "reason": "Error computing correlations: " + str(e)}

@app.route("/")
def index():
    path = "/home/pi/swine_monitor/index.html"
    with open(path) as f:
        html = f.read()
    return render_template_string(html)

@app.route("/api/data")
def api_data():
    return jsonify(latest)

@app.route("/api/camera")
def api_camera():
    """Legacy single-snapshot endpoint (base64 JSON) — kept for compatibility."""
    frame = get_camera_frame()
    if frame:
        return jsonify({"image": frame, "available": True})
    return jsonify({"image": None, "available": False})

@app.route("/video_feed")
def video_feed():
    """Live MJPEG stream — use this in <img src="/video_feed"> for a real live feed."""
    return Response(
        generate_mjpeg(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )

@app.route("/api/update", methods=["POST"])
def api_update():
    global latest
    data = request.get_json(force=True)
    if data:
        latest.update(data)
    return jsonify({"ok": True})

if __name__ == "__main__":
    import socket
    try:
        ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        ip = "your-pi-ip"
    print("Dashboard at http://" + ip + ":5000")
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)

@app.route("/api/analytics")
def api_analytics():
    hist = latest.get("history", [])
    result = compute_correlations(hist)
    return jsonify(result)
