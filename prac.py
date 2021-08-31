import pandas as pd


def start():
    key4 = 'space ctrl_r f1 f2 f3 f4 f5 f6 f7 f8 f9 f10 f11 f12 up down right left shift caps_lock tab backspace ' \
           'delete'
    key5 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890.!@#$%^&*(' \
           ')_+-='

    labels = []
    values = []
    for k2 in key4.split(" "):
        labels.append(k2)
        values.append(0)
    for k2 in key5:
        labels.append(k2)
        values.append(0)
    labels.append("Total")
    values.append(0)
    print(labels.index("Total"))
    i = 0
    for k in labels:
        print(k, ":", values[i])
        i += 1
    data = [labels, values]
    pdf = pd.DataFrame(data=data, index=["labels", "values"])
    pdf = pdf.T
    pdf.to_csv("save.csv", encoding="UTF-8")


def reader():
    df = pd.read_csv("save.csv")
    print(df["labels"])
    print(df["values"])



reader()
