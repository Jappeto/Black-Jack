# ----------------------------------------------------------------------
# blackjack.py
# Jacob Reppeto
# 08/01/2022
# ----------------------------------------------------------------------

from graphics import *
from CardDeck import *

# ----------------------------------------------------------------------

def drawCard(filename: str, x: int, y: int, window: GraphWin):
    """
    draw image specified by filename centered at (x, y) in window
    :param filename: filename for card - see cardInfo for details
    :param x: x-coordinate for center of card image
    :param y: y-coordinate for center of card image
    :param window: GraphWin to draw card in
    :return: None
    """
    
    p = Point(x, y)
    prefixes = ['cardset/', '../cardset/', './']
    for prefix in prefixes:
        fname = f'{prefix}{filename}'
        try:
            image = Image(p, fname)
            image.draw(window)
            return image
        except:
            pass
            
# ----------------------------------------------------------------------
    
    
def cardInfo(cardNumber) -> (int, str):
    """
    returns the blackjack value and and filename for card specified
    :param cardNumber: card 0 to 51
    :return: blackjack value 2-11 for card and filename - see below for these

    0-12 are the Ace-King of clubs
    13-25 are the Ace-King of spades
    26-38 are the Ace-King of hearts
    39-51 are the Ace-King of diamonds

    the blackjack value for the cards 2-9 are the corresponding
    number; 10, Jack, Queen, and King all have blackjack values of 10
    and an Ace has a value of 11

    filename is of the form: ##s.gif
    where ## is a two digit number (leading 0 if less than 10)
    and s is a letter corresponding to the suit value
    c for clubs, s for spades, h for hearts, d for diamonds
    """
    
    # calculate suit and face numbers
    suitNum = cardNumber // 13
    faceNum = cardNumber % 13
    
    # calculate blackjack value
    value = faceNum + 1
    if value > 10:
        value = 10
    elif value == 1:
        value = 11
        
    # calculate name of file
    # face is a number from 1 to 13 with leading zeros for 1-9
    suits = 'cshd'
    filename = f"{faceNum + 1:>02}{suits[suitNum]}.gif"
    return value, filename

# ----------------------------------------------------------------------

def isInside(point, box):
    #Checks to see if the click is inside the button that we made

    lowerLeft = box.getP1()
    upperRight = box.getP2()

    return lowerLeft.getX() <= point.getX() <= upperRight.getX() and lowerLeft.getY() <= point.getY() <= upperRight.getY()

def calculateScore(cards):
    #checks if the score is over 21 but there is an ace in your hand

    totalScore = 0
    aceCount = 0

    for card in cards:
        value, filename = cardInfo(card)
        totalScore += value

        if value == 11:
            aceCount +=1

    while totalScore > 21 and aceCount > 0:
        totalScore -=10
        aceCount -=1

    return totalScore



def main():
    # create window, card deck and shuffle it
    win = GraphWin('Blackjack', 800, 600)
    # in case use dark mode on Mac
    win.setBackground("white")

    button = Rectangle(Point(650, 250), Point(750, 300))
    button.setFill("gray")
    button.draw(win)

    label = Text(Point(700, 275), "Hit Me")
    label.draw(win)

    result = Text(Point(100, 500), "")
    result.draw(win)


    deck = CardDeck()
    deck.shuffle()

    playerCards = [deck.dealOne(), deck.dealOne()]
    dealerCards = [deck.dealOne()]
    playerScore = 0
    dealerScore = 0
    xPosition = 100

    # deals player cards
    for cards in playerCards:
        value, filename = cardInfo(cards)
        drawCard(filename, xPosition, 100, win)
        xPosition += 100
        playerScore += value

    pScore = Text(Point(100, 200), playerScore)
    pScore.draw(win)

    value, filename = cardInfo(dealerCards[0])
    drawCard(filename, 100, 300, win)
    dealerScore += value

    dScore = Text(Point(100, 400), dealerScore)
    dScore.draw(win)

    while playerScore <= 21:
        click = win.getMouse()
        if isInside(click, button):
            newCard = deck.dealOne()
            playerCards.append(newCard)

            value, filename = cardInfo(newCard)
            drawCard(filename, xPosition, 100, win)
            xPosition += 100
            playerScore = calculateScore(playerCards)
            pScore.setText(playerScore)


            if playerScore > 21:
                pScore.setText("Busted")
                break
        else:
            break


    if playerScore <= 21:
        xPosition = 200
        while dealerScore < 17:
            newCard = deck.dealOne()
            dealerCards.append(newCard)

            value, filename = cardInfo(newCard)
            drawCard(filename, xPosition, 300, win)
            xPosition += 100

            dealerScore = calculateScore(dealerCards)
            dScore.setText(dealerScore)


            if dealerScore > 21:
                dScore.setText("Busted")
                break

    if playerScore > 21:
        result.setText("Dealer Wins")
    elif dealerScore > 21:
        result.setText("player Wins")
    elif playerScore > dealerScore:
        result.setText("player Wins")
    elif playerScore < dealerScore:
        result.setText("Dealer Wins")
    else:
        result.setText("It is a tie")


    # wait for mouse click before closing window
    win.getMouse()
    win.close()
    
# ----------------------------------------------------------------------

if __name__ == '__main__':
    main()
    