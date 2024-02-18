import tkinter as tk
import math
import pandas as pd
import time
#read csv
df = pd.read_csv(r'C:\Users\Jannis\Documents\PyESP\PyESP\Filtered_Data\scans_angle_2_8125_pos_6_rot_1_filtered.csv')

#tkinter window
window = tk.Tk()
window.title("my window")
window.geometry('800x600')
#tkinte canvas
canvas = tk.Canvas(window, width=800, height=600)
canvas.pack()
circle_size = 10
oval_list = []
times_executed = 0

def rotate_point(x, y, cx, cy, angle):
    # Convert angle to radians
    angle_rad = math.radians(angle)
    
    # Translate point so that the center of rotation is at the origin
    translated_x = x - cx
    translated_y = y - cy
    
    # Perform rotation using rotation matrix
    rotated_x = translated_x * math.cos(angle_rad) - translated_y * math.sin(angle_rad)
    rotated_y = translated_x * math.sin(angle_rad) + translated_y * math.cos(angle_rad)
    
    # Translate the point back
    rotated_x += cx
    rotated_y += cy
    
    return rotated_x, rotated_y

def execute(row):
    global times_executed, oval_list
    # canvas.delete("point")
    # for i in range(times_executed+1):
        # var = times_executed-i
        # skip = 1 #needs<1, 1 for slowest
        # filling = "red" if i == times_executed else "black"
        # x,y = rotate_point(400,df.iloc[row,i*skip+1],400,300,var*360/len(df.iloc[row])*skip)
    y=df.iloc[row,times_executed]
    oval_list.insert(0,canvas.create_oval(400,y,400+circle_size,y+circle_size,fill="red", tags=f"point"))
    #     print("circle at:",x,y,x+circle_size,y+circle_size)
    # print(20*"-")
    times_executed += 1
    window.after(100, execute, row)

def move_ov():
    for idx, ov in enumerate(oval_list):
        old = canvas.coords(ov)
        x,y = rotate_point(old[0],old[1],400,300,0.78)
        canvas.coords(ov,x,y,x+circle_size,y+circle_size)
        if idx == 0: canvas.itemconfig(ov, fill="black")
    window.after(20, move_ov)

window.after(2,execute,266)
window.after(2,move_ov)


window.mainloop()