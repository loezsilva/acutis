import faker    
from flask.testing import FlaskClient
import json
import io

from tests.integration.campaign.post.test_create_campaign import generate_fake_image

faker = faker.Faker("pt_BR")

def test_update_campaign_success(
    test_client: FlaskClient,
    seed_admin_user_token,
    seed_campaign,
):
    
    campaign = seed_campaign
    imagem_capa = generate_fake_image()
    banner = generate_fake_image()

    data_to_update = {
        "descricao": faker.text(),
        "banner": "https://hesed-bucket.s3.amazonaws.com/landing_page_Teste%20register%20campaign_banner_9a34cda2-c4ff-4e3a-8c10-46600781a768.jpg?AWSAccessKeyId=AKIASPOWJHOT6GGQWXYD&Signature=rAFgfULelCMgc8yw7sFqQfvpClc%3D&Expires=1738334700",
        "id": faker.random_int(min=1, max=100),
        "texto_email_pos_registro": faker.text(),
        "texto_pos_registro": faker.text(),
        "tipo_cadastro": "Benfeitor",
        "titulo": faker.text(),
        "url": faker.url(),
        "cadastros_meta": faker.random_int(min=1, max=100),
        "cadastros_total_atingido": faker.random_int(min=1, max=100),
        "cadastros_total_mes_atual": faker.random_int(min=1, max=100),
        "campanha_nome": faker.text(),
        "chave_pix": None,
        "data_alteracao": None,
        "data_criacao": str(faker.date_time()),
        "data_fim": None,
        "data_inicio": None,
        "duracao": "permanente",
        "filename": "https://hesed-bucket.s3.amazonaws.com/campanha_Teste%20register%20campaign_e5f32a00-1c21-47ad-992d-b17a2b12077f_capa.jpg?AWSAccessKeyId=AKIASPOWJHOT6GGQWXYD&Signature=WeJmv2lOGDH%2BrN7IKD%2BL44y3hh4%3D&Expires=1738334700",
        "label_foto": None,
        "objetivo": "cadastro",
        "preenchimento_foto": False,
        "publica": 0,
        "status": 0,
        "valor_meta": None,
        "valor_total": None,
        "valor_total_mes_atual": None,
        "cadastrar_landing_page": 1
    }
    
    form_data = {
        "data": json.dumps(data_to_update),
        "imagem_capa": (io.BytesIO(imagem_capa), "disc-bg.jpg", "image/jpeg"),
        "banner": (io.BytesIO(banner), "disc-bg.jpg", "image/jpeg"),
    }

    response = test_client.put(
        f"/campaigns/{campaign.id}",
        content_type="multipart/form-data",
        data=form_data,
        headers=seed_admin_user_token,
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["msg"] == "Campanha atualizada com sucesso."
    
    