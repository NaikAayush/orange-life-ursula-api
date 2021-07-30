from app.storage import SqliteStorage
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.pre import reencrypt_hex
from app.types import AccessParams, AccessResponse, GrantParams

app = FastAPI()
store = SqliteStorage()


# allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/v1/grant")
def grantAccess(params: GrantParams):
    cfrag = reencrypt_hex(params.delegating_pk, params.receiving_pk, params.verifying_key, params.capsule, params.kfrag)
    store.store_cfrag_hex(cfrag, params.delegating_pk, params.receiving_pk, params.verifying_key, params.capsule)

    return True


@app.post("/v1/cfrags", response_model=AccessResponse)
def cfrags(params: AccessParams):
    res = store.load_cfrag(params.delegating_pk, params.receiving_pk, params.verifying_key)
    if res is None:
        raise HTTPException(status_code=400, detail="cfrag not found")
    cfrag, capsule = res
    return AccessResponse(capsule=capsule, cfrag=cfrag)
