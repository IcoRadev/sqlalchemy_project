import abc


class Entity(abc.ABC):
    def __enter__(self):
        return self
    #
    # @abc.abstractmethod
    # def add(self):
    #     raise NotImplementedError
    #
    # @abc.abstractmethod
    # def remove(self):
    #     raise NotImplementedError
    #
    # @abc.abstractmethod
    # def get(self):
    #     raise NotImplementedError
