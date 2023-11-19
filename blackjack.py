from abc import ABC, abstractmethod
from enum import Enum
from collections import Counter

J = 10
Q = 10
K = 10
CARD_TYPES = [2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, 11] #ace must be the last value
BLACKJACK = [10, 11]

THRESH = 21

DOUBLE_TURN_LIMIT = 1

class playerActions(Enum):
    """Enumerator of actions a participant may take"""
    STAND = 0
    HIT = 1
    DOUBLE_DOWN = 2
    SPLIT = 3

class cardSet(list[int]):
    """A list of ints that is meant to represent a list of card values"""
    ACE_ALT:int = 1
    def sum(self) -> int:
        """Sums the values contained wihtin the card set"""
        self.sort()
        res = 0
        for i in self:
            temp = res + i
            if temp > THRESH and i == CARD_TYPES[-1]:
                res += self.ACE_ALT
            else:
                res = temp
        return res
    def isBlackJack(self) -> bool:
        return Counter(self) == Counter(BLACKJACK)

class abstractHand(ABC):
    """Abstract class that represents a participant's hand"""
    cards:cardSet
    player:'abstractPlayer'
    @abstractmethod
    def __init__(self, player:'abstractPlayer', *cards:tuple[int]) -> None:...

    @abstractmethod
    def giveCard(self, card:int) -> None:
        """Appends the underlying cardSet with the given card"""

    @abstractmethod
    def sum(self) -> int:
        """Returns the sum of the held cards"""

    @abstractmethod
    def setCards(self, *cards:int) -> None:
        """Set's this hand's cards to the provided cards"""

    @abstractmethod
    def __str__(self) -> str:...

class abstractParticipant(ABC):
    """Abstract class that represents a blackjack participant, so either a dealer or a player"""
    name:str #for cosmetic purposes
    funds:int
    @abstractmethod
    def __init__(self, name:str, funds:int) -> None:...

    @abstractmethod
    def turn(self, dealerCards:cardSet, hand:abstractHand, turnId:int) -> playerActions:
        """Handles the player logic, returns an int indicating the action the player wants to take"""

class abstractPlayer(abstractParticipant):
    @abstractmethod
    def bet(self) -> int:
        """Requests the player's bet"""

class abstractDealer(abstractParticipant, abstractHand):
    """Abstract class that represent's a blackjack dealer, since a dealer cannot hold multiple hands it inherits from both participant and hand"""
    hiddenCard:int

class abstractGame(ABC):
    dealer:abstractDealer
    hands:list[abstractHand]
    bets:dict[abstractHand, int]
    turnId:int

class hand(abstractHand):
    def __init__(self, player:abstractPlayer, *cards:tuple[int]) -> int:
        self.player = player
        self.cards = cardSet(cards)
    def giveCard(self, card:int) -> None:
        self.cards.append(card)
    def setCards(self, *cards:int) -> None:
        self.cards.extend(cards)
    def sum(self) -> int:
        """Returns the sum of all cards the player has"""
        return self.cards.sum()
    def __str__(self) -> str:
        return f"{self.player.name}:{self.cards}"
    