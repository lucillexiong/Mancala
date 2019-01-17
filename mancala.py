#Final Project - Mancala
#Lucile Xiong
#Kalah is a board game in the family, Mancala. The objective of the game is to
#caputure more marbles than the the opponent. This program allows players to play
#one or two player games with different coloured marbles.

from random import *
from pygame import *
from math import *

#fonts
font.init()
ktcFontHead1=font.SysFont("Kristen ITC",150)
ktcFontHead2=font.SysFont("Kristen ITC",100)
ktcFontBody1=font.SysFont("Kristen ITC",75)
ktcFontBody2=font.SysFont("Kristen ITC",45)
ktcFontBody3=font.SysFont("Kristen ITC",35)
ktcFontBody4=font.SysFont("Kristen ITC",15)

screen=display.set_mode((1000,750))
alpha1=Surface((1000,750),SRCALPHA)

#Each pits Rects

#player 2's Rects
pit01Rect=Rect(211,223,83,133)
pit02Rect=Rect(309,223,83,133)
pit03Rect=Rect(407,223,83,133)
pit04Rect=Rect(505,223,83,133)
pit05Rect=Rect(603,223,83,133)
pit06Rect=Rect(701,223,83,133)

#player 1's Rects
pit11Rect=Rect(211,397,83,133) #pit 6
pit12Rect=Rect(308,397,83,133) #pit 5
pit13Rect=Rect(405,397,83,133) #pit 4
pit14Rect=Rect(502,397,83,133) #pit 3
pit15Rect=Rect(599,397,83,133) #pit 2
pit16Rect=Rect(696,397,83,133) #pit 1

page="menu"


#both games
def drawBoard(screen): #draw the game board
    boardImage=image.load("woodboard.jpg")
    boardImage=transform.scale(boardImage,(800,350))
    screen.blit(boardImage,(100,200))

def xyMarble(marblenum,player,pit): #figures our the position of each marble
    if pit==0:
        if marblenum%2==0:
            rx=1
        else:
            rx=0
        if marblenum%2==0:
            sub=-1
        else:
            sub=0
        if player==1:
            if marblenum>25:
                return(165,(marblenum-25)*31+225)
            if marblenum>17:
                return(135,(marblenum-18)*31+265)
            return(rx*34+123,(int(marblenum/2)+sub)*31+250)
        elif player==0:
            if marblenum>25:
                return(855,(marblenum-25)*31+225)
            if marblenum>16:
                return(825,(marblenum-18)*31+265)
            return(rx*37+803,(int(marblenum/2)+sub)*31+250)
    else:
        #In a real life mancala game, a player must remember the number of marbles in each pit. They are not allowed
        #to count the marbles when the pit becomes full. I chose more than 10 marbles as a full pit.
        while marblenum>10:
            marblenum-=10
        #Each marble has it's own x value and y value
        if player==0:
            pit=7-pit
        if marblenum==1:
            xvalue=111
            yvalue=72
        elif marblenum==2:
            xvalue=167
            yvalue=72
        elif marblenum==3 or marblenum==4 or marblenum==5 or marblenum==6:
            xvalue=139
        elif marblenum==7 or marblenum==10:
            xvalue=115
        elif marblenum==8 or marblenum==9:
            xvalue=162
        if marblenum==3:
            yvalue=57
        elif marblenum==4:
            yvalue=87
        elif marblenum==5:
            yvalue=23
        elif marblenum==6:
            yvalue=123
        elif marblenum==7 or marblenum==9:
            yvalue=42
        elif marblenum==8 or marblenum==10:
            yvalue=102
        #xdist is the distance between two touching pits when marblenum is the same
        if player==1:
            xdist=98
            ydist=0
        elif player==0:
            xdist=97
            ydist=172 #distance from the first row of pits and second row of pits
        return(100+xvalue+xdist*(pit-1),200+yvalue+ydist)

