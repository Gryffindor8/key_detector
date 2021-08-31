# import csv
import threading
import tkinter as tk
from tkinter import *

import pandas as pd
import pynput


def save(ind):
    global total1
    incre = int(value1[ind])
    incre += 1
    value1[ind] = incre
    total1 = int(value1[len(value1) - 1]) + 1
    value1[len(value1) - 1] = total1
    print(total1)
    data1 = [label1, value1]
    pdf1 = pd.DataFrame(data=data1, index=["labels", "values"])
    pdf1 = pdf1.T
    pdf1.to_csv("save.csv", encoding="UTF-8")


def on_press(key):
    try:
        p = str(key).replace("'", "").replace("Key.", "")
        index = label1.index(p)
        value_count = int(value1[int(index)])
        value_count += 1
        threading.Thread(target=save, args=(index,), daemon=True).start()
        update(value_count, index)
        if p == "\\x18":
            return False
    except:
        pass


def on_release(key2):
    if key2 == 'Key.esc':
        pass


def weight_calculate():
    global weight1
    try:
        if entry_box.get() != "":
            id1 = 0
            weight1 = entry_box.get()
            entry_box.clipboard_clear()
            entry_box.delete(0, "end")
            for k5 in value1:
                valuee = ((int(k5) / float(weight1)) * 100)
                weights[id1].config(text=valuee)
                id1 += 1
    except:
        pass


def update(txt, ind):
    global weight1
    if weight1 == 1:
        vl = 0
    else:
        vl = int(txt)
        vl = ((int(vl) / float(weight1)) * 100)
    total = int(value1[len(value1) - 1]) + 1
    switch.config(text=total1)
    press[len(press) - 1].config(text=total1)
    press[ind].config(text=txt)
    weights[ind].config(text=vl)


def up():
    with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def _on_frame_configure(args):
    canvas.configure(scrollregion=canvas.bbox("all"))


def _bound_to_mousewheel(event):
    canvas.bind_all("<MouseWheel>", _on_mousewheel)


def _unbound_to_mousewheel(event):
    canvas.unbind_all("<MouseWheel>")


def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")


if __name__ == '__main__':
    weight1 = 1
    root1 = Tk()
    root1.title("KeepTrak")
    root1.geometry('600x600')
    root1.config(bg="grey")
    root1.resizable(False, False)
    root1.columnconfigure(0, weight=0)
    root1.rowconfigure(0, weight=0)

    frame1 = Frame(root1, bg="grey", padx=25, pady=15)
    frame1.grid(row=0, column=0)

    name = Label(frame1, text='Advance Stats', fg="white", bg="grey", font=("Helvetica", 14))
    name.pack(padx=0, pady=0, side="left")

    switch = Label(frame1, text='', fg="white", bg="grey", font=("Helvetica", 14))
    switch.pack(padx=15, side="left")

    value = StringVar()
    entry_box = Entry(frame1, textvariable=value, width=10, highlightthickness=2, font=("Helvetica", 16))
    entry_box.pack(side="left")

    button = Button(frame1, width=5, fg="black", text="Enter", font=("Helvetica", 13), command=weight_calculate)
    button.pack(padx=5, side="left")
    h_frame = Frame(root1, background="gray")
    h_frame.grid(column=0, row=1, sticky=N + S + E + W)

    b_name = Label(h_frame, text="Button", bg="grey", fg="white", font=('Helvetica', 14))
    b_name.grid(row=1, column=0, padx=30)
    press = Label(h_frame, text="Total Press", bg="grey", fg="white", font=('Helvetica', 14))
    press.grid(row=1, column=1, padx=30)
    wear = Label(h_frame, text="Wear %", bg="grey", fg="white", font=('Helvetica', 14))
    wear.grid(row=1, column=2, padx=30)

    frame = Frame(root1, borderwidth=2, relief=SUNKEN, background="light gray")
    frame.grid(column=0, row=2, sticky=N + S + E + W)

    yscrollbar = Scrollbar(frame)
    yscrollbar.grid(column=1, row=2, sticky=N + S)

    canvas = Canvas(frame, bd=0, height=500, width=573, yscrollcommand=yscrollbar.set)
    canvas.grid(column=0, row=2, sticky=N + S + E + W)
    yscrollbar.config(command=canvas.yview)
    c_frame = Frame(canvas)
    canvas.create_window(10, 10, window=c_frame, anchor='nw')
    c_frame.bind("<Configure>", _on_frame_configure)
    c_frame.bind('<Enter>', _bound_to_mousewheel)
    c_frame.bind('<Leave>', _unbound_to_mousewheel)
    root1.bind_all("<1>", lambda event: event.widget.focus_set())

    try:
        df = pd.read_csv("save.csv")
        label1 = df["labels"]
        value1 = df["values"]
        label1 = label1.values.tolist()
        value1 = value1.values.tolist()
    except:
        key4 = 'space ctrl_l f1 f2 f3 f4 f5 f6 f7 f8 f9 f10 f11 f12 up down right page_up page_down left shift ' \
               'caps_lock tab backspace ' \
               'delete enter alt_l <255> esc \\\\ ctrl_r shift_l ""'
        key5 = 'abcdefghijklmnopqrstuvwxyz1234567890.!@#$%^&*(' \
               ')_+-=`[]{},|/<>~:;"?'
        label1 = []
        value1 = []
        for k2 in key4.split(" "):
            label1.append(k2)
            value1.append(0)
        for k2 in key5:
            label1.append(k2)
            value1.append(0)
        label1.append("Total")
        value1.append(0)
        # i1 = 0
        # for k0 in label1:
        #     i1 += 1
        data = [label1, value1]
        pdf = pd.DataFrame(data=data, index=["labels", "values"])
        pdf = pdf.T
        pdf.to_csv("save.csv", encoding="UTF-8")
    switch.config(text=value1[len(value1) - 1])
    press = []
    wear = []
    weights = []
    i = 0
    for k in value1:
        buttons = tk.Label(c_frame, text=label1[i], font=('Helvetica', 16, 'bold'))
        buttons.grid(column=1, row=i, padx=30)

        total_press = tk.Label(c_frame, text=k, font=('Helvetica', 16, 'bold'))
        total_press.grid(column=2, row=i, padx=30)

        wear = tk.Label(c_frame, text=0, font=('Helvetica', 16, 'bold'))
        wear.grid(column=3, row=i, padx=30)

        press.append(total_press)
        weights.append(wear)
        i += 1
    threading.Thread(target=up, daemon=True).start()
    root1.mainloop()
