from dataclasses import dataclass
from datetime import date


@dataclass
class Publicacao:
    """Representa uma publicação no Diário Oficial da União

    - A ementa, título e assinatura podem ser None

    """

    id: str
    secao: str
    tipo_normativo: str
    data: date
    escopo: str
    titulo: str
    ementa: str
    conteudo: str
    assinatura: str
    pdf: str
    id_materia: str
    motivo: str