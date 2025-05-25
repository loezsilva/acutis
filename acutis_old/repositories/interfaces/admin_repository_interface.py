from abc import ABC, abstractmethod
from typing import List

from models.usuario import Usuario


class AdminRepositoryInterface(ABC):

    @abstractmethod
    def get_all_regular_users(self) -> List[Usuario]: ...

    @abstractmethod
    def get_regular_users_quantity(self) -> int: ...
