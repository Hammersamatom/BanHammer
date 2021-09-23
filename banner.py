# BanHammer - Mass banning bot tool for Twitch
# Copyright (C) 2021  Joseph S. Pacheco-Corwin

import re
import socket
import time
import errno
import sys

# --------------------------------------------- Start Settings ----------------------------------------------------
HOST = "irc.twitch.tv"                          # Hostname of the IRC-Server in this case twitch's
PORT = 6667                                     # Default IRC-Port
CHAN = ""                                       # Channelname = #{Nickname}
NICK = ""                                       # Nickname = Twitch username
PASS = ""                                       # www.twitchapps.com/tmi/ will help to retrieve the required authkey
BNLT = ""                                       # List of individuals to ban
RLMT = 0.3025                                   # Ban speed of 0.3025 seconds by default
SPNT = 0                                        # Where to start in the Banlist
EPNT = "MAX"                                    # Where to end in the Banlist
# --------------------------------------------- End Settings -------------------------------------------------------


# --------------------------------------------- Start Global Variables ---------------------------------------------

twitchCon = ""
setEndPointToLength = True

# --------------------------------------------- End Global Variables ----------------------------------------------


# --------------------------------------------- Start Init Function ------------------------------------------------

# Check for the following lines
# "CHANNEL="
# "USER="
# "OAUTH="
# "BANLIST="
# "RATELIMIT="
# "STARTPOINT="
# "ENDPOINT="
def initConfig():
    paramCheckList = ["CHANNEL=", "USER=", "OAUTH=", "BANLIST=", "RATELIMIT=", "STARTPOINT=", "ENDPOINT="]
    parameters = []

    try:
        with open("config.txt", encoding='UTF-8') as config:
            parameters = config.readlines()
    except IOError:
        print("Config file not found. Please make a new valid config.txt")
        input("Press Enter to exit...")
        sys.exit()

    if len(parameters) < 5:
        print("Incomplete config.txt file")
        input("Press Enter to exit...")
        sys.exit()
    for item in parameters:
        if paramCheckList[0] in item: # CHANNEL=
            global CHAN
            CHAN = "#" + item.replace(paramCheckList[0], '')
            CHAN = CHAN.lstrip()
            CHAN = CHAN.rstrip()
        if paramCheckList[1] in item: # USER=
            global NICK
            NICK = item.replace(paramCheckList[1], '')
            NICK = NICK.lstrip()
            NICK = NICK.rstrip()
        if paramCheckList[2] in item: # OAUTH=
            global PASS
            PASS = item.replace(paramCheckList[2], '')
            PASS = PASS.lstrip()
            PASS = PASS.rstrip()
        if paramCheckList[3] in item: # BANLIST=
            global BNLT
            BNLT = item.replace(paramCheckList[3], '')
            BNLT = BNLT.lstrip()
            BNLT = BNLT.rstrip()
        if paramCheckList[4] in item: # RATELIMIT=
            global RLMT
            RLMT_DEFAULT = RLMT
            RLMT = item.replace(paramCheckList[4], '')
            RLMT = RLMT.lstrip()
            RLMT = RLMT.rstrip()
            if RLMT == "":
                RLMT = RLMT_DEFAULT
            else:
                RLMT = float(RLMT)
        if paramCheckList[5] in item: # STARTPOINT=
            global SPNT
            SPNT = item.replace(paramCheckList[5], '')
            SPNT = SPNT.lstrip()
            SPNT = SPNT.rstrip()
            if SPNT == "":
                SPNT = 0
            else:
                SPNT = int(SPNT)
        if paramCheckList[6] in item: # ENDPOINT=
            global EPNT
            global setEndPointToLength
            EPNT = item.replace(paramCheckList[6], '')
            EPNT = EPNT.lstrip()
            EPNT = EPNT.rstrip()
            if EPNT == "MAX" or EPNT == "":
                setEndPointToLength = True
            else:
                setEndPointToLength = False
                EPNT = int(EPNT)

    
# --------------------------------------------- End Init Function --------------------------------------------------


# --------------------------------------------- Start Functions ----------------------------------------------------
def send_pong(msg):
    twitchCon.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))


def send_message(chan, msg):
    try:
        twitchCon.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))
    except socket.error as error:
        if error.errno == errno.EPIPE:
            print("Broken Pipe durring Message Send! Rate limit too high? Exiting to prevent timeout!")
            input("Press Enter to exit...")
            sys.exit()


def send_nick(nick):
    twitchCon.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))


def send_pass(password):
    twitchCon.send(bytes('PASS %s\r\n' % password, 'UTF-8'))


