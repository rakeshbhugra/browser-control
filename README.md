please install miniconda first (google)

```
make install
```

run app
```
uvicorn src.playwright_fastapi_app.app:app --host 0.0.0.0 --port 4000 --reload
```