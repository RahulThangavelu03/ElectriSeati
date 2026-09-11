from fastapi import FastAPI

app=FastAPI(title="ElectriSeati API")


@app.get("/health")

def healthcheck():
    return {"status":"ok"}
