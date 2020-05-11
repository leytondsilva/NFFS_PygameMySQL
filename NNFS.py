import pygame
import time
import random
import db
import mysql.connector
from mysql.connector import errorcode
from mysql.connector import Error



pygame.init()
#Screeen Size definitions:
display_width = 800
display_height = 600

#Colour Definition in RGB Tuples:
black = (0,0,0)
white = (255,255,255)
red = (200,0,0)
green = (0,200,0)
bright_red = (255,0,0)
bright_green = (0,255,0)

myfont=pygame.font.SysFont("monospace",30)
blackcolor=(0,0,0)

block_color = (53,115,255)

car_width = 73

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('No Need for Speed')
clock = pygame.time.Clock()

carImg = pygame.image.load('racecar.png')
gameIcon = pygame.image.load('racecar.png')

pygame.display.set_icon(gameIcon)

pause = False
dodged=0
#crash = True

def things_dodged(count):
    font = pygame.font.SysFont("comicsansms", 25)
    text = font.render("Score: "+str(count), True, black)
    gameDisplay.blit(text,(0,0))

def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

def car(x,y):
    gameDisplay.blit(carImg,(x,y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

##def message_display(text):
##    largeText = pygame.font.SysFont("comicsansms",115)
##    TextSurf, TextRect = text_objects(text, largeText)
##    TextRect.center = ((display_width/2),(display_height/2))
##    gameDisplay.blit(TextSurf, TextRect)
##
##    pygame.display.update()
##
##    time.sleep(2)
##
##    game_loop()



def crash1():

    gameDisplay.fill(white)
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects("You Crashed", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    #db.insert(name,score)
    b=True
    while b:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                quitgame()
                b=False

        button("Play Again",150,450,100,50,green,bright_green,game_loop)
        button("Leaderboard!",300,450,200,50,green,bright_green,lb)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)

def crash():

    global dodged

    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    gameDisplay.fill(white)
    input_box = pygame.Rect((display_width/2),(display_height/1.5), 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    largeText = pygame.font.SysFont("comicsansms",48)
    TextSurf, TextRect = text_objects("Enter your name:", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done=True
                        db.insert(text,dodged)
                        crash1()
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        txt_surface = font.render(text, True, color)
        # Resize the box if the text is too long.
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        # Blit the text.
        gameDisplay.blit(txt_surface, (input_box.x+5, input_box.y+5))
        # Blit the input_box rect.
        pygame.draw.rect(gameDisplay, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)

def button(msg,x,y,w,h,ic,ac,action=None):

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)


def quitgame():
    db.disp()
    pygame.quit()
    quit()

def exi():
    pygame.quit()
    quit()

def unpause():
    global pause
    pause = False


def paused():
    global pause
    largeText = pygame.font.SysFont("comicsansms",115)
    TextSurf, TextRect = text_objects("Paused", largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)


    while pause:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                quitgame()
                pause=False

        #gameDisplay.fill(white)


        button("Continue",150,450,100,50,green,bright_green,unpause)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)


def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                exi()
                intro=False
            gameDisplay.fill(white)
        largeText = pygame.font.SysFont("comicsansms",80)
        TextSurf, TextRect = text_objects("No Need for Speed", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)
        button("GO!",150,450,100,50,green,bright_green,game_loop)
        button("Leaderboard!",300,450,200,50,green,bright_green,lb)
        button("Quit",550,450,100,50,red,bright_red,quitgame)
        pygame.display.update()
        clock.tick(15)
def lb():
    intro = True
    try:
       mySQLconnection = mysql.connector.connect(host='localhost',
                                 database='gameboard',
                                 user='root',
                                 password='')

       sql_select_Query = "SELECT * FROM user_info ORDER BY score DESC"
       cursor = mySQLconnection.cursor()
       cursor.execute(sql_select_Query)
       records = cursor.fetchall()
       rc = cursor.rowcount
       print("Total number of rows in student is - ", cursor.rowcount)
       print ("Printing each row's column values i.e.  student record")


       cursor.close()

    except Error as e :
        print ("Error while connecting to MySQL", e)
    finally:
        #closing database connection.
        if(mySQLconnection.is_connected()):
            mySQLconnection.close()
            print("MySQL connection is closed")
    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                exi()
                intro=False
            gameDisplay.fill(white)
        largeText = pygame.font.SysFont("comicsansms",40)
        TextSurf, TextRect = text_objects("HighScore", largeText)

        TextRect.center = (100,20)
        gameDisplay.blit(TextSurf, TextRect)


        font = pygame.font.SysFont("comicsansms", 25)
        text = font.render("Rank         Name          score", True, black)
        gameDisplay.blit(text,(5,50))



        font = pygame.font.SysFont("comicsansms", 25)
        if rc >= 1:
            text = font.render("1             "+str((records[0])[0]) +"             "    +str((records[0])[1]) , True, black)
            gameDisplay.blit(text,(5,80))
        if rc >= 2:
            text = font.render("2             "+str((records[1])[0]) +"             "    +str((records[1])[1]), True, black)
            gameDisplay.blit(text,(5,110))
        if rc >= 3:
            text = font.render("3             "+str((records[2])[0]) +"             "    +str((records[2])[1]), True, black)
            gameDisplay.blit(text,(5,140))
        if rc >= 4:
            text = font.render("4             "+str((records[3])[0]) +"             "    +str((records[3])[1]), True, black)
            gameDisplay.blit(text,(5,170))
        if rc >= 5:
            text = font.render("5             "+str((records[4])[0]) +"             "    +str((records[4])[1]), True, black)
            gameDisplay.blit(text,(5,200))
        if rc >= 6:
            text = font.render("6             "+str((records[5])[0]) +"             "    +str((records[5])[1]), True, black)
            gameDisplay.blit(text,(5,230))
        if rc >= 7:
            text = font.render("7             "+str((records[6])[0]) +"             "    +str((records[6])[1]), True, black)
            gameDisplay.blit(text,(5,260))
        if rc >= 8:
            text = font.render("8             "+str((records[7])[0]) +"             "    +str((records[7])[1]), True, black)
            gameDisplay.blit(text,(5,290))
        if rc >= 9:
            text = font.render("9             "+str((records[8])[0]) +"             "    +str((records[8])[1]), True, black)
            gameDisplay.blit(text,(5,320))
        if rc >= 10: 
            text = font.render("10            "+str((records[9])[0]) +"             "    +str((records[9])[1]), True, black)
            gameDisplay.blit(text,(5,350))


        button("GO!",150,450,100,50,green,bright_green,game_loop)
        button("Quit",550,450,100,50,red,bright_red,quitgame)

        pygame.display.update()
        clock.tick(15)



def game_loop():
    global pause
    global dodged

    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0

    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 4
    thing_width = 100
    thing_height = 100

    thingCount = 1

    dodged = 0

    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitgame()
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_p:
                    pause = True
                    paused()


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        gameDisplay.fill(white)

        # things(thingx, thingy, thingw, thingh, color)
        things(thing_startx, thing_starty, thing_width, thing_height, block_color)



        thing_starty += thing_speed
        car(x,y)
        things_dodged(dodged)

        if x > display_width - car_width or x < 0:
            crash()

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0,display_width)
            dodged += 1
            thing_speed += 1
            thing_width += (dodged * 1.2)

        if y < thing_starty+thing_height:
            print('y crossover')

            if x > thing_startx and x < thing_startx + thing_width or x+car_width > thing_startx and x + car_width < thing_startx+thing_width:
                print('x crossover')
                crash()

        pygame.display.update()
        clock.tick(75)

game_intro()
game_loop()

quitgame()
