# Notes you can mention in interviews

- Model boundary: the “model” is just a function today; swap with a real model (e.g., load a .pt/.pkl) in startup.

- Batch endpoint: improves throughput, reduces overhead.

- Validation: FastAPI’s Pydantic schemas give type validation & OpenAPI docs for free (/docs).

- Scaling: run with multiple workers (e.g., uvicorn --workers 4) behind a reverse proxy; add request timeouts & logging.

- Concurrency: I/O-bound models (remote vector DB, files) benefit from async (FastAPI); CPU-bound models may need process workers.
