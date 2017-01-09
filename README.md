# NCAN Summer Course Qualtrics Application Export Script Instructions

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

* Move the NCAN_scripts folder to your downloads folder
* Open a terminal window and navigate to the NCAN folder
* If necessary, open `export_apps.py` and update the `year` and `GDriveDestID` global variables as necessary.
* type: `./export_apps.py`
* Allow the Google Drive Authentication that will pop (needed in order to upload the files to Google Drive).

## Step 3: Check Google Drive

* Log on to your Google Drive account, and navigate to the appropriate folder to check if the files have uploaded to your account.