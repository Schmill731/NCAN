# export_support.py
#
# By Billy Schmitt
# schmitt@neurotechcenter.org
#
# Last Updated: 12/28/16
#
# Functions to help export QualtricsCSV files to an easy-to-read format.
# Designed to be used with 2017_export_apps.py

#Common junk to all Qualtrics (Legacy) CSV exports
commonJunk = ["ResponseSet", "BlankName", "ExternalDataReference", "BlankEmail",
    "IPAddress", "Status", "StartDate", "EndDate", "Finished",
    "Lat", "Long", "LocAcc", "Blank"]


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

        #Combine with commonJunk with unique junk
        junkHeaders = commonJunk + uniqueJunk

        #Remove junk
        for response in responses:
            for junk in junkHeaders:
                response.pop(junk)

        return responses

def drawLine(canvas, fontSize, field="", answer=""):
    """Draws a line on the PDF of size fontSize (in points), where field is 
    bolded and answer, which follows on the same line, is not. After answer, 
    the program skips to the next line."""

    canvas.setFont("Times-Bold", fontSize)
    canvas.textOut(field)
    canvas.setFont("Times-Roman", fontSize)
    canvas.textLine(answer)
