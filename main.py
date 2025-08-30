from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/proxy")
async def redirect_proxy(request: Request):
    params = dict(request.query_params)
    base_url = "https://viniciusacx-mediaflow-proxy.hf.space/proxy"
    query = "&".join([f"{k}={v}" for k, v in params.items()])
    return RedirectResponse(f"{base_url}?{query}")