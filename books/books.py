'''
Author: Aiden Chang, Duc Nguyen
Revised by: Aiden Chang
Winter 2021, cs257
Code will contain arg parse commands. See usage.txt for details.
'''
import argparse, csv, sys


def get_parsed_args():
  parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter) 
  '''for the newline characters RawTextHelpFormatter
  RawTextHelpFormatter inspired by some post in stack overflow'''
  
  parser.add_argument("--title", "-t", help='''
  Example: python3 books.py -t "Mobi"
  Searches for and displays all books containing the string **book title**. The string is case sensitive and all spaces must be included. Must contain quotation marks.
  '''
  , type = str, nargs = 1)
  '''Inspired by pythons argphase module'''

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

  
  parser.add_argument('--file', '-f', default='books.csv', help='the file to search for books')
  '''Get the file of to search in, default is books.csv'''
  args = parser.parse_args()
  return args

def get_books_matching_title(search_str, search_file):
  """
  Get a dictionary of books and their authors based on search string

  Parameters:
    search_str: String to search for(case-sensitive).
    search_file: The file to search in.

  Returns:
    titles_with_authors: A dictionary of books with their authors.
  """
  with open(search_file, newline = '') as csvfile:
    reader = csv.reader(csvfile, delimiter= ',')

    titles_with_authors = {}
    
    for row in reader:
      '''Check if the book's title has search string'''
      if search_str in row[0]:
          titles_with_authors[row[0]] = row[2]
    return titles_with_authors



def print_books_matching_title(search_str, print_file):
  """
  Formatted the print result of the title query

  Parameters:
    search_str: String to search for(case-sensitive).
    print_file: The file to search in.
  """
  print("You search for books with " + search_str + " in its title in " + print_file)
  titles_list = get_books_matching_title(search_str, print_file)
  if len(titles_list) == 0:
    print("Sorry, there are no matches. Please check the spelling, capitalization, and spacing. Type --help for more information.")
  for book in titles_list:
    print(book + " by " + titles_list[book])


def get_books_by_author(search_str, search_file):
  """
  Get a dictionary of books and their authors based on search string

  Parameters:
    search_str: String to search for(case-sensitive).
    search_file: The file to search in.

  Returns:
    authors_with_titles: A dictionary of books with their authors.
  """
  with open(search_file, newline = '') as csvfile:
    reader = csv.reader(csvfile, delimiter= ',') 
    '''inspired from python csv module'''
    authors_with_titles = {}
    for row in reader:
      authors_with_years, title = row[2].split(" ("), row[0]
      authors = [authors_with_years[0]]

      
      if len(authors_with_years) > 2:
        '''There are some books that have 2 authors'''
        second_author = authors_with_years[1].split(' and ')[1]
        authors.append(second_author)
      
      
      for name in authors:
        '''Check if the author's name has search string'''
        if search_str in name:
          if name not in authors_with_titles:
            authors_with_titles[name] = [title]
          else:
            authors_with_titles[name].append(title)
    return authors_with_titles


def print_books_by_author(search_str, print_file):
  """
  Formatted the print result of the author query

  Parameters:
    search_str: String to search for(case-sensitive).
    print_file: The file to search in.
  """
  print("You search for authors with " + search_str + " in their names in"  + print_file)
  authors_list = get_books_by_author(search_str, print_file)
  if len(authors_list) == 0:
    print("Sorry, there are no matches. Please check the spelling, capitalization, and spacing. Type --help for more information.")
  for name in authors_list:
    print(name + " has written:")
    for book in authors_list[name]:
      print("   " + book)


def get_books_by_years(start_year, end_year, search_file):
  """
  Get a dictionary of books and their published based on a range of year

  Parameters:
    start_year: The lower bound of the search range.
    end_year: The upper bound of the search range.
    search_file: The file to search in.

  Returns:
    titles_with_years: A dictionary of books with their publised_year.
  """
  titles_with_years = {}
  with open(search_file, newline = '') as csvfile: 
    '''inspired from python csv module'''
    reader = csv.reader(csvfile, delimiter= ',')
    for row in reader:
      title, published_year = row[0], int(row[1])
      if published_year >= int(start_year) and published_year <= int(end_year):
        titles_with_years[title] = [published_year]
    return titles_with_years


