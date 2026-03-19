from abc import ABC, abstractmethod


class NotificationStrategy(ABC):
    """
    Strategy Pattern — Abstract interface.
    Bütün bildiriş tipləri bu classdən miras alır.
    """

    @abstractmethod
    def send(self, recipient: str, subject: str, message: str) -> bool:
        pass


class NotificationContext:
    """
    Strategy Pattern — Context class.
    Hansı strategiyanı istifadə edəcəyini saxlayır.
    Runtime-da strategiyanı dəyişmək olar.
    """

    def __init__(self, strategy: NotificationStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: NotificationStrategy):
        """Strategiyanı dəyiş"""
        self._strategy = strategy

    def notify(self, recipient: str, subject: str, message: str) -> bool:
        """Seçilmiş strategiya ilə bildiriş göndər"""
        return self._strategy.send(recipient, subject, message)