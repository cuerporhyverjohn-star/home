---
name: retrain-fever-model
description: Retrain pig_model.pkl so its features and labels match ml_predict.py. Use when changing thresholds, features, or adding new data.
---
1. Features must be exactly [body_surface_temp, ammonia_ppm, activity_score, temp_rate_change], in this order.
2. Labels are AT_RISK / HEALTHY (as expected by ml_predict.py).
3. Train a RandomForestClassifier, print accuracy and a confusion matrix.
4. Back up the old pkl before overwriting; never commit .pkl files.
5. Verify with `python3 -c "from ml_predict import *; load_model()"`.