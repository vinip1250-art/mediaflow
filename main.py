from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/proxy")
async def redirect_proxy(request: Request):
    params = dict(request.query_params)

    # Extrair credenciais se existirem
    username = params.pop("username", None)
    password = params.pop("password", None)

    # Se o campo 'password' estiver presente, usá-lo como api_password
    if password:
        params["api_password"] = password

    # Montar a URL final
    base_url = "https://viniciusacx-mediaflow-proxy.hf.space/proxy"
    query = "&".join([f"{k}={v}" for k, v in params.items()])
    return RedirectResponse(f"{base_url}?{query}")

from fastapi import FastAPI

app = FastAPI()

# Suas outras rotas do Mediaflow Proxy estão aqui...

@app.get("/")
def health_check():
    return {"status": "ok"}

from fastapi import FastAPI

app = FastAPI()

# Suas outras rotas do Mediaflow Proxy estão aqui...

@app.get("/")

@app.get("/", methods=["GET", "HEAD"])
def health_check():
    return {"status": "ok"}
def health_check():
    return {"status": "ok"}
    

