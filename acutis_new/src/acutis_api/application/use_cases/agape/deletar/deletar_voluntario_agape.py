import uuid

from acutis_api.communication.enums.membros import PerfilEnum
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface
from acutis_api.exception.errors.not_found import HttpNotFoundError


class DeletarVoluntarioAgapeUseCase:
    def __init__(self, agape_repository: AgapeRepositoryInterface):
        self.agape_repository = agape_repository

    # db_usuario: Usuario = self.__database.session.get(
    #     Usuario, fk_usuario_id
    # )
    # if not db_usuario or db_usuario.deleted_at is not None:
    #     raise NotFoundError("Usuário não encontrado.")

    # permissao_usuario = PermissaoUsuario.query.filter_by(
    #     fk_usuario_id=db_usuario.id
    # ).first()

    # perfil_atual = self.__database.session.get(
    #     Perfil, permissao_usuario.fk_perfil_id
    # )
    # if perfil_atual.nome != ProfilesEnum.VOLUNTARIO_AGAPE:
    #     raise NotFoundError(
    #         "Não é possível remover um usuário que não é um voluntário."
    #     )

    # perfil_benfeitor = Perfil.query.filter_by(
    #     nome=ProfilesEnum.BENFEITOR
    # ).first()
    # if not perfil_benfeitor:
    #     raise NotFoundError("Perfil de benfeitor não encontrado.")

    # permissao_usuario.fk_perfil_id = perfil_benfeitor.id

    # try:
    #     self.__database.session.commit()
    # except Exception as exception:
    #     self.__database.session.rollback()
    #     raise exception

    def execute(self, lead_id: uuid.UUID) -> None:
        nome_perfil_voluntario = PerfilEnum.voluntario_agape.value
        nome_perfil_benfeitor = PerfilEnum.benfeitor.value

        lead = self.agape_repository.buscar_lead_por_id(id=lead_id)

        if not lead:
            raise HttpNotFoundError(f'Lead com ID {lead_id} não encontrado.')

        if nome_perfil_voluntario not in lead.nomes_dos_perfis:
            raise HttpNotFoundError(
                'Não é possível remover um usuário que não é um voluntário.'
            )

        permissao_lead = lead.permissoes_lead[0]

        perfil_voluntario = self.agape_repository.buscar_perfil_por_nome(
            nome_perfil_voluntario
        )

        perfil_benfeitor = self.agape_repository.buscar_perfil_por_nome(
            nome_perfil_benfeitor
        )

        if not perfil_voluntario:
            raise HttpNotFoundError(
                f"Perfil '{nome_perfil_voluntario}' não encontrado no sistema."
            )

        if not perfil_benfeitor:
            raise HttpNotFoundError('Perfil de benfeitor não encontrado.')

        permissao_lead.perfil_id = perfil_benfeitor.id

        self.agape_repository.salvar_alteracoes()
