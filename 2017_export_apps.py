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
import os
from export_support import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Functions
def readQualtricsCSV(filePath, header, uniqueJunk=[]):
    """Reads in Exported Qualtrics CSV files located at filePath, uses header to
    build a list of dictionaries where the keys are header, and then strips away
    the data located at uniqueJunk plus the common headers across all Qualtrics
    CSV exports."""

    #Read in file
    with open(filePath, newline='') as qualcsv:
        rawData = csv.DictReader(qualcsv, fieldnames=header)

        #Remove Qualtrics headers
        responses = list(rawData)[2:]

        #Common junk to all Qualtrics CSV exports
        commonJunk = ["ResponseSet", "BlankName", "ExternalDataReference", "BlankEmail",
            "IPAddress", "Status", "StartDate", "EndDate", "Finished",
            "Lat", "Long", "LocAcc", "Blank"]

        #Combine with commonJunk with unique junk
        junkHeaders = commonJunk + uniqueJunk

        #Remove junk
        for response in responses:
            for junk in junkHeaders:
                response.pop(junk)

        return responses

# Create headers for registration data
regHeader = ["RegID", "ResponseSet", "BlankName", "ExternalDataReference", 
    "BlankEmail", "IPAddress", "Status", "StartDate", "EndDate", "Finished", 
    "ResponseID", "Intro", "First", "Last", "Email", "Ones", "RecInfo", 
    "Rec1First", "Rec1Last", "Rec1Email", "Rec2First", "Rec2Last", "Rec2Email",
    "Rec3First", "Rec3Last", "Rec3Email", "Rec4First", "Rec4Last", "Rec4Email",
    "Lat", "Long", "LocAcc", "Blank"]
regJunk = ["ResponseID", "Intro", "Ones", "RecInfo"]

# Read in Registration Data
regs = readQualtricsCSV("../Summer_Course_2017_Registration.csv", regHeader, regJunk)

#Create headers for application data
appHeader = ["AppID", "ResponseSet", "BlankName", "ExternalDataReference",
    "BlankEmail", "IPAddress", "Status", "StartDate", "EndDate", "Finished",
    "First", "Last", "Email", "SOI", "TranscriptURL", "cvURL", "Lat",
    "Long", "LocAcc", "Blank"]

# Read in Application Data
apps = readQualtricsCSV("../Summer_Course_2017_Application.csv", appHeader)

# Remove blank responses from apps
apps = [x for x in apps if x["Email"] != '']
        
#Join applications with registrations
for app in apps:
    for reg in regs:
        if reg["Email"] == app["Email"]:
            app.update(reg)
            break

# Make folder for response if it does not exist
if not os.path.exists('2017_Applications'):
    os.makedirs('2017_Applications')

# Begin making Application PDFs
for app in apps:
    pdf = canvas.Canvas("2017_Applications/" + app["AppID"] + ".pdf",
        pagesize=letter)
    pdf.setFont("Times-Roman", 12)
    pdf.drawString(72, 744, "Applicant ID: " + app["AppID"])
    pdf.setFont("Times-Bold", 18)
    pdf.drawCentredString(306, 702, "Applicant Information")
    pdf.setFont("Times-Roman", 12)
    pdf.drawString(72, 648, "Name: " + app["First"] + " " + app["Last"])
    pdf.save()




