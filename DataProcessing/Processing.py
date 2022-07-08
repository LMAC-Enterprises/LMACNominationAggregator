from abc import ABC, abstractmethod


class MessagesProcessingBase(ABC):
    @abstractmethod
    def processMessages(self, messages: list):
        pass

    @abstractmethod
    def getGeneratedText(self) -> str:
        pass
