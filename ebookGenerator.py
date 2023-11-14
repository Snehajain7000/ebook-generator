print("Ebook Generator Backend Code Starting")
from pathlib import Path

from borb.pdf import Document
from borb.pdf import Page
from borb.pdf import SingleColumnLayout
from borb.pdf import Paragraph
from borb.pdf import Image
from borb.pdf import PDF
from borb.pdf import OrderedList
from borb.pdf import UnorderedList
from borb.pdf.canvas.font.font import Font
from borb.pdf.canvas.layout.table.flexible_column_width_table import FlexibleColumnWidthTable
from borb.pdf import HexColor
from decimal import Decimal
from pathlib import Path
from borb.pdf import Alignment
from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont
import aspose.words as aw

import random
import coverImageGenerator

from borb.pdf.canvas.line_art.line_art_factory import LineArtFactory
from borb.pdf.canvas.geometry.rectangle import Rectangle
from borb.pdf import ConnectedShape
from borb.pdf.page.page_size import PageSize
import typing

from borb.pdf.canvas.layout.image.barcode import Barcode, BarcodeType  
from borb.pdf.canvas.layout.layout_element import LayoutElement
# Starting the Server  
import os
import time

def startServer() :
    path_to_watch = "inputFolder/"
    fileName = ''
    print('Your folder path is"',path_to_watch,'"')
    before = dict ([(f, None) for f in os.listdir (path_to_watch)])
    while 1:
            after = dict ([(f, None) for f in os.listdir (path_to_watch)])
            added = [f for f in after if not f in before]
            if added:
                    print("Added: ", ", ".join (added))
                    fileName = added
                    break
            else:
                before = after

    #if New file is added, extracting information 
    filePath = "inputFolder/" + fileName[0]
    isExist = os.path.exists(filePath)
    print(isExist)
    f = open(filePath, 'r')
    text = f.read() 
    f.close() 
    print(text)
    return (text)




# Code to generate a QR code LayoutElement
qr_code: LayoutElement = Barcode(
    data="https://vitbhopal.ac.in/",
    width=Decimal(64),
    height=Decimal(64),
    type=BarcodeType.QR,
)

"""
This method will add a blue/purple artwork of lines 
and squares to the bottom right corner
of the given Page
"""
def add_colored_artwork_bottom_right_corner(page: Page) -> None:
    
    ps: typing.Tuple[Decimal, Decimal] = [468, 640]
    
    # Square
    ConnectedShape(
      points=[
          (ps[0] - 32, 40),
          (ps[0], 40),
          (ps[0], 40 + 32),
          (ps[0] - 32, 40 + 32),
      ],
      stroke_color=HexColor("d53067"),
      fill_color=HexColor("d53067"),
    ).paint(page, Rectangle(ps[0] - 32, 40, 32, 32))
    
    # Square
    ConnectedShape(
      points=[
          (ps[0] - 64, 40),
          (ps[0] - 32, 40),
          (ps[0] - 32, 40 + 32),
          (ps[0] - 64, 40 + 32),
      ],
      stroke_color=HexColor("eb3f79"),
      fill_color=HexColor("eb3f79"),
    ).paint(page, Rectangle(ps[0] - 64, 40, 32, 32))
    
    # Triangle
    ConnectedShape(
      points=[
          (ps[0] - 96, 40),
          (ps[0] - 64, 40),
          (ps[0] - 64, 40 + 32),
      ],
      stroke_color=HexColor("e01b84"),
      fill_color=HexColor("e01b84"),
    ).paint(page, Rectangle(ps[0] - 96, 40, 32, 32))
        
    # Line
    r: Rectangle = Rectangle(Decimal(0), Decimal(32), ps[0], Decimal(8))
    ConnectedShape(
      points=LineArtFactory.rectangle(r),
      stroke_color=HexColor("283592"),
      fill_color=HexColor("283592"),
    ).paint(page, r)

