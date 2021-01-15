'''
Author: Aiden Chang, Duc Nguyen
Winter 2021, cs257
Code will contain arg parse commands. See usage.txt for details.
'''
import argparse, csv, sys


def get_parsed_args():
  parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter) 
  #for the newline characters RawTextHelpFormatter
  #RawTextHelpFormatter inspired by some post in stack overflow
  
  parser.add_argument("--title", "-t", help='''
  Example: python3 books.py -t "Mobi"
  Searches for and displays all books containing the string **book title**. The string is case sensitive and all spaces must be included. Must contain quotation marks.
  '''
  , type = str, nargs = 1)
  #Inspired by pythons argphase module

  parser.add_argument("--author", "-a", help= '''
  Example: python3 books.py -a "Toni"
  Searches for and displays all authors containing the string **author name**. For each of those authors, every book by them is displayed. The string is case sensitive and all spaces must be included. Must contain quotation marks. 
  '''
  , type = str, nargs = 1)

  parser.add_argument("--multiSearch", "-ms", help = '''
  After the command is typed in, a prompt will appear and ask for the user input. 
  After the first prompt appears, type in the author's name you wish to search. Doing the same for the book title for the second prompt and the starting and ending year for the third prompt. 
  The input is case sensitive, and no need for quotation marks. Typing exit() will allow the user to abort the search and exit at any moment. Typing -0 will allow the user to skip the current prompt. After all three prompts, all the books fitting all three criteria will be displayed.
  ''', action="store_true")

  parser.add_argument("--year", "-y", help = '''
  Example: python3 books.py -y 1890 1900
  Searches for and displays all books published between the **start year** and the **end year** (inclusive). The **start year** must be smaller then the **end year**. 
  ''', type = int, nargs = 2  )

  #Get the file of to search in, default is books.csv
  parser.add_argument('--file', '-f', default='books.csv', help='the file to search for books')

  args = parser.parse_args()
  return args


"""
Get a dictionary of books and their authors based on search string

@param search_str string to search for(case-sensitive)
@param file the file to search in
@return dictionary of books with their authors
"""
def get_titles(search_str, file):
  with open(file, newline = '') as csvfile:
    reader = csv.reader(csvfile, delimiter= ',')

    titles_with_authors = {}
    #Check if the book's title has search string
    for row in reader:
      if search_str in row[0]:
          titles_with_authors[row[0]] = row[2]
    return titles_with_authors


"""
Formatted the print result of the title query
@param search_str string to search for(case-sensitive)
@param file the file to search in
"""
def print_titles(search_str, file):
  print("You search for books with " + search_str + " in its title in " + file)
  titles_list = get_titles(search_str, file)
  if len(titles_list) == 0:
    print("Sorry, there are no matches. Please check the spelling, capitalization, and spacing. Type --help for more information.")
  for book in titles_list:
    print(book + " by " + titles_list[book])

"""
Get a dictionary of books and their authors based on search string

@param search_str string to search for(case-sensitive)
@param file the file to search in
@return dictionary of books with their authors
"""
def get_authors(search_str, file):
  with open(file, newline = '') as csvfile:
    reader = csv.reader(csvfile, delimiter= ',') # inspired from python csv module

    authors_with_titles = {}
    for row in reader:
      authors_with_years, title = row[2].split(" ("), row[0]
      authors = [authors_with_years[0]]

      #There are some books that have 2 authors
      if len(authors_with_years) > 2:
        second_author = authors_with_years[1].split(' and ')[1]
        authors.append(second_author)
      
      #Check if the author's name has search string
      for name in authors:
        if search_str in name:
          if name not in authors_with_titles:
            authors_with_titles[name] = [title]
          else:
            authors_with_titles[name].append(title)
    return authors_with_titles

"""
Formatted the print result of the author query
@param search_str string to search for(case-sensitive)
@param file the file to search in
"""
def print_authors(search_str, file):
  print("You search for authors with " + search_str + " in their names in"  + file)
  authors_list = get_authors(search_str, file)
  if len(authors_list) == 0:
    print("Sorry, there are no matches. Please check the spelling, capitalization, and spacing. Type --help for more information.")
  for name in authors_list:
    print(name + " has written:")
    for book in authors_list[name]:
      print("   " + book)

