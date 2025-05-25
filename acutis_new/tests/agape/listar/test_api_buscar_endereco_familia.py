import json
from http import HTTPStatus
from uuid import uuid4, UUID
from unittest.mock import patch, MagicMock
import unittest # Added for SkipTest

# Importar o 'app' do Flask configurado para testes (geralmente de um conftest.py)
# Exemplo: from acutis_new.tests.conftest import app  # Ajuste este import conforme a estrutura
# Se 'app' não estiver disponível via conftest, pode ser necessário um setup mais complexo.
# Por agora, vamos assumir que 'app' pode ser importado ou acessado.
# Se não, o worker deve informar.

from acutis_api.communication.responses.agape import EnderecoResponse
from acutis_api.exception.errors.not_found import HttpNotFoundError

# Tentativa de importar app - Worker, ajuste se necessário
# O app não é diretamente usado, mas o 'client' fixture de conftest.py o utiliza.
# Não é necessário importar 'app' aqui se estivermos usando a fixture 'client'.


class TestApiBuscarEnderecoFamilia:

    # Helper _get_client removido pois usaremos a fixture 'client' diretamente injetada pelo pytest

    @patch('acutis_api.api.routers.agape.BuscarEnderecoFamiliaAgapeUseCase')
    def test_buscar_endereco_familia_sucesso(self, MockUseCase, client, membro_token): # 'client' e 'membro_token' são fixtures
        familia_id = uuid4()
        endereco_id = uuid4()

        mock_endereco_response_dict = {
            "id": str(endereco_id),
            "logradouro": "Rua Teste API",
            "numero": "123 API",
            "bairro": "Bairro Teste API",
            "cidade": "Cidade Teste API",
            "estado": "TS",
            "codigo_postal": "12345-000",
            "complemento": "Sala 1",
            "ponto_referencia": "Perto do rio",
            "latitude": -11.0,
            "longitude": -21.0,
        }
        mock_response_instance = EnderecoResponse.model_validate(mock_endereco_response_dict)

        mock_use_case_instance = MockUseCase.return_value
        mock_use_case_instance.execute.return_value = mock_response_instance

        # É necessário adicionar o token de autenticação no header
        # Assumindo que existe uma fixture 'membro_token' como em outros testes de API em acutis_new
        # Se não existir, este teste falhará ou precisará de ajuste.
        # Tentarei importar e usar 'membro_token' se estiver disponível em conftest geral.
        # Se o worker souber de um token específico para 'agape' ou um usuário padrão, melhor.
        # Por agora, vou simular um token genérico. Se falhar, o worker precisa avisar.
        # (Nota: A fixture 'membro_token' existe em acutis_new/tests/conftest.py)
        headers = {'Authorization': f'Bearer mock_token_se_necessario'}
        headers = {'Authorization': f'Bearer {membro_token}'}

        response = client.get(f'/agape/buscar-endereco-familia/{str(familia_id)}', headers=headers)
        data = json.loads(response.data)

        assert response.status_code == HTTPStatus.OK
        assert data['id'] == str(endereco_id)
        assert data['logradouro'] == "Rua Teste API"
        assert data['ponto_referencia'] == "Perto do rio"
        MockUseCase.assert_called_once() 
        mock_use_case_instance.execute.assert_called_once_with(familia_id=familia_id)

    @patch('acutis_api.api.routers.agape.BuscarEnderecoFamiliaAgapeUseCase')
    def test_buscar_endereco_familia_nao_encontrada(self, MockUseCase, client, membro_token): # 'client' e 'membro_token' são fixtures
        familia_id = uuid4()

        mock_use_case_instance = MockUseCase.return_value
        mock_use_case_instance.execute.side_effect = HttpNotFoundError("Família não encontrada")
        
        headers = {'Authorization': f'Bearer {membro_token}'}
        response = client.get(f'/agape/buscar-endereco-familia/{str(familia_id)}', headers=headers)
        data = json.loads(response.data)

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert data['detail'] == "Família não encontrada"
        mock_use_case_instance.execute.assert_called_once_with(familia_id=familia_id)

    @patch('acutis_api.api.routers.agape.BuscarEnderecoFamiliaAgapeUseCase')
    def test_buscar_endereco_familia_sem_endereco_associado(self, MockUseCase, client, membro_token): # 'client' e 'membro_token' são fixtures
        familia_id = uuid4()

        mock_use_case_instance = MockUseCase.return_value
        mock_use_case_instance.execute.side_effect = HttpNotFoundError(f"Família ágape {familia_id} não possui endereço associado.")
        
        headers = {'Authorization': f'Bearer {membro_token}'}
        response = client.get(f'/agape/buscar-endereco-familia/{str(familia_id)}', headers=headers)
        data = json.loads(response.data)

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert data['detail'] == f"Família ágape {familia_id} não possui endereço associado."
        mock_use_case_instance.execute.assert_called_once_with(familia_id=familia_id)
        
    @patch('acutis_api.api.routers.agape.BuscarEnderecoFamiliaAgapeUseCase')
    def test_buscar_endereco_familia_endereco_nao_encontrado_no_repositorio(self, MockUseCase, client, membro_token): # 'client' e 'membro_token' são fixtures
        familia_id = uuid4()
        endereco_id_inexistente = uuid4()

        mock_use_case_instance = MockUseCase.return_value
        mock_use_case_instance.execute.side_effect = HttpNotFoundError(f"Endereço {endereco_id_inexistente} não encontrado.")
        
        headers = {'Authorization': f'Bearer {membro_token}'}
        response = client.get(f'/agape/buscar-endereco-familia/{str(familia_id)}', headers=headers)
        data = json.loads(response.data)
        
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert data['detail'] == f"Endereço {endereco_id_inexistente} não encontrado."
        mock_use_case_instance.execute.assert_called_once_with(familia_id=familia_id)

    def test_buscar_endereco_familia_id_invalido(self, client, membro_token): # 'client' e 'membro_token' são fixtures
        headers = {'Authorization': f'Bearer {membro_token}'}
        response = client.get('/agape/buscar-endereco-familia/id-invalido-nao-uuid', headers=headers)
        
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        data = json.loads(response.data)
        
        # Detalhes da mensagem de erro podem variar um pouco com base na versão do Spectree/Pydantic
        error_detail = data.get("detail", {}).get("path", {}).get("familia_id", [{}])[0]
        error_type = error_detail.get("type", "")
        error_msg = error_detail.get("msg", "")

        assert "value_error.uuid" in error_type or "type_error.uuid" in error_type or "uuid_parsing" in error_type
        assert "Valid UUID" in error_msg or "UUID" in error_msg # Mensagem pode ser "Input should be a valid UUID" ou similar

    def test_buscar_endereco_familia_sem_token(self, client): # 'client' é a fixture
        familia_id = uuid4()
        response = client.get(f'/agape/buscar-endereco-familia/{str(familia_id)}')
        # Esperado 401 Unauthorized pois a rota é protegida por @jwt_required()
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        data = json.loads(response.data)
        assert "Missing Authorization Header" in data.get("msg", "") # Mensagem padrão do flask-jwt-extended
