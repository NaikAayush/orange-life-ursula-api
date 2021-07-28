import umbral


def reencrypt_bytes(
    delegating_pk: bytes,
    receiving_pk: bytes,
    verifying_key: bytes,
    capsule: bytes,
    kfrag: bytes,
):
    # convert to umbral objects
    delegating_pk_o = umbral.PublicKey.from_bytes(delegating_pk)
    receiving_pk_o = umbral.PublicKey.from_bytes(receiving_pk)
    verifying_key_o = umbral.PublicKey.from_bytes(verifying_key)
    capsule_o = umbral.Capsule.from_bytes(capsule)
    kfrag_o = umbral.KeyFrag.from_bytes(kfrag)

    # verify kfrag
    verified_kfrag = kfrag_o.verify(verifying_key_o, delegating_pk_o, receiving_pk_o)

    # reencrypt
    cfrag = umbral.pre.reencrypt(capsule_o, verified_kfrag)

    return bytes(cfrag)


def reencrypt_hex(
    delegating_pk: str, receiving_pk: str, verifying_key: str, capsule: str, kfrag: str
):
    return reencrypt_bytes(
        bytes.fromhex(delegating_pk),
        bytes.fromhex(receiving_pk),
        bytes.fromhex(verifying_key),
        bytes.fromhex(capsule),
        bytes.fromhex(kfrag),
    ).hex()
