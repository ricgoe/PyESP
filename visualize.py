from textwrap import fill
import tkinter as tk
import math
import pandas as pd
import time
#read csv
#df = pd.read_csv(r'C:\Users\Jannis\Documents\PyESP\PyESP\Filtered_Data\scans_angle_2_8125_pos_6_rot_1_filtered.csv')
df_1 = pd.read_csv(r'Filtered_Data\scans_angle_2_8125_pos_6_rot_1_filtered.csv')
df = df_1[df_1['shape'] == 'pentagon']
#tkinter window
window = tk.Tk()
window.title("my window")
window.geometry('800x600')
#tkinte canvas
canvas = tk.Canvas(window, width=800, height=600, bg="green")
canvas.pack()
circle_size = 20
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
    global times_executed
    canvas.delete("point")
    for i in range(times_executed+1):
        var = times_executed-i
        filling = "red" if i == times_executed else "black"
        x,y = rotate_point(400,df.iloc[row,i*2+1],400,300,var*2.8125*2)
        canvas.create_oval(x,y,x+circle_size,y+circle_size,fill=filling, tags=f"point")
    #     print("circle at:",x,y,x+circle_size,y+circle_size)
    # print(20*"-")
    times_executed += 1
    window.after(140, execute, row)

execute(2)


window.mainloop()