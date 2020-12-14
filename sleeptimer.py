import tkinter as tk
from threading import Timer
from os import system

class Sleeptimer():

    def __init__(self):
        self.BTN_DICT = {
                1: ('0.1', '30', '45'),
                2: ('60', '90', '120'),
            }
        self.ROOT = tk.Tk()
        self.BTN_TABLE = None
        self.TIMER_TO_ASK = None
        self.TIMER_TO_SHUT = None

    def main(self):
        '''Creates all GUI discribes actions on X button.
        '''
        
        vw = self.ROOT.winfo_screenwidth()
        vh = self.ROOT.winfo_screenheight()

        self.ROOT.geometry(
            f'160x150-{int(vw/2)}+{int(vh/2)}')
        asking_label = tk.Label(self.ROOT,
                                text='Enter time to sleep in minutes:',
                                bg='dark grey',
                                fg='white')

        asking_label.grid(row=0, column=0,
                        columnspan=len(self.BTN_DICT[1]))

        self.ROOT.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.create_table()

        self.ROOT.mainloop()

    def shutdown(self):
        """Shutting down your PC in hibernate mode (/h).
        """

        system(
            # "shutdown /h" #hibernate
            "rundll32.exe powrprof.dll,SetSuspendState 0,1,0" #sleep
            )

    def cancel(self):
        """Restarts program if user rejected shutting down for to ask again.
        """
        self.TIMER_TO_SHUT.cancel()
        self.ROOT.destroy()
        self.main()


    def ask_to_shut(self):
        """Asks user if he wants to cancel shutting down.
        """
        time = 4

        cancel_button = tk.Button(self.ROOT,
                                text=f'Выключение менее,\nчем через {str(time)} сек',
                                bg='red',
                                wraplength=-1,
                                width=6,
                                command=self.cancel)

        cancel_button.grid(rowspan=2,
                        columnspan=3,
                        sticky=tk.N+tk.S+tk.E+tk.W,)

        
        self.TIMER_TO_SHUT = Timer(time, self.shutdown)
        self.TIMER_TO_SHUT.start()
        self.ROOT.call('wm', 'attributes', '.', '-topmost', '1')


    def cancel_timer(self):
        """Stops timer on cancel button.
        """
        for k in self.BTN_TABLE:
            for v in self.BTN_TABLE[k]:
                v.config(state='normal')
        self.TIMER_TO_ASK.cancel()


    def start(self,time):
        """Starting timer when time button pressed.
        """
        self.TIMER_TO_ASK = Timer(float(time)*60, self.ask_to_shut)
        self.TIMER_TO_ASK.start()
        cancel_button = tk.Button(self.ROOT,
                                text='Cancel',
                                command=self.cancel_timer)

        cancel_button.grid(
            row=5, column=0,
            columnspan=len(self.BTN_DICT[1]),
            sticky=tk.N+tk.S+tk.E+tk.W,)

        for k in self.BTN_TABLE:
            for v in self.BTN_TABLE[k]:
                v.config(state='disabled')


    def on_closing(self):
        """Actions on closing program by press X button.
        """
        try:
            self.TIMER_TO_ASK.cancel()
            self.TIMER_TO_SHUT.cancel()
        except:
            self.ROOT.destroy()
        self.ROOT.destroy()


    def create_table(self):
        """Creates dictionary of buttons for choosing time.
        """
        self.BTN_TABLE = {
            1: ['0', '0', '0'],
            2: ['0', '0', '0'],
        }

        for k in self.BTN_DICT:
            clmn = 0
            for v in self.BTN_DICT[k]:

                
                self.BTN_TABLE[k][self.BTN_DICT[k].index(v)] = tk.Button(
                    self.ROOT, 
                    width=2, 
                    text=v, 
                    command=lambda v=v: self.start(v))

                self.BTN_TABLE[k][self.BTN_DICT[k].index(v)].grid(
                    sticky=tk.N+tk.S+tk.E+tk.W, 
                    row=k+2, 
                    column=clmn)
                clmn += 1

if __name__ == "__main__":
    timer = Sleeptimer()
    timer.main()
