# -*- coding: utf-8 -*-

import tkinter as tk
import os
import time


def run(program, *args):
    pid = os.fork()
    if not pid:
       os.execvp(program, (program,) + args)
    return pid


def park(b, pid):
    b.config(state=tk.DISABLED)
    print("\nParking timdimm telescope....\n")
    os.system("./park")
    b.config(text="Initialize")
    quit.config(state=tk.NORMAL)
    main.config(state=tk.DISABLED)
    b.config(state=tk.NORMAL)
    b.config(command=lambda c=b: init(c))


def init(b):
    print("\nInitializing mount....\n")
    pid = run("./init")
    quit.config(state=tk.DISABLED)
    time.sleep(60)
    main.config(state=tk.NORMAL)
    b.config(text="Park")
    b.config(command=lambda but=b, p=pid: park(but, p))
    print("READY  TO  START  SEEING  MEASUREMENTS\n")
    time.sleep(5)


def kill_kstars(b, pid):
    print("\nKilling KStars process #%d\n" % pid)
    os.system("kill -9 %d" % pid)
    time.sleep(10)
    os.system("killall kstars")
    b.config(relief=tk.RAISED)
    b.config(text="KStars")
    b.config(command=lambda c=b: kstars(c))


def kstars(b):
    pid = run("kstars")
    b.config(relief=tk.SUNKEN)
    b.config(text="Kill KStars")
    b.config(command=lambda but=b, p=pid: kill_kstars(but, p))


def killmeasure_seeing(b, pid):
    print("\nKilling main timDIMM process #%d\n" % pid)
    b.config(text="Stopping...")
    b.config(state=tk.DISABLED)
    os.system("touch STOP_SPIRAL")
    os.system("kill -9 %d" % pid)
    if os.path.isfile("current_object"):
        os.remove("current_object")
    time.sleep(5)
    os.system("./park")
    b.config(text="Measure Seeing")
    initpark.config(state=tk.NORMAL)
    b.config(state=tk.NORMAL)
    b.config(command=lambda c=b: measure_seeing(c))
    print('READY TO START MEASURING SEEING')


def measure_seeing(b):
    if os.path.isfile("STOP_SPIRAL"):
        os.remove("STOP_SPIRAL")
    os.system("./pygto900.py park_off")
    pid = run("./run_measure_seeing.py")
    b.config(text="Stop Measuring Seeing")
    initpark.config(state=tk.DISABLED)
    b.config(command=lambda but=b,p=pid: killmeasure_seeing(but, p))


def open_oxwagon(b):
    print('Opening Ox Wagon')
    os.system("oxwagon OPEN 3600")
    #os.system("./pygto900.py park") ### ADDITION OF PARK COMMAND ###

    #for i in range(6):
    #   print 'WAIT until both sliding and dropping roofs are FULLY OPENED before sending ANY new commands
    #   to the ox-wagon and/or telecope\n'
    #   time.sleep(60)
    #print 'Ox-wagon Fully Opened'
    #os.system("./ox_wagon.py RESET")
    #time.sleep(5)
    #os.system("./ox_wagon.py STATUS")
    #print "MAKE SURE that 'Telescope Powered On' in the above status is 'True'\n"
    #print "... if not open an other terminal and run the following commands:\n"
    #print "cd ~/timDIMM\n"
    #print "./ox_wagon.py reset\n"
    #print "./ox_wagon.py status\n"


def close_oxwagon(b):
    print('Closing Ox Wagon')
    os.system("oxwagon CLOSE")
    #time.sleep(10)
    #for i in range(8):
    #   print 'WAIT until both sliding and dropping roofs are FULLY CLOSED before sending ANY new commands to
    #   the ox-wagon and/or telecope\n'
    #   time.sleep(60)
    #print 'Ox-wagon Fully Closed'
    #os.system("./ox_wagon.py RESET")
    #time.sleep(2)
    #os.system("./ox_wagon.py STATUS")
    #print "MAKE SURE that 'Telescope Powered On' in the above status is 'False'\n"
    #print "... if not open an other terminal and run the following commands:\n"
    #print "cd ~/timDIMM\n"
    #print "./ox_wagon.py reset\n"
    #print "./ox_wagon.py status\n"


def synchronize(b):
    print('Synchronizing the software. PLEASE WAIT!')
    os.system("./pygto900.py sync")
    os.system("./pygto900.py status > sync.log")
    print('Now you can click Measure Seeing')


root = tk.Tk()
root.title("timDIMM")
root.geometry("200x300-0-0")

frame = tk.Frame(root)
frame.pack()

kstars_button = tk.Button(frame, text="KStars")
kstars_button.pack(padx=10, pady=5, fill=tk.X)
kstars_button.config(command=lambda b=kstars_button: kstars(b))

initpark = tk.Button(frame, text="Initialize")
initpark.pack(padx=10, pady=5, fill=tk.X)
initpark.config(command=lambda b=initpark: init(b))

main = tk.Button(frame, text="Measure Seeing", width=180)
main.pack(padx=10, pady=5, expand=True, fill=tk.X)
main.config(command=lambda b=main: measure_seeing(b))

wagon = tk.Button(frame, text="Open Ox Wagon", width=180)
wagon.pack(padx=10, pady=5, expand=True, fill=tk.X)
wagon.config(command=lambda b=wagon: open_oxwagon(b))

wagon = tk.Button(frame, text="Close Ox Wagon", width=180)
wagon.pack(padx=10, pady=5, expand=True, fill=tk.X)
wagon.config(command=lambda b=wagon: close_oxwagon(b))

wagon = tk.Button(frame, text="Synchronize", width=180)
wagon.pack(padx=10, pady=5, expand=True, fill=tk.X)
wagon.config(command=lambda b=wagon: synchronize(b))

quit = tk.Button(frame, text="QUIT", fg="red", command=frame.quit)
quit.pack(pady=20, padx=10, fill=tk.BOTH)


def main():
    root.mainloop()