def print_books_by_years(start_year, end_year, print_file):
  """
  Formatted the print result of the published year query

  Parameters:
    start_year: The lower bound of the search range.
    end_year: The upper bound of the search range.
    print_file: The file to search in
  """
  print("You search for books published from " + str(start_year) + " to " + str(end_year) + " in " + print_file)
  year_titles_list = get_books_by_years(start_year, end_year, print_file)
  if len(year_titles_list) == 0:
    print("Sorry, there are no matches. Please check the spelling, capitalization, and spacing. Type --help for more information.")
  for book in year_titles_list:
    print(book, year_titles_list[book])


def get_multi_search(search_file):
  """
  Get a dictionary of books based on multiple characteristic

  Parameters:
    search_file: The file to search in.
  """
  with open(search_file, newline = '') as csvfile:
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
    
    for book in data_set:
      '''Pop the books that does not have search string in its title'''
      data_set[:] = [x for x in data_set if title in x[0]] 
      '''inspired from some post in stackoverflow '''

    author = input("What is the author of the book?\n")
    if author == "_exit":
      sys.exit()
    elif author == '':
      pass
    else:
      '''Pop the books that does not have search string in its author's name'''
      for book in data_set:
        authors_with_years = book[2].split(" (")
        authors = [authors_with_years[0]]
        '''There are some books that have 2 authors'''
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
      '''Pop the books that published earlier than starting year'''
      try:
        for values in data_set:
          data_set[:] = [x for x in data_set if int(start_year) <= int(x[1])] 
      
      except ValueError:
        '''Return error if the input is not integer'''
        print("Wrong input type. This section will be passed")  

    end_year = input("Type in the upper bound of the published year.\n")
    if end_year == "_exit":
      sys.exit()
    elif end_year == '':
      pass

    else:
      '''Pop the books that published later than ending year'''
      try:
        for values in data_set:
          data_set[:] = [x for x in data_set if int(end_year) >= int(x[1])]
          
      except ValueError:
        '''Return error if the input is not integer'''
        print("Wrong input type. This section will be passed")  
    
    
    if ((title == '') and (author == '') and (start_year == '') and (end_year == '')):
      '''Return nothing if the users skip all'''
      data_set = {}
    return data_set


def print_multi_search(print_file):
  """
  Formatted the print result of the multisearch query

  Parameters:
    print_file: The file to search in.
  """
  books_list = get_multi_search(print_file)
  if len(books_list) == 0:
    print("Sorry, there are no matches. Please check the spelling, capitalization, and spacing. Type --help for more information.")
  for book in books_list:
    print(book[0] + " published in " + book[1] + " by " + book[2])

def main():
  parsed_args = get_parsed_args()
  aParser = parsed_args.file

  
  if (parsed_args.title != None and parsed_args.author != None) or \
    (parsed_args.title != None and parsed_args.year != None) or \
      (parsed_args.author != None and parsed_args.year != None):
    '''Warn the user to use the right feature'''
    print("There are too many arguments are being passed. Please use the multisearch feature.")
  
  elif (parsed_args.title != None):
    print_books_matching_title(parsed_args.title[0], aParser)
  elif (parsed_args.author != None):
    print_books_by_author(parsed_args.author[0], aParser)
  elif (parsed_args.year != None):
    if (parsed_args.year[0] > parsed_args.year[1]):
      print("The range of year you enter is not valid")
    else:
      print_books_by_years(parsed_args.year[0], parsed_args.year[1], aParser)
  else:
    print_multi_search(aParser)

if __name__ == '__main__':
	main()
 
'''
single purpose functions
Error messages should go to sys.stderr, not sys.stdout
'''