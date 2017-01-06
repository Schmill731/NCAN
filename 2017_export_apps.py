#!/usr/bin/env python3

# 2017_export_apps.py
#
# By Billy Schmitt
# schmitt@neurotechcenter.org
#
# Last Updated: 12/29/16
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
from pdf_templates import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Frame, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger
import glob

# High-level walkthrough
def main():

    #Import Qualtrics Data for use here
    regs = importRegistrationData()
    apps = importApplicationData()
    recs = importRecommendationData()
    dems = importDemographicData()

    #Join applications with registrations
    for app in apps:
        for reg in regs:
            if reg["Email"] == app["Email"]:
                app.update(reg)
                break

    #Join recommendations with applications
    for rec in recs:
        for app in apps:
            if app["Rec1Email"] == rec["Email"]:
                app["Rec1ID"] = rec["recID"]
            if app["Rec2Email"] == rec["Email"]:
                app["Rec2ID"] = rec["recID"]
            if app["Rec3Email"] == rec["Email"]:
                app["Rec3ID"] = rec["recID"]
            if app["Rec4Email"] == rec["Email"]:
                app["Rec4ID"] = rec["recID"]

    # Join demographic info with applications
    for dem in dems:
        for app in apps:
            if dem["AppID"] == app["AppID"]:
                app.update(dem)

    # Make folder for pdfs if it does not exist
    if not os.path.exists('../2017_Applications'):
        os.makedirs('../2017_Applications')

    # Make application PDFs
    for app in apps:

        #Add Basic info and SOI
        completed = makeApplicationPDF(app)

        # Open PDF for editing
        inpdf = PdfFileReader(open("../2017_Applications/{}.pdf".format(app["AppID"]), "rb"))
        outpdf = PdfFileWriter()

        #If incomplete, add a watermark
        if not completed:
            pageCount = inpdf.getNumPages()
            pages = []
            for num in range(0, pageCount):
                pages.append(inpdf.getPage(num))
            pages = addWatermark(pages)
            for page in pages:
                outpdf.addPage(page)

        # Open CV and Transcript
        cvPath = glob.glob("../Summer_Course_2017_Application/Q12/{}*.pdf".format(app["AppID"]))
        if cvPath:
            cvpdf = PdfFileReader(open(cvPath[0], "rb"))
            cvCount = cvpdf.getNumPages()
            cvPages = []
            for num in range(0, cvCount):
                cvPages.append(cvpdf.getPage(num))
            cvPages = addWatermark(cvPages)
            cvPages = addHeader(cvPages, app["AppID"])
            for page in cvPages:
                outpdf.addPage(page)

        # Write new PDF
        outputStream = open("../2017_Applications/{}.pdf".format(app["AppID"]), "wb")
        outpdf.write(outputStream)

        #delete header file
        os.remove("{}_Header.pdf".format(app["AppID"]))






#Helper Functions

def importRegistrationData():
    # Create headers for registration data
    regHeader = ["RegID", "ResponseSet", "BlankName", "ExternalDataReference", 
        "BlankEmail", "IPAddress", "Status", "StartDate", "EndDate", "Finished", 
        "ResponseID", "Intro", "First", "Last", "Email", "Ones", "RecInfo", 
        "Rec1First", "Rec1Last", "Rec1Email", "Rec2First", "Rec2Last", 
        "Rec2Email", "Rec3First", "Rec3Last", "Rec3Email", "Rec4First", 
        "Rec4Last", "Rec4Email", "Lat", "Long", "LocAcc", "Blank"]
    regJunk = ["ResponseID", "BlankEmail", "Intro", "Ones", "RecInfo"]

    # Read in Registration Data
    return readQualtricsCSV("../Summer_Course_2017_Registration.csv", regHeader, 
        regJunk)

def importApplicationData():
    #Create headers for application data
    appHeader = ["AppID", "ResponseSet", "BlankName", "ExternalDataReference",
        "BlankEmail", "IPAddress", "Status", "StartDate", "EndDate", "Finished",
        "First", "Last", "Email", "SOI", "TranscriptURL", "cvURL", "Lat",
        "Long", "LocAcc", "Blank"]
    appJunk = ["BlankEmail"]

    # Read in Application Data
    apps = readQualtricsCSV("../Summer_Course_2017_Application.csv", appHeader, appJunk)

    # Remove blank responses from apps
    return [x for x in apps if x["Email"] != '']

def importRecommendationData():
    # Create headers for recommendation data
    recHeader = ["recID", "ResponseSet", "BlankName", "ExternalDataReference", 
        "Email", "IPAddress", "Status", "StartDate", "EndDate", "Finished", 
        "AppFirst", "AppLast", "AppEmail", "Intro", "recURL", "Lat", "Long", 
        "LocAcc", "Blank"]
    recJunk = ["Intro", "recURL"]

    # Read in Recommendation Data
    return readQualtricsCSV("../Summer_Course_Recommendations.csv", recHeader, 
        recJunk)

def importDemographicData():
    # Create headers for demographic data
    demHeader = ["demID", "ResponseSet", "BlankName", "ExternalDataReference", 
        "BlankEmail", "IPAddress", "Status", "StartDate", "EndDate", "Finished", 
        "AppID", "AppFirst", "AppLast", "Intro", "Hispanic", "White", "Black", 
        "Native", "Asian", "Pacific", "JunkRaceOther", "RaceOther", "Gender", 
        "Bachelors", "Masters", "Doctoral", "Professional", "JunkEdOther", 
        "EdOther", "Lat", "Long", "LocAcc", "Blank"]
    demJunk = ["BlankEmail", "AppFirst", "AppLast", "Intro", "JunkRaceOther", 
        "JunkEdOther"]

    # Read in demographic data
    return readQualtricsCSV("../Demographic_Supplement.csv", demHeader, demJunk)


