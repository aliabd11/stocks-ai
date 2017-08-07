import csv
import itertools
import random

def generate_region_list(rows):
  print("generating random")
  i = 0
  region_list = ['Canada', 'United States', 'Mexico']
  csv_region_list = []
  while i < rows:
    csv_region_list.append(random.choice(region_list))
    i += 1
  return csv_region_list

def generate_percentage_true(rows, percent): # ex. percent = 0.30, 30% green stocks

  green_rows = [True] * int((rows * percent))
  other_rows = [False] * int((rows * (1 - percent)))

  green_list = green_rows + other_rows
  random.shuffle(green_list)
  return green_list

def generate_industry_sectors(rows, percent):
  i = 0
  sector_list = ['Health', 'Technology', 'Automotive', 'Drugs', 'Alcohol', 'Tobacco', 'Weapons']
  csv_sectors = []
  while i < rows:
    csv_sectors.append(random.choice(sector_list))
    i += 1
  return csv_sectors

def create_stocks_output(file_name):
  with open(file_name) as csvinput, open('output.csv', 'w') as csvoutput:
    writer = csv.writer(csvoutput, lineterminator='\n')
    reader = csv.reader(csvinput)

    reader.next()
    headers = reader.next()
    headers.append('Region List')
    headers.append('Green List')
    headers.append('Industry List')
    writer.writerow(headers)


    region_list = generate_region_list(3075) #input: number of rows in csv file
    green_list = generate_percentage_true(3080, 0.10) #casting as int so increase value to avod rounding errors
    industry_list = generate_industry_sectors(3075, 0.30)

    index = 0
    for row in reader:
      row.append(region_list[index])
      row.append(green_list[index])
      row.append(industry_list[index])
      writer.writerow(row)
      index += 1

    print("Output complete")
  return

def parse_as_dictionary(file_name):
  reader = csv.reader(open(file_name))

  result = {}
  for row in reader:
      key = row[0]
      result[key] = row[1:]
  print(result)

def generate_styles(rows):
  #mutual funds style box #http://www.investopedia.com/articles/basics/06/stylebox.asp
  i = 0
  vertical = ['large', 'medium', 'small']
  horizontal = ['value', 'blend', 'growth']
  styles = list(itertools.product(vertical, horizontal))

  final_style_list = []
  while i < rows:
    final_style_list.append(random.choice(styles))
    i += 1
  return final_style_list

def create_mutual_fund_output(file_name):
  with open(file_name) as csvinput, open('output.csv', 'w') as csvoutput:
    writer = csv.writer(csvoutput, lineterminator='\n')
    reader = csv.reader(csvinput)

    headers = reader.next()
    headers.append('Desired style')
    headers.append('High Management Fees') #True for High Fees, False For No
    writer.writerow(headers)


    style_list = generate_styles(3075) #input: number of rows in csv file
    fees_list = generate_percentage_true(3080, 0.10)

    index = 0
    for row in reader:
      row.append(style_list[index])
      row.append(fees_list[index])
      writer.writerow(row)
      index += 1

  return

'''To use uncomment and run the right method below''' # pls dont do dis
if __name__ == '__main__':
    print(
'''Welcome to research.py!
This program will perform some research on your data to figure out more information
about those companies.
Enter you file name to process: ''')
    # ask for input file name and processs it
# create_stocks_output('exchange.csv') #create output file with desired additional columns
# parse_as_dictionary('output.csv') #convert csv file into dictionary with first entry as key
# create_mutual_fund_output('mutualfunds.csv') #create output file (for mutual funds) with desired additional columns
