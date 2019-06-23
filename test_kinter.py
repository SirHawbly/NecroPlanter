#!/usr/local/bin/python3

# -----------------------------------------------------------------------------

"""
   Copyright (c) 2019 Christopher Bartlett
   [This program is licensed under the "MIT License"]
   Please see the file LICENSE in the source
   distribution of this software for license terms.
"""

# -----------------------------------------------------------------------------

from tkinter.font import Font
import tkinter as tk
from NecroMapObj import Map
from copy import deepcopy

# -----------------------------------------------------------------------------


class Test_Application(tk.Frame):
    
    map = Map(24, 48)
    # font = font.Font(family = "Courier", size = 12, weight = "bold")

    # -------------------------------------------------------------------------


    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
        # self.map.print_groups()

    # -------------------------------------------------------------------------


    def createWidgets(self):
        
        self.submit = tk.Button(self, text="Generate", highlightbackground='#3E4149')

        self.quitButton = tk.Button(self, height=1, activeforeground = '#000', highlightbackground = '#0a0', cursor='tcross', text='Quit', command=self.quit)

        self.text = tk.Label(self, height=1, width=10, foreground = '#aaf', background = '#ee0', text='things here')

        self.input = tk.Text(self, height=1, width=10, foreground = '#f9f', background = '#aa0')

        # m = self.get_map_string()

        self.text2 = tk.Label(self, height=50, width=120, justify=tk.LEFT, font=Font(family = "Courier",size = 12, weight = "bold"), text='', foreground='#aaa', background='#777')

        self.submit.grid()
        self.text.grid()
        self.text2.grid()
        self.input.grid()
        self.quitButton.grid()
    
    # -------------------------------------------------------------------------

# -----------------------------------------------------------------------------


# if this file is run 
if __name__ == '__main__':
    app = Test_Application() 
    app.master.title('Sample application') 
    app.mainloop() 

# -----------------------------------------------------------------------------
