# BAMPFA auto-FTP-it from Google Drive to Piction
## About
This set of python scripts automates the process of FTPing images that the BAMPFA Design Director collects in Google Drive from various departments into Piction, the museum's Digital Asset Management system \(DAMS\).

Currently, for each quarterly program guide published by BAMPFA, staff have to gather images in Drive for the designer, then move images into Piction using an FTP client. This automates that step, though staff **still** have to enter basic metadata for images in the Piction online interface.

Because trying to FTP directly from Drive to Piction is more of a pain than it's worth, these scripts read from a local folder that is synced to the Drive folder our designer uses.

Here's the folder structure the scripts expect in the Drive-synced folder

* Program Guide Images June/July/August 2017
    - Art images
    - Film images
    - Event images

And here's the FTP folder structure that Piction expects:

* Research\_Hub\_Collections
    - RH\_Events
    - RH\_Gallery\_Exhibitions
    - RH\_PFA\_Film\_Stills\_Series\_Collection

### File validation

The first step in processing the local synced folder is to check each file against the [filenaming conventions](https://docs.google.com/document/d/1gvPV2pyvgX9XgkxrmfKdFI4W6wJ48Z9RK451e4hhUDM/edit?usp=sharing) created by BAMPFA. Any files that don't match the prescribed rules for various categories of image \(or are not an approved filetype\) get rejected. This also includes matching various date formats, which are required for some types of images. Approved files get copied from the synced folder into a set of folders that match the Piction FTP folder structure. 

### Logging

A logging script notes each step of processing an image. Here are some examples: 

>##################################################
>
>shirt_2017-01-30_.jpg: This exhibition file is being checked ...
>ERROR
>shirt_2017-01-30_.jpg: Try renaming this exhibition image, please.
>
>##################################################
>
>shirt_2017-01-23_002.jpg: This exhibition file is being checked ...
>shirt_2017-01-23_002.jpg: Filename format is ok, proceeding to check the >date ...
>shirt_2017-01-23_002.jpg: SUCCESS, you didn't muck up the filename, let's see if it's already in Piction .... 
>shirt_2017-01-23_002.jpg This file is ready to be FTPed
>
>##################################################


Rejected files are sent to a local directory so they can be cleaned.

The logger also notes the status of FTP transfers. 

Part of the script that copies files into the FTP source folder also makes a list of all files that pass the filename validation, and any files that are already on that list are ignored.

## To do:

* Clean up scripts/check for consistency
* Change logger to note any FTP error codes that are returned
* Probably more