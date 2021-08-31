import csv
import threading
import pynput
# from pynput.keyboard import Listener


def start():
    global weight
    weight = int(input("Enter the wear:"))
    global key_dic
    found = 1
    try:
        reader = csv.DictReader(open('mycsvfile.csv'))
        key_dic = next(reader)
    except FileNotFoundError:
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
        # print(k )
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
        threading.Thread(target=save).start()
    if p == "\\x18":
        return False


def on_release(key2):
    if key2 == 'Key.esc':
        pass


if __name__ == '__main__':
    start()
    # Collect events until released
    with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
