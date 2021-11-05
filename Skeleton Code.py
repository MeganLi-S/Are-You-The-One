from math import remainder
import random
import tkinter
from Names import list_of_names
import itertools
import tkinter as tk
from tkinter import filedialog, Text
import os

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

def deal_with_notmatches(pairs, NotMatches):
    finallist = []
    pairings, remainder = make_pairings(pairs, NotMatches)

    for i in pairings:
        finallist.append(i)

    for i in remainder:
        finallist.append(i)

    return finallist
def random_pairings(contestants, NotMatches):
    
    random.shuffle(contestants)
    
    options = []
    for i in range(0, len(contestants), 2):
        pair = set()

        pair.add(contestants[i])
        pair.add(contestants[i+1])
        
        options.append(pair)
    matches = deal_with_notmatches(options, NotMatches)          
    return matches


def generate_players():
    players = random.sample(list_of_names, 16)
    return players
    
variable = 1
class GamePlay:
    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Main Menu")
        self.canvas = tk.Canvas(self.root, height = 700, width = 700, bg="#FF0789")
        self.canvas.grid(columnspan=3, rowspan=3)
        #define the root
        

        #the dark blue inner square
        self.myFrame = tk.Frame(self.root, bg = "#0C1793")
        self.myFrame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

        #creates the large yellow text in the middle of the opening screen
        MainPage_Text = tk.Label(self.myFrame, text = "ARE \nYOU \nTHE \nONE?", fg = "#FFFF00", bg = "#0C1793", 
                                font = ("Cooper Black", 50))
        
        #places the yellow text in the center of the window
        MainPage_Text.place(x = 280, y = 250, anchor="center")

        #create a button that when clicked, initializes the game
        PlayButton = tk.Button(self.myFrame, text = "Play Game", padx = 15, pady = 7, fg = "white", bg = "#24BCA8", font = "Impact",
                                command = self.initializegame)

        #places the button below the yellow text                        
        PlayButton.place(x=280, y=450, anchor="center")

        QuitButton = tk.Button(self.myFrame, text = "Quit", padx = 15, pady = 7, fg = "white", bg = "#24BCA8", font = "Impact",
                                command = self.quit)

        QuitButton.place(x=280, y=500, anchor = "center")

        self.root.mainloop()

    def quit(self):
        self.root.destroy()
        
    def initializegame(self, contestants = None, week = 1):

        #generate a list of contestants
        #these contestants will remain the same throughout the entirety of the game
        contestants = generate_players()
        self._contestants = contestants

        #Keep track of the matches that are already known to not be perfect matches
        self._notmatches = []

        #generate a list of perfect matches that the truth buth will compare
        #guesses to 
        self._perfectmatches = random_pairings(self._contestants, self._notmatches)

        self.week_num = week

        self.newwindow = tk.Toplevel(self.root, bg = "#0C1793")
        self.newwindow.title("Are You The One?")
        self.newwindow.geometry("700x700")

        

        ContinueButton = tk.Button(self.newwindow, text = "Match Contestants!", padx = 15, pady = 7, fg = "white", bg = "#24BCA8", font = "Impact",
                                command = self.random_guess_match)
        
        ContinueButton.place(x=350,y=350,anchor="center")

        GamePlay.play(self)
        #prompt user to start a new week
            #when new week initialized, call random_guess_match()
        pass
    def play(self):
        #print("not matches:" + str(self._notmatches))
        if len(self._contestants) == 2:
            self.newwindow.destroy()
            self.final_window = tk.Toplevel(self.root, bg ="#FF0789")
            self.final_window.title("End of Game")
            self.final_window.geometry("700x700")
            end_screen_label = tk.Label(self.final_window, text = "Congratulations!, Everybody has \n found their One True Love <3", 
                                        fg = "white", bg = "#FF0789", font = ("Freestyle Script", 35))
            end_screen_label.place(x = 350, y = 350, anchor = "center")
            self.final_window.after(5000, lambda: self.final_window.destroy())

            print("Congratulat ions! Everybody has found their One True Love <3")
            
            return

        weeklabel = tk.Label(self.newwindow, text = "Week {}".format(self.week_num), fg = "#FFFF00", bg = "#0C1793", font = ("Cooper Black", 50))
        weeklabel.place(x=350, y=70, anchor = "center")
         #creates a new window when the game starts with the title of 'Are You The One?'
        #it is the same size (700x700) as the main menu
        


    def random_guess_match(self):
        #guess_pairings = randomize self._contestants into pairs
        

        guess_pairings = random_pairings(self._contestants, self._notmatches)
        #print("guess 1:" + str(guess_pairings))
        
        
        #print("guess 2:" + str(guess_pairings))

        perfect_matches_for_round = 0
        #compare guess_pairings to self._perfectmatches
        #print("guess pairings: " + str(guess_pairings))

        for i in guess_pairings:
            if i in self._perfectmatches:
                perfect_matches_for_round += 1
        #if perfect match:
            #perfect_matches_for_round += 1
        
        if perfect_matches_for_round != 0:

            self.week_num += 1

            self.truthbooth = tk.Toplevel(self.root, bg = "#0C1793")
            self.truthbooth.title("Truth Booth")
            self.truthbooth.geometry("700x700")
            self.TruthBooth_Button= tk.Button(self.truthbooth, text = "Are You The One?", padx = 15, pady = 7, fg = "white", bg = "#24BCA8", font = "Impact",
                                command = lambda : self.truth_booth(guess_pairings[0]))
        
            self.TruthBooth_Button.place(x=350,y=350,anchor="center")
            
        else:
            for i in guess_pairings:
                self._notmatches.append(i)
            self.week_num += 1
            GamePlay.play(self)
        
    def truth_booth(self, test_couple):
        self.TruthBooth_Button.place_forget()

        truthboothlabel = tk.Label(self.truthbooth, text = "Welcome to the \n Truth Booth!", fg = "#FFFF00", bg = "#0C1793", font = ("Cooper Black", 50))
        
        truthboothlabel.place(x=350, y=100, anchor = "center")
        
        self.LeaveTruthBooth_Button= tk.Button(self.truthbooth, text = "Exit Truth Booth", padx = 15, pady = 7, fg = "white", bg = "#24BCA8", font = "Impact",
                                command = lambda : [self.truthbooth.destroy(), self.play()])
        
        self.LeaveTruthBooth_Button.place(x=350,y=500,anchor="center")
        
        print("you have made it to the truth booth")

        if test_couple in self._perfectmatches:
            self._perfectmatches.remove(test_couple)
            for i in test_couple:
                self._contestants.remove(i)
            print("You have found a perfect match!")

            Perfect_Match_Label = tk.Label(self.truthbooth, text = "You have found a Perfect Match!!!", fg = "pink",
                                            bg = "#0C1793", font = ("Cooper Black", 30))
            Perfect_Match_Label.place(x = 350, y = 250, anchor = "center")
            
        else:
            print("not a perfect match :(")
            self._notmatches.append(test_couple)
            Not_Match_Label = tk.Label(self.truthbooth, text = "It wasn't meant to be :(", fg = "white",
                                            bg = "#0C1793", font = ("Cooper Black", 30))
            Not_Match_Label.place(x = 350, y = 250, anchor = "center")


if __name__ == "__main__":
    game = GamePlay()
    
