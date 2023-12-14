import random as rr

def feed_log(old_response):
    new_response = old_response + "\n" + str(rr.randint(0, 1000))
    return new_response

with open("tt.txt", "wt") as f:
    for i in range(100):
        f.write("TT "+str(rr.randint(0, 1000))+"\n")

    
        