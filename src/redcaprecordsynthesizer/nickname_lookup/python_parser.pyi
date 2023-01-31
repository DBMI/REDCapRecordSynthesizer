from typing import Optional, Union

class NicknameGenerator:
    def __init__(self, filename: str = ...) -> None:
        self.__names = None
        self.__names_dict = None
        ...
    def get(
        self, name: str, default: Optional[str] = ...
    ) -> Union[Optional[str], Optional[list]]: ...
    @classmethod
    def __names_file(cls):
        pass
