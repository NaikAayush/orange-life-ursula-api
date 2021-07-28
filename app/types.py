from pydantic import BaseModel

class GrantParams(BaseModel):
    delegating_pk: str
    receiving_pk: str
    verifying_key: str
    capsule: str
    kfrag: str

class AccessParams(BaseModel):
    delegating_pk: str
    receiving_pk: str
    verifying_key: str


class AccessResponse(BaseModel):
    capsule: str
    cfrag: str
