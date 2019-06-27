import tkinter
import time
import csv

# Uses keyboard keys '1' '2' and '3' for selecting projects. 
# Currently window must be in focus when pressing keys.
# Click save button to save to csv (will be named project_time_stamps.csv)
# csv must be closed when you click save
# Currently hard coded project names

class GUI:
    def __init__(self, master):
        self.master = master
        self.projectManager = ProjectManager() # Create an instance of ProjectManager class 
        self.master.bind("<KeyPress>", self.key_pressed) # Listen for any key press and call key_pressed function
        self.create_save_button()

    # Will only get called in frame in focus (not ideal)
    def key_pressed(self, e):
        if(e.char == '1' or e.char == '2' or e.char == '3'):
            self.projectManager.key_press(e.char) 

    def create_save_button(self):
        self.save_button = tkinter.Button(self.master, command= self.projectManager.save_task_durations)
        self.save_button.configure(
            text="Save", background="Grey", 
            padx=50
        )
        self.save_button.pack(side=tkinter.TOP)

class ProjectManager:
    def __init__(self):
        self.project_time_stamps = {1:[], 2:[], 3:[]}
        self.selected_proj = -1

    def key_press(self, key):
        proj_id = int(key)
        if(proj_id != self.selected_proj): # If project currently selected don't both adding another time stamp
            self.selected_proj = proj_id
            self.project_time_stamps[proj_id].append(time.ctime(time.time())) # time.ctime(time.time()) gives local time stamp
    
    def save_task_durations(self):
        with open('project_time_stamps.csv', 'w') as f:
            for key in self.project_time_stamps.keys():
                f.write('Project {},'.format(key))
                for duration in self.project_time_stamps[key]:
                    f.write("{},".format(duration))
                f.write('\n')

root = tkinter.Tk()
root.title("Test")
main_ui = GUI(root)
root.mainloop()