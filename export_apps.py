#!/usr/bin/env python3

# export_apps.py
#
# By Billy Schmitt
# schmitt@neurotechcenter.org
#
# Last Updated: 1/9/17
#
# Used to convert Qualtrics CSV response data to easy-to-review PDFs for each 
# response. Assumes that the CSV files and other folders are located in the 
# parent directory (..) and are named as follows (default of Qualtrics exports):
# Demographic Supplement Responses: Demographic_Supplement.csv
# Summer Course Recommendation Responses: Summer_Course_Recommendations.csv
# Summer Course Recommendation Files: Q1 (Folder)
# Summer Course {year} Registration Responses: Summer_Course_{year}_Registration.csv
# Summer Course {year} Application Responses: Summer_Course_{year}_Application.csv
# Summer Course {year} Application Files: Summer_Course_{year}_Application (Folder)

# Import necessary libraries
import os
import shutil
import collections
import csv
from glob import glob
from export_support import *
from pdf_templates import *
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from PyPDF2 import PdfFileWriter, PdfFileReader
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Global variables
year = "2017"
GDriveDestID = "0B67b4FFl6pYlVnY2cVpFbjlGdmM"

# High-level Walkthrough of script
def main():
    print("\n--------Exporting {} Applications--------".format(year))

    # Import Qualtrics Data for use here- this is only the data, no file uploads
    print("Importing Data...")
    regs = ImportRegistrationData()
    apps = ImportApplicationData()
    recs = ImportRecommendationData()
    dems = ImportDemographicData()

    # Join registration data with application data
    print("Combining data...")
    for app in apps:
        for reg in regs:
            if reg["Email"] == app["Email"]:
                app.update(reg)
                break

    # Join recommendation data with application data
    for app in apps:
        for rec in recs:
            # Save number of recommenders
            recCount = 0

            # Link recommenders with applications
            for num in range(1, 5):
                if "Rec{}Email".format(num) in app.keys():
                    if app["Rec{}Email".format(num)] == rec["Email"]:
                        app["Rec{}ID".format(num)] = rec["recID"]
                        recCount += 1
            app["RecCount"] = recCount

    # Join demographic info with applications
    for dem in dems:
        for app in apps:
            if dem["AppID"] == app["AppID"]:
                app.update(dem)

    # Create and/or clean up workspace for files
    print("Creating folder for applications...")
    appFolder = "../{}_Applications".format(year)
    if not os.path.exists(appFolder):
        # Create workspace (e.g. folder to hold applications)
        os.makedirs(appFolder)
    else:
        # Clean up workspace (e.g. delete all files in folder)
        for file in os.listdir(appFolder):
            file_path = os.path.join(appFolder, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    # Make section template PDFs
    templates = ["Cover Page", "Statement of Interest", "CV or Resume",
        "(Unofficial) Transcript", "Recommendation Letter #1", 
        "Recommendation Letter #2", "Recommendation Letter #3", 
        "Recommendation Letter #4"]
    for template in templates:
        MakeSectionPdf(template)

    # Make application PDFs
    print("\n--------Making PDFs--------")
    appCount = 1
    for app in apps:
        print("Starting Application {} of {}...".format(appCount,
            len(apps)))

        #Create dictionary to hold PDF pages
        docs = collections.OrderedDict()

        # Make SOI first (basic info last, to check if all parts submitted)
        MakeSoiPdf(app)
        soi = GetPdf("{}_SOI.pdf".format(app["AppID"]))
        docs["Statement of Interest"] = soi

        # Get CV
        cvExists = False
        cv = GetPdf("../Summer_Course_{}_Application/Q12/{}*.pdf".format(year,
            app["AppID"]))
        if cv:
            docs["CV or Resume"] = cv
            cvExists = True

        # Get transcript
        transcriptExists = False
        transcript = GetPdf("../Summer_Course_{}_Application/Q11/{}*.pdf".format(year,
            app["AppID"]))
        if transcript:
            docs["(Unofficial) Transcript"] = transcript
            transcriptExists = True

        # Get recommendation letters and add it to WIP PDF
        letterExists = [None]
        for num in range(1, 5):
            letterExists.append(False)
            if "Rec{}ID".format(num) in app.keys():
                letter = GetPdf("../Q1/{}*.pdf".format(app["Rec{}ID".format(num)]))
                if letter:
                    docs["Recommendation Letter #" + str(num)] = letter
                    letterExists[num] = True

        # Dictionary of Existence
        fileExists = {"CV": cvExists, "Transcript": transcriptExists,
            "Letters": letterExists}

        # Make Cover Page
        completed = MakeCoverPage(app, fileExists)

        # Get Cover Page
        cover = GetPdf("{}_cover.pdf".format(app["AppID"]))

        # Add pages to PDF (with header and watermark, if appropriate)
        appPdf = PdfFileWriter()
        pages = AddHeader(cover.pages, app)
        pages = AddSection(pages, "Cover Page")
        if not completed:
            pages = AddWatermark(pages)
        for page in pages:
            appPdf.addPage(page)

        for section, doc in docs.items():
            pages = AddHeader(doc.pages, app)
            pages = AddSection(pages, section)
            if not completed:
                pages = AddWatermark(pages)
            for page in pages:
                appPdf.addPage(page)

        # Write PDF
        appStream = open("../{}_Applications/{}_{}.pdf".format(year, app["Last"], 
            app["AppID"]), "wb")
        appPdf.write(appStream)

        # Increase count for display
        appCount += 1

    print("\n--------Post-Processing PDFs--------")

    # Delete temporary files
    print("Deleting Temporary Files...")
    filesToDelete = ["SOI", "cover", "WIP", "Header"]
    for ext in filesToDelete:
        for file in glob("*_{}.pdf".format(ext)):
            os.remove(file)

    os.remove("Cover Page.pdf")
    os.remove("Statement of Interest.pdf")
    os.remove("CV or Resume.pdf")
    os.remove("(Unofficial) Transcript.pdf")
    os.remove("Recommendation Letter #1.pdf")
    os.remove("Recommendation Letter #2.pdf")
    os.remove("Recommendation Letter #3.pdf")
    os.remove("Recommendation Letter #4.pdf")

    # Create applicant CSV file
    print("Creating Applicant CSV File...")
    with open("../{}_Applications/{} Applicants.csv".format(year, year), "w") as appCsv:
        csvHeader = ["AppID", "First", "Last", "Email"]
        writer = csv.DictWriter(appCsv, fieldnames=csvHeader, restval="ERROR", 
            extrasaction="ignore")
        writer.writeheader()
        for app in apps:
            writer.writerow(app)



    print("\n--------Uploading files to Google Drive--------")

    # Authenticate Google Drive
    gauth = GoogleAuth()

    # Create local webserver and auto-handle authentication.
    gauth.LocalWebserverAuth()

    # Create GoogleDrive instance with authenticated GoogleAuth instance.
    drive = GoogleDrive(gauth)

    # Delete all old application files
    file_list = drive.ListFile({'q': "'{}' in parents and trashed=false".format(GDriveDestID)}).GetList()
    for file in file_list:
        if ("R_" in file["title"] and ".pdf" in file["title"]) or ".csv" in file["title"]:
            file.Delete()

    # Upload files to Google Drive
    appCount = 1
    print("\n\n--------Starting Drive Upload--------")
    for app in apps:
        print("Uploading {} of {}...".format(appCount, len(apps)))
        file = drive.CreateFile({"parents": [{"kind": "drive#fileLink", 
            "id": "{}".format(GDriveDestID)}], 
            "title":"{}: {}.pdf".format(app["Last"], app["AppID"])})

        # Read file and set it as a content of this instance.
        file.SetContentFile("../{}_Applications/{}_{}.pdf".format(year,
            app["Last"], app["AppID"]))
        file.Upload() # Upload the file.
        appCount += 1

    file = drive.CreateFile({"parents": [{"kind": "drive#fileLink", 
        "id": "{}".format(GDriveDestID)}], 
        "title":"{} Applicants.csv".format(year)})
    file.SetContentFile("../{}_Applications/{} Applicants.csv".format(year, year))
    file.Upload()



    print("\n--------Success! All Done.--------")



#Helper Functions

def ImportRegistrationData():
    """Imports registration data from csv file. Assumes file is located in same 
    directory as the script."""

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

def ImportApplicationData():
    """Imports application data from csv file (leaving out blank applications).
    Assumes file is located in same directory as the script. NOTE: This only
    imports the data, and not any files."""

    #Create headers for application data
    appHeader = ["AppID", "ResponseSet", "BlankName", "ExternalDataReference",
        "BlankEmail", "IPAddress", "Status", "StartDate", "EndDate", "Finished",
        "First", "Last", "Email", "SOI", "TranscriptURL", "cvURL", "Lat",
        "Long", "LocAcc", "Blank"]
    appJunk = ["BlankEmail"]

    # Read in Application Data
    apps = readQualtricsCSV("../Summer_Course_2017_Application.csv", appHeader,
        appJunk)

    # Remove blank responses from apps
    return [x for x in apps if x["Email"] != '']

def ImportRecommendationData():
    """Imports recommendation data from csv file. Assumes file is located in 
    same directory as the script. NOTE: This only imports the data, and not any
    files."""

    # Create headers for recommendation data
    recHeader = ["recID", "ResponseSet", "BlankName", "ExternalDataReference", 
        "Email", "IPAddress", "Status", "StartDate", "EndDate", "Finished", 
        "AppFirst", "AppLast", "AppEmail", "Intro", "recURL", "Lat", "Long", 
        "LocAcc", "Blank"]
    recJunk = ["Intro", "recURL"]

    # Read in Recommendation Data
    return readQualtricsCSV("../Summer_Course_Recommendations.csv", recHeader, 
        recJunk)

def ImportDemographicData():
    """Imports demographic data from csv file. Assumes file is located in same 
    directory as the script."""

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


def MakeCoverPage(app, fileExists):
    """Makes the cover page of the application, which includes basic information
    about the applicant (including demographic info), their recommender's
    information, and the status of their application (complete v. incomplete).
    Cover page is saved as appID_cover.pdf."""
    #Create PDF

    cover = SimpleDocTemplate("{}_cover.pdf".format(app["AppID"]), 
        pagesize=letter, topMargin=108, rightMargin=72, leftMargin=72,
        bottomMargin=72)

    # Compile text to print on PDF
    text = [
        Paragraph("Basic Information", styles["heading1"]),
        Paragraph("<b>Name:</b> {} {}".format(app["First"], app["Last"]), 
            styles["normal"]),
        Paragraph("<b>Email:</b> {}".format(app["Email"]), styles["normal"]),
        Paragraph("Demographic Information", styles["heading1"])]

    # Add demographic info
    if "demID" not in app.keys():
        text.append(Paragraph("Applicant did not complete optional" + 
            " demographic supplement.", styles["normal"]))
        for _ in range(0, 2):
            text.append(Paragraph("", styles["normal"]))
    else:
        # Hispanic or Latino Information
        hispanic = ""
        if app["Hispanic"] == "2":
            hispanic = "No"
        elif app["Hispanic"] == "1":
                hispanic = "Yes"
        elif not hispanic:
            hispanic = "No answer"
        text.append(Paragraph("<b>Are you Hispanic or Latino?</b> {}".format(hispanic),
            styles["normal"]))

        #Race/Ethnicity
        race = ""
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
        text.append(Paragraph("<b>Race or Ethnicity:</b> {}".format(race),
            styles["normal"]))

        # Gender
        gender = ""
        if app["Gender"] == "1":
            gender = "Male"
        elif app["Gender"] == "2":
            gender = "Female"
        elif gender:
            gender = "No answer"
        text.append(Paragraph("<b>Gender:</b> {}".format(gender),
            styles["normal"]))

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
        text.append(Paragraph("<b>Education:</b> {}".format(ed),
            styles["normal"]))

    # Counter to track number of recommendations submitted
    recsSubmitted = 0

    #Print recommender info
    text.append(Paragraph("Recommender Information", styles["heading1"]))
    for i in range(1, 5):
        if "Rec{}Email".format(i) in app.keys():
            if app["Rec{}Email".format(i)]:
                text.append(Paragraph("Recommender #" + str(i), styles["heading2"]))
                text.append(Paragraph("<b>Name:</b> {} {}".format(app["Rec" + 
                    str(i) + "First"], app["Rec" + str(i) + "Last"]), 
                    styles["normal"])),
                text.append(Paragraph("<b>Email:</b> {}".format(app["Rec" + 
                    str(i) + "Email"]), styles["normal"]))

                # Check whether letter was submitted
                if fileExists["Letters"][i]:
                    recSubmit = "YES"
                    recsSubmitted += 1
                else:
                    recSubmit = "NO (Check Recommendation Letters folder in case of error)"
                text.append(Paragraph("<b>Recommendation Submitted?</b> {}".format(recSubmit),
                    styles["normal"]))
        else:
            break

    # If application is incomplete, print that
    completed = True
    if recsSubmitted < 2 or not fileExists["CV"] or not fileExists["Transcript"]:
        text.append(Paragraph("", styles["heading1"]))
        text.append(Paragraph("APPLICATION INCOMPLETE", styles["title"]))
        completed = False

        #State reasons why application is incomplete
        if recsSubmitted < 2:
            text.append(Paragraph("Reason: Less than 2 recommendation letters",
                styles["title"]))
        if not fileExists["CV"]:
            text.append(Paragraph("Reason: No CV (check CV folder in case of error)",
                styles["title"]))
        if not fileExists["Transcript"]:
            text.append(Paragraph("Reason: No Transcript (check Transcript folder in case of error)",
                styles["title"]))

    #Make template
    def CoverTemplate(canvas, doc): CoverPage(app, canvas, doc)

    # Make PDF with pre-defined page templates.
    cover.build(text, onFirstPage=CoverTemplate)

    return completed

def MakeSoiPdf(app):
    """Creates the applicant's statement of interest (SOI), as a pdf, with a 
    headercontaining the applicant's ID, and a title that states how long the 
    SOI is. Saves it in the application folder, named appID_SOI"""

    # Create PDF
    pdf = SimpleDocTemplate("{}_SOI.pdf".format(app["AppID"]), 
        pagesize=letter, topMargin=108, rightMargin=72, leftMargin=72, 
        bottomMargin=72)

    # Holder for text to go in PDF
    text = []

    # Split SOI along line breaks and add to text
    soi = app["SOI"].split(" / ")
    for para in soi:
        text.append(Paragraph(para, styles["soi"]))

    # Save PDF, using the SoiCanvasMaker class
    pdf.build(text, canvasmaker=SoiCanvasMaker)


# Run everything!
if __name__ == "__main__":
    main()


