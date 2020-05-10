import tkinter as tk
from threading import Timer
import os


def shutdown():
    """Shutting down your PC in hibernate mode (/h).
    """
    os.system("shutdown /h")


def main():
    '''Creates all GUI discribes actions on X button.
    '''
    global btn_dict, root

    btn_dict = {
        1: ('15', '30', '45'),
        2: ('60', '90', '120'),
    }

    root = tk.Tk()
    root.geometry('160x200-%d+%d' % (
                  root.winfo_screenwidth()/2,
                  root.winfo_screenheight()/2))
    tk.Label(root, text="Enter time to sleep in minutes:", bg='dark grey',
             fg='white').grid(row=0, column=0, columnspan=len(btn_dict[1]))

    root.protocol("WM_DELETE_WINDOW", on_closing)
    create_table()

    root.mainloop()


def cancel():
    """Restarts program if user rejected shutting down for to ask again.
    """
    timer_to_shut.cancel()
    root.destroy()
    main()


def ask_to_shut():
    """Asks user if he wants to cancel shutting down.
    """
    global timer_to_shut

    tk.Button(root, text='Выключение менее,\nчем через 10 сек', bg='red',
              wraplength=-1, width=6,  command=lambda: cancel()
              ).grid(rowspan=2, columnspan=3,
                     sticky=tk.N+tk.S+tk.E+tk.W,)
    timer_to_shut = Timer(10, shutdown)
    timer_to_shut.start()
    root.call('wm', 'attributes', '.', '-topmost', '1')


def cancel_timer():
    """Stops timer on cancel button.
    """
    for k in btn_table:
        for v in btn_table[k]:
            v.config(state='normal')
    timer_to_ask.cancel()


def start(time):
    """Starting timer when time button pressed.
    """
    global timer_to_ask
    timer_to_ask = Timer(float(time)*60, ask_to_shut)
    timer_to_ask.start()
    tk.Button(root, text='Cancel', command=lambda: cancel_timer()).grid(
        row=5, column=0, columnspan=len(btn_dict[1]), sticky=tk.N+tk.S+tk.E+tk.W,)

    for k in btn_table:
        for v in btn_table[k]:
            v.config(state='disabled')


def on_closing():
    """Actions on closing program by press X button.
    """
    try:
        timer_to_ask.cancel()
        timer_to_shut.cancel()
    except:
        root.destroy()
    root.destroy()


def create_table():
    """Creates dictionary of buttons for choosing time.
    """
    global btn_table
    btn_table = {1: ['0', '0', '0'],
                 2: ['0', '0', '0'],
                 }

    for k in btn_dict:
        clmn = 0
        for v in btn_dict[k]:

            btn_table[k][btn_dict[k].index(v)] = tk.Button(
                root, width=2, text=v, command=lambda v=v: start(v))
            btn_table[k][btn_dict[k].index(v)].grid(
                sticky=tk.N+tk.S+tk.E+tk.W, row=k+2, column=clmn)
            clmn += 1


main()