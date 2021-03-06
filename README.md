# NCAN Summer Course Qualtrics Application Export Script Instructions

## Description

These instructions describe how to render the NCAN Summer Course applications into easy-to-read PDFs. A copy of the NCAN scripts folder, which includes this readme, is accessible on GitHub at: `https://github.com/Schmill731/NCAN`. This GitHub will always contain the newest version of this script (and others for the summer course). Please note that it does not contain the requisite `client_secrets.json` file as this contains sensitive data. Please contact Billy Schmitt if you require this file.

## Step 1: Download Qualtrics CSV and Files

* Log-in to Qualtrics
* Download the Registration Data
	1. Navigate to the `Summer Course 2017 Registration` Survey's **Data & Analysis** Module.
	1. Click `Export & Import`.
	1. Click `Export Data`.
	1. Click `Export Data with Legacy Format`.
	1. Click `Download`.
	
* Download the Application Data
	1. Navigate to the `Summer Course 2017 Application` Survey's **Data & Analysis** Module.
	1. Download the CSV Data.
		1. Click `Export & Import`.
		1. Click `Export Data`.
		1. Click `Export Data with Legacy Format`.
		1. Click `Download`.
	1. Download the User-Submitted Files 
		1. Click `Export & Import`.
		1. Click `Export Data`.
		1. Click `Export Data with Legacy Format`.
		1. Click `User-Submitted Files`.
		1. Click `Download`.
		1. If necessary, navigate to your Downloads folder and unzip the file just downloaded.
		
* Download the Recommendation Data
	1. Navigate to the `Summer Course Recommendations` Survey's **Data & Analysis** Module.
	1. Download the CSV Data.
		1. Click `Export & Import`.
		1. Click `Export Data`.
		1. Click `Export Data with Legacy Format`.
		1. Click `Download`.
	1. Download the User-Submitted Files 
		1. Click `Export & Import`.
		1. Click `Export Data`.
		1. Click `Export Data with Legacy Format`.
		1. Click `User-Submitted Files`.
		1. Click `Download`.
		1. If necessary, navigate to your Downloads folder and unzip the file just downloaded.

* Download the Demographic Supplement Data
	1. Navigate to the `Demographic Supplement` Survey's **Data & Analysis** Module.
	1. Click `Export & Import`.
	1. Click `Export Data`.
	1. Click `Export Data with Legacy Format`.
	1. Click `Download`.

## Step 2: Run the Script

* Move the NCAN folder (and unzip it, if necessary) to your downloads folder
* Open a terminal window and navigate to the NCAN folder (likely `cd C:/users/your_username/downloads/NCAN`).
* If this is your first time running the script on this computer, ensure you have python 3 installed (run `python3 -V` to find out) and run: `pip3 install --user -r requirements.txt`
* If necessary, open `export_apps.py` and update the `year` and `GDriveDestID` global variables as necessary.
	* You can obtain the ID for the folder you wish to place the applicant PDFs by going to the folder on your Google Drive account and looking at the URL for that folder: `https://drive.google.com/drive/u/1/folders/the_id_is_here`
* type: `./export_apps.py`
* Allow the Google Drive Authentication that will pop up (needed in order to upload the files to Google Drive).
* Please note that it will take a while to run. Making PDFs should not take a while (less than a minute per application), but uploading could take longer (~2 minutes per application), especially if you are uploading the files into a Google Drive folder that is not owned by you.

## Step 3: Check Google Drive

* Log on to your Google Drive account, and navigate to the appropriate folder to check if the files have uploaded to your account.