def join_channel(chan):
    twitchCon.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))


def part_channel(chan):
    try:
        twitchCon.send(bytes('PART %s\r\n' % chan, 'UTF-8'))
    except socket.error as error:
        if error.errno == errno.EPIPE:
            print("Broken Pipe during Channel Leave! Restart the program!")
            input("Press Enter to exit...")
            sys.exit()
# --------------------------------------------- End Functions ------------------------------------------------------


# --------------------------------------------- Start Helper Functions ---------------------------------------------
def get_sender(msg):
    result = ""
    for char in msg:
        if char == "!":
            break
        if char != ":":
            result += char
    return result


def get_message(msg):
    result = ""
    i = 3
    length = len(msg)
    while i < length:
        result += msg[i] + " "
        i += 1
    result = result.lstrip(':')
    return result


def connect():
    global twitchCon
    twitchCon = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    twitchCon.connect((HOST, PORT))
    send_pass(PASS)
    send_nick(NICK)
    join_channel(CHAN)


def disconnect():
    global twitchCon
    part_channel(CHAN)
    twitchCon.close()


def reconnect():
    disconnect()
    time.sleep(1/4)
    connect()

# --------------------------------------------- End Helper Functions -----------------------------------------------


# --------------------------------------------- Core Functions -----------------------------------------------------

def main():
    # Initialization phase
    global SPNT
    global EPNT
    initConfig()

    ### Ignore all of this. Initial setup phase.

    # Set recentException to False so a reconnect() isn't called early
    recentException = False
    
    # Initialize lines list
    lines = []
    try:
        with open(BNLT, encoding='UTF-8') as file:
            lines = file.readlines()
    except IOError:
        print("Banlist file not found.")
        input("Press Enter to exit...")
        sys.exit()


    ### Error checking for list Start and End spots
    if setEndPointToLength == True:
        EPNT = len(lines)
    elif setEndPointToLength == False:
        if EPNT > len(lines):
            print("ENDPOINT= is over the list length. Setting to the length of the list...")
            EPNT = len(lines)
        
    if SPNT > EPNT:
        print("STARTPOINT= is more than ENDPOINT=. Qutting...")
        sys.exit()
    elif SPNT < 0:
        print("STARTPOINT= is less than 0. Setting it to 0...")
        SPNT = 0

    # Initialize the listCounter variable to SPNT, whether that be somewhere in the list, or set to 0
    listCounter = SPNT


    ### Connection phase
    # Initialize connection
    connect()

    # Set   data   variable to empty
    data = ""

    ### Print stats phase
    # Print the number of lines detected
    print("Number of people to ban: %s" % (EPNT - SPNT))
    print("Bans per minute: %s" % (60/RLMT))
    print("Total time: %s hours" % (((EPNT - SPNT) / (60/RLMT))/60))

    while True:
        try:
            try:
                # Set non-blocking. Required in order to skip the receive stage,
                # so banning can happen as fast as possible
                twitchCon.setblocking(False)
                data = twitchCon.recv(1024).decode('UTF-8')
                twitchCon.setblocking(True)
            except socket.error:
                print("No new RECVed data")
                recentException = True
            except socket.timeout:
                print("Socket timeout")
            
            if len(data) == 0 and recentException == False:
                print("Booted, reconnecting...")
                reconnect()

            data_split = re.split(r"[~\r\n]+", data)

            for line in data_split:
                line = str.split(line)

                if len(line) >= 2:
                    if line[0] == 'PING':
                        send_pong(line[1])
                        print("[ Sent PONG ]")
                    if line[1] == 'PRIVMSG':
                        sender = get_sender(line[0])
                        message = get_message(line)
                        print(sender + ": " + message)

            if listCounter < EPNT:
                print(("[" + str(listCounter) + "] Sending ban for %s" % lines[listCounter]).rstrip())
                send_message(CHAN, "/ban %s" % lines[listCounter])
                listCounter += 1
                time.sleep(RLMT)

            if listCounter == EPNT:
                print("End of list hit. Qutting...")
                input("Press Enter to exit...")
                sys.exit()

            data = ""
            recentException = False
        
        except socket.error:
            print("ACTUAL Socket error / Attempting to reconnect automatically...")
            reconnect()

        except socket.timeout:
            print("Socket timeout / Twitch kicked you off")      
            disconnect()
            input("Press Enter to retry...")
            connect()

        except KeyboardInterrupt:
            print("\nQutting...")
            disconnect()
            input("Press Enter to exit...")
            sys.exit() 




        

# --------------------------------------------- End Core Functions ---------------------------------------------------


main()