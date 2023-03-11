import PyPDF2
import re
import csv

# extracting_text.py
from PyPDF2 import PdfFileReader

def process_total(line):
    dollar_index = line.find("$")
    if dollar_index != -1:
        end_index = line.find(" ", dollar_index)
        amount = line[dollar_index + 1:end_index]
    return amount

def process_page(page_data, page_count):
    lines = page_data.split('\n')
    invoice = ''
    total = ''
    customer = ''
    po = ''
    for i in range(len(lines)):
        if "DUEPO" in lines[i] or "JOB#" in lines[i]:
            invoice = lines[i+1].split()[0]
        elif "PHONE PHONE" in lines[i]:
            total = process_total(lines[i-1])
        elif "TALPAYMENT" in lines[i]:
            customer = lines[i-2]
            po = re.sub(r'\d{1,2}/\d{1,2}/\d{4}', '', lines[i-3])
    return [page_count, customer, po, invoice, total]

def text_extractor(pathPdf, pathCsv):
    with open(pathPdf, 'rb') as pdf:
        with open(pathCsv, mode='w') as csv_file:
            pdf_reader = PyPDF2.PdfReader(pdf)
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['PAGE', 'CUSTOMER', 'PO', 'INVOICE',  'TOTAL'])
            pages = len(pdf_reader.pages)
            for page_count in range(pages):
                page = pdf_reader.pages[page_count]
                page_data = page.extract_text()
                data = process_page(page_data, page_count+1)
                csv_writer.writerow(data) 
                percent = int((page_count / pages) * 100)
                with open('P{}.txt'.format(page_count+1), 'w') as f:
                    f.write(page_data)
                print('\r{}%'.format(percent), end='')

    return 'Done.'

# Example usage
 
pdf_text = text_extractor('CLEAN.pdf', 'CLEAN.csv')
print('\r100%\ndone')