import tkinter as tk

window = tk.Tk()

frame = tk.Frame(master=window, width=900, height=500)
frame.pack()


label1 = tk.Button(master=frame, text="Game Deck", bg="red")
label1.place(x=0, y=0)

label2 = tk.Button(master=frame, text="Display Deck", bg="yellow")
label2.place(x=150, y=0)

label3 = tk.Button(master=frame, text="Spades", bg="grey")
label3.place(x=400, y=0)

label4 = tk.Button(master=frame, text="Clubs", bg="grey")
label4.place(x=500, y=0)

label5 = tk.Button(master=frame, text="Hearts", bg="orange")
label5.place(x=600, y=0)

label6 = tk.Button(master=frame, text="Diamonds", bg="orange")
label6.place(x=700, y=0)

deck1 = tk.Button(master=frame, text="Deck1", bg="blue")
deck1.place(x=25, y=200)

deck2 = tk.Button(master=frame, text="Deck 2", bg="blue")
deck2.place(x=150, y=200)

deck3 = tk.Button(master=frame, text="Deck 3", bg="blue")
deck3.place(x=275, y=200)

deck4 = tk.Button(master=frame, text="Deck 4", bg="blue")
deck4.place(x=400, y=200)

deck5 = tk.Button(master=frame, text="Deck 5", bg="blue")
deck5.place(x=525, y=200)

deck6 = tk.Button(master=frame, text="Deck 6", bg="blue")
deck6.place(x=650, y=200)

deck7 = tk.Button(master=frame, text="Deck 7", bg="blue")
deck7.place(x=775, y=200)



import random

cardvalues={1:"A",11:"J",12:"Q",13:"K"}
for i in range(2,11):
    cardvalues[i]=i
cardsuits={1:"spades",2:"clubs",3:"hearts",4:"diamonds"}
receiving=False
sourcedeck=None

class Card:
    def __init__(self,suit,value,faceup):
        if not(suit in cardsuits.keys() and value in cardvalues.keys() and faceup in [True,False]):
            raise SyntaxError("Inappropriate card parameters: "+str(suit)+" "+str(value)+" "+str(faceup))
        self.suit=suit
        self.value=value
        self.faceup=faceup

    def flip(self):
        self.faceup=not self.faceup
        return self

    def show(self):
        if self.faceup:
            return str(cardvalues[self.value])+" of " +str(cardsuits[self.suit])
        else:
            return "TM"

    def nextlowval(self):
        return self.value-1

    def oppcolor(self):
        if self.suit in [1,2]:
            return [3,4]
        else:
            return [1,2]

    def sendTofin(self,findeck):
        findeck.addcard(self)

class Deck:
    def __init__(self,cards,button):
        self.cards=cards
        self.button=button

    def size(self):
        return len(self.cards)

    def addcard(self,card):
        if self.match(card):
            self.cards.append(card)
            self.showgraph()

    def takecard(self):
        return self.card.pop()

    def faceupcards(self):
        return [card for card in self.cards if card.faceup]

    def transfer(self,source,number,front=True,cond=True,flip=False):
        if cond and source.size()>0:
            if flip:
                addition=[card.flip() for card in reversed(source.cards[len(source.cards)-number:len(source.cards)])]
            else:
                 addition=source.cards[len(source.cards)-number:len(source.cards)]
            if front:
                self.cards+=addition
            else:
                 self.cards=addition+self.cards
            source.cards=source.cards[0:len(source.cards)-number]


    def shuffle(self):
        random.shuffle(self.cards)

    def showgraph(self):
        self.button.configure(text=self.show(),command=lambda : self.press())
        

class FullDeck(Deck):
    def __init__(self,faceup,button):
        super().__init__([Card(suit,value,faceup) for suit in cardsuits.keys() for value in cardvalues.keys()],button)

