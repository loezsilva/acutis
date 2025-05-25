from exceptions.error_types.http_forbidden import ForbiddenError
from handlers.vocacional.utils.verificar_permissoes_vocacional import verificar_permissoes_vocacional
from models import vocacional
from repositories.interfaces.vocacional.vocacional_repository_interface import InterfaceVocacionalRepository

class DeletarVocacional:
    def __init__(self, vocacional_repository: InterfaceVocacionalRepository):
        self.__vocacional_repository = vocacional_repository        

    def execute(self, fk_usuario_vocacional_id: int):
        
        vocacional = self.__vocacional_repository.get_usuario_vocacional(fk_usuario_vocacional_id)
        
        filtros_permissoes = verificar_permissoes_vocacional()

        if (
            vocacional.genero != filtros_permissoes["deletar"]
            and 
            filtros_permissoes["deletar"] != "todos"   
        ):
            
            raise ForbiddenError("Você não tem permissão para relizar está ação")
        
        return self.__vocacional_repository.delete_vocacional(fk_usuario_vocacional_id)
        
