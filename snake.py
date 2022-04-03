import sys 
from os import path
import tkinter as tk
from PIL import Image,ImageTk
from random import randint

MOVE_INCREMENT = 20
MOVES_PER_SECOND = 15
#moves_per_second = 15
GAME_SPEED = 1000 // MOVES_PER_SECOND

class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(width=600,height=620,background="black",highlightthickness=0)

        self.snake_positions=[(100,100),(80,100),(60,100)]
        self.food_position=self.set_new_food_position()
        self.direction="Right"

        self.score=0

        self.load_assets()
        self.create_objects()

        self.bind_all("<Key>",self.on_key_press)
        self.pack()
        self.after(GAME_SPEED,self.perform_actions)
        
    def load_assets(self):
        try:
            #bundle_dir=getattr(sys,"_MEIPASS",path.abspath(path.dirname(__file__)))
            #path_to_snake=path.join(bundle_dir,"assets","snake.png") 
            self.snake_body_image=Image.open("./asserts/snake.png") # ovde zamenim putanju do slike sa path_to_snake
            self.snake_body=ImageTk.PhotoImage(self.snake_body_image)

            #path_to_food=path.join(bundle_dir,"assets","food.png") 
            self.food_image=Image.open("./asserts/food.png") # ovde zamenim putanju do slike sa path_to_food
            self.food=ImageTk.PhotoImage(self.food_image)
        except IOError as error:
            print(error)
            root.destroy()

    def create_objects(self):
        self.create_text(100,12,text=f"Score: {self.score}",tag="score",fill="pink",font=("TkDefaultFont",16))
        for x,y in self.snake_positions:
            self.create_image(x,y,image=self.snake_body,tag="snake") #tag vraca slike iz canvasa ili ih nadje u canvasu

        self.create_image(self.food_position[0],self.food_position[1],image=self.food,tag="food") # takodje, mozemo da napisemo i kao *self.food_position

        self.create_rectangle(7,27,593,613,outline="blue") #govori gde ce da pocne i da se zavrsi, tj. gore levo i dole desno, te koordinate

    def check_collisions(self):
        head_x_position,head_y_position=self.snake_positions[0]

        return (head_x_position in (0,600) or head_y_position in (20,620) or (head_x_position,head_y_position) in self.snake_positions[1:]) # proverava da li je zmija izasla van ovih granica, a isto proveravam da li je glava jedan od elemenata tela zmije

    def check_food_collision(self):
        if self.snake_positions[0]==self.food_position:
            self.score+=1
            self.snake_positions.append(self.snake_positions[-1]) # poslednji element se dodaje na zmiju

            self.create_image(*self.snake_positions[-1],image=self.snake_body,tag="snake")

            #if self.score %5==0:
                #global moves_per_second
                #moves_per_second +=1

            self.food_position=self.set_new_food_position()
            self.coords(self.find_withtag("food"),self.food_position)

            score=self.find_withtag("score")
            self.itemconfigure(score,text=f"Score: {self.score}",tag="score")

    def end_game(self):
        self.delete(tk.ALL) # izbrisace sve iz njega
        self.create_text(self.winfo_width()/2,self.winfo_height()/2,text=f"Game over. You score is {self.score}",fill="red",font=("TkDefaultFont",20))
        
    def move_snake(self):
        head_x_position,head_y_position=self.snake_positions[0] # ovo je 0, jer smo uzeli prvu torku (100,100), koja nam je glava zmije, a ostale torke su telo zmije
        
        if self.direction=="Left":
            new_head_position=(head_x_position - MOVE_INCREMENT, head_y_position) # definise poziciju glave
        elif self.direction=="Right":
            new_head_position=(head_x_position + MOVE_INCREMENT, head_y_position)
        elif self.direction=="Down":
            new_head_position=(head_x_position, head_y_position + MOVE_INCREMENT)
        elif self.direction=="Up":
            new_head_position=(head_x_position, head_y_position - MOVE_INCREMENT)

        self.snake_positions=[new_head_position] + self.snake_positions[:-1]  

        for segment,position in zip(self.find_withtag("snake"),self.snake_positions): # pronalazimo sve elemente koji imaju tag=snake i sve pozicije
            self.coords(segment,position) #daje trenutne koordiante kad je samo segment, a sa position pomera element na novu poziciju

    def on_key_press(self,e):
        new_direction=e.keysym
        all_directions=("Up","Down","Left","Right")
        opposites=({"Up","Down"},{"Left","Right"})

        if (new_direction in all_directions and {new_direction,self.direction} not in opposites):
            self.direction=new_direction

    def perform_actions(self):
        if self.check_collisions():
            self.end_game()
            return
        self.check_food_collision()
        self.move_snake()
        self.after(GAME_SPEED,self.perform_actions) #poziva ovu definisanu funkciju nakon 75 milisekundi

    def set_new_food_position(self):
        while True:
            x_position=randint(1,29) * MOVE_INCREMENT
            y_position=randint(3,30) * MOVE_INCREMENT
            food_position=(x_position,y_position)

            if food_position not in self.snake_positions:
                return food_position

try:
    root=tk.Tk()
    root.title("Snake")
    root.resizable(False,False)

    board=Snake()
    board.pack()


    root.mainloop()
except:
    import traceback
    traceback.print_exc()
    input("Press Enter to end...")