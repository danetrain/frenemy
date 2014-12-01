#!/usr/bin/python

import re
import Tkinter as tk
import os

root = tk.Tk()

root.title("Welcome to MiTM")

scrapperUrlLabel = tk.Label(root, text="Enter Scrapper URL")
scrapperOutLabel = tk.Label(root, text="Enter Scrapper Output File Name")
spoofTargetLabel = tk.Label(root, text="Enter ArpSpoof Target's MAC Address")
spoofInterfaceLabel = tk.Label(root, text="Enter ArpSpoof Interface")
spoofSleepLabel = tk.Label(root, text="Enter ArpSpoof Sleep Time Between two packets")
spoofHostLabel = tk.Label(root, text="Enter ArpSpoof Host to take over")

scrapperUrlLabel.grid(column=0, row=0, sticky=tk.W, ipadx=2, ipady=2, padx=2, pady=2)
scrapperOutLabel.grid(column=0, row=2, sticky=tk.W, ipadx=2, ipady=2, padx=2, pady=2)
spoofTargetLabel.grid(column=0, row=4, sticky=tk.W, ipadx=2, ipady=2, padx=2, pady=2)
spoofInterfaceLabel.grid(column=0, row=6, sticky=tk.W, ipadx=2, ipady=2, padx=2, pady=2)
spoofSleepLabel.grid(column=0, row=8, sticky=tk.W, ipadx=2, ipady=2, padx=2, pady=2)
spoofHostLabel.grid(column=0, row=10, sticky=tk.W, ipadx=2, ipady=2, padx=2, pady=2)

scrapperUrlVar = tk.StringVar()

scrapperOutVar = tk.StringVar()
spoofTargetVar = tk.StringVar()
spoofInterfaceVar = tk.StringVar()
spoofSleepVar = tk.StringVar()
spoofHostVar = tk.StringVar()

scrapperUrlVar.set("http://facebook.com/login")
scrapperOutVar.set("facebook")
spoofTargetVar.set("00:00:00:00:00:00")
spoofInterfaceVar.set("")
spoofSleepVar.set("1")
spoofHostVar.set("192.168.1.0")

scrapperUrlEntry = tk.Entry(root, textvariable=scrapperUrlVar)
scrapperOutEntry = tk.Entry(root, textvariable=scrapperOutVar)
spoofTargetEntry = tk.Entry(root, textvariable=spoofTargetVar)
spoofInterfaceEntry = tk.Entry(root, textvariable=spoofInterfaceVar)
spoofSleepEntry = tk.Entry(root, textvariable=spoofSleepVar)
spoofHostEntry = tk.Entry(root, textvariable=spoofHostVar)

scrapperUrlEntry.grid(column=1, row=0, sticky=tk.E, ipadx=2, ipady=2, padx=2, pady=2)
scrapperOutEntry.grid(column=1, row=2, sticky=tk.E, ipadx=2, ipady=2, padx=2, pady=2)
spoofTargetEntry.grid(column=1, row=4, sticky=tk.E, ipadx=2, ipady=2, padx=2, pady=2)
spoofInterfaceEntry.grid(column=1, row=6, sticky=tk.E, ipadx=2, ipady=2, padx=2, pady=2)
spoofSleepEntry.grid(column=1, row=8, sticky=tk.E, ipadx=2, ipady=2, padx=2, pady=2)
spoofHostEntry.grid(column=1, row=10, sticky=tk.E, ipadx=2, ipady=2, padx=2, pady=2)

tk.Label(root, text="").grid(column=0, row=12, columnspan=2, ipadx=2, ipady=2, padx=2, pady=2)


def main():
    runButton = tk.Button(root, text="Run", command=validate_inputs)
    runButton.grid(column=0, row=14, columnspan=2, sticky=tk.N + tk.E + tk.W + tk.S, ipadx=2, ipady=2, padx=2, pady=2)

    root.mainloop()


errorLabel1 = tk.Label(root, text="Input Error")
errorLabel2 = tk.Label(root, text="Input Error")
errorLabel3 = tk.Label(root, text="Input Error")
errorLabel4 = tk.Label(root, text="Input Error")
errorLabel5 = tk.Label(root, text="Input Error")
errorLabel6 = tk.Label(root, text="Input Error")