def drawMarbles(screen,marbles): #draws each pit 
    drawBoard(screen)
    for x in range(2):
        for y in range(7):
            if marbles[x][y]!=0:
                for m in range(1,marbles[x][y]+1,1):
                    screen.blit(transform.scale(image.load(cmarble),(30,30)),xyMarble(m,x,y))

def checkDone(marbles): #check if the game is done
    for r in range(2):
        if sum(marbles[r])==marbles[r][0]:
            return True 
    return False

#one player
def kalahAI(marbles):
    avoid0=[] #avoid adding more marbles to the other player's side
    avoid1=[] #not a good move on computer's side
    for c in range(1,7): #repeat move, closest to the pit
        if marbles[1][c]==c:
            return c

    #If a player lands in an empty pit on their side and the opposite pit is full, the marbles from both pits
    #is captured by the player
    for c in range(1,7):
        orig=c
        player=1
        seeds=marbles[1][c]
        big=0
        bigpos=0
        for i in range(seeds):
            c-=1
            if c==0 and player==0:
                c-=1
            if c==-1:
                c=6
                player=1-player
            if i==seeds-1 and player==1 and marbles[0][7-c]!=0 and marbles[1][c]==0:
                if marbles[0][7-c]+marbles[1][c]>big:
                    big=marbles[0][7-c]+1
                    bigpos=orig
        if bigpos>0:
            return bigpos

    #makes a list of places to avoid so the other player does not get more marbles
    for c in range(6,-1,-1):
        if marbles[0][c]==c or marbles[0][c]==c-1:
            avoid0.append(c)

    for c in range(1,7):
        orig=c
        seeds=marbles[1][c]
        player=1
        for i in range(seeds):
            c-=1
            if c==0 and player==0:
                c-=1
            if c==-1:
                c=6
                player=1-player
            if player==0 and c in avoid0:
                avoid1.append(orig)
    
    for c in range(1,7):
        if marbles[1][c]>=c and c not in avoid1:
            return c

    #If marbles exceed a certain number in these pits, they will most likely be caputure by the other player 
    for c in range(1,4):
        if marbles[1][c]>c+5:
            return c

    #logically the more marbles you keep on your side of the pit, the more marbles you can capture
    for c in range(6,0,-1):
        if marbles[1][c]!=0:
            return c

#used for the one player game
def moveMarbles1(player,marbles,pit):
    seeds=marbles[player][pit] # the seeds in the pit to be distributed
    marbles[player][pit]=0 #Removes all the seeds from the pit
    drawMarbles(screen,marbles)
    change=False
    for i in range(seeds): #distributes the seeds
        pit-=1
        if pit==-1:
            pit=6
            player=1-player
            #indicates which side of the board the last seed landed in
            if change:
                change=False
            else:
                change=True
        if pit==0 and change: #does not add a marble into the opponent's store
            pit=6
            player=1-player
            change=False
            marbles[player][pit]+=1
        else:
            marbles[player][pit]+=1
        if i==seeds-1 and change==False and marbles[player][pit]==1 and pit!=0 and marbles[1-player][7-pit]!=0: #last move, player side, landed in empty pit
            marbles[player][0]+=marbles[player][pit]
            marbles[player][pit]=0
            marbles[player][0]+=marbles[1-player][7-pit] #adds from opposite pit
            marbles[1-player][7-pit]=0
        if i==seeds-1 and pit==0 and change==False:
            drawMarbles(screen,marbles)
            if player==0 and change==False:
                return marbles,True #current player gets another move
            elif player==1 and change:
                return marbles,True #current player gets another move
            else:
                pos=kalahAI(marbles)
            moveMarbles1(player,marbles,pos)
    return marbles,False

