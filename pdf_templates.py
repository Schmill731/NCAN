# pdf_templates.py
#
# By Billy Schmitt
# schmitt@neurotechcenter.org
#
# Last Updated: 12/29/16
#
# Document and page templates to make the generation of PDFs more standard.

# imports
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import BaseDocTemplate
from reportlab.lib.units import inch
from reportlab.lib.colors import black
from reportlab.lib.enums import TA_LEFT, TA_CENTER

#Create paragraph styles for application

#Normal for most parts of the application
styles = {
    "normal": ParagraphStyle(
        "normal",
            fontName='Times-Roman',
            fontSize=12,
            leading=14,
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            alignment=TA_LEFT,
            spaceBefore=0,
            spaceAfter=0,
            bulletFontName='Times-Roman',
            bulletFontSize=10,
            bulletIndent=0,
            textColor= black,
            backColor=None,
            wordWrap=None,
            borderWidth= 0,
            borderPadding= 0,
            borderColor= None,
            borderRadius= None,
            allowWidows= 1,
            allowOrphans= 0,
            textTransform=None,  
            endDots=None,         
            splitLongWords=1
        ),
}

#Title for title on each page
styles["title"] = ParagraphStyle(
    "title",
    parent=styles["normal"],
    fontName='Times-Bold',
    fontSize=18,
    leading=18,
    alignment=TA_CENTER)

#Heading for each section
styles["heading1"] = ParagraphStyle(
    "heading1",
    fontName='Times-Bold',
    fontSize=14,
    spaceBefore=36,
    leading=16)

styles["heading2"] = ParagraphStyle(
    "heading2",
    parent=styles["normal"],
    fontName="Times-Bold",
    fontSize=12,
    leading=14,
    spaceBefore=14)

styles["soi"] = ParagraphStyle(
    "soi",
    parent=styles["normal"],
    firstLineIndent=36)


# class ApplicantPDF(BaseDocTemplate):
#     """A document template for creating PDFs from applicant responses."""

#     def __init__(self, appID):
#         super().__init__(appID + ".pdf", pagesize=letter, 
#             topMargin=inch/2)

#     def afterInit(self):



