from PyPDF2 import PdfFileWriter, PdfFileReader
from glob import glob
from tqdm import tqdm

pdf_dirs = glob('samples/*/*/*/*.pdf')
for pdf_dir in tqdm(pdf_dirs):
    inputpdf = PdfFileReader(open(pdf_dir, 'rb'))
    for i in range(inputpdf.numPages):
        p = inputpdf.getPage(i)
        p.scaleBy(3)
        output = PdfFileWriter()
        output.addPage(p)
        out_pdf = pdf_dir.split('.')[0]+'.'+str(i)+'.pdf'
        print(out_pdf)
        with open(out_pdf, 'wb') as outputStream:
            output.write(outputStream)
