#long term I want to see if I can make a machine learning thing to teach ais how to play uno

import enum
import random

class Color(enum.Enum):
    red = 0
    blue = 1
    green = 2
    yellow = 3
    wild = 4

class CardEffect(enum.Enum):
    none = 0
    reverse = 1
    skip = 2
    draw2 = 3
    wild = 4
    draw4 = 5

class Card:
    def __init__(self, color, number, effect):
        self.color = color
        self.number = number
        self.effect = effect
    def __hash__(self): return hash(id(self))
    def __eq__(self, x): return x is self
    def __ne__(self, x): return x is not self
    def __repr__(self):
        if(self.number > -1):
            return self.color.name + " " + str(self.number)
        else:
            return self.color.name + " " + self.effect.name

class Player:
    def __init__(self, hand, name):
        self.hand = hand
        self.name = name
    def __repr__(self):
        return self.name

    def ChooseCard(self):
        eligibleCards = []
        for card in self.hand:
            if(CanCardBePlayed(card)):
                eligibleCards.append(card)
        if(len(eligibleCards) == 0):
            return None
        else:
            #these ai put approximately 0 thought into picking which card to play
            return random.choice(eligibleCards)

drawPile = []
discardPile = []
players = [] #index 0 is the player with the current turn, the next player is index 1, and so on
fakeColor = Color.wild
gameOngoing = True

def DrawCard():
    if(len(drawPile) != 0):
        return drawPile.pop()
    else:
        ShuffleDiscardPile()
        return DrawCard()

def PlayerDrawCard(player):
    player.hand.append(DrawCard())

def ShuffleDiscardPile():
    #shuffle discard pile into draw pile
    drawPile.extend(discardPile)
    discardPile.clear()
    random.shuffle(drawPile)
    #get a new card, if its a wild then its not eligible, and shuffle again
    newPotentialTopDiscard = drawPile.pop()
    if(newPotentialTopDiscard.color == Color.wild):
        print("Redraw")
        discardPile.append(newPotentialTopDiscard)
        ShuffleDiscardPile()
    else:
        PutCardOnDiscardPile(newPotentialTopDiscard)
        #if it was a reverse then the first player still gets to go, but the order is reversed
        if(newPotentialTopDiscard.effect == CardEffect.reverse):
            NextPlayer()
            NextPlayer()

def PutCardOnDiscardPile(card):
    discardPile.append(card)
    print(repr(card) + " was played")
    match card.effect:
        case CardEffect.none:
            None
        case CardEffect.reverse:
            Reverse()
        case CardEffect.skip:
            Skip()
        case CardEffect.draw2:
            Draw2()
        case CardEffect.wild:
            Wild()
        case CardEffect.draw4:
            Draw4()

def NextPlayer():
    players.append(players[0])
    players.remove(players[0])

def Reverse():
    players.insert(0, players.pop())
    players.reverse()

def Skip():
    print(players[0].name + " was skipped")
    NextPlayer()

def Draw2():
    #official rules dont have stacking +2s, but i might make it an option idk
    print(players[0].name + " had to draw 2")
    PlayerDrawCard(players[0])
    PlayerDrawCard(players[0])
    NextPlayer()

def Wild():
    #placeholder for having the color be chosen by the players
    global fakeColor
    fakeColor = Color(random.randrange(4))

def Draw4():
    Wild()
    print(players[0].name + " had to draw 4")
    for i in range(4):
        PlayerDrawCard(players[0])
    NextPlayer()

def GetTopOfDiscardPile():
    return discardPile[len(discardPile)-1]

def CanCardBePlayed(cardInQuestion):
    card = GetTopOfDiscardPile()
    #apparently in the official rules +4 wilds cannot be played unless you cant play anything else, 
    #which kindof throws a wrench in to this, so im going to ignore that rule for now, 
    #as I never knew it was a thing until looking up the official ones
    if(cardInQuestion.color == Color.wild):
        return True
    if(card.color == Color.wild):
        return cardInQuestion.color == fakeColor
    if(cardInQuestion.color == card.color):
        return True
    if((cardInQuestion.number != -1) and (cardInQuestion.number == card.number)):
        return True 
    if((cardInQuestion.effect != CardEffect.none) and (cardInQuestion.effect == card.effect)):
        return True

def SetupPlayers():
    players.clear()
    players.append(Player([], "John"))
    players.append(Player([], "Milov"))
    players.append(Player([], "Kerzky"))
    players.append(Player([], "桜"))
    print("The players are: ")
    print(players)

def SetupGame():
    drawPile.clear()
    discardPile.clear()
    #goes through all colors
    for color in range(4):
        #adds 0-9 for each color
        for cardNumber in range(10):
            drawPile.append(Card(Color(color), cardNumber, CardEffect.none))
        drawPile.append(Card(Color(color), -1, CardEffect.reverse))
        drawPile.append(Card(Color(color), -1, CardEffect.skip))
        drawPile.append(Card(Color(color), -1, CardEffect.draw2))
    drawPile.append(Card(Color.wild, -1, CardEffect.wild))
    drawPile.append(Card(Color.wild, -1, CardEffect.wild))
    drawPile.append(Card(Color.wild, -1, CardEffect.draw4))
    drawPile.append(Card(Color.wild, -1, CardEffect.draw4))
    ShuffleDiscardPile()
    #draw hands
    for player in players:
        for i in range(7):
            PlayerDrawCard(player)
        print(player.name + "'s starting hand looks like:")
        print(player.hand)

def PlayerTurn(player):
    print(player.name + "'s turn")
    card = player.ChooseCard()
    NextPlayer()
    if(card is None):
        PlayerDrawCard(player)
        print(player.name+" had to draw")
    else:
        player.hand.remove(card)
        PutCardOnDiscardPile(card)
        if(len(player.hand) == 1):
            #for now players will be smart enough to say uno each time
            print(player.name+": Uno!")
        if(len(player.hand) == 0):
            print(player.name+": I won!")
            global gameOngoing 
            gameOngoing = False

def PlayGame():
    print("Starting!")
    SetupPlayers()
    SetupGame()
    global gameOngoing 
    turns = 0
    while(gameOngoing and turns < 1000):
        PlayerTurn(players[0])
        turns+=1
        if(turns > 1000):
            print("Game end by heat death of the universe")

PlayGame()