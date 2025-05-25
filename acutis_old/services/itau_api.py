from typing import Dict, Literal
import requests
import uuid


from config import (
    ITAU_URL_AUTH,
    ITAU_PIX_CLIENT_ID,
    ITAU_PIX_CLIENT_SECRET,
    ITAU_BOLETO_CLIENT_ID,
    ITAU_BOLETO_CLIENT_SECRET,
    ITAU_URL_BOLETO,
    ITAU_URL_PIX,
    ITAU_URL_BOLECODE,
)


class ItauAPI:
    def __init__(
        self, auth_type: Literal["pix", "bolecode", "pix_recebimentos", "boleto"]
    ):
        if auth_type not in ["pix", "bolecode", "pix_recebimentos", "boleto"]:
            raise ValueError("Tipo de autenticação inválida!")

        MAP_CLIENT_ID = {
            "pix": ITAU_PIX_CLIENT_ID,
            "bolecode": ITAU_PIX_CLIENT_ID,
            "pix_recebimentos": ITAU_PIX_CLIENT_ID,
            "boleto": ITAU_BOLETO_CLIENT_ID,
        }

        MAP_CLIENT_SECRET = {
            "pix": ITAU_PIX_CLIENT_SECRET,
            "bolecode": ITAU_PIX_CLIENT_SECRET,
            "pix_recebimentos": ITAU_PIX_CLIENT_SECRET,
            "boleto": ITAU_BOLETO_CLIENT_SECRET,
        }

        MAP_BASE_URL = {
            "pix": ITAU_URL_PIX,
            "bolecode": ITAU_URL_BOLECODE,
            "pix_recebimentos": ITAU_URL_BOLECODE,
            "boleto": ITAU_URL_BOLETO,
        }

        self.type = auth_type
        self.auth_url = ITAU_URL_AUTH
        self.client_id = MAP_CLIENT_ID[auth_type]
        self.client_secret = MAP_CLIENT_SECRET[auth_type]
        self.certificate = self.load_certificate(auth_type)
        self.token = None
        self.base_url = MAP_BASE_URL[auth_type]

    def load_certificate(self, auth_type: str):
        cert_filename = (
            "./archives/certificado_pix.crt"
            if auth_type in ["pix", "bolecode", "pix_recebimentos"]
            else "./archives/certificado_boleto.crt"
        )
        key_filename = (
            "./archives/chave_pix.key"
            if auth_type in ["pix", "bolecode", "pix_recebimentos"]
            else "./archives/chave_boleto.key"
        )
        return (cert_filename, key_filename)

    def get_token(self):
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        headers = {
            "x-itau-flowID": "1",
            "x-itau-correlationID": "2",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = requests.post(
            url=self.auth_url, data=payload, headers=headers, cert=self.certificate
        )

        if response.status_code == 200:
            token_data = response.json()
            self.token = token_data.get("access_token")
        else:
            raise Exception(
                f"Ocorreu um erro ao gerar o token. Status code: {response.status_code} - {response.text}"
            )

    def put(self, path: str, body):
        self.get_token()
        url = self.base_url + path

        headers = {
            "x-itau-apikey": self.client_id,
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        response = requests.put(url, json=body, headers=headers, cert=self.certificate)

        try:
            return response.json(), response.status_code
        except:
            raise Exception(
                f"Ocorreu um erro ao requisitar o PUT. Status code: {response.status_code}"
            )

    def get(self, path: str, params: Dict = None):
        self.get_token()
        url = self.base_url + path

        headers = {
            "x-itau-apikey": self.client_id,
            "Authorization": f"Bearer {self.token}",
            "x-itau-correlationID": str(uuid.uuid4()),
            "x-itau-flowID": str(uuid.uuid4()),
            "Content-Type": "application/json",
        }

        response = requests.get(
            url, params=params, headers=headers, cert=self.certificate
        )

        try:
            return response.json(), response.status_code
        except:
            raise Exception(
                f"Ocorreu um erro ao requisitar o GET. Status code: {response.status_code}"
            )

    def post(self, path: str, body) -> tuple:
        self.get_token()
        url = self.base_url + path

        headers = {
            "x-itau-apikey": self.client_id,
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        response = requests.post(url, json=body, headers=headers, cert=self.certificate)

        try:
            return response.json(), response.status_code
        except:
            raise Exception(
                f"Ocorreu um erro ao requisitar o POST. Status code: {response.status_code}"
            )
