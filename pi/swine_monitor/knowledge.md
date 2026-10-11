# Swine Monitor – Project Knowledge
## Purpose
IoT early-detection system for swine fever: thermal + motion + ammonia sensing, ML risk scoring, live dashboard, Telegram alerts.
## Hardware (Raspberry Pi)
- MLX90640 thermal camera (I2C, 32x24, 4 Hz)
- 3x HC-SR501 PIR on GPIO BCM 17/27/22 (zones 1–3)
- MQ-135 via ADS1115 (addr 0x48, channel 0); R0 calibrated in clean air
- Pi camera (picamera2) for MJPEG feed with thermal overlay
## Data flow
sensor.py (thermal thread, ~4 Hz) → main.py monitoring_loop → ml_predict.py → POST /api/update → app.py → index.html; cloud.py sends Telegram alerts + ThingSpeak.
## Key thresholds
Fever ≥ 40.5 °C, elevated ≥ 40.0 °C, NH3 warning > 20 ppm / danger > 35 ppm.
## Configuration
Secrets are read from environment variables (.env, not committed): TELEGRAM_BOT_TOKEN, THINGSPEAK_API_KEY. See .env.example.
## Known issues
- train_on_pi.py (5 features, NORMAL/ELEVATED/FEVER) does not match ml_predict.py (4 features: temp, nh3, activity, temp_diff; AT_RISK/HEALTHY).
- Paths are hardcoded to /home/pi/swine_monitor.
- Sensors fall back to simulation mode if libraries are missing.