"""
This method will add a gray artwork of squares and triangles in the upper right corner
of the given Page
"""
def add_gray_artwork_to_upper_right_corner(page: Page) -> None:

    # define a list of gray colors
    grays: typing.List[HexColor] = [
        HexColor("A9A9A9"),
        HexColor("D3D3D3"),
        HexColor("DCDCDC"),
        HexColor("E0E0E0"),
        HexColor("E8E8E8"),
        HexColor("F0F0F0"),
    ]

    # we're going to use the size of the page later on,
    # so perhaps it's a good idea to retrieve it now
    ps: typing.Tuple[Decimal, Decimal] = [468, 640]

    # now we'll write N triangles in the upper right corner
    # we'll later fill the remaining space with squares
    N: int = 4
    M: Decimal = Decimal(32)
    for i in range(0, N):
        x: Decimal = ps[0] - N * M + i * M
        y: Decimal = ps[1] - (i + 1) * M
        rg: HexColor = random.choice(grays)
        ConnectedShape(
            points=[(x + M, y), (x + M, y + M), (x, y + M)],
            stroke_color=rg,
            fill_color=rg,
        ).paint(page, Rectangle(x, y, M, M))

    # now we can fill up the remaining space with squares
    for i in range(0, N - 1):
        for j in range(0, N - 1):
            if j > i:
                continue
            x: Decimal = ps[0] - (N - 1) * M + i * M
            y: Decimal = ps[1] - (j + 1) * M
            rg: HexColor = random.choice(grays)
            ConnectedShape(
                points=[(x, y), (x + M, y), (x + M, y + M), (x, y + M)],
                stroke_color=rg,
                fill_color=rg,
            ).paint(page, Rectangle(x, y, M, M))

def add_chapter(page: Page, str, num, content = '') -> None:

    chapterLayout = SingleColumnLayout(page)
    add_gray_artwork_to_upper_right_corner(page)
    add_colored_artwork_bottom_right_corner(page)
    if(num == 1):
        chapterLayout.add(Paragraph(str, font_size=20, font="Courier-oblique", font_color=HexColor('#00008B')))
        chapterLayout.add(Paragraph(content, font_size=16, font_color=HexColor('#FF0000'),respect_newlines_in_text=True, font="Courier"))
        chapterLayout.add(Image(
            Path("distrust2.png"),
            width=100,
            height=100,
            horizontal_alignment=Alignment.CENTERED,
            vertical_alignment=Alignment.BOTTOM,
            border_radius_bottom_left=5))
    elif(num == 2):
        chapterLayout.add(Paragraph(str, font_size=20, font="Courier-oblique", font_color=HexColor('#00008B')))
        chapterLayout.add(Paragraph(content, font_size=12, font_color=HexColor('#FF0000'),respect_newlines_in_text=True, font="Courier"))
        chapterLayout.add(Image(
            Path("img2a.png"),
            width=100,
            height=100,
            horizontal_alignment=Alignment.CENTERED,
            vertical_alignment=Alignment.BOTTOM,
            border_radius_bottom_left=5))
    elif(num ==3):
        chapterLayout.add(Paragraph(str, font_size=20, font="Courier-oblique", font_color=HexColor('#00008B')))
        chapterLayout.add(Paragraph(content, font_size=16, font_color=HexColor('#FF0000'),respect_newlines_in_text=True, font="Courier"))
        chapterLayout.add(Image(
            Path("img4a.png"),
            width=100,
            height=100,
            horizontal_alignment=Alignment.CENTERED,
            vertical_alignment=Alignment.BOTTOM,
            border_radius_bottom_left=5))
    elif(num ==4):
        chapterLayout.add(Paragraph(str, font_size=20, font="Courier-oblique", font_color=HexColor('#00008B')))
        chapterLayout.add(Paragraph(content, font_size=18, font_color=HexColor('#FF0000'),respect_newlines_in_text=True, font="Courier"))
        chapterLayout.add(Image(
            Path("img7a.png"),
            width=100,
            height=100,
            horizontal_alignment=Alignment.CENTERED,
            vertical_alignment=Alignment.BOTTOM,
            border_radius_bottom_left=5))
    elif(num ==5):
        chapterLayout.add(Paragraph(str, font_size=20, font="Courier-oblique", font_color=HexColor('#00008B')))
        chapterLayout.add(Paragraph(content, font_size=16, font_color=HexColor('#FF0000'),respect_newlines_in_text=True, font="Courier"))
        chapterLayout.add(Image(
            Path("img6a.png"),
            width=100,
            height=100,
            horizontal_alignment=Alignment.CENTERED,
            vertical_alignment=Alignment.BOTTOM,
            border_radius_bottom_left=5))
    elif(num ==6):
        chapterLayout.add(Paragraph(str, font_size=20, font="Courier-oblique", font_color=HexColor('#00008B')))
        chapterLayout.add(Paragraph(content, font_size=16, font_color=HexColor('#FF0000'),respect_newlines_in_text=True, font="Courier"))
        chapterLayout.add(Image(
            Path("img8a.png"),
            width=100,
            height=100,
            horizontal_alignment=Alignment.CENTERED,
            vertical_alignment=Alignment.BOTTOM,
            border_radius_bottom_left=5))
    elif(num ==7):
        chapterLayout.add(Paragraph(str, font_size=20, font="Courier-oblique", font_color=HexColor('#00008B')))
        chapterLayout.add(Paragraph(content, font_size=16, font_color=HexColor('#FF0000'),respect_newlines_in_text=True, font="Courier"))
        chapterLayout.add(Image(
            Path("img9a.png"),
            width=100,
            height=100,
            horizontal_alignment=Alignment.CENTERED,
            vertical_alignment=Alignment.BOTTOM,
            border_radius_bottom_left=5))
    elif(num ==8):
        chapterLayout.add(Paragraph(str, font_size=20, font="Courier-oblique", font_color=HexColor('#00008B')))
        chapterLayout.add(Paragraph(content, font_size=16, font_color=HexColor('#FF0000'),respect_newlines_in_text=True, font="Courier"))
        chapterLayout.add(Image(
            Path("img10a.png"),
            width=100,
            height=100,
            horizontal_alignment=Alignment.CENTERED,
            vertical_alignment=Alignment.BOTTOM,
            border_radius_bottom_left=5))
        