#used for the two player game
def moveMarbles2(player,marbles,pit):
    seeds=marbles[player][pit] # the seeds in the pit to be distributed
    marbles[player][pit]=0 #Removes all the seeds from the pit
    drawMarbles(screen,marbles)
    change=False

    for i in range(seeds): #distributes the seeds
        pit-=1
        if pit==-1:
            pit=6
            player=1-player
            #indicates which side of the board the last seed landed in
            if change:
                change=False
            else:
                change=True

        if pit==0 and change: #does not add a marble into the opponent's store
            pit=6
            player=1-player
            change=False
            marbles[player][pit]+=1
        else:
            marbles[player][pit]+=1

        if i==seeds-1 and change==False and marbles[player][pit]==1 and pit!=0 and marbles[1-player][7-pit]!=0: #last move, player side, landed in empty pit
            marbles[player][0]+=marbles[player][pit]
            marbles[player][pit]=0
            marbles[player][0]+=marbles[1-player][7-pit] #adds from opposite pit
            marbles[1-player][7-pit]=0

        if i==seeds-1 and pit==0 and change==False:
            return marbles,True

    return marbles,False

def menu():
    running = True
    buttons = [Rect(250,y*120+300,500,100) for y in range(3)]
    buttonpic=transform.scale(image.load("menubutton.jpg"),(500,100))
    backgroundpic=transform.scale(image.load("menubackground.jpg"),(1000,750))
    vals = ["play","instructions","credit"]
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                return "exit"
        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()

        #background
        screen.blit(backgroundpic,(0,0))
        draw.rect(alpha1,(255,255,255,70),(0,0,1000,750))
        screen.blit(alpha1,(0,0))
        screen.blit(ktcFontHead1.render("Mancala",True,(0,0,0)),(182,0,100,150))

        for r,v in zip(buttons,vals):
            screen.blit(buttonpic,r)
            if v=="play":
                screen.blit(ktcFontBody1.render(v.capitalize(),True,(0,0,0)),(425,300,500,100))
            if v=="instructions":
                screen.blit(ktcFontBody1.render(v.capitalize(),True,(0,0,0)),(273,420,500,100))
            if v=="credit":
                screen.blit(ktcFontBody1.render(v.capitalize(),True,(0,0,0)),(380,540,500,100))
            if r.collidepoint(mx,my):
                draw.rect(screen,(255,255,255),r,2) #highlights the rect being hovered on
                if mb[0]==1:
                    return v
            else:
                draw.rect(screen,(0,0,0),r,2)
                
        display.flip()

def instructions():
    #background
    backgroundpic=transform.scale(image.load("menubackground.jpg"),(1000,750))
    screen.blit(backgroundpic,(0,0))
    draw.rect(alpha1,(255,255,255,70),(0,0,1000,750))
    screen.blit(alpha1,(0,0))
    
    screen.blit(ktcFontHead2.render("Instructions",True,(0,0,0)),(200,0,50,150))
    screen.blit(transform.scale(image.load("instructions.jpg"),(800,484)),(100,140))
    
    #menu button
    menubuttonRect=Rect(425,650,150,100)
    buttonpic=transform.scale(image.load("menubutton.jpg"),(150,100))
    screen.blit(buttonpic,menubuttonRect)
    screen.blit(ktcFontBody2.render("Menu",True,(0,0,0)),(436,665,150,100))

    running=True
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running=False
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()
        
        draw.rect(screen,(0,0,0),menubuttonRect,2)
        if menubuttonRect.collidepoint((mx,my)):
            draw.rect(screen,(255,255,255),menubuttonRect,2)
            if mb[0]==1:
                return "menu"
        else:
            draw.rect(screen,(0,0,0),menubuttonRect,2)
        display.flip()
    return "exit"

