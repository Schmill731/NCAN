#!/usr/bin/env python3

# 2017_export_apps.py
#
# By Billy Schmitt
# schmitt@neurotechcenter.org
#
# Last Updated: 12/28/16
#
# Used to convert Qualtrics CSV response data to easy-to-review PDFs for each 
# response. Assumes that the CSV files and other folders are located in the 
# ../directory and are named as follows:
# Demographic Supplement Responses: Demographic_Supplement.csv
# Summer Course Recommendation Responses: Summer_Course_Recommendations.csv
# Summer Course Recommendation Files: Q1 (Folder)
# Summer Course 2017 Registration Responses: Summer_Course_2017_Registration.csv
# Summer Course 2017 Application Responses: Summer_Course_2017_Application.csv
# Summer Course 2017 Application Responses: Summer_Course_2017_Application (Folder)

# Import necessary libraries
import csv

# Create headers for registration data
regHeader = ["RegID", "ResponseSet", "BlankName", "ExternalDataReference", 
    "BlankEmail", "IPAddress", "Status", "StartDate", "EndDate", "Finished", 
    "ResponseID", "Intro", "FirstName", "LastName", "Email", "Ones", "RecInfo", 
    "Rec1First", "Rec1Last", "Rec1Email", "Rec2First", "Rec2Last", "Rec2Email",
    "Rec3First", "Rec3Last", "Rec3Email", "Rec4First", "Rec4Last", "Rec4Email",
    "Lat", "Long", "LocAcc"]

regs = None

# Read in Registration Data
with open('../Summer_Course_2017_Registration.csv', newline='') as regFile:
    registrations = csv.DictReader(regFile, fieldnames=regHeader)
    
    # Remove the Qualtrics headers
    regs = list(registrations)[2:]

print(regs)