#Code to Create Cover Page of the Book
def add_cover_page(pdf: Document, title, author, font_size, font_size_author, theme='Horror') -> None:
    coverImage = coverImageGenerator.random('As I Lay Dying', 'William Faulkner')
    #templates = ['Blocks','Column','Cross','Gradient', 'Ornate Border 1 Dark', 'Ornate Border 1', 'Ornate Border 2 Dark', 'Ornate Border 2', 'Ornate Corners 1', 'Ornate Corners 2','Ornate Corners 3', 'Ornate Corners 4', 'Ornate Title 1 Dark', 'Ornate Title 1', 'Rings','Simple Dark','Simple', 'Tiles','Window']
    #template = random.choice(templates)
    template = theme
    # generate specific cover and write it to a file
    with open('coverImage.svg', 'w') as stream:
        stream.write(coverImageGenerator.cover(
            title=title,
            author=author,
            template=template,
            colors=['#d3dcf2', '#b0c0e8', '#6692c3', '#4878a4', '#00305a', '#cc33ff'],
            font='BelieveIt-DvLE.ttf',
            font_size=font_size,  # Used for the title of the book.
            font_size_author=font_size_author  # Used for the authors.
            ))

    # SVG file's path
    fileName = "coverImage.svg"

    # create a document
    doc = aw.Document()

    # create a document builder and initialize it with document object
    builder = aw.DocumentBuilder(doc)

    # insert SVG image to document
    shape = builder.insert_image(fileName)

    # OPTIONAL
    # Calculate the maximum width and height and update page settings 
    # to crop the document to fit the size of the pictures.
    pageSetup = builder.page_setup
    pageSetup.page_width = shape.width
    pageSetup.page_height = shape.height
    pageSetup.top_margin = 0
    pageSetup.left_margin = 0
    pageSetup.bottom_margin = 0
    pageSetup.right_margin = 0

    # save as PNG
    doc.save("svg-to-png.pdf")

    with open("svg-to-png.pdf", "rb") as pdf_file_handle:
        input_pdf_001 = PDF.loads(pdf_file_handle)

    pdf.add_document(input_pdf_001)

    #Code for Cover Page Ends Here

