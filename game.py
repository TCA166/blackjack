from blackjack import abstractDealer, playerActions, abstractGame, abstractPlayer, CARD_TYPES, THRESH
from random import shuffle
from players import dealerBase, interactivePlayer, playerBase

class gameBase(abstractGame):
    """A basic game of blackjack"""
    def __init__(self, dealer:abstractDealer=dealerBase("Dealer"), players:tuple[abstractPlayer]=(interactivePlayer("Player"), ), deckNum:int=1) -> None:
        self.cards = []
        for i in range(deckNum):
            self.cards.extend(CARD_TYPES)
        shuffle(self.cards)
        self.turnId = 0
        self.dealer = dealer
        self.dealer.setCards(self.cards.pop(), self.cards.pop())
        self.players = players
        self.bets = {}
        for p in self.players:
            self.bets[p] = p.bet()
            p.setCards(self.cards.pop(), self.cards.pop())
            
    def turn(self) -> list[abstractPlayer] | None:
        """Performs a turn, returns None in case game hasn't been resolved yet"""
        self.turnId += 1
        keepGoing = False #if everybody STANDs then this remains false and the game ends
        for p in self.players: #foreach player
            if p.cards.sum() < THRESH:
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
            if p.cards.isBlackJack():
                if highest != THRESH + 1:
                    winner = [p]
                    highest = THRESH + 1
                else:
                    winner.append(p)
            else:
                thisSum = p.cards.sum()
                if thisSum <= THRESH:
                    if highest < thisSum:
                        highest = thisSum
                        winner = [p]
                    elif highest == thisSum:
                        winner.append(p)
        #Resolve the dealer
        dealerSum = self.dealer.cards.sum() + self.dealer.hiddenCard
        if self.dealer.cards.isBlackJack():
            if highest != THRESH + 1:
                winner = [self.dealer]
                highest = THRESH + 1
            else:
                winner.append(self.dealer)
        else:
            if dealerSum <= THRESH:
                if highest < dealerSum:
                    winner = [self.dealer]
                elif highest == dealerSum:
                    winner.append(self.dealer)
        #pay out the bets
        #TODO finish
        for key, value in self.bets.items():
            if key in winner:
                value = int(value * 1.5)
                self.dealer.funds -= value
                key.funds += value
            else:
                self.dealer.funds += value
        return winner
    
    def play(self) -> list[abstractPlayer]:
        """Runs turns until a winner presents iself"""
        res = None
        while res == None:
            res = self.turn()
        return res

if __name__ == "__main__":
    game = gameBase(players=(playerBase("AI"), interactivePlayer("Player")))
    print("Winners:")
    for w in game.play():
        print(str(w))
