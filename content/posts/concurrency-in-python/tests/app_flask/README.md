# How to run

Dev server:

```shell
#pip install -r requirements.txt
python app_flask.py
# -> http://127.0.0.1:5000/health
```

# Prod-style (multi-process):

```shell
# 4 workers, threaded worker class for light I/O; tune for your workload
gunicorn -w 4 -k gthread -b 0.0.0.0:8000 "app:create_app()"
# Consider --preload to load the model once in the master and fork workers:
# gunicorn -w 4 -k gthread --preload -b 0.0.0.0:8000 "app:create_app()"
```

# Quick `curls`

```shell
curl -s localhost:8000/health
#curl -s -X POST localhost:8000/predict -H "Content-Type: application/json" -d '{"text":"I love this, great day!"}'
#curl -s -X POST localhost:8000/predict-batch -H "Content-Type: application/json" -d '{"texts":["awesome","this is bad","meh"]}'
```
