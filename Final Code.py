from math import remainder
import random
import tkinter
from tkinter.constants import BOTH, YES
from Names import list_of_names
import itertools
import tkinter as tk
from tkinter import filedialog, Text
import time
from PIL import Image, ImageTk


#Function that makes pairings and takes into account who we know are not matches
def make_pairings(options, NotMatches):
    random_pairings_list = []
    remainder = []
    seen = NotMatches

    for pair in options:
        if pair in seen:
            for i in pair:
                remainder.append(i)
        else:
            random_pairings_list.append(pair)

    if len(remainder) != 0:
        remainderpairs = []
        for i in range(0,(len(remainder) //2)):
            pair = set()
            pair.add(remainder[i])
            pair.add(remainder[(len(remainder) // 2) + i])
            remainderpairs.append(pair)
        return random_pairings_list, remainderpairs
    else:
        return random_pairings_list, remainder

#Function that pairs with the notmatches 
def deal_with_notmatches(pairs, NotMatches):
    finallist = []
    pairings, remainder = make_pairings(pairs, NotMatches)

    for i in pairings:
        finallist.append(i)

    for i in remainder:
        finallist.append(i)

    return finallist

#The random pairings function that is the backbone to each round
def random_pairings(contestants, NotMatches):
    
    #shuffle the contestants so that the matching is random each round

    #random.shuffle(contestants)
    
    options = []
    for i in range(0, len(contestants), 2):
        pair = set()

        pair.add(contestants[i])
        pair.add(contestants[i+1])
        
        options.append(pair)
    matches = deal_with_notmatches(options, NotMatches)          
    return matches

#Pulls names from an external file to create a list of 16 names
def generate_players():
    players = random.sample(list_of_names, 16)
    return players
    
variable = 1

#the main class where the magic happens
class GamePlay:
    def __init__(self):
        self.week_num = 1
        contestants = generate_players() #create a list of players
        contestants_copy = []
        for i in contestants:
            contestants_copy.append(i) #creates a copy of contestants just for safe measure
        self._contestants = contestants_copy
        if self.week_num == 1:
            self._originalcontestants = contestants.copy() #this is for the purpose of storing the original list somewhere
                                                           # since the original list will get changed throughout the game
        n = 1
        self._beenmatched = [n for i in self._originalcontestants] #a list of numbers that will get filled in as the pairs get matched

        print(contestants)
        print(self._contestants)
        print(self._originalcontestants)

        #Keep track of the matches that are already known to not be perfect matches
        self._notmatches = []

        #define the root
        self.root = tk.Tk()
        self.root.title("Main Menu")
        self.canvas = tk.Canvas(self.root, height = 700, width = 700) #bg="#FF0789")
        self.canvas.grid(columnspan=3, rowspan=3)
        #Open the image for the background
        logo = Image.open('C:\\CSE2050\\Honors\\phonto (1).jpg')
        logo = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(image=logo)
        logo_label.image = logo
        logo_label.grid(column=0, row=0)
        #the dark blue inner square
        self.myFrame = tk.Frame(self.root, bg = "#202A44")
        self.myFrame.place(relwidth=0.7, relheight=0.7, relx=0.15, rely=0.15)

        #creates the large yellow text in the middle of the opening screen
        self.MainPage_Text = tk.Label(self.myFrame, text = "ARE YOU \nTHE ONE?", fg = "White", bg = "#202A44", 
                                font = ("Impact", 80))
        
        #places the yellow text in the center of the window
        self.MainPage_Text.place(x = 250, y = 225, anchor="center")

        #create a button that when clicked, initializes the game
        self.PlayButton = tk.Button(self.myFrame, text = "Play Game", padx = 15, pady = 7, fg = "white", bg = "#24BCA8", font = "Impact",
                                command = self.initializegame)

        #places the button below the main text                        
        self.PlayButton.place(x=90, y=420, anchor="center")

        self.PlayWithOwnCharButton = tk.Button(self.myFrame, text = "Play with Own Characters", padx = 15, pady = 7, fg = "white", bg = "#24BCA8", font = "Impact", 
                                command = self.entercharacters)

        self.PlayWithOwnCharButton.place(x = 350, y = 420, anchor = "center")

        self.QuitButton = tk.Button(self.myFrame, text = "Quit", padx = 15, pady = 7, fg = "white", bg = "#24BCA8", font = "Impact",
                                command = self.quit)

        self.QuitButton.place(x=50, y=50, anchor = "center")
        
        self.root.mainloop()

        
    def entercharacters(self):
        #this opens up a window for the user to enter a list of names they want to use

        self.entercharacterswindow = tk.Toplevel(self.root, bg = "#202A44")
        self.entercharacterswindow.title("Truth Booth")
        self.entercharacterswindow.geometry("500x500")

        self.nameslabel = tk.Label(self.entercharacterswindow, text = "Enter 16 names below \nseparated by a comma", fg = "White", bg = "#202A44", 
                                font = ("Impact", 30)) #creates the text at the top of the window

        self.nameslabel.place(x = 250, y = 100, anchor = "center")
                            
        #creates a text box
        inputtxt = tk.Text(self.entercharacterswindow,
                   height = 10,
                   width = 30)

        inputtxt.place(x = 250, y = 250, anchor = "center")
        
        #the following function takes the input text and converts it into a list of names to be used during the game. 
        #it will raise an error for the user if the user has not input exactly 16 names
        def ExportInput():
            inp = inputtxt.get(1.0, "end-1c")
            self._contestants = inp.split(", ")
            if len(self._contestants) < 16:
                self.entercharacterswindow.destroy()
                errorwindow = tk.Toplevel(self.root, bg = "#202A44")
                errorwindow.title("Error")
                errorwindow.geometry("500x500")
                errorlabel = tk.Label(errorwindow, text = "you need at exactly 16 players!", fg = "White", bg = "#202A44", 
                                        font = ("Impact", 20))
                errorlabel.place(x = 250, y = 250, anchor = "center")
                def destroyhelp():
                    errorwindow.destroy()
                    self.entercharacters()
                errorwindow.after(3000, lambda: destroyhelp())
                
                return
                
            if self.week_num == 1:
                self._originalcontestants = self._contestants.copy()
            n = 1
            self._beenmatched = [n for i in self._originalcontestants]
            self.submitbutton.destroy()
            self.entercharacterswindow.destroy()
            self.PlayWithOwnCharButton.destroy()
            self.initializegame()

        #calls the exportinput function
        self.submitbutton = tk.Button(self.entercharacterswindow, text = "submit", fg = "white", bg = "#202A44", 
                                        command = ExportInput)

        self.submitbutton.place(x = 250, y = 400, anchor = "center")

    def quit(self):
        self.root.destroy() #destroys the whole game

    #for the ease of creating a lot of buttons at once
    def create_button(self, contestants, color = None, num = None):
        color = "#202A44"
        return tk.Button(self.trackingwindow, text = str(contestants[num]), padx = 4, pady= 2, fg = "white", bg = color, font = "Impact")
        
    def initializegame(self, contestants = None, week = 1):
        self.PlayWithOwnCharButton.destroy()

        #generate a list of perfect matches that the truth buth will compare
        #guesses to 
        self._perfectmatches = random_pairings(self._contestants, self._notmatches)

        self.week_num = week

        #Gets rid of the main page
        self.PlayButton.destroy()
        self.QuitButton.destroy()
        self.MainPage_Text.destroy()

        #initialize a continue button
        self.ContinueButton = tk.Button(self.myFrame, text = "Match Contestants!", padx = 15, pady = 7, fg = "white", bg = "#24BCA8", font = "Impact",
                                command = self.random_guess_match)
        
        self.ContinueButton.place(x=250,y=400,anchor="center")

        #opens up a window wher we will keep track of the players
        self.trackingwindow = tk.Toplevel(self.root, bg = "white")
        self.trackingwindow.title("Who Has Been Matched?")
        self.trackingwindow.geometry("300x600")
        def resize_image(event):
            new_width = event.width
            new_height = event.height
            image = copy_of_image.resize((new_width, new_height))
            photo = ImageTk.PhotoImage(image)
            label.config(image = photo)
            label.image = photo #avoid garbage collection

        #putting an image in the background of the tracking window
        image = Image.open('C:\\CSE2050\\Honors\\pinkandblue.png')
        copy_of_image = image.copy()
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(self.trackingwindow, image = photo)
        label.bind('<Configure>', resize_image)
        label.pack(fill=BOTH, expand = YES)
        self.list_of_buttons = {}

        #the following is a lot of buttons being created
        self.button1 = self.create_button(self._contestants, "gray", 0)
        self.list_of_buttons[self.button1] = self._contestants[0] #adding this button to a dictionary of buttons for the purpose of later 
                                                                  #making those buttons green
        self.button1.place(x=75, y=25, anchor = "center")

        self.button2 = self.create_button(self._contestants, "gray", 1)
        self.list_of_buttons[self.button2] = self._contestants[1]
        self.button2.place(x=75, y= 100, anchor = "center")

        self.button3 = self.create_button(self._contestants, "gray", 2)
        self.list_of_buttons[self.button3] = self._contestants[2]
        self.button3.place(x=75, y=175, anchor = "center")

        self.button4 = self.create_button(self._contestants, "gray", 3)
        self.list_of_buttons[self.button4] = self._contestants[3]
        self.button4.place(x=75, y=250, anchor = "center")

        self.button5 = self.create_button(self._contestants, "gray", 4)
        self.list_of_buttons[self.button5] = self._contestants[4]
        self.button5.place(x=75, y=325, anchor = "center")

        self.button6 = self.create_button(self._contestants, "gray", 5)
        self.list_of_buttons[self.button6] = self._contestants[5]
        self.button6.place(x=75, y=400, anchor = "center")

        self.button7 = self.create_button(self._contestants, "gray", 6)
        self.list_of_buttons[self.button7] = self._contestants[6]
        self.button7.place(x=75, y=475, anchor = "center")

        self.button8 = self.create_button(self._contestants, "gray", 7)
        self.list_of_buttons[self.button8] = self._contestants[7]
        self.button8.place(x=75, y=550, anchor = "center")

        self.button9 = self.create_button(self._contestants, "gray", 8)
        self.list_of_buttons[self.button9] = self._contestants[8]
        self.button9.place(x=200, y=25, anchor = "center")

        self.button10 = self.create_button(self._contestants, "gray", 9)
        self.list_of_buttons[self.button10] = self._contestants[9]
        self.button10.place(x=200, y=100, anchor = "center")

        self.button11 = self.create_button(self._contestants, "gray", 10)
        self.list_of_buttons[self.button11] = self._contestants[10]
        self.button11.place(x=200, y=175, anchor = "center")

        self.button12 = self.create_button(self._contestants, "gray", 11)
        self.list_of_buttons[self.button12] = self._contestants[11]
        self.button12.place(x=200, y=250, anchor = "center")

        self.button13 = self.create_button(self._contestants, "gray", 12)
        self.list_of_buttons[self.button13] = self._contestants[12]
        self.button13.place(x=200, y=325, anchor = "center")

        self.button14 = self.create_button(self._contestants, "gray", 13)
        self.list_of_buttons[self.button14] = self._contestants[13]
        self.button14.place(x=200, y=400, anchor = "center")

        self.button15 = self.create_button(self._contestants, "gray", 14)
        self.list_of_buttons[self.button15] = self._contestants[14]
        self.button15.place(x=200, y=475, anchor = "center")

        self.button16 = self.create_button(self._contestants, "gray", 15)
        self.list_of_buttons[self.button16] = self._contestants[15]
        self.button16.place(x=200, y=550, anchor = "center")

        GamePlay.play(self)
        
        pass

    def play(self):
        self.weeklabel = None
        def new_round():
            self.root.destroy()
            game = GamePlay()
        
        if len(self._perfectmatches) <= 2:
            pass

        list_of_pairs_left = []
        for i in self._perfectmatches:
            for j in i:
                list_of_pairs_left.append(j)
        for name in self._originalcontestants:
            if name not in list_of_pairs_left:
                for key in self.list_of_buttons:
                    if self.list_of_buttons[key] == name:
                        key.configure(bg = "green")

        if len(self._perfectmatches) <= 1:
            
            self.ContinueButton.destroy()

            self.end_screen_label = tk.Label(self.myFrame, text = "Congratulations!, Everybody has \n found their One True Love <3", 
                                        fg = "pink", bg = "#202A44", font = ("Freestyle Script", 35))
            self.end_screen_label.place(x = 250, y = 250, anchor = "center")
            
            self.end_screen_label.after(5000, lambda: new_round())

            print("Congratulat ions! Everybody has found their One True Love <3")
            
            return

        self.weeklabel = tk.Label(self.myFrame, text = "Week {}".format(self.week_num), fg = "white", bg = "#202A44", font = ("Impact", 50))

        fflist = []
        ff1 = "Couples who spend at least \n 10 minutes a day \n laughing together are more \n likely to have a \n stronger relationship"
        fflist.append(ff1)
        ff2 = "It takes only 4 minutes \n to decide whether you like \n someone or not"
        fflist.append(ff2)
        ff3 = "Romantic love is biochemically\n indistinguishable from having\n a severe obsessive-compulsive\n disorder"
        fflist.append(ff3)
        ff4 = "Philophobia is the fear\n of falling in love."
        fflist.append(ff4)
        ff5 = "23 percent of the couples\n who meet through online \ndating end up marrying."
        fflist.append(ff5)
        ff6 = "There are about 3 million\n first dates every day\n worldwide."
        fflist.append(ff6)
        ff7 = "A survey revealed that\n 52 percent of women say \ntheir husband is not \ntheir soulmate."
        fflist.append(ff7)
        ff8 = "Statistically, men are more\n likely to say “I love you” \nin a relationship than women."
        fflist.append(ff8)
        ff9 = "The act of falling in \nlove is known to have a calming\n effect on a persons body \nand mind. "
        fflist.append(ff9)
        ff10 = "Its scientifically proven: \nbeing in love makes you \na less productive person."
        fflist.append(ff10)

        integer = random.randint(0, 9)

        self.funfactlabel = tk.Label(self.myFrame, text = fflist[integer], fg = "pink", bg = "#202A44", font = ("Forte", 20))
        self.funfactlabel.place(x = 250, y = 250, anchor = "center")
        self.weeklabel.place(x=250, y=100, anchor = "center")


    def random_guess_match(self):
        
        if self.weeklabel == None:
            pass
        else:
            self.weeklabel.destroy()
            self.funfactlabel.destroy()
    
        guess_pairings = random_pairings(self._contestants, self._notmatches)
    
        perfect_matches_for_round = 0
        
        if len(guess_pairings) == 2:
            if guess_pairings[0] not in self._perfectmatches:
                new_couple1 = set()
                x = guess_pairings[0].pop()
                y = guess_pairings[0].pop()
                z = guess_pairings[1].pop()
                w = guess_pairings[1].pop()
                new_couple1.add(x)
                new_couple1.add(z)
                new_couple2 = set()
                new_couple2.add(y)
                new_couple2.add(w)
                guess_pairings[0], guess_pairings[1] = new_couple1, new_couple2

        for i in guess_pairings:
            if i in self._perfectmatches:
                perfect_matches_for_round += 1
        
        if perfect_matches_for_round != 0:

            self.week_num += 1

            self.truthbooth = tk.Toplevel(self.root, bg = "#202A44")
            self.truthbooth.title("Truth Booth")
            self.truthbooth.geometry("700x700")
            
            test_couple_list = []
            for i in guess_pairings[0]:
                test_couple_list.append(i)

            textoptions = []
            textoption1 = "Looks like things are really heating up \n for {} and {}. \n \n Let's see if they're a perfect match!".format(test_couple_list[0], test_couple_list[1])
            textoptions.append(textoption1)
            textoption2 = "There seems to be some\n chemistry between \n {} and {} this week. \n \n Could this be their one true love?".format(test_couple_list[0], test_couple_list[1])
            textoptions.append(textoption2)
            textoption3 = "Wowza! \n {} and {} really hit it off \n this week! \n \n But is it really meant to be?".format(test_couple_list[0], test_couple_list[1])
            textoptions.append(textoption3)
            textoption4 = "{} and {} seem \n pretty confident \n in their pairing this week. \n \n Now it's all in the hands \n of the powers that be".format(test_couple_list[0], test_couple_list[1])
            textoptions.append(textoption4)
            integer = random.randint(0, 3)

            self.truthbooth_text = tk.Label(self.truthbooth,
                                    text = textoptions[integer],
                                    fg = "white", bg = "#202A44", font = ("Impact", 30))
            self.truthbooth_text.place(x = 350, y = 300, anchor = "center")
            self.TruthBooth_Button= tk.Button(self.truthbooth, text = "Are You The One?", padx = 15, pady = 7, fg = "white", bg = "#24BCA8", font = "Impact",
                                command = lambda : self.truth_booth(guess_pairings[0]))
        
            self.TruthBooth_Button.place(x=350,y=550,anchor="center")
            
        else:
            for i in guess_pairings:
                self._notmatches.append(i)
            self.week_num += 1
            GamePlay.play(self)
        
    def truth_booth(self, test_couple):
        self.TruthBooth_Button.place_forget()
        self.truthbooth_text.place_forget()

        truthboothlabel = tk.Label(self.truthbooth, text = "Welcome to the \n Truth Booth!", fg = "#FFFF00", bg = "#202A44", font = ("Impact", 50))
        
        truthboothlabel.place(x=350, y=100, anchor = "center")
        
        self.LeaveTruthBooth_Button= tk.Button(self.truthbooth, text = "Exit Truth Booth", padx = 15, pady = 7, fg = "white", bg = "#24BCA8", font = "Impact",
                                command = lambda : [self.truthbooth.destroy(), self.play()])
        
        self.LeaveTruthBooth_Button.place(x=350,y=500,anchor="center")
        
        print("you have made it to the truth booth")
        test_couple_list = []
        for i in test_couple:
            test_couple_list.append(i)

        print("testing {} with {}".format(test_couple_list[0], test_couple_list[1]))

        for i in self._perfectmatches:

            if test_couple == i:
                
                self._perfectmatches.remove(test_couple)

                if len(self._perfectmatches) <= 1:
                    self._perfectmatches.pop()
                    for i in self._perfectmatches:
                        for j in i:
                            self._contestants.remove(j)
    
                for i in test_couple:
                    print(self._originalcontestants)
                    print(self._contestants)
                    inde = self._originalcontestants.index(i)
                    
                    self._beenmatched[inde] = i

                self._notmatches.append(i)
                for i in test_couple:
                    self._contestants.remove(i)
                    
                print("You have found a perfect match!")

                Perfect_Match_Label = tk.Label(self.truthbooth, text = "You have found a Perfect Match!!!", fg = "pink",
                                            bg = "#202A44", font = ("Cooper Black", 30))
                Perfect_Match_Label.place(x = 350, y = 250, anchor = "center")

                return
        
        print("not a perfect match :(")
        self._notmatches.append(test_couple)
        Not_Match_Label = tk.Label(self.truthbooth, text = "It wasn't meant to be :(", fg = "white",
                                            bg = "#202A44", font = ("Cooper Black", 30))
        Not_Match_Label.place(x = 350, y = 250, anchor = "center")


if __name__ == "__main__":
    game = GamePlay()
    
