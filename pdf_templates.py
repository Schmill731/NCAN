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

def AppHeader(funct):
    def wrapper(app, canvas, doc):
        #Save state of PDF
        canvas.saveState()

        #Set Running Header of Applicant ID
        canvas.setFont("Times-Roman", 12)
        canvas.drawString(6, 778, "Applicant ID: " + app["AppID"])

        #Add other templates
        funct(app, canvas, doc)

        #Restore the PDF
        canvas.restoreState()

    return wrapper

@AppHeader
def BasicInfoPage(app, canvas, doc):
    #Write basic applicant info
    canvas.setFont("Times-Bold", 18)
    canvas.drawCentredString(306, 702, "Applicant Information")

@AppHeader
def BlankHeader(app, canvas, doc):
    #Just add the header, nothing else
    pass
 
########################################################################
class PageNumCanvas(canvas.Canvas):
    """
    http://code.activestate.com/recipes/546511-page-x-of-y-with-reportlab/
    http://code.activestate.com/recipes/576832/
    """
 
    #----------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """Constructor"""
        canvas.Canvas.__init__(self, *args, **kwargs)
        self.pages = []
 
    #----------------------------------------------------------------------
    def showPage(self):
        """
        On a page break, add information to the list
        """
        self.pages.append(dict(self.__dict__))
        self._startPage()
 
    #----------------------------------------------------------------------
    def save(self):
        """
        Add the page number to each page (page x of y)
        """
        page_count = len(self.pages)

        self.__dict__.update(self.pages[0])
        canvas.Canvas.showPage(self)
 
        for page in self.pages[1:]:
            self.__dict__.update(page)
            self.draw_page_number(page_count)
            canvas.Canvas.showPage(self)
 
        canvas.Canvas.save(self)
 
    #----------------------------------------------------------------------
    def draw_page_number(self, page_count):
        """
        Add the page number
        """
        self.setFont("Times-Bold", 18)
        self.drawCentredString(306, 702, "Statement of Interest: Page {} of {}".format(int(self._pageNumber) - 1, page_count - 1))





