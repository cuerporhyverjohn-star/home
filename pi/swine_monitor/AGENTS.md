# AGENTS.md
## Setup / run
- Install: `pip3 install python-dotenv flask numpy scikit-learn`
- Copy `.env.example` to `.env` and fill in real values.
- Run on the Pi: `python3 main.py` (dashboard at http://<pi-ip>:5000)
- Without hardware, sensors auto-switch to simulation mode.
## Rules
- NEVER hardcode or print secrets; read them from environment variables.
- Never commit .env, .pkl, .csv or subscribers.json.
- Keep the model feature order in sync with ml_predict.py.
- Work on a feature branch, never directly on master.
## Layout
sensor.py, pir.py, ammonia.py, camera.py, ml_predict.py, cloud.py, app.py, main.py, index.html