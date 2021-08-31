import csv
import threading
from tkinter import *
from tkinter.ttk import Treeview, Style

import pynput


# from pynput.keyboard import Listener
def destroy():
    global t1
    root.destroy()
    quit()


def advance_stats():
    global table
    global key_dic
    root1 = Tk()
    root1.title("KeebTrak")
    root1.geometry('600x600')
    root.resizable(False, False)
    root1.config(bg="grey")
    frame1 = Frame(root1, bg="grey", padx=25, pady=15)
    frame1.grid(row=0, column=0)
    name = Label(frame1, text='Advance Stats', fg="white", bg="grey", font=("Helvetica", 14))
    name.pack(pady=2, side="left")
    switch = Label(frame1, text='Switch Lifetime', fg="white", bg="grey", font=("Helvetica", 14))
    switch.pack(padx=15, side="left")
    value = StringVar()
    entry_box = Entry(frame1, textvariable=value, width=10, highlightthickness=2, font=("Helvetica", 16))
    entry_box.pack(side="left")
    button = Button(frame1, width=5, fg="black", text="Enter", font=("Helvetica", 13), )
    button.pack(padx=5, side="left")
    frame2 = Frame(root1)
    frame2.grid(row=1, column=0)

    verscrlbar = Scrollbar(frame2, orient="vertical")
    verscrlbar.pack(side='right', fill="y")

    horscrlbar = Scrollbar(frame2, orient="horizontal")
    horscrlbar.pack(side='bottom', fill="x")

    cols = ('Button', 'Total Presses', 'Wear')
    table = Treeview(frame2, columns=cols, show='headings', height="24", style="mystyle.Treeview",
                     selectmode='browse', yscrollcommand=verscrlbar.set, xscrollcommand=horscrlbar.set)
    for col in cols:
        table.heading(col, text=col)

    style = Style()
    style.configure("mystyle.Treeview.Heading", font=('Helvetica', 10, 'bold'))
    table.pack(padx=5, pady=5)

    table.column("#1", minwidth=10, width=190, stretch=NO)
    table.column("#2", minwidth=10, width=190, stretch=NO)
    table.column("#3", minwidth=10, width=190, stretch=NO)
    count = 0
    for k in key_dic:
        table.insert(parent="", index='end', iid=count, values=(k, key_dic[k], 0))
        count += 1
    verscrlbar.configure(command=table.yview)
    horscrlbar.configure(command=table.xview)
    root.protocol('WM_DELETE_WINDOW', destroy)

    root1.mainloop()


def show_advance_stats():
    pass


def start():
    global weight
    global key_dic
    # weight = int(input("Enter the wear:"))
    weight = 2332
    found = 1
    try:
        reader = csv.DictReader(open('mycsvfile.csv'))
        key_dic = next(reader)
    except:
        found = 0
        key_dic = {}

    if found == 0:
        key2 = 'space ctrl_r f1 f2 f3 f4 f5 f6 f7 f8 f9 f10 f11 f12 up down right left shift caps_lock tab backspace ' \
               'delete'
        key3 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890.!@#$%^&*(' \
               ')_+-='
        for k in key2.split(" "):
            key_dic[k] = 0
        for k in key3:
            key_dic[k] = 0
        key_dic['total'] = 0
        save()


def save():
    global key_dic
    total = int(key_dic['total'])
    total = total + 1
    key_dic['total'] = total
    for k in key_dic:
        item = int(key_dic[k])
        item = (item / weight) * 100
        if k != 'total':
            print(k, ":", item)
    try:
        with open('mycsvfile.csv', 'w') as f:
            w = csv.DictWriter(f, key_dic.keys())
            w.writeheader()
            w.writerow(key_dic)
    except:
        pass


def on_press(key):
    global key_dic
    keys = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890.!@#$%^&*(' \
           ')_+-=spacectrl_rf1f2f3f4f5f6f7f8f9f10f11f12updownrightleftshiftcaps_locktabdeletebackspace'
    p = str(key).replace("'", "").replace("Key.", "")
    if p in keys:
        vl = int(key_dic[p])
        vl = vl + 1
        key_dic[p] = vl
        threading.Thread(target=save, daemon=True).start()
    if p == "\\x18":
        return False


def on_release(key2):
    if key2 == 'Key.esc':
        pass
    #     return False


def st():
    start()
    with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == '__main__':
    global t1
    global root
    t1 = threading.Thread(target=st, daemon=True)
    t1.start()
    root = Tk()
    root.title("KeebTrak")
    root.geometry('600x300')
    root.config(bg="grey")
    label = Label(root, text="Keeb Trak", fg="white", bg="grey", height=2,
                  font=("Helvetica", 30))
    label.pack(fill="x")
    label2 = Label(root, text="Total Presses", fg="white", bg="grey", height=1,
                   font=("Helvetica", 16))
    label2.pack(pady=1, fill="x")
    label = Label(root, text="1111111111111", fg="white", bg="grey", height=1,
                  font=("Helvetica", 30))
    label.pack(fill="x", pady=5)
    button = Button(root, width=12, fg="black", text="Advance Stats", font=("Helvetica", 14), command=advance_stats)
    button.pack(pady=10)
    root.protocol('WM_DELETE_WINDOW', destroy)

    root.mainloop()