class EmptyDeck(Deck):
    def __init__(self,button):
        super().__init__([],button)

    def travelnum(self,dest):
        return 1

    def receive(self):
        global receiving
        global sourcedeck
        receiving=False
        self.transfer(sourcedeck,sourcedeck.travelnum(self))
        sourcedeck.showgraph()

    def press(self):
        global receiving
        global sourcedeck
        if self.size()>0:
            frontcard=self.cards[self.size()-1]
            if not(frontcard.faceup):
                frontcard.flip()
            elif not(receiving):
                receiving=True
                sourcedeck=self
                return None
        if receiving:
            self.receive()
        self.showgraph()
            

class SolDeck(FullDeck):
    def __init__(self,button,displaydeck):
        super().__init__(False,button)
        self.displaydeck=displaydeck

    def displayto(self):
        numself=min(3,self.size())
        self.transfer(self.displaydeck,self.displaydeck.size(),False,True,True)
        self.displaydeck.transfer(self,numself,False,True,True)
        self.showgraph()
        self.displaydeck.showgraph()

    def press(self):
        self.displayto()

    def show(self):
        return str(self.size())+" cards"

class DisplayDeck(EmptyDeck):
    def __init__(self,button):
        super().__init__(button)

    def show(self):
        return "\n".join([card.show() for card in self.cards])

    def sendto(self,dest):
        dest.addcard(self.takecard())
        self.showgraph()

    def receive(self):
        receive=False

class HoldDeck(EmptyDeck):
    def __init__(self,n,sourcedeck,button):
        super().__init__(button)
        super().transfer(sourcedeck,n)

    def match(self,card):
        if self.size()==0:
            return card.value==13
        else:
            testcard=self.cards[len(self.cards)-1]
            return testcard.faceup and card.suit in testcard.oppcolor() and card.value==testcard.nextlowval()
      
    def transfer(self, source, num):
        movingtestcard=source.cards[len(source.cards)-num]
        cond=self.match(movingtestcard)
        super().transfer(source,num,True,cond)

    def travelnum(self,dest):
        if dest.size()>0:
            acceptedcardnum=dest.cards[dest.size()-1].value-1
        else:
             acceptedcardnum=13
        if self.faceupcards()[0].value>=acceptedcardnum and self.faceupcards()[len(self.faceupcards())-1].value<=acceptedcardnum:
            return acceptedcardnum-self.faceupcards()[len(self.faceupcards())-1].value+1
        else:
            return 1

    def show(self):
        return str(self.size()) +" cards \n"+ "\n".join([card.show() for card in self.faceupcards()])


class FinalDeck(EmptyDeck):
    def __init__(self,suit,button):
        super().__init__(button)
        self.suit=suit

    def match(self,card):
        if self.size()==0:
            return card.suit==self.suit and card.value==1
        else:
            return card.suit==self.suit and card.value==self.cards[self.size()-1].value+1

    def transfer(self, source, num):
        movingtestcard=source.cards[len(source.cards)-num]
        cond=self.match(movingtestcard)
        super().transfer(source,num,True,cond)

    def show(self):
        if self.size()>0:
            return self.cards[self.size()-1].show()
        else:
            return cardsuits[self.suit]

def my_mainloop(finales):
    x=0
    for i in range(1,5):
        x+=finales[i-1].size()
    if x==52:
        print("YOu wIn")
    window.after(1000,lambda : my_mainloop(finales))

def solitaire():
    displaydeck=DisplayDeck(label2)
    gamedeck=SolDeck(label1,displaydeck)
    gamedeck.shuffle()
    holds=[]
    holdbuttons=[deck1,deck2,deck3,deck4,deck5,deck6,deck7]
    for i in range(0,7):
        holds.append(HoldDeck(i,gamedeck,holdbuttons[i]))
        holds[i].showgraph()
    finals=[]
    finalbuttons=[label3,label4,label5,label6]
    for i in range(1,5):
        finals.append(FinalDeck(i,finalbuttons[i-1]))
        finals[i-1].showgraph()
    gamedeck.showgraph()
    displaydeck.showgraph()
    window.after(1000,lambda : my_mainloop(finals))
    

solitaire()
    
