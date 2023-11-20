from blackjack import abstractPlayer, abstractDealer, playerActions, cardSet, hand, abstractHand, DOUBLE_TURN_LIMIT

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
    
    def bet(self, hand:abstractHand | None = None) -> int:
        bet = int(self.funds / 4)
        self.funds -= bet
        return bet

class interactivePlayer(playerBase):
    def turn(self, dealerCards:cardSet, hand:abstractHand, turnId:int) -> playerActions:
        print(f"Turn:{turnId}")
        print(f"Dealer cards:[X]{dealerCards}")
        print(str(hand))
        while True:
            actionNames = ["Hit", "stand"]
            if turnId <= DOUBLE_TURN_LIMIT:
                actionNames.append("double down")
            if hand.cards[0] == hand.cards[1] and turnId == 1:
                actionNames.append("split")
            actions = tuple(a[0:2].upper() for a in actionNames)
            prompt = ", ".join(actionNames[:-1]) + " or " + actionNames[-1] + "?[" +  "/".join(actions) + "]"
            action = input(prompt).upper()
            if action not in actions:
                print("Command misunderstood")
            elif action == "HI":
                return playerActions.HIT
            elif action == "ST":
                return playerActions.STAND
            elif action == "DO":
                return playerActions.DOUBLE_DOWN
            elif action == "SP":
                return playerActions.SPLIT
    def bet(self, hand:abstractHand | None = None) -> int:
        print(f"Funds:{self.funds}")
        if hand != None:
            print(hand)
        bet = int(input("Input bet:"))
        self.funds -= bet
        return bet
