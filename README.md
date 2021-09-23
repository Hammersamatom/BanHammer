# BanHammer v0.2 - A mass-banning tool for Twitch - Now bans at Twitch's speed limit!
## SPECIAL NOTE

* Windows Defender and other Anti-Virus software ***WILL*** mark ```BanHammer.exe``` as a virus
	* This project uses ```PyInstaller``` to make the executable file ```BanHammer.exe```
	* In the ***INFINITE WISDOM*** of Microsoft and other Anti-Virus providers, they've marked every executable made with ```PyInstaller``` as a virus instead of improving their virus detection
  * This software is currently licensed with a standard GPLv3 license which is found in the file ```LICENSE.md``` on this GitHub page.

## Changelog - Current: v0.2
### v0.2 - 9/22/2021
#### Added
- Added a config setting to change how quickly the program bans
- Added setting custom end points when banning lists
- Added error checking for the starting point in the ```config.txt``` file
- Added error handling for Broken Pipes
- Added a dirty hack to reconnect when Twitch dilently disconnects the program

#### Fixed
- Fixed ```config.txt``` parsing to handle leading whitespace better
- Fixed disconnect function
- <span style="color:limegreen">Fixed slow ban-rate, it's now the maximum allowed by Twitch</span>

### v0.1 - 9/21/2021
- Initial release

## Donate here if you want
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/W7W06AY2V)

## Requirements

- Windows
  - The EXE file ```BanHammer.exe```
  - [Twitch Account OAuth token](https://www.twitchapps.com/tmi/)

- Linux / macOS
  - Python 3.0 or over
  - The Python script ```banner.py```
  - [Twitch Account OAuth token](https://www.twitchapps.com/tmi/)


## Setup
1. Make a folder anywheres you like to store the EXE/Python script and the other files
2. Download the ```BanHammer.exe``` file or ```banner.py``` Python script from the ```Releases``` section of this GitHub page and put them in the new folder you just made
3. You're gonna need to make a ```config.txt``` file with the following contents
   ```
   CHANNEL=this_is_a_channel_name
   USER=ThisIsYourModeratorUsername
   OAUTH=oauth:hafh80vesee5urltfzsxkpv67cgcjo
   BANLIST=list.txt
   RATELIMIT=0.3025
   STARTPOINT=0
   ENDPOINT=MAX
   ```
   ```
   NOTE 1: The OAuth token used in the example is fake, you can get a real one in the Requirements section
   
   NOTE 2: In the config above, list.txt can be replaced with the name of any text file that follows the
   requirements listed below
   
   NOTE 3: RATELIMIT= is the seconds between bans. If left empty it will default to 0.3025 seconds per ban
   
   NOTE 4: STARTPOINT= can be left empty, it will default to the start of the list
   
   NOTE 5: ENDPOINT= can be set to MAX or be left empty. If so, the program will run over the entire list
   ```

4. You're also going to need a ```list.txt``` of people to ban, with one name per line
    ```
    hoss000312
    hoss000759
    hoss000952
    hoss00132
    hoss00132__
    hoss00275
    hoss00301
    blueberrydogs_perikan00
    blueberrydogs_skenshi
    blueberrydogs_tanipotato
    blueberrydogs_auau____
    blueberrydogs_jpmasaki
    ...
    ```
    You *do not* want a ```list.txt``` formatted like below, with the ```/ban``` already added or with a ```ban reason```
    ```
    /ban hoss000312 Ban Reason
    /ban hoss000759 Hate Bot
    /ban hoss000952 Hate Bot
    /ban hoss00132 Hate Bot
    /ban hoss00132__ Hate Bot
    /ban hoss00275 Hate Bot
    /ban hoss00301 
    /ban blueberrydogs_perikan00
    /ban blueberrydogs_skenshi
    /ban blueberrydogs_tanipotato
    /ban blueberrydogs_auau____
    /ban blueberrydogs_jpmasaki
    ...
    ```
5. Both the ```config.txt``` file and ```list.txt``` file should be in the same folder as the Python script or EXE file

## Usage

1. Double check any lists you use just in case there's someone who *shouldn't* be banned in it

2. If an individual is already banned, the program will skip them

3. Execute the ```BanHammer.exe``` file on Windows, or the Python script on other platforms

## Some notes and tips

- The message ```No new RECVed data``` is normal, it just means that there hasn't been any relevant data sent back to the program
- If you ever need to stop the program prematurely, you can use the keyboard combination **Ctrl+C**
- If you *do* need to stop the program and restart it later, the number in [ ] on the bottom left is the most recent ban
    - You can then set the ```config.txt``` line with ```STARTPOINT=``` to that number, and the program will pick up where it left off. This will be automatic in the future
- Sometimes, Twitch won't send messaging in a streamer's chat if this program is running. This only happens when you use the same Moderator account for both this program, and active chatting