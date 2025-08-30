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
    Retorna 200 OK para evitar que o serviço seja reiniciado.
    """
    return {"status": "ok"}

@app.head("/")
def health_check_head():
    """
    Endpoint para verificação de saúde com o método HEAD.
    """
    return JSONResponse(status_code=200)

@app.get("/proxy/ip")
def get_public_ip(request: Request):
    """
    Retorna o IP público do proxy, essencial para o Real-Debrid.
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
    
    # Extrai e remapeia a senha para a api_password
    password = params.pop("password", None)
    if password:
        params["api_password"] = password

    # Constrói a URL de destino
    base_url = "https://viniciusacx-mediaflow-proxy.hf.space/proxy"
    query = "&".join([f"{k}={v}" for k, v in params.items()])
    
    return RedirectResponse(f"{base_url}?{query}")
