# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 07:28:18 2021

@author: tinscore
"""
import os
from shutil import copyfile, copytree, rmtree
from datetime import datetime

# %%
homedir = os.path.expanduser('~') + '\documents\my games\Terraria\players'
character = input('Character to Save or Load: ')

localMapFolder = '\\'.join((homedir, character))
localPlayerFile = localMapFolder + '.plr'

remoteMapFolder = f'C:\\Path\\To\\Backup\\Players\\{character}' # Input path to your backup folder
remotePlayerFile = remoteMapFolder + '.plr'

lastMod = {}

# %% - Check if files exist - get last mod time for comparison
try:
    lastMod['local'] = os.stat(localPlayerFile).st_mtime
    localTimestamp = datetime.fromtimestamp(lastMod['local'])
    localDateTime = [localTimestamp.year,
                     localTimestamp.month,
                     localTimestamp.day,
                     localTimestamp.hour,
                     localTimestamp.minute]
    lastMod['local'] = datetime(*localDateTime).timestamp()

except FileNotFoundError:
    if os.path.exists(remotePlayerFile):
        copyfile(remotePlayerFile, localPlayerFile)
        copytree(remoteMapFolder, localMapFolder)
        print('Creating Character locally')
        input('Press any key to exit...')
        os._exit(1)
    else:
        print('Local and Remote files do not exist')
        input('Press any key to exit...')
        os._exit(1)
try:
    lastMod['remote'] = os.stat(remotePlayerFile).st_mtime
    remoteTimestamp = datetime.fromtimestamp(lastMod['remote'])
    remoteDateTime = [remoteTimestamp.year,
                      remoteTimestamp.month,
                      remoteTimestamp.day,
                      remoteTimestamp.hour,
                      remoteTimestamp.minute]
    lastMod['remote'] = datetime(*remoteDateTime).timestamp()
except FileNotFoundError:
    copyfile(localPlayerFile, remotePlayerFile)
    copytree(localMapFolder, remoteMapFolder)
    print('Creating Character remotely')
    input('Press any key to exit...')
    os._exit(1)

# compare last mod times - overwrite older file with newer contents
if lastMod['local'] == lastMod['remote']:  # if equal
    input('Files are equal - Press Enter to exit...')

elif lastMod['local'] > lastMod['remote']:  # if local newer
    print("Local Newer - Updating Remote")
    copyfile(localPlayerFile, remotePlayerFile)

    rmtree(remoteMapFolder)
    copytree(localMapFolder, remoteMapFolder)
    input('Press any key to exit...')

else:  # else remote newer
    print("Remote Newer - Updating Local")
    copyfile(remotePlayerFile, localPlayerFile)

    rmtree(localMapFolder)
    copytree(remoteMapFolder, localMapFolder)
    input('Press any key to exit...')