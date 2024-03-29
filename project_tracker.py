import tkinter
import time
import csv
from collections import defaultdict

# Uses keyboard keys '1' '2' '3' '4' '5' and '6' for selecting projects. 
# Currently window must be in focus when pressing keys.
# Click export button to export to csv (will be named project_time_stamps.csv)
# csv must be closed when you click save

class GUI:
    def __init__(self, master):
        self.num_of_buttons = 6
        self.master = master
        self.projectManager = ProjectManager(self.num_of_buttons) # Create an instance of ProjectManager class 
        self.master.bind("<KeyPress>", self.key_pressed) # Listen for any key press and call key_pressed function
        self.create_project_name_inputs(self.num_of_buttons)
        self.create_export_button()
        self.num_proj_names_in_edit_mode = 0 # Used to allow numbers in project names without counting as a button press

    # Will only get called if frame in focus (not ideal)
    def key_pressed(self, e):
        for i in range(1, self.num_of_buttons + 1):
            if(int(e.char) == i and self.num_proj_names_in_edit_mode == 0): # If 1 or more project names in input mode ignore button press (should add warning to user)
                self.projectManager.key_press(e.char) 

    # Each input is made of a label, an entry input and a button that disables and enables the input
    def create_project_name_inputs(self, num_inputs):
        for i in range(num_inputs):
            tkinter.Label(self.master, 
                text="Button {}'s project name: ".format(i+1)
                ).grid(row = i, column = 0)

            project_name = tkinter.StringVar()
            project_name.set(self.projectManager.get_project_name(i+1))    
            entry = tkinter.Entry(self.master, 
                textvariable = project_name, state='disabled')
            entry.grid(row = i, column = 1)

            btn_text = tkinter.StringVar()
            btn_text.set("Change")
            btn = tkinter.Button(self.master, textvariable = btn_text, 
                command = lambda sel_entry = entry, text = btn_text, 
                entry_text = project_name, index = i+1: 
                self.button_click(sel_entry, text, entry_text, index))
            btn.grid(row = i, column = 2, pady = 5, padx = 5, sticky="ew")

    # Called when the change button is pressed 
    def button_click(self, entry, btn_text, entry_text, index):
        if (btn_text.get() == "Change"): # Enter project name assignment mode for given input
            entry.config(state='normal')
            btn_text.set("Set")
            self.num_proj_names_in_edit_mode += 1  # Increase the number of inputs in edit mode
        else : # Set the newly entered project name to the appropriate button 
            entry.config(state='disabled')
            btn_text.set("Change")
            self.projectManager.set_project_name(index, entry_text.get()) # Set new project name
            self.num_proj_names_in_edit_mode -= 1 # Decrease the number of inputs in edit mode

    def create_export_button(self):
        self.save_button = tkinter.Button(
            self.master, 
            command = self.projectManager.save_task_durations)
        self.save_button.configure(
            text="Export", padx=5
        )
        self.save_button.grid(row = self.num_of_buttons + 1, column = 2)

class ProjectManager:
    def __init__(self, num_of_buttons):
        self.project_time_stamps = defaultdict(list)
        self.project_names = defaultdict(str)
        for i in range(1, num_of_buttons + 1):
            self.project_names[i] = "Project {}".format(i)
        self.selected_proj = ""

    def key_press(self, key):
        proj_id = self.project_names[int(key)]
        if(proj_id != self.selected_proj): # If project currently selected don't both adding another time stamp
            self.selected_proj = proj_id
            self.project_time_stamps[proj_id].append(time.ctime(time.time())) # time.ctime(time.time()) gives local time stamp
    
    def save_task_durations(self):
        with open('project_time_stamps.csv', 'w') as f:
            for key in self.project_time_stamps.keys():
                f.write("{}, ".format(key))
                for duration in self.project_time_stamps[key]:
                    f.write("{},".format(duration))
                f.write('\n')

    def set_project_name(self, index, name):
        self.project_names[index] = name

    def get_project_name(self, index):
        return self.project_names[index]

root = tkinter.Tk()
root.title("Project tracker")
GUI(root)
root.mainloop()