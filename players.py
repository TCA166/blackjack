from blackjack import abstractPlayer, abstractDealer, playerActions, cardSet, hand, abstractHand, DOUBLE_TURN_LIMIT

def safeFunc(func):
    def inner(*args, **kwargs):
        for arg in args:
            t = type(arg)
            arg = t(arg)
        for key, value in kwargs.items():
            t = type(value)
            kwargs[key] = t(value)
        func(*args, **kwargs)
    return inner

class dealerBase(abstractDealer, hand):
    """Basic dealer that follows all the standard rules"""
    def __init__(self, name:str, funds:int=1000) -> None:
        self.player = self
        self.name = name
        self.funds = funds
        self.cards = cardSet()

    def setCards(self, *cards: int) -> None:
        self.hiddenCard = cards[0]
        return super().setCards(*cards[1:])

    def sum(self) -> int:
        return self.cards.sum() + self.hiddenCard
    
    def turn(self, dealerCards:cardSet, hand:abstractHand, turnId:int) -> playerActions:
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

    def turn(self, dealerCards:cardSet, hand:abstractHand, turnId:int) -> playerActions:
        if hand.sum() > 11:
            return playerActions.STAND
        return playerActions.HIT
    
    def bet(self) -> int:
        bet = int(self.funds / 4)
        self.funds -= bet
        return bet

class interactivePlayer(playerBase):
    def turn(self, dealerCards:cardSet, hand:abstractHand, turnId:int) -> playerActions:
        print(f"Turn:{turnId}========")
        print(f"Dealer cards:[X]{dealerCards}")
        print(str(hand))
        while True:
            action = input("Hit, stand or double down?[H/S/D]").capitalize()
            if action == "H":
                return playerActions.HIT
            elif action == "S":
                return playerActions.STAND
            elif action == "D":
                if turnId > DOUBLE_TURN_LIMIT:
                    print("Too late to double down")
                else:
                    return playerActions.DOUBLE_DOWN
            else:
                print("Command misunderstood")
    def bet(self) -> int:
        print(f"Funds:{self.funds}")
        bet = int(input("Input bet:"))
        self.funds -= bet
        return bet
