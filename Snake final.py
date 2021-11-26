"""
Snake - Game
Zapoctovy program
Michaela Markova, 1. rocnik, kruh 37
zimni semestr 2019/20
Programovani 1, NPRG030
"""

import pygame
import random

pygame.init() #initialisation

pygame.display.set_caption("SNAKE") #window caption

#colors
red = (255, 0, 0)
green = (9, 255, 25)
black = (0, 0, 0)
blue = (0, 0, 201)
yellow = (255, 255, 18)

#screen settings
width = 800
height = 600
square = 20 #size of the "pixel" (square, block, whatever you call it)
screen = pygame.display.set_mode((width, height)) #takes touple and makes window with given measurements
highest_score = 0

#fps settings
clock = pygame.time.Clock()
snake_speed = 8

class Message:
    """class for showing text in the game"""
    def __init__(self, msg):
        self.msg = msg
    font = pygame.font.SysFont(None, 50) #makes the font object out of the system fonts, with the given size
    def blit_message(self, where):
        mesg = self.font.render(self.msg, True, red)    #makes the new surface with given text, antialias (if True, then the text has smooth edges)
                                                        #and the color of the text
        screen.blit(mesg, [width//10, where] ) #shows the new surface on the screen

class Food:
    food_x = 0 #coordinates of food
    food_y = 0
    def generate_position(self):
        """generating of the food"""
        self.food_x = int(round(random.randrange(0, width - square)//square)*square) #generates the coordinate of the food in the range of window
        self.food_y = int(round(random.randrange(0, height - square)//square)*square) #size, then divides and times that number by size of the square
                                                                                    #so the food will appear in the grid and wont be shifted
    def draw(self):
        """draws food on the screen"""
        pygame.draw.rect(screen, yellow, [self.food_x, self.food_y, square, square])
        
    def food_coordinates(self):
        """returns the coordinates of the food"""
        return [self.food_x, self.food_y]
        
class Snake():
    """
    Snake class with different methods,
    that express different properties of snake in the game
    """
    
    def __init__(self, x, y, delta_x, delta_y, snake_list, lenght, head):
        self.x = x #initial coordinates
        self.y = y
        self.delta_x = delta_x #change of the coordinates
        self.delta_y = delta_y
        self.snake_list = snake_list #snake is represented by a list of pieces, every piece of snake has it's own coordinates
        self.lenght = lenght #lenght of the snake
        self.head = head    #coordinates of head of the snake in a form of list
        
    def direction(self, direct):
        """keeps the direction of snake's movement, until it's changed"""
        if direct == "left":
            self.delta_x = -square
            self.delta_y = 0
        elif direct == "right":
            self.delta_x = square
            self.delta_y = 0
        elif direct == "down":
            self.delta_x = 0
            self.delta_y = square
        elif direct == "up":
            self.delta_x = 0
            self.delta_y = -square
            
    def wall_collision(self):
        """checks, if the head didn't run into the wall"""
        if self.x >= width or self.x < 0 or self.y >= height or self.y < 0:
            return True
        
    def move_direction(self):
        """changing the coordinates to make the move itself"""
        self.x = self.x + self.delta_x #in the beginning delta = 0, snake doesn't move
        self.y = self.y + self.delta_y #then the coordinates change according to the direction
        
    def move_snake(self):
        """makes the illusion of snake moving"""
        self.head = [] #small list of the head of the snake, into which I put two coordinates
        self.head.append(self.x)
        self.head.append(self.y)
        self.snake_list.append(self.head) #then I append the head to the list of snake (so it's in the end of the list)
        if len(self.snake_list) > self.lenght:
            del self.snake_list[0]  #we added head to the snake_list, so lenght of snake_list increased, but if the snake's lenght shouldn't
                                    #increase (it increases just in the case he ate the food), so
                                    #we cut off his tail piece (which is on position [0] in snake_list)
            
    def self_collision(self):
        """checks, if the head didn't run into the snake instelf"""
        for x in self.snake_list[:-1]: #check every piece, except for the last one (last one is the head)
            if x == self.head: #head hits one of the pieces of body
                return True
            
    def draw_snake(self):
        """draws the snake on the screen"""
        for coordinate in self.snake_list[:-1]: #pieces of snake except for head
            pygame.draw.rect(screen, green, [coordinate[0], coordinate[1], square, square]) #draws the piece on given coordinates and of given size
        pygame.draw.rect(screen, blue, [self.head[0], self.head[1], square, square]) #same, just for head
        
    def head_coordinates(self):
        """returns the coordinates of head in a form of list"""
        return [self.x, self.y] #even "return self.head" works
    
    def increase_lenght(self):
        """increases the lenght of the snake"""
        self.lenght += 1
        
    def return_snake(self):
        """returns the list of the snake"""
        return self.snake_list

def GameLoop():
    quit_game = False
    game_over = False

    global highest_score
    score = 0

    #initialisation of snake, making it appear in the middle of the screen in the grid
    snake = Snake((((width//2)//square)*square), (((height//2)//square)*square), 0, 0, [], 1, [])

    food1 = Food()
    food2 = Food()
    food1.generate_position() #generates the position for food
    food2.generate_position()

    while not quit_game: #loop of the game

        while game_over == True:
            screen.fill(black) #game over screen
            Message("Game over. ").blit_message(height//5)
            Message("Your score is " + str(score)).blit_message((height//5)*2)
            Message("Highest score " + str(highest_score)).blit_message((height//5)*3)
            Message("Press Esc - Quit or Space - Play again").blit_message((height//5)*4)
            pygame.display.update() #updates the screen so the messages show up

            for event in pygame.event.get(): #pygame.event.get() returns the list of events (pressed keys, mouse position etc.)
                if event.type == pygame.QUIT: #clicked the cross in the corner of the window
                    quit_game = True
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        quit_game = True #completely jumps out of the game and it terminates itself
                        game_over = False
                    if event.key == pygame.K_SPACE:
                        GameLoop() #starts again the game loop

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: #clicked the cross in the corner
                quit_game = True #jumps out of this loop and ends the game
                
            if event.type == pygame.KEYDOWN: #the key is pressed down
                if event.key == pygame.K_LEFT:
                    snake.direction("left")
                elif event.key == pygame.K_RIGHT:
                    snake.direction("right")
                elif event.key == pygame.K_DOWN:
                    snake.direction("down")
                elif event.key == pygame.K_UP:
                    snake.direction("up")
                
        screen.fill(black) #fills the whole screen with the black (so the snake doesnt draw colorful line like a snail)

        #then draws other elements (food, snake) on the black screen in it's (new) position
        
        food1.draw()
        food2.draw()

        snake.move_direction()
        snake.move_snake() #makes the snake move

        if snake.wall_collision(): #hits the wall
            game_over = True
        
        if snake.self_collision(): #hit myself
            game_over = True

        snake.draw_snake() #draws the snake
        
        pygame.display.update() #updates the part of the screen with some change

        if snake.head_coordinates() == food1.food_coordinates(): #snake eats the food
            food1.generate_position()
            while food1.food_coordinates() in snake.return_snake() or (food2.food_coordinates() == food1.food_coordinates()):
                                                                    #in a case the food would spawn on the snake or in another food,
                                                                    #I just keep changing its coordinates, until it spawns correctly
                food1.generate_position() 
            snake.increase_lenght() #wont cut of the last piece (tail) of a snake, as it would normally happen, if it didn't eat the food
            score += 1 #increases the score and compares with highest scrore
            if score > highest_score:
                highest_score = score
            
        if snake.head_coordinates() == food2.food_coordinates(): #same, just for second food
            food2.generate_position()
            while (food2.food_coordinates() in snake.return_snake()) or (food2.food_coordinates() == food1.food_coordinates()):
                food2.generate_position()
            snake.increase_lenght()
            score += 1
            if score > highest_score:
                highest_score = score
                
        clock.tick(snake_speed) #this stops the game loop for a bit (otherwise the snake would move insanely fast)

    pygame.quit() #deinitialisation
    quit()
    
GameLoop()

    
