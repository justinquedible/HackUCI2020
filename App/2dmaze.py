import turtle
import maze_util
import math
import pygame
import cv2

wn = turtle.Screen()
wn.bgcolor("peru")
wn.title("Where are you spongebob?!")
wn.setup(700, 700)
wn.tracer(0)

# set the shapes to some picture
turtle.register_shape("assets/wall.gif")
turtle.register_shape("assets/FinishSmall.gif")
turtle.register_shape("assets/playersmall.gif")
turtle.register_shape("assets/down.gif")
turtle.register_shape("assets/up.gif")
turtle.register_shape("assets/lift.gif")

# create pen
class Pen(turtle.Turtle):
    def __init__(self, texture):
        turtle.Turtle.__init__(self)
        self.penup() # so not drawing anything yet
        self.shape(texture)
        self.speed(0)# is the fastest speed 

# create player
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("assets/FinishSmall.gif")
        self.penup()
        self.speed(0)
        self.level = 1

    # directions that the player can go into 
    def go_up(self):
        # calculate the spot to move to and see if there is a wall
        move_to_x = player.xcor()
        move_to_y = player.ycor() + 24

        # check if the space has a wall
        if(move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
        
    def go_down(self):
        # calculate the spot to move to and see if there is a wall
        move_to_x = player.xcor()
        move_to_y = player.ycor() - 24

        # check if the space has a wall
        if(move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_right(self):
        # calculate the spot to move to and see if there is a wall
        move_to_x = player.xcor() + 24
        move_to_y = player.ycor()

        # check if the space has a wall
        if(move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def go_left(self):
        # calculate the spot to move to and see if there is a wall
        move_to_x = player.xcor() - 24
        move_to_y = player.ycor()

        # check if the space has a wall
        if(move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
    
    def is_collision(self, other):
        a = self.xcor() - other.xcor()
        b = self.ycor() - other.ycor()
        distance = math.sqrt((a **2) + (b ** 2))

        if distance < 5:
            return True
        else:
            return False

    def go_ascend(self):
        x, y = player.pos()
        x = int((x + 288) / 24)
        y = int(( 288 - y) / 24)

        if maze.grid[self.level][x][y] == 3 or maze.grid[self.level][x][y] == 5:
            self.level = self.level + 1
            setup_maze(maze.getLevel(self.level))
    
    def go_descend(self):
        x, y = player.pos()
        x = int((x + 288) / 24)
        y = int(( 288 - y) / 24)

        if maze.grid[self.level][x][y] == 4 or maze.grid[self.level][x][y] == 5:
            self.level = self.level - 1
            setup_maze(maze.getLevel(self.level))

class EndMe(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("assets/playersmall.gif")
        self.penup()
        self.speed(0)

    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle()

# create level setup function
def setup_maze(level):
    # Create class instance of Pen
    wallPen.clearstamps()
    downStairPen.clearstamps()
    upStairPen.clearstamps()
    walls.clear()
    bothStairsPen.clearstamps()

    wallPen.goto(2000,2000)
    downStairPen.goto(2000,2000)
    upStairPen.goto(2000,2000)
    bothStairsPen.goto(2000,2000)
    endIt.goto(2000, 2000)

    #print(level)
    for x in range(len(level)):
        for y in range(len(level[x])):
            # get the character at each x, y coordinate
            # Note the order of y and x in the next line
            element = level[x][y]
            
            # calculate the sreen x, y coordinates
            screen_x = -288 + (x * 24) # each space is 24 bits wide
            screen_y = 288 - (y * 24)

            # check if it is a 0 (representing a wall)
            if element == 0:
                wallPen.goto(screen_x, screen_y)
                wallPen.stamp()
                # add wall, so user doesn't go through walls
                walls.append((screen_x, screen_y))
            elif element == 3: #Representing stairs going up
                upStairPen.goto(screen_x, screen_y)
                upStairPen.stamp()
            elif element == 4: #Representing stairs going down
                downStairPen.goto(screen_x, screen_y)
                downStairPen.stamp()
            elif element == 5: #Representing both stairs
                bothStairsPen.goto(screen_x, screen_y)
                bothStairsPen.stamp()
            
            # if character is a P (representing the player)
            if element == 2:
                player.goto(screen_x, screen_y)
                level[y][x] = 1
                
            if element == 9:
                endIt.goto(screen_x, screen_y)
    #Print floor #
    turtle.clear()
    turtle.color('red')
    style = ('Courier', 30, 'italic')
    turtle.penup()
    turtle.goto(-270,320)
    turtle.write(("Floor: " + str(player.level)), font=style, align='center')
    turtle.hideturtle()

# Plays music file
def play_music(musicFile):
    pygame.init()
    pygame.mixer.music.load(musicFile)
    pygame.mixer.music.play()

# Plays endgame patrick clip
def play_endgame():
    cap = cv2.VideoCapture("assets/patrick_clip.mp4")
    if (cap.isOpened()== False):
        print("Error opening video file")
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            cv2.imshow('Frame', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()

# Starts playing background music
play_music("assets/music_bg.mp3")

player = Player()

# Create walls coordinate list
walls = []

# set up the level
wallPen = Pen("assets/wall.gif")
upStairPen = Pen("assets/up.gif")
downStairPen = Pen("assets/down.gif")
bothStairsPen = Pen("assets/lift.gif")
endIt = EndMe()

maze = maze_util.Maze(25,25,25)
setup_maze(maze.getLevel(1))   # initialize the maze

# keyboard bindings
turtle.listen()
turtle.onkey(player.go_left, "Left")
turtle.onkey(player.go_right, "Right")
turtle.onkey(player.go_up, "Up")
turtle.onkey(player.go_down, "Down")
turtle.onkey(player.go_ascend, "q")
turtle.onkey(player.go_descend, "a")

# turn off screen updates
wn.tracer(0)

# main game loop
while True:
    # Check for player collision with the end location
    if player.is_collision(endIt):
        play_music("assets/screaming.mp3")
        play_endgame()
        endIt.destroy()
        print("Patrick has caught SpongeBob")
        turtle.bye()
    wn.update()