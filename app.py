# app.py
import time
from collections import deque

from flask import Flask, render_template, request, flash, jsonify

# Optional CORS (safe to keep even if not installed)
try:
    from flask_cors import CORS
    CORS_ENABLED = True
except Exception:
    CORS_ENABLED = False

# Your translator + loaded assets
from mt.translator import translate
from mt.loader import assets  # provides assets.config

app = Flask(__name__)
app.secret_key = "dev-secret"  # replace in production

if CORS_ENABLED:
    # Allow all origins in dev; tighten in production
    CORS(app)

# -----------------------------
# Tiny per-IP sliding-window rate limiter (memory only)
# -----------------------------
RATE_LIMIT_MAX = 20           # max requests
RATE_LIMIT_WINDOW_SEC = 60    # per this many seconds
_request_times = {}           # ip -> deque[timestamps]

def allow_request(ip: str) -> bool:
    now = time.time()
    dq = _request_times.setdefault(ip, deque())
    # drop old timestamps
    while dq and now - dq[0] > RATE_LIMIT_WINDOW_SEC:
        dq.popleft()
    if len(dq) >= RATE_LIMIT_MAX:
        return False
    dq.append(now)
    return True

def get_client_ip():
    # Respect reverse proxy header if present
    return request.headers.get("X-Forwarded-For", request.remote_addr or "unknown")

# Helper: read max English length regardless of key name used in config.json
def get_max_eng_len():
    cfg = assets.config or {}
    return cfg.get("max_en")

# -----------------------------
# Web UI route
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        src = (request.form.get("src") or "").strip()
        if not src:
            flash("Please enter English text.", "warn")
            return render_template("index.html", src="", translation=None)

        max_eng = get_max_eng_len()
        if max_eng:
            approx_tokens = len(src.split())
            if approx_tokens > max_eng:
                flash(f"Input is long; using first ~{max_eng} tokens.", "info")

        try:
            translation = translate(src)
        except Exception as e:
            translation = ""
            flash(f"Translation failed: {e}", "error")

        return render_template("index.html", src=src, translation=translation)

    # GET
    return render_template("index.html", src="", translation=None)

# -----------------------------
# JSON API
# -----------------------------
@app.route("/api/translate", methods=["POST"])
def api_translate():
    ip = get_client_ip()
    if not allow_request(ip):
        return jsonify({"error": "Too Many Requests"}), 429

    if not request.is_json:
        return jsonify({"error": "Expected application/json"}), 400

    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "Field 'text' is required"}), 400

    max_eng = get_max_eng_len()
    approx_tokens = len(text.split())
    truncated = bool(max_eng and approx_tokens > max_eng)

    try:
        out = translate(text)
        return jsonify({
            "translation": out,
            "input_tokens_approx": approx_tokens,
            "max_eng_len": max_eng,
            "truncated": truncated
        }), 200
    except Exception as e:
        return jsonify({"error": f"translation_failed: {str(e)}"}), 500

# -----------------------------
# Entrypoint
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
