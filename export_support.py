# export_support.py
#
# By Billy Schmitt
# schmitt@neurotechcenter.org
#
# Last Updated: 12/29/16
#
# Functions to help export QualtricsCSV files to an easy-to-read format.
# Designed to be used with 2017_export_apps.py

#imports
import csv
import os
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.units import inch
from pdf_templates import *
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger

#Common junk to all Qualtrics (Legacy) CSV exports
commonJunk = ["ResponseSet", "BlankName", "ExternalDataReference",
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


watermark = PdfFileReader(open("watermark.pdf", "rb")).getPage(0)
def addWatermark(pages):
    for page in pages:
        page.mergePage(watermark)
    return pages

def addHeader(pages, appID):
    header = PdfFileReader(open("../2017_Applications/{}_Header.pdf".format(appID), "rb")).getPage(0)
    for page in pages:
        page.mergePage(header)
    return pages
