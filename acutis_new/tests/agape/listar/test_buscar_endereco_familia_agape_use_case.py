import unittest
from unittest.mock import MagicMock, create_autospec
from uuid import uuid4

from acutis_api.application.use_cases.agape.buscar.buscar_endereco_familia_agape import BuscarEnderecoFamiliaAgapeUseCase
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.domain.entities.familia_agape import FamiliaAgape as FamiliaAgapeEntity
from acutis_api.domain.entities.endereco import Endereco as EnderecoEntity
from acutis_api.communication.responses.agape import EnderecoResponse
from acutis_api.exception.errors.not_found import HttpNotFoundError

class TestBuscarEnderecoFamiliaAgapeUseCase(unittest.TestCase):

    def setUp(self):
        self.mock_agape_repository = create_autospec(AgapeRepositoryInterface)
        self.use_case = BuscarEnderecoFamiliaAgapeUseCase(agape_repository=self.mock_agape_repository)

    def test_execute_sucesso(self):
        # Arrange
        familia_id = uuid4()
        endereco_id = uuid4()

        mock_familia = MagicMock(spec=FamiliaAgapeEntity)
        mock_familia.id = familia_id
        mock_familia.fk_endereco_id = endereco_id
        # Adicione outros campos necessários para FamiliaAgapeEntity se o construtor exigir
        # mock_familia.deletado_em = None 

        mock_endereco = MagicMock(spec=EnderecoEntity)
        mock_endereco.id = endereco_id
        mock_endereco.logradouro = "Rua Teste"
        mock_endereco.numero = "123"
        mock_endereco.bairro = "Bairro Teste"
        mock_endereco.cidade = "Cidade Teste"
        mock_endereco.estado = "TS"
        mock_endereco.codigo_postal = "12345-678"
        mock_endereco.complemento = "Apto 101"
        mock_endereco.ponto_referencia = "Perto da praça"
        mock_endereco.latitude = -10.0
        mock_endereco.longitude = -20.0
        # Adicione outros campos necessários para EnderecoEntity

        self.mock_agape_repository.buscar_familia_agape_por_id.return_value = mock_familia
        self.mock_agape_repository.buscar_endereco_por_id.return_value = mock_endereco

        # Act
        result = self.use_case.execute(familia_id=familia_id)

        # Assert
        self.assertIsInstance(result, EnderecoResponse)
        self.assertEqual(result.id, endereco_id)
        self.assertEqual(result.logradouro, "Rua Teste")
        self.assertEqual(result.codigo_postal, "12345-678")
        self.assertEqual(result.ponto_referencia, "Perto da praça")
        self.mock_agape_repository.buscar_familia_agape_por_id.assert_called_once_with(familia_id)
        self.mock_agape_repository.buscar_endereco_por_id.assert_called_once_with(endereco_id)

    def test_execute_familia_nao_encontrada(self):
        # Arrange
        familia_id = uuid4()
        self.mock_agape_repository.buscar_familia_agape_por_id.side_effect = HttpNotFoundError("Família não encontrada")

        # Act & Assert
        with self.assertRaises(HttpNotFoundError) as context:
            self.use_case.execute(familia_id=familia_id)
        self.assertIn("Família não encontrada", str(context.exception))
        self.mock_agape_repository.buscar_familia_agape_por_id.assert_called_once_with(familia_id)
        self.mock_agape_repository.buscar_endereco_por_id.assert_not_called()

    def test_execute_familia_sem_fk_endereco_id(self):
        # Arrange
        familia_id = uuid4()
        mock_familia = MagicMock(spec=FamiliaAgapeEntity)
        mock_familia.id = familia_id
        mock_familia.fk_endereco_id = None # Família sem endereço associado
        # mock_familia.deletado_em = None

        self.mock_agape_repository.buscar_familia_agape_por_id.return_value = mock_familia

        # Act & Assert
        with self.assertRaises(HttpNotFoundError) as context:
            self.use_case.execute(familia_id=familia_id)
        self.assertIn(f"Família ágape {familia_id} não possui endereço associado.", str(context.exception))
        self.mock_agape_repository.buscar_familia_agape_por_id.assert_called_once_with(familia_id)
        self.mock_agape_repository.buscar_endereco_por_id.assert_not_called()

    def test_execute_endereco_nao_encontrado(self):
        # Arrange
        familia_id = uuid4()
        endereco_id = uuid4()

        mock_familia = MagicMock(spec=FamiliaAgapeEntity)
        mock_familia.id = familia_id
        mock_familia.fk_endereco_id = endereco_id
        # mock_familia.deletado_em = None

        self.mock_agape_repository.buscar_familia_agape_por_id.return_value = mock_familia
        self.mock_agape_repository.buscar_endereco_por_id.side_effect = HttpNotFoundError("Endereço não encontrado")

        # Act & Assert
        with self.assertRaises(HttpNotFoundError) as context:
            self.use_case.execute(familia_id=familia_id)
        self.assertIn("Endereço não encontrado", str(context.exception))
        self.mock_agape_repository.buscar_familia_agape_por_id.assert_called_once_with(familia_id)
        self.mock_agape_repository.buscar_endereco_por_id.assert_called_once_with(endereco_id)

if __name__ == '__main__':
    unittest.main()
