from acutis_api.communication.responses.agape import ItemEstoqueAgapeResponse
from acutis_api.domain.repositories.agape import AgapeRepositoryInterface


class AdicionarVoluntarioAgapeUseCase:
    """
    Caso de uso para adicionar um voluntário
    """

    def __init__(
        self,
        agape_repository: AgapeRepositoryInterface,
    ):
        self.__repository = agape_repository

    def execute(
        self,
        lead_id,
    ) -> dict:
        # Busca o item de estoque pelo ID
        self.__repository.adicionar_voluntario_agape(lead_id)

        # Persiste as alterações
        self.__repository.salvar_alteracoes()

        return 

    """
    def update_user_profile_to_agape_voluntary(
        self, fk_usuario_id: Usuario
    ) -> None:
        db_usuario: Usuario = self.__database.session.get(
            Usuario, fk_usuario_id
        )
        if not db_usuario or db_usuario.deleted_at is not None:
            raise NotFoundError("Usuário não encontrado.")

        perfil = Perfil.query.filter_by(
            nome=ProfilesEnum.VOLUNTARIO_AGAPE
        ).first()
        if not perfil:
            raise NotFoundError("Perfil de voluntário não encontrado.")

        permissao_usuario = PermissaoUsuario.query.filter_by(
            fk_usuario_id=db_usuario.id
        ).first()

        permissao_usuario.fk_perfil_id = perfil.id

        try:
            self.__database.session.commit()
        except Exception as exception:
            self.__database.session.rollback()
            raise exception
    """