def makeApplicationPDF(app):
    #Create PDF
    pdf = SimpleDocTemplate("../2017_Applications/{}.pdf".format(app["AppID"]), 
        pagesize=letter, topMargin=108, rightMargin=72, leftMargin=72, bottomMargin=72)

    # Compile Info to Print on PDF
    info = [
        Paragraph("Basic Information", styles["heading1"]),
        Paragraph("<b>Name:</b> {} {}".format(app["First"], app["Last"]), styles["normal"]),
        Paragraph("<b>Email:</b> {}".format(app["Email"]), styles["normal"]),
        Paragraph("Demographic Information", styles["heading1"])]

    # Add demographic info
    if "demID" not in app.keys():
        info.append(Paragraph("Applicant did not complete optional" + 
            " demographic supplement.", styles["normal"]))
        for _ in range(0, 2):
            info.append(Paragraph("", styles["normal"]))
    else:
        # Hispanic or Latino Information
        hispanic = ""
        if app["Hispanic"] == "2":
            hispanic = "No"
        elif app["Hispanic"] == "1":
                hispanic = "Yes"
        elif not hispanic:
            hispanic = "No answer"
        info.append(Paragraph("<b>Are you Hispanic or Latino?</b> {}".format(hispanic), styles["normal"]))

        #Race/Ethnicity
        race = ""
        def addComma(str):
            if str:
               return str + ", "
            else:
                return str
        if app["White"]:
            race = race + "White"
        if app["Black"]:
            race = addComma(race)
            race = race + "Black/African American"
        if app["Native"]:
            race = addComma(race)
            race = race + "American Indian/Alaska Native"
        if app["Asian"]:
            race = addComma(race)
            race = race + "Asian"
        if app["Pacific"]:
            race = addComma(race)
            race = race + "Native Hawaiian/Pacific Islander"
        if app["RaceOther"]:
            race = addComma(race)
            race = race + app["Other"]
        if not race:
            race = "No answer"
        info.append(Paragraph("<b>Race or Ethnicity:</b> {}".format(race), styles["normal"]))

        # Gender
        gender = ""
        if app["Gender"] == "1":
            gender = "Male"
        elif app["Gender"] == "2":
            gender = "Female"
        elif gender:
            gender = "No answer"
        info.append(Paragraph("<b>Gender:</b> {}".format(gender), styles["normal"]))

        #Education
        ed = ""
        if app["Bachelors"]:
            ed = "Bachelor's Degree"
        if app["Masters"]:
            ed = addComma(ed)
            ed = ed + "Master's Degree"
        if app["Doctoral"]:
            ed = addComma(ed)
            ed = ed + "Doctoral Degree"
        if app["Professional"]:
            ed = addComma(ed)
            ed = ed + "Professional Degree"
        if app["EdOther"]:
            ed = addComma(ed)
            ed = ed + app["Other"]
        if not ed:
            ed = "No answer"
        info.append(Paragraph("<b>Education:</b> {}".format(ed), styles["normal"]))

    #Determine number of recommenders
    recCount = 2
    if "Rec3Email" in app.keys():
        recCount = 3
    elif "Rec4Email" in app.keys():
        recCount = 4

    #Counter to track # of recommendation letters submitted
    recsSubmitted = 0

    #Print recommender info
    info.append(Paragraph("Recommender Information", styles["heading1"]))
    for i in range(1, recCount):
        info.append(Paragraph("Recommender #" + str(i), styles["heading2"]))
        info.append(Paragraph("<b>Name:</b> {} {}".format(app["Rec" + str(i) + "First"], app["Rec" + str(i) + "Last"]), styles["normal"])),
        info.append(Paragraph("<b>Email:</b> {}".format(app["Rec" + str(i) + "Email"]), styles["normal"]))

        # Check whether letter was submitted
        if "Rec" + str(i) + "ID" in app.keys():
            recSubmit = "YES"
            recsSubmitted += 1
        else:
            recSubmit = "NO"
        info.append(Paragraph("<b>Recommendation Submitted?</b> {}".format(recSubmit), styles["normal"]))

    # If application is incomplete, print that
    completed = True
    if recsSubmitted < 2:
        info.append(Paragraph("", styles["heading1"]))
        info.append(Paragraph("APPLICATION INCOMPLETE", styles["title"]))
        info.append(Paragraph("Reason: Less than 2 recommendation letters", styles["title"]))
        completed = False

    #Add a Page Break for the application
    info.append(PageBreak())

    #Split SOI along line breaks
    soi = app["SOI"].split(" / ")
    for para in soi:
        info.append(Paragraph(para, styles["soi"]))

    #Make templates
    def BasicInfo(canvas, doc): BasicInfoPage(app, canvas, doc)
    def soiTemplate(canvas, doc): BlankHeader(app, canvas, doc)

    # Make PDF with pre-defined page templates.
    pdf.build(info, onFirstPage=BasicInfo, onLaterPages=soiTemplate, canvasmaker=PageNumCanvas)

    #Make pdf with header to add to each page of application
    header = SimpleDocTemplate("{}_Header.pdf".format(app["AppID"]), 
        pagesize=letter, topMargin=108, rightMargin=72, leftMargin=72, bottomMargin=72)
    def headerTemplate(canvas, doc): BlankHeader(app, canvas, doc)

    header.build([Paragraph("", styles["title"])], onFirstPage=headerTemplate)

    #Return whether the application is complete or not.
    return completed



# Run everything!
if __name__ == "__main__":
    main()