def credit():
    #background
    backgroundpic=transform.scale(image.load("menubackground.jpg"),(1000,750))
    screen.blit(backgroundpic,(0,0))
    draw.rect(alpha1,(255,255,255,70),(0,0,1000,750))
    screen.blit(alpha1,(0,0))
    
    screen.blit(ktcFontHead2.render("Credits",True,(0,0,0)),(310,100,50,150))
    screen.blit(image.load("credits.jpg"),(279,254))

    #menu button
    buttonpic=transform.scale(image.load("menubutton.jpg"),(150,100))
    menubuttonRect=Rect(425,608,150,100)
    buttonpic=transform.scale(image.load("menubutton.jpg"),(150,100))
    screen.blit(buttonpic,menubuttonRect)
    screen.blit(ktcFontBody2.render("Menu",True,(0,0,0)),(436,623,150,100))

    running = True
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()

        #allows the user to go back to the menu
        if menubuttonRect.collidepoint((mx,my)):
            draw.rect(screen,(255,255,255),menubuttonRect,2)
            if mb[0]==1:
                return "menu"
        else:
            draw.rect(screen,(0,0,0),menubuttonRect,2)

        display.flip()
    return "exit"

#
def drawType(rect1,rect2):
    buttonpic=transform.scale(image.load("menubutton.jpg"),(100,100))
    screen.blit(buttonpic,rect1)
    screen.blit(buttonpic,rect2)
    draw.rect(screen,(0,0,0),rect1,2)
    draw.rect(screen,(0,0,0),rect2,2)
    screen.blit(ktcFontBody3.render("1",True,(0,0,0)),(412.5,270,100,100))
    screen.blit(ktcFontBody3.render("player",True,(0,0,0)),(371,305,100,100))
    screen.blit(ktcFontBody3.render("2",True,(0,0,0)),(569.5,270,100,100)) #center this
    screen.blit(ktcFontBody3.render("player",True,(0,0,0)),(528,305,100,100))

