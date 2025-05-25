from http import HTTPStatus
from flask.testing import FlaskClient

def test_get_ficha_vocacional(test_client: FlaskClient, seed_admin_user_token, seed_ficha_vocacional):
    
    response = test_client.get(
        "/vocacional/listar-fichas-vocacionais", 
        headers=seed_admin_user_token
    )
    
    assert response.status_code == HTTPStatus.OK
    
    data_response = response.get_json()
    
    assert "fichas_vocacionais" in data_response
    
    key_ficha_vocacional = data_response["fichas_vocacionais"]

    for ficha in key_ficha_vocacional:
        key_cadastro_vocacional = ficha["cadastro_vocacional"]
        
        assert key_cadastro_vocacional
        assert "bairro" in key_cadastro_vocacional and isinstance(key_cadastro_vocacional["bairro"], str)
        assert "cep" in key_cadastro_vocacional and isinstance(key_cadastro_vocacional["cep"], str)
        assert "cidade" in key_cadastro_vocacional and isinstance(key_cadastro_vocacional["cidade"], str)
        assert "created_at" in key_cadastro_vocacional and isinstance(key_cadastro_vocacional["created_at"], str)
        assert "data_nascimento" in key_cadastro_vocacional and isinstance(key_cadastro_vocacional["data_nascimento"], str)
        assert "detalhe_estrangeiro" in key_cadastro_vocacional and isinstance(key_cadastro_vocacional["detalhe_estrangeiro"], str )or key_cadastro_vocacional["detalhe_estrangeiro"] is None
        assert "documento_identidade" in key_cadastro_vocacional and isinstance(key_cadastro_vocacional["documento_identidade"], str)
        assert "email" in key_cadastro_vocacional and isinstance(key_cadastro_vocacional["email"], str)
        assert "estado" in key_cadastro_vocacional and isinstance(key_cadastro_vocacional["estado"], str) or key_cadastro_vocacional["detalhe_estrangeiro"] is None
        assert "fk_usuario_vocacional_id" in key_cadastro_vocacional and isinstance(key_cadastro_vocacional["fk_usuario_vocacional_id"], int)
        assert "genero" in key_cadastro_vocacional and isinstance(key_cadastro_vocacional["genero"], str) and key_cadastro_vocacional["genero"] in ["masculino", "feminino"]
        assert "id" in key_cadastro_vocacional and isinstance(key_cadastro_vocacional["id"], int)
        assert "nome" in key_cadastro_vocacional and isinstance(key_cadastro_vocacional["nome"], str)
        
        assert "pais" in key_cadastro_vocacional and isinstance(key_cadastro_vocacional["pais"], str)
        assert "rua" in key_cadastro_vocacional and isinstance(key_cadastro_vocacional["rua"], str) or key_cadastro_vocacional["rua"] is None
        assert "status" in key_cadastro_vocacional and isinstance(key_cadastro_vocacional["status"], str) and key_cadastro_vocacional["status"] in ["pendente", "aprovado", "reprovado"]
        assert "pais" in key_cadastro_vocacional and isinstance(key_cadastro_vocacional["pais"], str)
        
        key_ficha_do_vocacional = ficha["ficha_do_vocacional"]        
        assert key_ficha_do_vocacional
        
        assert "aceitacao_familiar" in key_ficha_do_vocacional and isinstance(key_ficha_do_vocacional["aceitacao_familiar"], str)
        assert "cursos" in key_ficha_do_vocacional and isinstance(key_ficha_do_vocacional["cursos"], str)
        assert "deixou_religiao_anterior_em" in key_ficha_do_vocacional and isinstance(key_ficha_do_vocacional["deixou_religiao_anterior_em"], str)
        assert "descricao_problema_saude" in key_ficha_do_vocacional and isinstance(key_ficha_do_vocacional["descricao_problema_saude"], str)
        assert "escolaridade" in key_ficha_do_vocacional and isinstance(key_ficha_do_vocacional["escolaridade"], str)
        assert "estado_civil" in key_ficha_do_vocacional and isinstance(key_ficha_do_vocacional["estado_civil"], str)
        assert "fk_usuario_vocacional_id" in key_ficha_do_vocacional and isinstance(key_ficha_do_vocacional["fk_usuario_vocacional_id"], int)
        assert "foto_vocacional" in key_ficha_do_vocacional and isinstance(key_ficha_do_vocacional["foto_vocacional"], str)
        assert "identificacao_instituto" in key_ficha_do_vocacional and isinstance(key_ficha_do_vocacional["identificacao_instituto"], str)
        assert "motivacao_admissao_vocacional" in key_ficha_do_vocacional and isinstance(key_ficha_do_vocacional["motivacao_admissao_vocacional"], str)
        assert "motivacao_instituto" in key_ficha_do_vocacional and isinstance(key_ficha_do_vocacional["motivacao_instituto"], str)
        assert "motivo_divorcio" in key_ficha_do_vocacional and isinstance(key_ficha_do_vocacional["motivo_divorcio"], str) or key_ficha_do_vocacional["motivo_divorcio"] == None
        assert "profissao" in key_ficha_do_vocacional and isinstance(key_ficha_do_vocacional["profissao"], str)
        assert "referencia_conhecimento_instituto" in key_ficha_do_vocacional and isinstance(key_ficha_do_vocacional["referencia_conhecimento_instituto"], str)
        assert "remedio_controlado_inicio" in key_ficha_do_vocacional and isinstance(key_ficha_do_vocacional["remedio_controlado_inicio"], str)
        assert "remedio_controlado_termino" in key_ficha_do_vocacional and isinstance(key_ficha_do_vocacional["remedio_controlado_termino"], str)
        assert "rotina_diaria" in key_ficha_do_vocacional and isinstance(key_ficha_do_vocacional["rotina_diaria"], str)
        assert "seminario_realizado_em" in key_ficha_do_vocacional and isinstance(key_ficha_do_vocacional["seminario_realizado_em"], str)
        assert "testemunho_conversao" in key_ficha_do_vocacional and isinstance(key_ficha_do_vocacional["testemunho_conversao"], str)
        assert "sacramentos" in key_ficha_do_vocacional and isinstance(key_ficha_do_vocacional["sacramentos"], list)

        key_pre_cadastro = ficha["pre_cadastro"]
        assert key_pre_cadastro
        assert "created_at" in key_pre_cadastro and isinstance(key_pre_cadastro["created_at"], str)
        assert "email" in key_pre_cadastro and isinstance(key_pre_cadastro["email"], str)
        assert "id" in key_pre_cadastro and isinstance(key_pre_cadastro["id"], int)
        assert "nome" in key_pre_cadastro and isinstance(key_pre_cadastro["nome"], str)
        assert "status" in key_pre_cadastro and isinstance(key_pre_cadastro["status"], str) and key_pre_cadastro["status"] in ["pendente", "aprovado", "reprovado"]
        assert "telefone" in key_pre_cadastro and isinstance(key_pre_cadastro["telefone"], str)
        
        
        

    