"""
Get a dictionary of books and their published based on a range of year

@param start_year the lower bound of the search range
@param end_year the upper bound of the search range
@param file the file to search in
@return dictionary of books with their publised_year
"""
def get_published_years(start_year, end_year, file):
  titles_with_years = {}
  with open(file, newline = '') as csvfile: # inspired from python csv module
    reader = csv.reader(csvfile, delimiter= ',')
    for row in reader:
      title, published_year = row[0], int(row[1])
      if published_year >= int(start_year) and published_year <= int(end_year):
        titles_with_years[title] = [published_year]
    return titles_with_years

"""
Formatted the print result of the published year query
@param start_year the lower bound of the search range
@param end_year the upper bound of the search range
@param file the file to search in
"""
def print_published_years(start_year, end_year, file):
  print("You search for books published from " + str(start_year) + " to " + str(end_year) + " in " + file)
  year_titles_list = get_published_years(start_year, end_year, file)
  if len(year_titles_list) == 0:
    print("Sorry, there are no matches. Please check the spelling, capitalization, and spacing. Type --help for more information.")
  for book in year_titles_list:
    print(book, year_titles_list[book])

"""
Get a dictionary of books based on multiple characteristic

@param file the file to search in
"""
def get_multi_search(file):
  with open(file, newline = '') as csvfile:
    reader = csv.reader(csvfile, delimiter= ',')
    data_set = []
    for row in reader:
      data_set.append(row)

    print("This is the multisearch feature. The input does not need quotation marks. You can press Enter to skip a section or type _exit to cancel the whole search")

    title = input("What is the title of the book? \n")
    if title == "_exit":
      sys.exit()
    elif title == '':
      pass
    #Pop the books that does not have search string in its title
    for book in data_set:
      data_set[:] = [x for x in data_set if title in x[0]] #inspired from some post in stackoverflow 

    author = input("What is the author of the book?\n")
    if author == "_exit":
      sys.exit()
    elif author == '':
      pass
    else:
      #Pop the books that does not have search string in its author's name
      for book in data_set:
        authors_with_years = book[2].split(" (")
        authors = [authors_with_years[0]]
        #There are some books that have 2 authors
        if len(authors_with_years) > 2:
          authors.append(authors_with_years[1].split(' and ')[1])

        if author not in author[0]:
          if (len(authors) == 1) or (author not in author[1]):
            data_set.pop(book)

    start_year = input("Type in the lower bound of the published year.\n")
    if start_year == "_exit":
      sys.exit()
    elif start_year == '':
      pass
    else:
      #Pop the books that published earlier than starting year
      try:
        for values in data_set:
          data_set[:] = [x for x in data_set if int(start_year) <= int(x[1])] 
      #Return error if the input is not integer
      except ValueError:
        print("Wrong input type. This section will be passed")  

    end_year = input("Type in the upper bound of the published year.\n")
    if end_year == "_exit":
      sys.exit()
    elif end_year == '':
      pass

    else:
      #Pop the books that published later than ending year
      try:
        for values in data_set:
          data_set[:] = [x for x in data_set if int(end_year) >= int(x[1])]
      #Return error if the input is not integer
      except ValueError:
        print("Wrong input type. This section will be passed")  
    
    #Return nothing if the users skip all
    if ((title == '') and (author == '') and (start_year == '') and (end_year == '')):
      data_set = {}
    return data_set

"""
Formatted the print result of the multisearch query

@param file the file to search in
"""
def print_multi_search(file):
  books_list = get_multi_search(file)
  if len(books_list) == 0:
    print("Sorry, there are no matches. Please check the spelling, capitalization, and spacing. Type --help for more information.")
  for book in books_list:
    print(book[0] + " published in " + book[1] + " by " + book[2])

def main():
  parsed_args = get_parsed_args()
  file = parsed_args.file

  #Warn the user to use the right feature
  if (parsed_args.title != None and parsed_args.author != None) or (parsed_args.title != None and parsed_args.year != None) or (parsed_args.author != None and parsed_args.year != None):
    print("There are too many arguments are being passed. Please use the multisearch feature.")
  
  elif (parsed_args.title != None):
    print_titles(parsed_args.title[0], file)
  elif (parsed_args.author != None):
    print_authors(parsed_args.author[0], file)
  elif (parsed_args.year != None):
    if (parsed_args.year[0] > parsed_args.year[1]):
      print("The range of year you enter is not valid")
    else:
      print_published_years(parsed_args.year[0], parsed_args.year[1], file)
  else:
    print_multi_search(file)

if __name__ == '__main__':
	main()
 