#play screen
def play():
    global cmarble
    
    gametype=""
    cmarble="" #colour of the marble

    #background
    backgroundpic=transform.scale(image.load("menubackground.jpg"),(1000,750))
    screen.blit(backgroundpic,(0,0))
    draw.rect(alpha1,(255,255,255,70),(0,0,1000,750))
    screen.blit(alpha1,(0,0))
    screen.blit(ktcFontHead1.render("Mancala",True,(0,0,0)),(182,0,100,150))
    buttonpic1=transform.scale(image.load("menubutton.jpg"),(100,100))
    buttonpic2=transform.scale(image.load("menubutton.jpg"),(150,100))

    #level buttons
    kalahoneRect=Rect(371,270,100,100)
    kalahtwoRect=Rect(528,270,100,100)

    #colour buttons
    blueRect=Rect(57,445,100,100)
    greenRect=Rect(214,445,100,100)
    purpleRect=Rect(371,445,100,100)
    redRect=Rect(528,445,100,100)
    whiteRect=Rect(685,445,100,100)
    yellowRect=Rect(842,445,100,100)

    #menu and play button
    playRect=Rect(764,620,150,100)
    previousRect=Rect(86,620,150,100)

    running=True
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                return "exit"
        mx,my = mouse.get_pos()
        mb = mouse.get_pressed()

        #menu button
        screen.blit(buttonpic2,previousRect)
        draw.rect(screen,(0,0,0),previousRect,2)
        screen.blit(ktcFontBody2.render("Menu",True,(0,0,0)),(97,635,150,100))
        if previousRect.collidepoint((mx,my)):
            draw.rect(screen,(255,255,255),previousRect,2)
            if mb[0]==1:
                return "menu"
        else:
            draw.rect(screen,(0,0,0),previousRect,2)
        #play button
        if cmarble!="": #appears when a gametype and colour is selected
            screen.blit(buttonpic2,playRect)
            draw.rect(screen,(0,0,0),playRect,2)
            screen.blit(ktcFontBody2.render("Start",True,(0,0,0)),(780,635,150,100))
        if playRect.collidepoint((mx,my)) and mb[0]==1:
                return gametype

        #user chooses between one and two player
        screen.blit(ktcFontBody2.render("Select a game:",True,(0,0,0)),(343,200,100,100))
        if gametype=="":
            drawType(kalahoneRect,kalahtwoRect)
        if mb[0]==1 and kalahoneRect.collidepoint((mx,my)):
            gametype="kalahone"
            draw.rect(screen,(255,255,255),kalahoneRect,2)
            draw.rect(screen,(0,0,0),kalahtwoRect,2)
        if mb[0]==1 and kalahtwoRect.collidepoint((mx,my)):
            gametype="kalahtwo"
            draw.rect(screen,(0,0,0),kalahoneRect,2)
            draw.rect(screen,(255,255,255),kalahtwoRect,2)

        #user chooses colour of marbles
        if gametype!="" and cmarble=="": #appears only if a game type is selected
            screen.blit(ktcFontBody2.render("Select a colour:",True,(0,0,0)),(328,375,100,100))
            screen.blit(buttonpic1,blueRect)
            screen.blit(buttonpic1,greenRect)
            screen.blit(buttonpic1,redRect)
            screen.blit(buttonpic1,purpleRect)
            screen.blit(buttonpic1,whiteRect)
            screen.blit(buttonpic1,yellowRect)
            draw.rect(screen,(0,0,0),blueRect,2)
            draw.rect(screen,(0,0,0),greenRect,2)
            draw.rect(screen,(0,0,0),redRect,2)
            draw.rect(screen,(0,0,0),purpleRect,2)
            draw.rect(screen,(0,0,0),whiteRect,2)
            draw.rect(screen,(0,0,0),yellowRect,2)
            screen.blit(transform.scale(image.load("blue.png"),(100,100)),blueRect)
            screen.blit(transform.scale(image.load("green.png"),(100,100)),greenRect)
            screen.blit(transform.scale(image.load("red.png"),(100,100)),redRect)
            screen.blit(transform.scale(image.load("purple.png"),(100,100)),purpleRect)
            screen.blit(transform.scale(image.load("white.png"),(100,100)),whiteRect)
            screen.blit(transform.scale(image.load("yellow.png"),(100,100)),yellowRect)
        if mb[0]==1 and blueRect.collidepoint((mx,my)):
            cmarble="blue.png"
            draw.rect(screen,(255,255,255),blueRect,2)
            draw.rect(screen,(0,0,0),greenRect,2)
            draw.rect(screen,(0,0,0),redRect,2)
            draw.rect(screen,(0,0,0),purpleRect,2)
            draw.rect(screen,(0,0,0),whiteRect,2)
            draw.rect(screen,(0,0,0),yellowRect,2)
        if mb[0]==1 and greenRect.collidepoint((mx,my)):
            cmarble="green.png"
            draw.rect(screen,(0,0,0),blueRect,2)
            draw.rect(screen,(255,255,255),greenRect,2)
            draw.rect(screen,(0,0,0),redRect,2)
            draw.rect(screen,(0,0,0),purpleRect,2)
            draw.rect(screen,(0,0,0),whiteRect,2)
            draw.rect(screen,(0,0,0),yellowRect,2)
        if mb[0]==1 and redRect.collidepoint((mx,my)):
            cmarble="red.png"
            draw.rect(screen,(0,0,0),blueRect,2)
            draw.rect(screen,(0,0,0),greenRect,2)
            draw.rect(screen,(255,255,255),redRect,2)
            draw.rect(screen,(0,0,0),purpleRect,2)
            draw.rect(screen,(0,0,0),whiteRect,2)
            draw.rect(screen,(0,0,0),yellowRect,2)
        if mb[0]==1 and purpleRect.collidepoint((mx,my)):
            cmarble="purple.png"
            draw.rect(screen,(0,0,0),blueRect,2)
            draw.rect(screen,(0,0,0),greenRect,2)
            draw.rect(screen,(0,0,0),redRect,2)
            draw.rect(screen,(255,255,255),purpleRect,2)
            draw.rect(screen,(0,0,0),whiteRect,2)
            draw.rect(screen,(0,0,0),yellowRect,2)
        if mb[0]==1 and whiteRect.collidepoint((mx,my)):
            cmarble="white.png"
            draw.rect(screen,(0,0,0),blueRect,2)
            draw.rect(screen,(0,0,0),greenRect,2)
            draw.rect(screen,(0,0,0),redRect,2)
            draw.rect(screen,(0,0,0),purpleRect,2)
            draw.rect(screen,(255,255,255),whiteRect,2)
            draw.rect(screen,(0,0,0),yellowRect,2)
        if mb[0]==1 and yellowRect.collidepoint((mx,my)):
            cmarble="yellow.png"
            draw.rect(screen,(0,0,0),blueRect,2)
            draw.rect(screen,(0,0,0),greenRect,2)
            draw.rect(screen,(0,0,0),redRect,2)
            draw.rect(screen,(0,0,0),purpleRect,2)
            draw.rect(screen,(0,0,0),whiteRect,2)
            draw.rect(screen,(255,255,255),yellowRect,2)
        display.flip()

