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
from glob import glob
from reportlab.platypus import Paragraph, SimpleDocTemplate, Frame
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

def addComma(str):
    """Adds a comma (and space) to the end of a string if there is something
    already saved in the string (particularly useful for lists)."""
    if str:
       return str + ", "
    else:
        return str

def GetPathway(path):
    """Looks for a pathway matching `path` and returns the filepath to that
    file, if it exists, else None."""
    filePath = glob(path)
    if filePath:
        return filePath[0]
    else:
        return None

def GetPdf(path):
    """Gets a a PDF at the specified path and returns the object (or None if it
    doesn't exist)"""
    pdfPath = GetPathway(path)
    if pdfPath:
        pdf = PdfFileReader(open(pdfPath, "rb"), strict = False)
        return  pdf
    else:
        return None

def MakeHeaderPdf(app):
    """Makes a pdf with just the running header of the application, so it can be
    added to each page later. Saved as appID_Header.pdf."""
    headerPdf = SimpleDocTemplate("{}_Header.pdf".format(app["AppID"]), 
        pagesize=letter)
    def headerTemplate(canvas, doc): Header(app, canvas, doc)

    headerPdf.build([Paragraph("", styles["title"])], onFirstPage=headerTemplate)

watermark = GetPdf("watermark.pdf").getPage(0)
def AddWatermark(pages):
    """Adds a watermark to each page of pages. Pages is expected to a list of 
    page object from PdfFileReader. Watermark is taken from sample file located 
    in same directory as the script."""
    for page in pages:
        page.mergePage(watermark)
    return pages

def AddHeader(pages, app):
    """Adds a header to each page of pages. Pages is expected to a list of 
    page object from PdfFileReader. Header is taken from sample file located in 
    same directory as the script."""
    MakeHeaderPdf(app)
    header = GetPdf("{}_Header.pdf".format(app["AppID"])).getPage(0)
    for page in pages:
        page.mergePage(header)
    return pages
