from abc import ABC, abstractmethod
from enum import Enum
from collections import Counter

J = 10
Q = 10
K = 10
CARD_TYPES = [2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, 11] #ace must be the last value
BLACKJACK = [10, 11]

THRESH = 21

class playerActions(Enum):
    HIT = 1
    STAND = 0

class cardSet(list[int]):
    """A list of ints that is meant to represent a list of card values"""
    ACE_ALT:int = 1
    def sum(self) -> int:
        """Sums the values contained wihtin the card set"""
        res = 0
        for i in self:
            if res > THRESH and i == CARD_TYPES[-1]:
                res += self.ACE_ALT
            else:
                res += i
        return res
    def isBlackJack(self) -> bool:
        return Counter(self) == Counter(BLACKJACK)

class abstractParticipant(ABC):
    cards:cardSet
    name:str
    funds:int
    @abstractmethod
    def __init__(self, name:str, funds:int) -> None:...

    @abstractmethod
    def setCards(self, *cards:tuple[int]) -> None:
        """Provides the player with the cards"""

    @abstractmethod
    def turn(self, game:'abstractGame') -> playerActions:
        """Handles the player logic, returns an int indicating the action the player wants to take"""

    def __str__(self) -> str:
        return f"{self.name}|{self.funds}:{self.cards}"

    def sum(self) -> int:
        """Returns the sum of all cards the player has"""
        return self.cards.sum()

class abstractPlayer(abstractParticipant):
    @abstractmethod
    def bet(self) -> int:
        """Requests the player bet at the start of the game"""

class abstractDealer(abstractParticipant):
    hiddenCard:int

class abstractGame(ABC):
    dealer:abstractDealer
    players:list[abstractPlayer]
    turnId:int
