import re
import socket
import time
import sys

# --------------------------------------------- Start Settings ----------------------------------------------------
HOST = "irc.twitch.tv"                          # Hostname of the IRC-Server in this case twitch's
PORT = 6667                                     # Default IRC-Port
CHAN = ""                                       # Channelname = #{Nickname}
NICK = ""                                       # Nickname = Twitch username
PASS = ""                                       # www.twitchapps.com/tmi/ will help to retrieve the required authkey
BNLT = ""                                       # List of individuals to ban
SPNT = 0                                        # Where to start in the Banlist
# --------------------------------------------- End Settings -------------------------------------------------------


# --------------------------------------------- Start Global Variables ---------------------------------------------

twitchCon = ""

# --------------------------------------------- End Global Variables ----------------------------------------------


# --------------------------------------------- Start Init Function ------------------------------------------------

# Check for the following lines
# "CHANNEL="
# "USER="
# "OAUTH="
# "BANLIST="
# "STARTPOINT="
def initConfig():
    paramCheckList = ["CHANNEL=", "USER=", "OAUTH=", "BANLIST=", "STARTPOINT="]
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
        if paramCheckList[0] in item:
            global CHAN
            CHAN = "#" + item.replace(paramCheckList[0], '')
            CHAN = CHAN.rstrip()
        if paramCheckList[1] in item:
            global NICK
            NICK = item.replace(paramCheckList[1], '')
            NICK = NICK.rstrip()
        if paramCheckList[2] in item:
            global PASS
            PASS = item.replace(paramCheckList[2], '')
            PASS = PASS.rstrip()
        if paramCheckList[3] in item:
            global BNLT
            BNLT = item.replace(paramCheckList[3], '')
            BNLT = BNLT.rstrip()
        if paramCheckList[4] in item:
            global SPNT
            SPNT = item.replace(paramCheckList[4], '')
            SPNT = SPNT.rstrip()
            SPNT = int(SPNT)

    
# --------------------------------------------- End Init Function --------------------------------------------------


# --------------------------------------------- Start Functions ----------------------------------------------------
def send_pong(msg):
    twitchCon.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))


def send_message(chan, msg):
    twitchCon.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))


def send_nick(nick):
    twitchCon.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))


def send_pass(password):
    twitchCon.send(bytes('PASS %s\r\n' % password, 'UTF-8'))


def join_channel(chan):
    twitchCon.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))


def part_channel(chan):
    twitchCon.send(bytes('PART %s\r\n' % chan, 'UTF-8'))
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

# --------------------------------------------- End Helper Functions -----------------------------------------------


# --------------------------------------------- Core Functions -----------------------------------------------------

def main():
    # Initialization phase
    initConfig()

    # Ignore all of this. Initial setup.
    trueCount = SPNT
    count = SPNT
    lines = []
    try:
        with open(BNLT, encoding='UTF-8') as file:
            lines = file.readlines()
    except IOError:
        print("Banlist file not found.")
        input("Press Enter to exit...")
        sys.exit()

    # Initialize connection
    connect()

    # Set   data   variable to empty
    data = ""

    # Print the number of lines detected
    print("Number of people to ban: %s" % len(lines))

    while True:
        try:
            try:
                twitchCon.setblocking(False)
                data = twitchCon.recv(1024).decode('UTF-8')
                twitchCon.setblocking(True)
            except socket.error:
                print("No new RECVed data")
                trueCount += 1
            except socket.timeout:
                print("Socket timeout")
                
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

            if count < len(lines):
                print(("[" + str(count) + "] [" + str(trueCount) + "] Sending ban for %s" % lines[count]).rstrip())
                send_message(CHAN, "/ban %s" % lines[count])
                count += 1
                time.sleep(2/5)

            if count == len(lines):
                sys.exit()

            data = ""
        
        except socket.error:
            print("ACTUAL Socket error / Attempting to reconnect...")
            connect()

        except socket.timeout:
            print("Socket timeout / Twitch kicked you off")      
            input("Press Enter to exit...")

        except KeyboardInterrupt:
            print("Qutting...")
            input("Press Enter to exit...")
            sys.exit() 




        

# --------------------------------------------- End Core Functions ---------------------------------------------------


main()