from abc import ABC
from typing import Any, AsyncGenerator, Union

class Agent(ABC):
    async def run(
        self, messages: list[dict], stream: bool = False
    ) -> Union[dict[str, Any], AsyncGenerator[dict[str, Any], None]]:
        raise NotImplementedError