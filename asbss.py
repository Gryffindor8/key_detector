import threading
import time
import tkinter as tk
from itertools import cycle

root = tk.Tk()
my_list = cycle([".", "..", "...", ""])


def update(txt):
    labl[0].config(text="Loading{}".format(next(my_list)))
    labl[1].config(text="Loading{}".format(next(my_list)))
    labl[2].config(text=txt)
def up():
    for i in range(10):
        update(str(i))
        time.sleep(3)
    # root.after(1000, change_text)


labl = []

for k in range(5):
    l = tk.Label(root, text="ok")
    l.pack()
    labl.append(l)
threading.Thread(target=up).start()
root.mainloop()
