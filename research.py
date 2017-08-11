import csv
import itertools
import random
import math

def generate_region_list(rows):
  i = 0
  region_list = ['Canada', 'United States', 'Mexico']
  csv_region_list = []
  while i < rows:
    csv_region_list.append(random.choice(region_list))
    i += 1
  return csv_region_list

def generate_percentage_true(rows, percent): # ex. percent = 0.30, 30% green stocks
  green_rows = [True] * int(math.ceil((rows * percent)))
  other_rows = [False] * int(math.ceil((rows * (1 - percent))))

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

def check_row_count(file_name):
  reader = csv.reader(open(file_name))
  row_count = sum(1 for row in reader)
  return row_count

def create_stocks_output(file_name):
  with open(file_name) as csvinput, open('output.csv', 'w') as csvoutput:
    writer = csv.writer(csvoutput, lineterminator='\n')
    reader = csv.reader(csvinput)

    reader.next()
    headers = reader.next()
    headers.append('Region')
    headers.append('Green')
    headers.append('Industry')
    writer.writerow(headers)

    row_count = check_row_count(file_name)

    region_list = generate_region_list(row_count) #input: number of rows in csv file
    green_list = generate_percentage_true(row_count, 0.10) #pick desired percentage
    industry_list = generate_industry_sectors(row_count, 0.30)

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
  print(result['MIND'][15])

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

    row_count = check_row_count(file_name)


    style_list = generate_styles(row_count) #input: number of rows in csv file
    fees_list = generate_percentage_true(row_count, 0.10)

    index = 0
    for row in reader:
      row.append(style_list[index])
      row.append(fees_list[index])
      writer.writerow(row)
      index += 1

  return

if __name__ == '__main__':
    desired_function = input('Enter your desired process (s to create stocks output, d to parse as dictionary, m to create mutual fund output): ')

    options = ["s", "d", "m"]
    while desired_function not in options:
      desired_function = input("Choose one of [%s]:" % ", ".join(options))

    file_name = input('Enter a file name to process: ')

    if (desired_function == 's'):
      create_stocks_output(file_name) # create output file with desired additional columns
    elif (desired_function == 'd'):
      parse_as_dictionary(file_name) # convert csv file into dictionary with first entry as key
    elif (desired_function == 'm'):
      create_mutual_fund_output(file_name) # create output file (for mutual funds) with desired additional columns
