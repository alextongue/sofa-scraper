import os
import pathlib
from bs4 import BeautifulSoup
import requests
from time import time
import pysofaconventions


def fetch_links(directoryurl, extension, howmany=[]):

    soup = BeautifulSoup(requests.get(directoryurl).content, features="lxml") # requests.get fetches the html of the file explorer

    tags = soup.findAll('a') # finds all "...<a..." strings?

    dl_links = []

    count = 0
    for entry in tags:
        if entry['href'].endswith(extension):
            dl_links.append(directoryurl + entry['href'])
            count += 1
        if (howmany and count >= howmany):
            break
            

    #dl_links = [directoryurl + entry['href'] for entry in tags if entry['href'].endswith(extension)] # in each <a ... > string, take "href=" string
 
    return dl_links

def download_links(argLinkList, argSubdirs="", printFileOutput=False):
    startTime = time()

    aDirectory = os.path.join(os.getcwd(), argSubdirs)     
    print('Downloading files to ' + aDirectory)

    for link in argLinkList:
        
        t0 = time()

        aFilename = link.split('/')[-1] # filename = last string delimited by '/'
        responseObj = requests.get(link, stream=True) # get the full path to file (response object...)
       
        aDestination =  os.path.join(aDirectory, aFilename)
        pathlib.Path(aDirectory).mkdir(parents=True, exist_ok=True)

        with open(aDestination, 'wb') as localWrite: # create local file
            numChunks = 0
            for chunk in responseObj.iter_content(chunk_size=65536):
                if chunk:
                    numChunks += 1
                    localWrite.write(chunk)

        t1 = time() - t0

        if (printFileOutput):
            print("\"" + aDestination +  "\" written (%.3f seconds, %i chunks)"%(t1, numChunks))

    totalTime = time() - startTime
    print("Download finished (%.3f seconds)"%totalTime)

    return