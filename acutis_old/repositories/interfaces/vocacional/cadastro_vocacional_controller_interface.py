from abc import ABC, abstractmethod
from ast import Dict, Tuple
from http import HTTPStatus


class CadastroVocacionalControllerInterface(ABC):
    @abstractmethod
    def execute(self): pass
        
    @abstractmethod
    def __handler_register_cadastro_vocacional(self, data_to_insert: Dict) -> Tuple:
        pass