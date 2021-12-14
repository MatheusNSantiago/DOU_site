from datetime import datetime
from typing import List
from model import Publicacao
import boto3
import os
from boto3.dynamodb.conditions import Attr, Key


class SumulaDB:
    def __init__(self) -> None:
        dynamodb = boto3.resource(
            "dynamodb",
            region_name="sa-east-1",
            aws_access_key_id=os.environ["ACCESS_KEY"],
            aws_secret_access_key=os.environ["SECRET_KEY"],
        )

        self._table = dynamodb.Table("sumula-dou")

        self.publicacoes = self.get_all_publications()

    def get_all_publications(self):
        response = self._table.scan()

        resp = response["Items"]
        while "LastEvaluatedKey" in response:
            response = self._table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
            resp.extend(response["Items"])

        # Transforma todas os items que não forem aquele de guardar data (13834509) em publicacoes
        pubs = [Publicacao(**item) for item in resp if item["id_materia"] != "13834509"]

        return pubs

    def publicacoes_do_dia_por_escopo(self, data: str):
        subjects: dict[str, List[Publicacao]] = dict()

        for pub in self.publicacoes:
            if (pub.data == data):
                try:
                    subjects[pub.escopo].append(pub)
                except:
                    subjects[pub.escopo] = [pub]
                    
        for escopo, pubs in subjects.items():
            subjects[escopo] = sorted(pubs, key=lambda pub: pub.titulo)
            

        return subjects

    def get_unique_dates(self):
        response = self._table.get_item(Key={"id_materia": "13834509"})
        item = response["Item"]
        dates = eval(item["conteudo"])

        unique_dates = sorted(
            [datetime.strptime(date, "%Y-%m-%d").date() for date in dates]
        )

        return unique_dates