def main():

    # start the server to talk with the UI
    text = startServer()
    x = text.split(";")
    titleName = x[0]
    authorName = x[1]
    theme = x[2]
    chapterCount = int(x[3])
    chapter1Info = x[4]
    chapter2Info = x[5]
    chapter3Info = x[6]
    chapter4Info = x[7]
    
    ch1pt = chapter1Info.split(":")
    ch1pt1title = ch1pt[2]
    ch1pt1content = ch1pt[3]
    ch1pt2title = ch1pt[4]
    ch1pt2content = ch1pt[5]
    ch1pt3title = ch1pt[6]
    ch1pt3content = ch1pt[7]

    ch2pt = chapter2Info.split(":")
    ch2pt1title = ch2pt[2]
    ch2pt1content = ch2pt[3]
    ch2pt2title = ch2pt[4]
    ch2pt2content = ch2pt[5]
    ch2pt3title = ch2pt[6]
    ch2pt3content = ch2pt[7]

    ch3pt = chapter3Info.split(":")
    ch3pt1title = ch3pt[2]
    ch3pt1content = ch3pt[3]
    ch3pt2title = ch3pt[4]
    ch3pt2content = ch3pt[5]
    ch3pt3title = ch3pt[6]
    ch3pt3content = ch3pt[7]

    ch4pt = chapter4Info.split(":")
    ch4pt1title = ch4pt[2]
    ch4pt1content = ch4pt[3]
    ch4pt2title = ch4pt[4]
    ch4pt2content = ch4pt[5]
    ch4pt3title = ch4pt[6]
    ch4pt3content = ch4pt[7]

    
    # Read Info from UI ends



    print(titleName)
    print(authorName)
    # create an empty Document
    pdf = Document()

    # add cover page
    title=titleName,
    author=authorName,
    add_cover_page(pdf, title, author, 110, 85, theme)

    print("Wait Now")



    # add Preaface Page
    preface_page = Page(width=468, height=640)
    pdf.add_page(preface_page)
    add_gray_artwork_to_upper_right_corner(preface_page)
    add_colored_artwork_bottom_right_corner(preface_page)
    # use a PageLayout (SingleColumnLayout in this case)
    layout = SingleColumnLayout(preface_page)

    # add a Paragraph object
    layout.add(Paragraph("Preface", font_size=24, font_color=HexColor('#00008B')))
    layout.add(Paragraph("""I realize that this book will create a great deal of controversy. It has never been easy to convinve the public that a enginner can do anything. 
                    
This Book contains ten poems which were written after midnight by an enginner, Author is now working as SDE at MNC firm and he wrote these poems when he was in college.
                         
These Poems are dedicated to most imporatant parts of author's life where he encountered feelings of Losing, Healing, Learning, Winning and Grateful.
""", font_size=16, padding_right=9,respect_newlines_in_text=True, respect_spaces_in_text=True))
    
    layout.add(
    FlexibleColumnWidthTable(number_of_columns=2, number_of_rows=1)
    .add(qr_code)
    .add(
        Paragraph(
            """
            VIT Academic Block
            VIT Bhopal, Aastha
            Madhya Pradesh, India
            """,
            padding_top=Decimal(4),
            respect_newlines_in_text=True,
            font_color=HexColor("#666666"),
            font_size=Decimal(10),
        )
    )
    .no_borders(),
)

    #Preface Page Code Ends Here




    #add table of content page
    toc_page = Page(width=468, height=640)
    pdf.add_page(toc_page)

    layout1 = SingleColumnLayout(toc_page)
    add_gray_artwork_to_upper_right_corner(toc_page)
    add_colored_artwork_bottom_right_corner(toc_page)
    layout1.add(Paragraph("Table of Contents",  font_size=24, font_color=HexColor('#00008B')))
    layout1.add(
            UnorderedList()
            .add(Paragraph("Losing                       (4-6)", font_size=16, font="Courier-oblique", respect_newlines_in_text=True, respect_spaces_in_text=True))
            .add(Paragraph("Healing                      (7-8)", font_size=16, font="Courier-oblique", respect_spaces_in_text=True))
            .add(Paragraph("Learning                     (9)", font_size=16, font="Courier-oblique", respect_spaces_in_text=True))
            .add(Paragraph("Winning                      (10-11)", font_size=16, font="Courier-oblique", respect_spaces_in_text=True))
        )

    #table of content ends here

    #add chapter 1
    if(ch1pt1content):
        chapter_1_page_1 = Page(width=468, height=640)
        add_chapter(chapter_1_page_1, ch1pt1title, 1, ch1pt1content)
        pdf.add_page(chapter_1_page_1)
    if(ch1pt2content):
        chapter_1_page_2 = Page(width=468, height=640)
        add_chapter(chapter_1_page_2, ch1pt2title, 2, ch1pt2content)
        pdf.add_page(chapter_1_page_2)
    if(ch1pt3content):
        chapter_1_page_3 = Page(width=468, height=640)
        add_chapter(chapter_1_page_3, ch1pt3title, 3, ch1pt3content)
        pdf.add_page(chapter_1_page_3)

    #add chapter 2

    if(ch2pt1content):
        chapter_2_page_1 = Page(width=468, height=640)
        add_chapter(chapter_2_page_1, ch2pt1title, 4, ch2pt1content)
        pdf.add_page(chapter_2_page_1)
    if(ch2pt2content):
        chapter_2_page_2 = Page(width=468, height=640)
        add_chapter(chapter_2_page_2, ch2pt2title, 5, ch2pt2content)
        pdf.add_page(chapter_2_page_2)
    if(ch2pt3content):
        chapter_2_page_3 = Page(width=468, height=640)
        add_chapter(chapter_2_page_3, ch2pt3title, 5, ch2pt3content)
        pdf.add_page(chapter_2_page_3)

    # chapter 2 ends here

    #add chapter 3

    if(ch3pt1content):
        chapter_3_page_1 = Page(width=468, height=640)
        add_chapter(chapter_3_page_1, ch3pt1title, 6, ch3pt1content)
        pdf.add_page(chapter_3_page_1)
    if(ch3pt2content):
        chapter_3_page_2 = Page(width=468, height=640)
        add_chapter(chapter_3_page_2, ch3pt2title, 6, ch3pt2content)
        pdf.add_page(chapter_3_page_2)
    if(ch3pt3content):
        chapter_3_page_3 = Page(width=468, height=640)
        add_chapter(chapter_3_page_3, ch3pt3title, 6, ch3pt3content)
        pdf.add_page(chapter_3_page_3)

    # chapter 3 ends here

    #add chapter 4

    if(ch4pt1content):
        chapter_4_page_1 = Page(width=468, height=640)
        add_chapter(chapter_4_page_1, ch4pt1title, 7, ch4pt1content)
        pdf.add_page(chapter_4_page_1)
    if(ch4pt2content):
        chapter_4_page_2 = Page(width=468, height=640)
        add_chapter(chapter_4_page_2, ch4pt2title, 8, ch4pt2content)
        pdf.add_page(chapter_4_page_2)
    if(ch4pt3content):
        chapter_4_page_3 = Page(width=468, height=640)
        add_chapter(chapter_4_page_3, ch4pt3title, 8, ch4pt3content)
        pdf.add_page(chapter_4_page_3)

    # chapter 4 ends here

    #add_back_cover

    title1='eBook Created using Notes2Book Tool',
    author1='Live, Love and Laugh',
    add_cover_page(pdf, title1, author1, 65, 45, theme)
        
    # store the PDF
    with open(Path("output.pdf"), "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, pdf)

if __name__ == "__main__":
    main()