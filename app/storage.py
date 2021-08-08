import sqlite3
from typing import Union


class Storage:
    def store_cfrag_hex(
        self,
        cfrag: str,
        delegating_pk: str,
        receiving_pk: str,
        verifying_key: str,
        capsule: str,
    ):
        cfrag, delegating_pk, receiving_pk, verifying_key, capsule
        raise NotImplementedError()

    def load_cfrag(self, delegating_pk: str, receiving_pk: str, verifying_key: str):
        delegating_pk, receiving_pk, verifying_key
        raise NotImplementedError()


class SqliteStorage(Storage):
    def __init__(self, filename="ursula.db"):
        self.filename = filename
        with sqlite3.connect(filename) as conn:
            conn.execute(
                """
    CREATE TABLE IF NOT EXISTS ursula (delegating text, receiving text, verifying text, cfrag text, capsule text)
    """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS requests (address text, pubkey text)
    """
            )

    def store_cfrag_hex(
        self,
        cfrag: str,
        delegating_pk: str,
        receiving_pk: str,
        verifying_key: str,
        capsule: str,
    ):
        with sqlite3.connect(self.filename) as con:
            con.execute(
                "REPLACE INTO ursula (delegating, receiving, verifying, cfrag, capsule) VALUES (?, ?, ?, ?, ?)",
                (delegating_pk, receiving_pk, verifying_key, cfrag, capsule),
            )

    def load_cfrag(self, delegating_pk: str, receiving_pk: str, verifying_key: str):
        with sqlite3.connect(self.filename) as con:
            item = con.execute(
                "SELECT cfrag, capsule FROM ursula WHERE delegating = ? AND receiving = ? AND verifying = ?",
                (delegating_pk, receiving_pk, verifying_key),
            ).fetchone()
        if item is None:
            return None
        return (item[0], item[1])

    def addRequest(self, address, pubkey):
        with sqlite3.connect(self.filename) as con:
            con.execute(
                "REPLACE INTO requests (address, pubkey) VALUES (?, ?)",
                (address, pubkey),
            )

    def getPubKey(self, address):
        with sqlite3.connect(self.filename) as con:
            item = con.execute(
                "SELECT address, pubkey FROM requests WHERE address = ?", (address,)
            ).fetchone()
        if item is None:
            return None
        return item[1]
