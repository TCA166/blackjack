from blackjack import abstractPlayer, abstractDealer, playerActions, abstractGame, cardSet

class dealerBase(abstractDealer):
    """Basic dealer that follows all the standard rules"""
    def __init__(self, name:str, funds:int=1000) -> None:
        self.name = name
        self.funds = funds
    
    def setCards(self, hiddenCard:int, *cards:tuple[int]) -> None:
        self.hiddenCard = hiddenCard
        self.cards = cardSet(cards)

    def sum(self) -> int:
        return self.cards.sum() + self.hiddenCard
    
    def turn(self, game:abstractGame) -> playerActions:
        if self.sum() < 17:
            return playerActions.HIT
        return playerActions.STAND
    
    def __str__(self) -> str:
        return f"{self.name}|{self.funds}:{str([self.hiddenCard] + self.cards)}"

class playerBase(abstractPlayer):
    """Basic player that implements the never bust strategy"""
    def __init__(self, name:str, funds:int=100) -> None:
        self.name = name
        self.funds = funds

    def setCards(self, *cards:int) -> None:
        self.cards = cardSet(cards)

    def turn(self, game:abstractGame) -> playerActions:
        if self.sum() > 11:
            return playerActions.STAND
        return playerActions.HIT
    
    def bet(self) -> int:
        bet = int(self.funds / 4)
        self.funds -= bet
        return bet

class interactivePlayer(playerBase):
    def turn(self, game:abstractGame) -> playerActions:
        print(f"Turn:{game.turnId}========")
        print(f"Dealer cards:[X]{game.dealer.cards}")
        for p in game.players:
            if p != self:
                print(f"{p.name} cards:{p.cards}")
        print(str(self))
        while True:
            action = input("Hit or stand?[H/S]").capitalize()
            if action == "H":
                return playerActions.HIT
            elif action == "S":
                return playerActions.STAND
            else:
                print("Command misunderstood")
    def bet(self) -> int:
        print(f"Funds:{self.funds}")
        bet = int(input("Input bet:"))
        self.funds -= bet
        return bet
