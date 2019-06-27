import tkinter
import time
import csv
import serial   #You need to install pySerial
import queue
import threading

# Uses arduino with 3 buttons for selecting projects. 
# Click save button to save to csv (will be named project_time_stamps.csv)
# csv must be closed when you click save
# Currently hard coded project names

class GUI:
    def __init__(self, master):
        self.master = master
        self.project_manager = ProjectManager() # Create an instance of ProjectManager class 
        self.set_up_serial()
        self.create_save_button()

    # set_up_serial and poll_queue should probably be moved to a seperate class
    def set_up_serial(self):
        self.queue = queue.Queue()
        SerialThread(self.queue).start()
        self.master.after(100, self.poll_queue)

    def poll_queue(self):
        try:
            msg = self.queue.get(0)   
            self.project_manager.key_press(msg[0])
            self.master.after(100, self.poll_queue)
        except queue.Empty:
            self.master.after(100, self.poll_queue)

    def create_save_button(self):
        self.save_button = tkinter.Button(self.master, command= self.project_manager.save_task_durations)
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

class SerialThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue  # Queue is a shared data structure with gui thread used to pass data between two threads
        self.arduino = serial.Serial('COM5', 115200, timeout=.1) # Sets up serial connection with arduino. First argument is dependent on which usb port arduino is using. Second argument must match what is set in arduino code

    def run(self):
        while True:
            data = self.arduino.readline()[:-1] # readline is a blocking call
            if data:
                self.queue.put(data.decode('UTF-8'))

root = tkinter.Tk()
root.title("Test")
main_ui = GUI(root)
root.mainloop()