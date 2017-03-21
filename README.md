# BAMPFA auto-FTP-it from Google Drive to Piction
## About
This set of python scripts automates the process of FTPing images that the BAMPFA Design Director collects in Google Drive from various departments into Piction, the museum's Digital Asset Management system \(DAMS\).

Currently, for each quarterly program guide published by BAMPFA, staff have to gather images in Drive for the designer, then move images into Piction using an FTP client. This automates that step, though staff **still** have to enter basic metadata for images in the Piction online interface.

Because trying to FTP directly from Drive to Piction is more of a pain than it's worth, these scripts read from a local folder that is synced to the Drive folder our designer uses (aka this is really just a way to validate and FTP local files).

The ```master.py``` script is run by a cron job every evening. 

---
**Here's the flow of files:**\
Staff upload images to Drive\
Drive syncs the images to a local folder\
The scripts (run each evening):
* look for properly named files in the local folder that are not already in Piction
* copy new files with rejected filenames to a local Reject pile
* copy new files with valid filenames to a set of different, non-synced folders to stage for FTP (separated by Film Stills/Gallery Exhibitions/Event Images)
* FTP the contents of these staging folders to our Piction hotfolders, which get loaded each night
* delete the contents of the staging folders
* log each step

Here's the folder structure the scripts expect in the Drive-synced folder (it's really just looking for a directory with the pattern "\*\*/Images \*/\*\*"):

* [There can be any number of parent directories]
    - 2017 JUNE-JULY-AUG
        - [There can be any number of sibling directories]
        - Images — Events JJA17
            - [Images can be in any subdirectory]
        - Images — Exhibitions JJA17
        - Images — Films JJA17

And here's the FTP folder structure that Piction expects:

* Research\_Hub\_Collections
    - RH\_Events
    - RH\_Gallery\_Exhibitions
    - RH\_PFA\_Film\_Stills\_Series\_Collection

## FYIs
Non-standard Python modules used:

[pyfiglet](https://github.com/pwaller/pyfiglet)\
[pexpect](https://github.com/pexpect/pexpect)\
[Python Imaging Library (PIL)](https://pypi.python.org/pypi/PIL)\
[numpy](http://www.numpy.org/)\
[Anaconda](https://www.continuum.io/downloads) takes care of a lot of these.

I had some trouble setting up the cron job to run correctly. I am running OSX 10.11.6 and found a few StackOverload threads that led to me explicitly declaring the version of Python I wanted to run in all scripts and in crontab:

```45 19 * * * /Users/user/anaconda/bin/python /Users/user/Desktop/drive2Piction/FTPs/master.py```

In trying to get the scheduled job running I also set up a launch daemon .plist (OSX officially deprecated crontab), which is included here for referenced but not used. Maybe I'll use it later.

Without declaring UTF-8 as the encoding for all of the text files read by the scripts, cron ran into errors with accented characters.

Since I'm running this every evening long after I've gone home, I have set my computer to wake a couple of minutes before hand every day, then go to sleep an hour later. Otherwise, the cron job (or the launch daemon) wouldn't run.

There are a lot of absolute paths specified out of convenience. If I or anyone else here needs to move the scripts or staging folders it will be a pain to redo all these. FYI.

## File validation

The first step in processing the local synced folder is to check each file against the [filenaming conventions](https://docs.google.com/document/d/1gvPV2pyvgX9XgkxrmfKdFI4W6wJ48Z9RK451e4hhUDM/edit?usp=sharing) created by BAMPFA. Any files that don't match the prescribed rules for various categories of image \(or are not an approved filetype\) get rejected. This also includes matching various date formats, which are required for some types of images. Approved files get copied from the synced folder into a set of folders that match the Piction FTP folder structure. 

## Logging

A logging script notes each step of processing an image. Here are some examples: 

>##################################################
>
>shirt_2017-01-30_.jpg: This exhibition file is being checked ...\
>ERROR\
>shirt_2017-01-30_.jpg: Try renaming this exhibition image, please.
>
>##################################################
>
>shirt_2017-01-23_002.jpg: This exhibition file is being checked ...\
>shirt_2017-01-23_002.jpg: Filename format is ok, proceeding to check the date ...\
>shirt_2017-01-23_002.jpg: SUCCESS, you didn't muck up the filename, let's see if it's already in Piction ....\
>shirt_2017-01-23_002.jpg This file is ready to be FTPed
>
>##################################################


Rejected files are sent to a local directory so they can be cleaned.

The logger also notes the status of FTP transfers. 

Part of the script that copies files into the FTP source folder also makes a list of all files that pass the filename validation, and any files that are already on that list are ignored.

## To do:

* Configure logger to note any FTP error codes that are returned
* Figure out workflow with staff to handle renaming rejected files
* Maybe autocorect common filename errors (spaces, accented Latin characters)
* Make things rely less on explicit absolute paths.