def validate_inputs():
    regexURL = r'^(https?):\/\/(([a-z0-9$_\.\+!\*\'\(\),;\?&=-]|%[0-9a-f]{2})+(:([a-z0-9$_\.\+!\*\'\(\),;\?&=-]|%[0-9a-f]{2})+)?@)?(?#)((([a-z0-9]\.|[a-z0-9][a-z0-9-]*[a-z0-9]\.)*[a-z][a-z0-9-]*[a-z0-9]|((\d|[1-9]\d|1\d{2}|2[0-4][0-9]|25[0-5])\.){3}(\d|[1-9]\d|1\d{2}|2[0-4][0-9]|25[0-5]))(:\d+)?)(((\/+([a-z0-9$_\.\+!\*\'\(\),;:@&=-]|%[0-9a-f]{2})*)*(\?([a-z0-9$_\.\+!\*\'\(\),;:@&=-]|%[0-9a-f]{2})*)?)?)?(#([a-z0-9$_\.\+!\*\'\(\),;:@&=-]|%[0-9a-f]{2})*)?$'
    regexOUT = r'^[\w,\s-]+(\.[A-Za-z]{1,6})?$'
    regexMAC = r'^([0-9A-F]{2}[:-]){5}([0-9A-F]{2})$'
    regexINT = r'^$'
    regexSLP = r'^\d+$'
    regexHST = r'^(?=.{1,255}$)[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?(?:\.[0-9A-Za-z](?:(?:[0-9A-Za-z]|-){0,61}[0-9A-Za-z])?)*\.?$'

    matchScrapperUrl = re.match(regexURL, scrapperUrlEntry.get().strip(), re.M | re.I | re.U)
    matchScrapperOut = re.match(regexOUT, scrapperOutEntry.get().strip(), re.M | re.I)
    matchSpoofTarget = re.match(regexMAC, spoofTargetEntry.get().strip(), re.M | re.I)
    matchSpoofInterface = re.match(regexINT, spoofInterfaceEntry.get().strip(), re.M | re.I)
    matchSpoofSleep = re.match(regexSLP, spoofSleepEntry.get().strip(), re.M | re.I)
    matchSpoofHost = re.match(regexHST, spoofHostEntry.get().strip(), re.M | re.I)

    if matchScrapperUrl:
        errorLabel1.grid_remove()
    else:
        errorLabel1.grid(column=0, row=1, columnspan=2, ipadx=2, ipady=2, padx=2, pady=2)
    if matchScrapperOut:
        errorLabel2.grid_remove()
    else:
        errorLabel2.grid(column=0, row=3, columnspan=2, ipadx=2, ipady=2, padx=2, pady=2)
    if matchSpoofTarget:
        errorLabel3.grid_remove()
    else:
        errorLabel3.grid(column=0, row=5, columnspan=2, ipadx=2, ipady=2, padx=2, pady=2)
    if matchSpoofInterface:
        errorLabel4.grid_remove()
    else:
        errorLabel4.grid(column=0, row=7, columnspan=2, ipadx=2, ipady=2, padx=2, pady=2)
    if matchSpoofSleep:
        errorLabel5.grid_remove()
    else:
        errorLabel5.grid(column=0, row=9, columnspan=2, ipadx=2, ipady=2, padx=2, pady=2)
    if matchSpoofHost:
        errorLabel6.grid_remove()
    else:
        errorLabel6.grid(column=0, row=11, columnspan=2, ipadx=2, ipady=2, padx=2, pady=2)

    root.update_idletasks()

    if matchScrapperUrl and matchScrapperOut and matchSpoofTarget \
            and matchSpoofInterface and matchSpoofSleep and matchSpoofHost:
        accept_inputs()
    else:
        deny_inputs()


def deny_inputs():
    print "Bad Inputs. Please Fix."


def accept_inputs():
    scrapperUrl = scrapperUrlEntry.get().strip()
    scrapperOut = scrapperOutEntry.get().strip()
    spoofTarget = spoofTargetEntry.get().strip()
    spoofInterface = spoofInterfaceEntry.get().strip()
    spoofSleep = spoofSleepEntry.get().strip()
    spoofHost = spoofHostEntry.get().strip()

    os.system("./htmlscraper.py " + scrapperUrl + " " + scrapperOut)


if __name__ == '__main__':
    main()
