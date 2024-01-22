"""Superclass for llm tools."""
from abc import ABC, abstractmethod

class Tool(ABC):
    """Superclass for llm tools."""
    def __init__(self, function_definition):
        self.function_definition = function_definition

    @classmethod
    @abstractmethod
    def call(cls, kwargs):
        """This is the method that is called when the tool is used."""
        raise NotImplementedError("Subclasses must implement call()")
    