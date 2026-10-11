---
name: calibrate-mq135
description: Recalibrate the MQ-135 ammonia sensor R0 value in clean air and update ammonia.py. Use when NH3 readings look wrong or after replacing the sensor.
---
1. Confirm the sensor has warmed up (≥ 24h on first use, ≥ 10 min otherwise) in clean air.
2. Run `python3 calibrate_r0.py` and note the averaged R0.
3. Update `R0` in `ammonia.py` and fix the calibration date comment.
4. Sanity check: clean-air NH3 should read near 0–10 ppm.
5. Commit with message "Recalibrate MQ-135 R0".