#returns the pit the user chose for a two player game
def pos(mx,my,player):
    if player==0:
        if pit16Rect.collidepoint((mx,my)):
            return 1
        elif pit15Rect.collidepoint((mx,my)):
            return 2
        elif pit14Rect.collidepoint((mx,my)):
            return 3
        elif pit13Rect.collidepoint((mx,my)):
            return 4
        elif pit12Rect.collidepoint((mx,my)):
            return 5         
        elif pit11Rect.collidepoint((mx,my)):
            return 6

    elif player==1:
        if pit01Rect.collidepoint((mx,my)):
            return 1
        elif pit02Rect.collidepoint((mx,my)):
            return 2
        elif pit03Rect.collidepoint((mx,my)):
            return 3
        elif pit04Rect.collidepoint((mx,my)):
            return 4
        elif pit05Rect.collidepoint((mx,my)):
            return 5         
        elif pit06Rect.collidepoint((mx,my)):
            return 6

    return None

#returns the pit the user chose for a one player game    
def pos1(mx,my):
    if pit16Rect.collidepoint((mx,my)):
        return 1
    elif pit15Rect.collidepoint((mx,my)):
        return 2
    elif pit14Rect.collidepoint((mx,my)):
        return 3
    elif pit13Rect.collidepoint((mx,my)):
        return 4
    elif pit12Rect.collidepoint((mx,my)):
        return 5         
    elif pit11Rect.collidepoint((mx,my)):
        return 6

