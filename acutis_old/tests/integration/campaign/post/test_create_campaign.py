import io
import json
from flask.testing import FlaskClient
from PIL import Image

def generate_fake_image():
    image = Image.new("RGB", (100, 100), color=(255, 0, 0))
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="JPEG")
    image_bytes.seek(0)
    return image_bytes.read() 

def test_create_campaign_register_campaign_success(
    test_client: FlaskClient, seed_admin_user_token
):
    imagem_capa = generate_fake_image()
    imagem_fundo = generate_fake_image()
    banner = generate_fake_image()

    data_campaign = {  
        "status": 0,
        "publica": 0,
        "preenchimento_foto": False,
        "duracao": "permanente",
        "objetivo": "cadastro",
        "cadastrar_landing_page": 1,
        "titulo": "Teste register campaign",
        "label_foto": None,
        "data_inicio": None,
        "data_fim": None,
        "descricao": "abndabodfbofdfsdfsd",
        "texto_email_pos_registro": "aaaaaaaa",
        "texto_pos_registro": "bbbbbbbbb",
        "url": "dhnoasobdaso34",
        "valor_meta": None,
        "cadastros_meta": "123",
        "tipo_cadastro": "Benfeitor",
    }

    form_data = {
        "data": json.dumps(data_campaign),  
        "imagem_capa": (io.BytesIO(imagem_capa), "disc-bg.jpg", "image/jpeg"),
        "imagem_fundo": (io.BytesIO(imagem_fundo), "background.jpg", "image/jpeg"),
        "banner": (io.BytesIO(banner), "banner.jpg", "image/jpeg"),
    }

    response = test_client.post(
        "/campaigns",
        data=form_data,  
        headers=seed_admin_user_token,
    )

    assert response.status_code == 201
    data = response.get_json()
    assert data["msg"] == "Campanha cadastrada com sucesso."