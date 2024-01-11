from PIL import Image
from pdf2image import convert_from_path
from preview_generator.manager import PreviewManager
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


class thumbnail:
    def __init__(self, filename):
        self.filename = filename

    def generate_thumbnail(self, img, output_file):
        img.thumbnail((640, 480))
        new = Image.new('RGB', (640, 480), (255, 255, 255))
        new.paste(img, ((640 - img.size[0]) // 2, (480 - img.size[1]) // 2))
        new.save(output_file)
        new.show()

    def image(self, output_file):
        img = Image.open(self.filename)
        self.generate_thumbnail(img, output_file)

    def svg(self, output_file):
        drawing = svg2rlg(self.filename)
        renderPM.drawToFile(drawing, output_file, fmt='PNG')
        img = Image.open(output_file)
        self.generate_thumbnail(img, output_file)

    def pdf(self, output_file):
        pages = convert_from_path(self.filename)
        if pages:
            page = pages[0]
        else:
            print("Error with doc format")
        self.generate_thumbnail(page, output_file)

    def docs(self, output_file):
        manager = PreviewManager('media/tmp/', create_folder=True)
        pdf_file_path = manager.get_pdf_preview(self.filename)
        pages = convert_from_path(pdf_file_path)
        if pages:
            page = pages[0]
        else:
            print("Error with doc format")
        self.generate_thumbnail(page, output_file)


filename = input("Enter file path: ")
if filename.endswith('.jpg') or filename.endswith('.png') or \
   filename.endswith('.webp'):
    thumbnail(filename).\
        image("media/"+filename.split('.')[-1]+"_to_thumbnail.jpg")
elif filename.endswith('.svg'):
    thumbnail(filename).\
        svg("media/"+filename.split('.')[-1]+"_to_thumbnail.jpg")
elif filename.endswith('.pdf'):
    thumbnail(filename).\
        pdf("media/"+filename.split('.')[-1]+"_to_thumbnail.jpg")
elif filename.endswith('.odt') or filename.endswith('.ods') or \
 filename.endswith('.odp') or filename.endswith('.docx') or \
 filename.endswith('.pptx') or filename.endswith('.xls') or \
 filename.endswith('.xlsx'):
    thumbnail(filename).\
        docs("media/"+filename.split('.')[-1]+"_to_thumbnail.jpg")
else:
    print("Can't convert thumbnail for "+filename.split('.')[-1]+" filetype.")
