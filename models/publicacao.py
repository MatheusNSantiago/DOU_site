from dataclasses import dataclass
import re
from datetime import date


@dataclass
class Publicacao:
    """Representa uma publicação no Diário Oficial da União

    - A ementa, título e assinatura podem ser None

    """

    id: str
    secao: str
    tipo_normativo: str
    data: str
    escopo: str
    titulo: str
    ementa: str
    conteudo: str
    assinatura: str
    pdf: str
    id_materia: str
    motivo: str

    def __post_init__(self):
        """ Limpa a publicação """
        # Tirar o excesso do título
        if self.titulo != None:
            self.titulo = self.titulo.upper()
            
            self.titulo = re.sub(r",? DE .+2021?", "", self.titulo)

        escopos_importantes = [
            "Banco Central do Brasil",
            "Ministério da Economia",
            "Presidência da República",
            "Conselho de Controle de Atividades Financeiras",
            "Atos do Poder Legislativo",
            "Atos do Poder Executivo",
            "Ministério Público da União",
            "Ministério do Trabalho e Previdência",
        ]
        
        for escopo in self.escopo.split("/")[::-1]:
            # caso um dos escopos seja importante
            if escopo in escopos_importantes:
                self.escopo = escopo  # Muda o escopo para ser só o importante
                break

            # Caso não tiver nenhum escopo imporante
            else:
                self.escopo = "Outros"

        self.ementa = self.ementa if self.ementa else ""

        