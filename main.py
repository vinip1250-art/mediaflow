from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
import os

# Inicializa o FastAPI uma única vez
app = FastAPI()

# ----------------- Rotas de Verificação de Saúde -----------------

@app.get("/")
def health_check():
    """
    Endpoint para verificação de saúde do Render.
    Retorna 200 OK.
    """
    return {"status": "ok"}

@app.head("/")
def health_check_head():
    """
    Endpoint para verificação de saúde com o método HEAD.
    Retorna uma resposta vazia com status 200 OK.
    """
    return JSONResponse(content={})

@app.get("/proxy/ip")
def get_public_ip(request: Request):
    """
    Retorna o IP público do proxy, essencial para o Real-Debrid.
    O IP é extraído do cabeçalho X-Forwarded-For, adicionado pelo Render.
    """
    ip_address = request.headers.get("X-Forwarded-For")
    if ip_address:
        ip_address = ip_address.split(",")[0].strip()
        return {"ip": ip_address}
    
    return {"ip": request.client.host}

# ----------------- Rota Principal do Proxy -----------------

@app.get("/proxy")
async def redirect_proxy(request: Request):
    """
    Redireciona as requisições para o proxy do Hugging Face.
    """
    params = dict(request.query_params)
    
    password = params.pop("password", None)
    if password:
        params["api_password"] = password

    base_url = "https://viniciusacx-mediaflow-proxy.hf.space/proxy"
    query = "&".join([f"{k}={v}" for k, v in params.items()])
    
    return RedirectResponse(f"{base_url}?{query}")
