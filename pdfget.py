import PyPDF2
import re
import csv
import sys
import builtins

# extracting_text.py
from PyPDF2 import PdfFileReader

# Long Island City NY 11105$13.83    <==
# PHONE PHONE
def process_total(line):
    dollar_index = line.find("$")
    if dollar_index != -1:
        end_index = line.find(" ", dollar_index)
        amount = line[dollar_index + 1:end_index]
    return amount

# DUEPO or JOB#
# 1787153 11/15/2022                 <==
def process_invoice(line):
    return line.split()[0]

# 127367                             <==
# CLEAN HARBORS ENVIRONMEN
# TALPAYMENT 
def process_customer(line):
    return line

# 9/16/2022 W221567000               <==
# 127367
# CLEAN HARBORS ENVIRONMEN
# TALPAYMENT 
def process_po(line):
    return re.sub(r'\d{1,2}/\d{1,2}/\d{4}', '', line)


def process_page(page_data, page_count):
    lines = page_data.split('\n')
    invoice = ''
    total = ''
    customer = ''
    po = ''
    for i in range(len(lines)):
        if "DUEPO" in lines[i] and "JOB#" in lines[i]:
            invoice = process_invoice(lines[i+1])
        elif "PHONE PHONE" in lines[i]:
            total = process_total(lines[i-1])
        elif "TALPAYMENT" in lines[i]:
            customer = process_customer(lines[i-2])
            po = process_po(lines[i-3]) 
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

                if builtins.__debug__:
                    print(data)

                csv_writer.writerow(data) 
                percent = int((page_count / pages) * 100)
                with open('c:\\temp\\P{}.txt'.format(page_count+1), 'w') as f:
                    f.write(page_data)
                print('\r{}%'.format(percent), end='')
 #                break

    return 'Done.'

# Example usage
# 'CLEAN.pdf', 'CLEAN.csv'
 
def main(arg1, arg2):
    print("Convert from pdf file:", arg1)
    print("convert to CSV file:", arg2)
    pdf_text = text_extractor(arg1, arg2)
 
    print('\r100%\ndone')

if __name__ == "__main__":
    # Check if the correct number of arguments were provided
    if len(sys.argv) != 3:
        print("Usage: python script.py arg1 arg2")
        sys.exit(1)

    # Get the command line arguments
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]

    # Call the main function with the provided arguments
    main(arg1, arg2)