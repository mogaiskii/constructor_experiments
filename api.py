import abc


class ComponentRelationAbstract(abc.ABC):
    @property
    @abc.abstractmethod
    def price(self): ...

    @property
    @abc.abstractmethod
    def title(self): ...
