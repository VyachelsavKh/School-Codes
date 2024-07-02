from abc import ABCMeta, abstractmethod

class IUpdatingSelector(metaclass=ABCMeta):
    @abstractmethod
    def update_values(self):
        pass
    
    @abstractmethod
    def get_value(self) -> str:
        pass

    @abstractmethod
    def clear(self):
        pass