def kalahone():
    #background
    backgroundpic=transform.scale(image.load("menubackground.jpg"),(1000,750))
    screen.blit(backgroundpic,(0,0))
    draw.rect(alpha1,(255,255,255,70),(0,0,1000,750))
    screen.blit(alpha1,(0,0))

    screen.blit(ktcFontHead1.render("Mancala",True,(0,0,0)),(182,0,100,150))
    buttonpic1=transform.scale(image.load("menubutton.jpg"),(300,100))
    buttonpic2=transform.scale(image.load("menubutton.jpg"),(400,300))

    #sets the game up
    player=0
    marbles=[[4]*7 for i in range(2)]
    marbles[0][0]=0
    marbles[1][0]=0
    drawBoard(screen)
    drawMarbles(screen,marbles)

    #end screen
    endRect=Rect(300,225,400,300)

    #informs the user who's turn it is
    turnRect=Rect(435,363,153,33)

    #three buttons at the bottom
    menuRect=Rect(350,600,300,100)
    newgameRect=Rect(675,600,300,100)
    instrRect=Rect(25,600,300,100)

    done=False #if the game is done
    running=True
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()

        #allows the user to go to different parts of the game
        screen.blit(buttonpic1,menuRect)
        screen.blit(buttonpic1,newgameRect)
        screen.blit(buttonpic1,instrRect)
        screen.blit(ktcFontBody2.render("Menu",True,(0,0,0)),(437,617,150,100))
        screen.blit(ktcFontBody2.render("Instructions",True,(0,0,0)),(37,617,150,100))
        screen.blit(ktcFontBody2.render("New Game",True,(0,0,0)),(706,617,150,100))
        if menuRect.collidepoint((mx,my)):
            draw.rect(screen,(255,255,255),menuRect,2)
            if mb[0]==1:
                return "menu"
        else:
            draw.rect(screen,(0,0,0),menuRect,2)
        if newgameRect.collidepoint((mx,my)):
            draw.rect(screen,(255,255,255),newgameRect,2)
            if mb[0]==1:
                return "play"
        else:
            draw.rect(screen,(0,0,0),newgameRect,2)
        if instrRect.collidepoint((mx,my)):
            draw.rect(screen,(255,255,255),instrRect,2)
            if mb[0]==1:
                return "instructions"
        else:
            draw.rect(screen,(0,0,0),instrRect,2)

        #user makes a move
        if mb[0]==1 and player==0:
            mpos=pos(mx,my,player)
            if mpos!=None:
                drawBoard(screen)
                marbles,re=moveMarbles2(player,marbles,mpos)
                mpos=None
                drawMarbles(screen,marbles)
                if re: #gives the user a repeat move
                    mpos=pos(mx,my,player)
                    marbles,re=moveMarbles2(player,marbles,mpos)
                else:
                    player=1-player #changes players
            
            #updates the screen
            drawBoard(screen)
            drawMarbles(screen,marbles)
            if player==0:
                screen.blit(ktcFontBody4.render("Your turn",True,(0,0,0)),turnRect)
            if player==1:
                screen.blit(ktcFontBody4.render("Computer's turn",True,(0,0,0)),turnRect)

        #computer makes a move
        if player==1:
            marbles,re=moveMarbles1(player,marbles,kalahAI(marbles))
            player=1-player
            drawBoard(screen)
            drawMarbles(screen,marbles)
            if player==0:
                screen.blit(ktcFontBody4.render("Your turn",True,(0,0,0)),turnRect)
            if player==1:
                screen.blit(ktcFontBody4.render("Computer's turn",True,(0,0,0)),turnRect)

        #the game is finished
        if checkDone(marbles) and done==False:
            done=True

            #all the remaining marbles are added to the pits
            for i in range(1,7,1):
                marbles[0][0]+=marbles[0][i]
                marbles[1][0]+=marbles[1][i]

            drawMarbles(screen,marbles)
            draw.rect(alpha1,(255,255,255,111),(0,0,1000,750))
            screen.blit(alpha1,(0,0))
            screen.blit(buttonpic2,endRect)
            draw.rect(screen,(0,0,0),endRect,2)

            #informs the user on who won
            if marbles[0][0]>marbles[1][0]:
                screen.blit(ktcFontBody2.render("You win!",True,(0,0,0)),(407,225))
            elif marbles[1][0]>marbles[0][0]:
                screen.blit(ktcFontBody2.render("Computer wins!",True,(0,0,0)),(328,225))
            else:
                screen.blit(ktcFontBody1.render("Tie!",True,(0,0,0)),(430,225))
            screen.blit(ktcFontBody2.render("You: "+str(marbles[0][0]),True,(0,0,0)),(375,340))
            screen.blit(ktcFontBody2.render("Computer: "+str(marbles[1][0]),True,(0,0,0)),(375,430))

        display.flip()
    return "exit"

