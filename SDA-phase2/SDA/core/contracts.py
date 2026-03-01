"""
core/contracts.py
-----------------
The Core owns and defines ALL contracts (Protocols).
Other modules must satisfy these shapes — no inheritance required (structural typing).
"""

from typing import Protocol, List, Any, runtime_checkable

@runtime_checkable
class DataSink(Protocol):
    """
    Outbound Abstraction.
    The Core calls `write()` to push results out.
    Any Output plugin must implement this exact signature.
    """
    def write(self, report_type: str, data: Any) -> None:
        ...


class PipelineService(Protocol):
    """
    Inbound Abstraction.
    The Input plugin calls `execute()` to hand raw records to the Core.
    Any Input plugin must call this to pass data in.
    """
    def execute(self, raw_data: List[Any]) -> None:
        ...
