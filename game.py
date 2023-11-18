from blackjack import abstractDealer, playerActions, abstractGame, abstractPlayer, abstractParticipant, CARD_TYPES, THRESH
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
        self.bets:dict[abstractPlayer, int] = {}
        for p in self.players:
            self.bets[p] = p.bet()
            p.setCards(self.cards.pop(), self.cards.pop())
            
    def turn(self) -> list[abstractParticipant] | None:
        """Performs a turn, returns None in case game hasn't been resolved yet"""
        self.turnId += 1
        keepGoing = False #if everybody STANDs then this remains false and the game ends
        for p in self.players: #foreach player
            if p.cards.sum() < THRESH:
                action = p.turn(self)
                if action == playerActions.HIT:
                    p.cards.append(self.cards.pop())
                    keepGoing = True
        if not keepGoing:
            return self.resolve()
        return None
    
    def resolve(self) -> list[abstractParticipant]:
        """Determines who is the winner and returns a list of winners"""
        #handle the dealer's turn
        action = self.dealer.turn(self)
        while action != playerActions.STAND:
            if action == playerActions.HIT:
                self.dealer.cards.append(self.cards.pop())
            action = self.dealer.turn(self)
        winner = []
        ignore = []
        #Resolve the dealer
        if self.dealer.cards.isBlackJack(): #if the dealer has a blackjack then he insta wins against everybody who didnt also blackJack
            dealerSum = THRESH + 1
        else:
            dealerSum = self.dealer.sum()
        if dealerSum > THRESH: #if the dealer went bust then everybody wins
            dealerSum = 0
        #Resolve each of the players
        for p in self.players:
            thisSum = p.cards.sum()
            if thisSum <= THRESH:
                if p.cards.isBlackJack():
                    thisSum = THRESH + 1
                if thisSum > dealerSum:
                    winner.append(p)
                elif thisSum == dealerSum:
                    ignore.append(p)
        self.payOut(winner, ignore)
        return winner
    
    def payOut(self, winners:list[abstractParticipant], ignore:list[abstractParticipant]=[]) -> None:
        """Pays out the bets of each winner and collects loser's bets to the dealer"""
        for key, value in self.bets.items():
            if key in winners:
                bonus = int(value * 0.5)
                self.dealer.funds -= bonus
                key.funds += value + bonus
            elif key in ignore:
                key.funds += value
            else:
                self.dealer.funds += value

    def play(self) -> list[abstractParticipant]:
        """Runs turns until a winner presents iself"""
        res = None
        while res == None:
            res = self.turn()
        return res

if __name__ == "__main__":
    game = gameBase(players=(playerBase("AI"), interactivePlayer("Player")))
    res = game.play()
    print(game.dealer)
    print("Winners:")
    for w in res:
        print(str(w))