def kalahtwo():
    #background
    backgroundpic=transform.scale(image.load("menubackground.jpg"),(1000,750))
    screen.blit(backgroundpic,(0,0))
    draw.rect(alpha1,(255,255,255,70),(0,0,1000,750))
    screen.blit(alpha1,(0,0))
    
    screen.blit(ktcFontHead1.render("Mancala",True,(0,0,0)),(182,0,100,150))
    buttonpic1=transform.scale(image.load("menubutton.jpg"),(300,100))
    buttonpic2=transform.scale(image.load("menubutton.jpg"),(400,300))

    #sets the game up
    player=0
    marbles=[[4]*7 for i in range(2)]
    marbles[0][0]=0
    marbles[1][0]=0
    drawBoard(screen)
    drawMarbles(screen,marbles)

    #end screen
    endRect=Rect(300,225,400,300)

    #informs the user who's turn it is
    turnRect=Rect(435,363,153,33)

    #menu, new game, instructions
    menuRect=Rect(350,600,300,100)
    newgameRect=Rect(675,600,300,100)
    instrRect=Rect(25,600,300,100)

    done=False
    running=True
    while running:
        for evnt in event.get():          
            if evnt.type == QUIT:
                running = False
        mx,my=mouse.get_pos()
        mb=mouse.get_pressed()

        #allows the user to go to different parts of the game
        screen.blit(buttonpic1,menuRect)
        screen.blit(buttonpic1,newgameRect)
        screen.blit(buttonpic1,instrRect)
        screen.blit(ktcFontBody2.render("Menu",True,(0,0,0)),(437,617,150,100))
        screen.blit(ktcFontBody2.render("Instructions",True,(0,0,0)),(37,617,150,100))
        screen.blit(ktcFontBody2.render("New Game",True,(0,0,0)),(706,617,150,100))
        if menuRect.collidepoint((mx,my)):
            draw.rect(screen,(255,255,255),menuRect,2)
            if mb[0]==1:
                return "menu"
        else:
            draw.rect(screen,(0,0,0),menuRect,2)
        if newgameRect.collidepoint((mx,my)):
            draw.rect(screen,(255,255,255),newgameRect,2)
            if mb[0]==1:
                return "play"
        else:
            draw.rect(screen,(0,0,0),newgameRect,2)
        if instrRect.collidepoint((mx,my)):
            draw.rect(screen,(255,255,255),instrRect,2)
            if mb[0]==1:
                return "instructions"
        else:
            draw.rect(screen,(0,0,0),instrRect,2)

        if mb[0]==1:
            mpos=pos(mx,my,player)
            if mpos!=None:
                marbles,re=moveMarbles2(player,marbles,mpos)
                mpos=None
                drawMarbles(screen,marbles)
                if re: #extra turn
                    mpos=pos(mx,my,player)
                    marbles,re=moveMarbles2(player,marbles,mpos)
                else:
                    player=1-player

            #updates the user
            drawMarbles(screen,marbles)
            screen.blit(ktcFontBody4.render("Player "+str(player+1)+"'s turn",True,(0,0,0)),turnRect)

        #the game is finished
        if checkDone(marbles) and done==False:
            done=True

            #adds up all the marbles
            for i in range(1,7,1):
                marbles[0][0]+=marbles[0][i]
                marbles[1][0]+=marbles[1][i]
            
            drawMarbles(screen,marbles)
            draw.rect(alpha1,(255,255,255,111),(0,0,1000,750))
            screen.blit(alpha1,(0,0))
            screen.blit(buttonpic2,endRect)
            draw.rect(screen,(0,0,0),endRect,2)

            #Tells the players who won.
            if marbles[0][0]>marbles[1][0]:
                screen.blit(ktcFontBody2.render("Player 1 wins!",True,(0,0,0)),(355,225))
            elif marbles[1][0]>marbles[0][0]:
                screen.blit(ktcFontBody2.render("Player 2 wins!",True,(0,0,0)),(355,225))
            else:
                screen.blit(ktcFontBody1.render("Tie!",True,(0,0,0)),(430,225))
            screen.blit(ktcFontBody2.render("Player 1: "+str(marbles[0][0]),True,(0,0,0)),(375,340))
            screen.blit(ktcFontBody2.render("Player 2: "+str(marbles[1][0]),True,(0,0,0)),(375,430))

        display.flip()
    return "exit"

#takes the user to different parts of the game
while page!="exit":
    if page=="menu":
        page=menu()
    if page=="play":
        page=play()
    if page=="instructions":
        page=instructions()
    if page=="credit":
        page=credit()
    if page=="kalahone":
        page=kalahone()
    if page=="kalahtwo":
        page=kalahtwo()

font.quit()
quit()
