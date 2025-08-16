import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
import sqlite3
import json

import globalConfig as cg

colourDropdownOptions = ["Select Colour", "Red", "Blue", "Green", "Yellow", "Purple"]
colourDropdownOptionsRGBs = [None, (255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0), (138, 43, 226)]

class SimInfoInputHandler:
    #SCREENS
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Physics Ball Simulator")
        self.root.geometry("300x110")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        #EDIT SETTINGS BUTTON
        cogIcon = Image.open("Images/cogIcon.png")
        cogIcon = cogIcon.resize((20, 20))
        cogIcon = ImageTk.PhotoImage(cogIcon)
        openSettingsButton = tk.Button(self.root, text="Edit Sim Settings", image=cogIcon, compound="top", command=self.editSettingsScreen)
        openSettingsButton.grid(row=1, column=0, pady=(10, 5))

        #RUN SIM BUTTON
        runSimButton = tk.Button(self.root, text="Run Sim", command=self.runSim)
        runSimButton.grid(row=12, column=0, pady=10, padx=10)

        self.root.mainloop()
            
    def editSettingsScreen(self):
        self.settingsRoot = tk.Tk()
        self.settingsRoot.title("Physics Ball Simulator")
        self.settingsRoot.geometry("300x550")
        
        #BALLS
        tk.Label(self.settingsRoot, text="Ball Settings").grid(row=0, column=0)
    
        ballNumLabel = tk.Label(self.settingsRoot, text="Number of balls: ")
        ballNumLabel.grid(row=1, column=0, pady=(20, 5))

        self.ballNumEntry = tk.Entry(self.settingsRoot)
        self.ballNumEntry.grid(row=2, column=0, pady=(5, 20), padx=10)
        
        ballRadiusLabel = tk.Label(self.settingsRoot, text="Ball Radius: ")
        ballRadiusLabel.grid(row=3, column=0, pady=(20, 5))

        self.ballRadiusEntry = tk.Entry(self.settingsRoot)
        self.ballRadiusEntry.grid(row=4, column=0, pady=(5, 20), padx=10)

        self.useRandomBallColours = tk.IntVar()
        self.useRandomBallColours.set(1)

        useRandomBallColoursCheckbox = tk.Checkbutton(self.settingsRoot, text="Use random ball colours for clarity", variable=self.useRandomBallColours, command=self.toggleDropdown)
        useRandomBallColoursCheckbox.grid(row=5, column=0)

        self.selectedColour = tk.StringVar()
        self.selectedColour.set(colourDropdownOptions[0])

        self.selectColourDropdown = tk.OptionMenu(self.settingsRoot, self.selectedColour, *colourDropdownOptions)
        self.selectColourDropdown.grid(row=6, column=0)
        self.selectColourDropdown.grid_remove()

        #SIM
        gravityLabel = tk.Label(self.settingsRoot, text="Gravity: ")
        gravityLabel.grid(row=7, column=0, pady=(20, 5))

        self.gravityEntry = tk.Entry(self.settingsRoot)
        self.gravityEntry.grid(row=8, column=0, pady=(5, 20), padx=10)
        
        frictionLabel = tk.Label(self.settingsRoot, text="Friction: ")
        frictionLabel.grid(row=9, column=0, pady=(20, 5))

        self.frictionEntry = tk.Entry(self.settingsRoot)
        self.frictionEntry.grid(row=10, column=0, pady=(5, 20), padx=10)
        
        targetFpsLabel = tk.Label(self.settingsRoot, text="Target FPS: ")
        targetFpsLabel.grid(row=11, column=0, pady=(20, 5))

        self.targetFpsEntry = tk.Entry(self.settingsRoot)
        self.targetFpsEntry.grid(row=12, column=0, pady=(5, 20), padx=10)
        
        #SAVE
        saveSettingsButton = tk.Button(self.settingsRoot, text="Save", command=self.saveSettings)
        saveSettingsButton.grid(row=13, column=0, pady=10, padx=10)

        self.settingsRoot.mainloop()
        
    #ACTIONS
    def saveSettings(self):
        settings = {}
        
        try:
            ballNum = int(self.ballNumEntry.get())
            ballRadius = float(self.ballRadiusEntry.get())
            ballColour = colourDropdownOptionsRGBs[colourDropdownOptions.index(self.selectedColour.get())]
            
            gravity = float(self.gravityEntry.get())
            friction = float(self.frictionEntry.get())
            targetFPS = int(self.targetFpsEntry.get())
            
            if not (0 <= friction <= 1):
                messagebox.showerror("Error", "Friction must be 0-1.")
                return

            if ballNum <= 0 or ballRadius <= 0 or targetFPS <= 0:
                messagebox.showerror("Error", "Make sure all numbers are positive and non-zero.")
                return
            
            if targetFPS < 60:
                answer = messagebox.askyesno("Low FPS", f"You have set the target FPS to {targetFPS}. FPS below 60 could cause collisions to be incorrectly handled. We recommend going no lower.\nDo you still want to continue?")

                if not answer:
                    return
            
            if self.useRandomBallColours.get() == 0 and ballColour:
                settings["ballNum"] = ballNum
                settings["ballRadius"] = ballRadius
                settings["targetFPS"] = targetFPS
                settings["ballColour"] = ballColour
                settings["gravity"] = gravity
                settings["friction"] = 1-friction
                settings["randomBallColours"] = False
                
                conn = sqlite3.connect("Database/settingsDb.db")
                cursor = conn.cursor()
                
                cursor.execute("CREATE TABLE IF NOT EXISTS Settings (settingsDict)")
                conn.commit()
                
                cursor.execute("DELETE FROM Settings")
                conn.commit()
                
                cursor.execute("INSERT INTO Settings (settingsDict) VALUES (?)", (json.dumps(settings),))
                conn.commit()
                
                conn.close()
                
                self.settingsRoot.destroy()
                
            elif self.useRandomBallColours.get() == 1:
                settings["ballNum"] = ballNum
                settings["ballRadius"] = ballRadius
                settings["targetFPS"] = targetFPS
                settings["ballColour"] = None
                settings["gravity"] = gravity
                settings["friction"] = 1-friction
                settings["randomBallColours"] = True
                
                conn = sqlite3.connect("Database/settingsDb.db")
                cursor = conn.cursor()
                
                cursor.execute("CREATE TABLE IF NOT EXISTS Settings (settingsDict)")
                conn.commit()
                
                cursor.execute("DELETE FROM Settings")
                conn.commit()
                
                cursor.execute("INSERT INTO Settings (settingsDict) VALUES (?)", (json.dumps(settings),))
                conn.commit()
                
                conn.close()
                
                self.settingsRoot.destroy()
            
            elif not ballColour:
                messagebox.showerror("Error", "Please choose a colour or select 'Use random ball colours for clarity'.")
                
        except ValueError:
            messagebox.showerror("Error", "Please make sure entries are valid numbers.")
        
    def toggleDropdown(self):
        if self.useRandomBallColours.get() == 1:
            self.selectColourDropdown.grid_remove()
        else:
            self.selectColourDropdown.grid()

    def runSim(self):
        conn = sqlite3.connect("Database/settingsDb.db")
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT settingsDict FROM Settings")
            settings = cursor.fetchone()
        except sqlite3.OperationalError:
            settings = None
        
        if settings:
            settings = json.loads(settings[0])
            
            cg.ballNum = settings["ballNum"]
            cg.ballRadius = settings["ballRadius"]
            cg.targetFPS = settings["targetFPS"]
            if settings["ballColour"]:
                cg.ballColour = settings["ballColour"]
            cg.gravity = settings["gravity"]
            cg.friction = settings["friction"]
            cg.randomBallColours = settings["randomBallColours"]
        else:
            messagebox.showerror("Select Sim Settings", "Please select sim settings before running.")
            
            conn.close()
            return
        
        conn.close()
        
        self.root.destroy()