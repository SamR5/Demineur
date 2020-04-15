#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.messagebox
import random
import itertools as it
import time as t

nearbyCells = tuple((i, j) for i in range(-1, 2) for j in range(-1, 2)
                           if (i, j) != (0, 0))


class MineField():
    """Class representing the mine field"""
    def __init__(self, master, size=10, minesRatio=0.25):
        self.size = size
        self.minesRatio = minesRatio
        self.mines = int(self.minesRatio * self.size ** 2)
        # coordinates from (0, 0) to (size-1, size-1)
        self.fieldCoord = [(i, j) for i, j in it.product(range(self.size),
                                                         range(self.size))]
        # history of dug and flagged cells
        self.dug = set()
        self.flagged = set()
        self.create_field()
        self.count_mines()
        self.master = master
        self.GUI()
        
        self._start = -1.0 # because buttons take time to create
        self._running = 0
        self.timer()
        self.start()
    
    def create_field(self):
        """Create the mine field"""
        self.field = {(i, j):' ' for i, j in self.fieldCoord}
        # place mines
        mines2 = self.mines
        coord = self.fieldCoord[:] #[(i, j) for i in range(self.size) for j in range(self.size)]
        while mines2 != 0:
            row, col = random.choice(coord)
            self.field[(row, col)] = 9 # 9 = mine
            coord.remove((row, col))
            mines2 -= 1
    
    def count_mines(self):
        """Get the number of mines around each cells"""
        for row, col in self.fieldCoord:
            # don't count mines around mines
            if self.field[(row, col)] == 9:
                continue
            count = 0
            for i, j in nearbyCells:
                try:
                    if self.field[(row+i, col+j)] == 9: # if mine
                        count += 1
                except KeyError:
                    pass
            self.field[(row, col)] = count
    
    def start(self):
        """Start the stopwatch, ignore if running."""
        if not self._running:
            self._start = t.time()
            self._running = 1
            self._update()
    
    def _update(self): 
        """Update the label with elapsed time."""
        if self._running:
            self._elapsedtime.set(str(int(t.time() - self._start)))
            self._timer = self.master.after(100, self._update)
    
    def timer(self):
        """"""
        self._elapsedtime = tk.StringVar()
        self._elapsedtime.set(0.0)
        self.chrono = tk.Label(self.statusBar, textvariable=self._elapsedtime)
        self.chrono.pack(side='left')
    
    def GUI(self):
        """"""
        # main frame of the mine field
        self.buttons = {}
        self.labels = {}
        self.mainFrame = tk.Frame(self.master)
        self.mainFrame.pack()
        for r, c in self.fieldCoord:
            lab = tk.Label(self.mainFrame, text=str(self.field[(r, c)]),
                           bg='goldenrod', width=2, bd=7)
            lab.grid(row=r, column=c)
            self.labels[(r, c)] = lab
            
            button = tk.Button(self.mainFrame, bg='green', relief='ridge',
                               command=lambda x=(r, c): self.dig(*x))
            button.bind('<Button-3>', lambda event, x=(r, c): self.flag(*x))
            button.grid(row=r, column=c)
            self.buttons[(r, c)] = button
        
        # informations about the current game
        self.statusBar = tk.Frame(self.master)
        self.statusBar.pack(fill='x', side='bottom')
        sizetext = " "*3 + "size: {0}x{0} ".format(self.size)
        minetext = " "*3 + "{} mines ".format(self.mines)
        try:
            lvl = self.lvlVar.get()
            lvltxt = ("easy" if lvl==1 else "intermediate" if lvl==2 else "hard")
        except AttributeError:
            lvltxt = "intermediate"
        self.s = tk.Label(self.statusBar, text=sizetext)#, relief='sunken')
        self.m = tk.Label(self.statusBar, text=minetext)#, relief='sunken')
        self.lvl = tk.Label(self.statusBar, text="difficulty: " + lvltxt)
        
        self.m.pack(side='right')
        self.s.pack(side='right')
        self.lvl.pack(side='right')
        
        # menu
        self.menubar = tk.Menu(self.master)
        self.menubar.add_command(label="Options", command=self.settings)
        self.menubar.add_command(label="Restart", command=self.restart)
        self.master.config(menu=self.menubar)
    
    def settings(self):
        """New window with the settings"""
        self.window = tk.Toplevel()
        self.window.title("Settings")
        self.window.grab_set()
        f = "Comicsans 10 bold"
        # size of the field
        self.sizeVar = tk.IntVar()
        self.smallR = tk.Radiobutton(self.window, text="Small\n\n7x7",
                                     variable=self.sizeVar, value=1, font=f,
                                     indicatoron=False, width=14, height=5)
        self.medR = tk.Radiobutton(self.window, text="Medium\n\n13x13",
                                   variable=self.sizeVar, value=2, font=f,
                                   indicatoron=False, width=14, height=5)
        self.bigR = tk.Radiobutton(self.window, text="Big\n\n22x22",
                                   variable=self.sizeVar, value=3, font=f,
                                   indicatoron=False, width=14, height=5)
        # difficulty
        self.lvlVar = tk.IntVar()
        self.easyR = tk.Radiobutton(self.window, text="Easy\n\n13% mines",
                                    variable=self.lvlVar, value=1, font=f,
                                    indicatoron=False, width=14, height=5)
        self.interR = tk.Radiobutton(self.window, text="Intermediate\n\n19% mines",
                                     variable=self.lvlVar, value=2, font=f,
                                     indicatoron=False, width=14, height=5)
        self.hardR = tk.Radiobutton(self.window, text="Hard\n\n29% mines",
                                    variable=self.lvlVar, value=3, font=f,
                                    indicatoron=False, width=14, height=5)
        # buttons
        self.valid = tk.Button(self.window, text="Accept", font=f, width=11,
                               command=self.change_settings)
        self.cancel = tk.Button(self.window, text="Cancel", font=f, width=11,
                                command=self.window.destroy)
        self.smallR.grid(row=0, column=0)
        self.medR.grid(row=1, column=0)
        self.bigR.grid(row=2, column=0)
        self.easyR.grid(row=0, column=1)
        self.interR.grid(row=1, column=1)
        self.hardR.grid(row=2, column=1)
        self.cancel.grid(row=3, column=0)
        self.valid.grid(row=3, column=1)
    
    def dig(self, r, c, flagbypass=False):
        """Dig the mine field at (i, j)"""
        # out of field when 0 near border
        if r not in range(self.size) or c not in range(self.size):
            return
        # dig on a flag
        if (r, c) in self.flagged and not flagbypass:
            return self.flag(r, c)
        # already dug
        elif (r, c) in self.dug:
            return
        
        self.dug.add((r, c))
        # dig on a mine
        if self.field[(r, c)] == 9:
            return self.loose(r, c)
        # dig on an isolated cell
        elif self.field[(r, c)] == 0:
            self.buttons[(r, c)].destroy()
            for i, j in nearbyCells:
                self.dig(r+i, c+j, flagbypass=True)
        # dig on any other cell
        elif self.field[(r, c)] in range(1, 9):
            self.buttons[(r, c)].destroy()
        else:
            print('error', r, c)
            return self.display()
        #
        if len(self.dug) == self.size**2 - self.mines:
            return self.win()
    
    def flag(self, i, j):
        """Add/Remove a flag on the cell (i, j)"""
        if (i, j) in self.flagged:
            self.flagged.remove((i, j))
            self.buttons[(i, j)]['bg'] = 'green'
        else:
            self.flagged.add((i, j))
            self.buttons[(i, j)]['bg'] = 'blue'
    
    def display(self):
        """Display the grid in the terminal"""
        for i, j in self.fieldCoord:
            print(self.field[(i, j)], end=' ')
            if j == self.size - 1:
                print()
    
    def win(self):
        """On win, ask user if he wants to retry"""
        self._running = 0
        ans = tk.messagebox.askyesno(title="Won", message="Well played\n" +\
                                     "Do you want to retry ?")
        if ans == True:
            return self.restart()
        else:
            return self.master.destroy()
    
    def loose(self, r, c):
        """"""
        self.buttons[(r, c)].destroy()
        self.labels[(r, c)]['bg'] = 'red'
        self.labels[(r, c)]['text'] = 'X'
        self.dug.remove((r, c))
        for r, c in self.fieldCoord:
            if (r, c) in self.flagged:
                if self.field[(r, c)] == 9:
                    self.labels[(r, c)]['text'] = 'X'
                self.labels[(r, c)]['bg'] = 'cyan'
            elif (r, c) in self.dug:
                self.labels[(r, c)]['bg'] = 'dark goldenrod'
            elif self.field[(r, c)] == 9:
                self.labels[(r, c)]['text'] = 'X'
            self.buttons[(r, c)].destroy()
        self._running = 0
    
    def restart(self):
        """Reinitialize all"""
        self.mines = int(self.minesRatio * self.size ** 2)
        self.fieldCoord = [(i, j) for i, j in it.product(range(self.size),
                                                         range(self.size))]
        self.dug = set()
        self.flagged = set()
        self.create_field()
        self.count_mines()
        
        self.mainFrame.destroy()
        self.statusBar.destroy()
        self.GUI()
        
        self._start = -1.0
        self._running = 0
        self.timer()
        self.start()
    
    def change_settings(self):
        """Changes the field settings according to the user's choice"""
        sz = self.sizeVar.get()
        lvl = self.lvlVar.get()
        self.size = (7 if sz == 1 else 13 if sz == 2 else 22)
        self.minesRatio = (0.13 if lvl == 1 else 0.19 if lvl == 2 else 0.29)
        self.window.destroy()
        return self.restart()


if __name__ == '__main__':
    root = tk.Tk()
    MF = MineField(master=root, size=13, minesRatio=0.19)
    root.mainloop()
