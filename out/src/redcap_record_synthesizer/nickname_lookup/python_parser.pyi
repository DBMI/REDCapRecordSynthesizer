from . import get_data as get_data
from typing import Any, Optional, Union

class NicknameGenerator:
    def __init__(self, filename: Optional[Any] = ...) -> None: ...
    def get(self, name: str, default: Optional[str]=...) -> Union[Optional[str], Optional[list]]: ...
