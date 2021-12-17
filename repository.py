from typing import List
from model import Publicacao
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import datetime
import os

class SumulaDB:
    def __init__(self) -> None:
        cred = credentials.Certificate(
            {
                "type": "service_account",
                "project_id": "sumula-dou",
                "private_key_id": "83ab6174f69ce38bc55133d7ef9507e86f5f5e52",
                "private_key": os.environ["PRIVATE_KEY"],
                "client_email": "firebase-adminsdk-hdk8k@sumula-dou.iam.gserviceaccount.com",
                "client_id": os.environ["CLIENT_ID"],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-hdk8k%40sumula-dou.iam.gserviceaccount.com",
            }
        )
        firebase_admin.initialize_app(cred, {"projectId": "sumula-dou"})
        self.db = firestore.client()

    def publicacoes_do_dia_por_escopo(self, data):
        subjects: dict[str, List[Publicacao]] = dict()

        docs = self.db.collection(data).stream()
        for doc in docs:
            pub = Publicacao(**doc.to_dict())
            subjects.setdefault(pub.escopo, []).append(pub)

        for escopo, pubs in subjects.items():
            subjects[escopo] = sorted(pubs, key=lambda pub: pub.titulo)

        return subjects

    def get_unique_dates(self):
        collections = self.db.collections()
        to_date = lambda x: datetime.datetime.strptime(x, "%Y-%m-%d").date()
        return [to_date(collection.id) for collection in collections]
