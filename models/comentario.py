from dataclasses import dataclass
from datetime import datetime, timezone
import re
import uuid

import pytz


@dataclass
class Comentario:
    conteudo: str
    created_at: str
    na_sumula_do_dia: str
    uid: str = str(uuid.uuid4())

    def to_firestore(self):
        return {
            "conteudo": self.conteudo,
            "created_at": self.created_at,
            "na_sumula_do_dia": self.na_sumula_do_dia,
        }

    @staticmethod
    def from_firestore(doc):
        _doc = doc.to_dict()

        created_at = re.sub(r"\..+$", "", _doc["created_at"])
        created_at = (
            datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
            .replace(tzinfo=timezone.utc)
            .astimezone(pytz.timezone("Brazil/East"))
        ).strftime("%d/%m/%Y as %H:%M:%S")

        return Comentario(
            conteudo=_doc["conteudo"],
            created_at=created_at,
            na_sumula_do_dia=_doc["na_sumula_do_dia"],
            uid=doc.id,
        )
