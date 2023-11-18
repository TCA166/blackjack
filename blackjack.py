from abc import ABC, abstractmethod
from random import shuffle
from enum import Enum

J = 10
Q = 10
K = 10
CARD_TYPES = [2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K, 11] #ace must be the last value

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

class abstractPlayer(ABC):
    cards:cardSet
    name:str

    @abstractmethod
    def __init__(self, name:str, *cards:tuple[int]) -> None:...

    @abstractmethod
    def turn(self, game:'abstractGame') -> playerActions:
        """Handles the player logic, returns an int indicating the action the player wants to take"""
        ...

    def sum(self) -> int:
        """Returns the sum of all cards the player has"""
        return self.cards.sum()

class abstractGame(ABC):
    dealer:abstractPlayer
    players:list[abstractPlayer]
    turnId:int

class dealerBase(abstractPlayer):
    def __init__(self, name:str, hiddenCard:int, *cards:tuple[int]) -> None:
        self.name = name
        self.hiddenCard = hiddenCard
        self.cards = cardSet(cards)
    def sum(self) -> int:
        return self.cards.sum() + self.hiddenCard
    def turn(self, game:abstractGame) -> playerActions:
        if self.sum() < 17:
            return playerActions.HIT
        return playerActions.STAND

class playerBase(abstractPlayer):
    """Basic player that implements the never bust strategy"""
    def __init__(self, name:str, *cards: tuple[int]) -> None:
        self.name = name
        self.cards = cardSet(cards)
    def turn(self, game:abstractGame) -> playerActions:
        if self.sum() > 11:
            return playerActions.STAND
        return playerActions.HIT

class interactivePlayer(playerBase):
    def turn(self, game:abstractGame) -> playerActions:
        print(f"Turn:{game.turnId}========")
        print(f"Dealer cards:[X]{game.dealer.cards}")
        for p in game.players:
            if p != self:
                print(f"{p.name} cards:{p.cards}")
        print(f"My cards:{self.cards}")
        while True:
            action = input("Hit or stand?[H/S]").capitalize()
            if action == "H":
                return playerActions.HIT
            elif action == "S":
                return playerActions.STAND
            else:
                print("Command misunderstood")

class gameBase(abstractGame):
    def __init__(self, dealer:type=dealerBase, players:tuple[tuple[type, str]]=((interactivePlayer, "Player"),), deckNum:int=1) -> None:
        self.cards = []
        for i in range(deckNum):
            self.cards.extend(CARD_TYPES)
        shuffle(self.cards)
        self.turnId = 0
        self.dealer:dealerBase = dealer("Dealer", self.cards.pop(), self.cards.pop())
        self.players:tuple[abstractPlayer] = tuple(t[0](t[1], self.cards.pop(), self.cards.pop()) for t in players)
    def turn(self) -> list[abstractPlayer] | None:
        """Performs a turn, returns None in case game hasn't been resolved yet"""
        self.turnId += 1
        keepGoing = False #if everybody STANDs then this remains false and the game ends
        for p in self.players: #foreach player
            if p.cards.sum() > THRESH:
                break
            action = p.turn(self)
            if action == playerActions.HIT:
                p.cards.append(self.cards.pop())
                keepGoing = True
        #handle the dealer's turn
        if self.dealer.sum() <= THRESH and self.dealer.turn(self) == playerActions.HIT:
            self.dealer.cards.append(self.cards.pop())
            keepGoing = True
        if not keepGoing:
            return self.resolve()
        return None
    def resolve(self) -> list[abstractPlayer]:
        """Determines who is the winner and returns a list of winners"""
        winner = list()
        highest = 0
        #Resolve each of the players
        for p in self.players:
            thisSum = p.cards.sum()
            if thisSum <= THRESH:
                if highest < thisSum:
                    highest = thisSum
                    winner = [p]
                elif highest == thisSum:
                    winner.append(p)
        #Resolve the dealer
        dealerSum = self.dealer.cards.sum() + self.dealer.hiddenCard
        if dealerSum <= THRESH:
            if highest < dealerSum:
                winner = [self.dealer]
            elif highest == dealerSum:
                winner.append(self.dealer)
        return winner
    def play(self) -> list[abstractPlayer]:
        """Runs turns until a winner presents iself"""
        res = None
        while res == None:
            res = self.turn()
        return res

if __name__ == "__main__":
    game = gameBase(players=((playerBase, "AI"), (interactivePlayer, "Player")))
    for w in game.play():
        print(w.name)
