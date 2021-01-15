'''
Author: Aiden Chang, Duc Nguyen
Winter 2021, cs257
Code will contain arg parse commands. See usage.txt for details.
'''
import argparse, csv

filename = "books.csv" 

#Output a list of books based on the category
def findBooks(filename, category, firstArgument = None, secondArgument = None):
    bookList = [] #output list
    with open(filename, newline = '') as csvfile: #refrenced from python csv module
        reader = csv.reader(csvfile, delimiter= ',')
        if category == "title":  
            #search by title  
            for row in reader:
                if firstArgument in row[0]:
                    bookList.append(row[0])
            
        elif category == "year": 
            #search by year   
            for row in reader:
                if firstArgument<= int(row[1]) and secondArgument >= int(row[1]):
                    bookList.append(row[0])
         
        elif category == "author":
            #Search by author
            for row in reader:
                if firstArgument in row[2]:
                    bookList.append("Book by " + row[2] + ": "  + row[0])
        
        elif category == "ms": 
            #multisearch
            dataSet = []
            for row in reader:
                #making a copy of the entire book list
                dataSet.append(row)
            aTitle = input("What is the title of the book? No need for quotation marks. Press enter to skip. Type _exit to cancle the search.")
            if aTitle == "_exit":
                exit()
            if aTitle == '':
                pass
            else:
                for values in dataSet:
                    #eliminates the books that dont contain the title
                    dataSet[:] = [x for x in dataSet if aTitle in x[0]] #inspired from some post in stackoverflow 

            aAuthor = input("What is the author of the book? No need for quotation marks. Press enter to skip. Type _exit to cancle the search.")
            if aAuthor == "_exit":
                exit()
            if aAuthor == '':
                pass
            else:
                for values in dataSet:
                    dataSet[:] = [x for x in dataSet if aAuthor in x[2]]

            aYear = input("Type in the lower range(the earlier year) of the publish year. No need for quotation marks. Press enter to skip. Type _exit to cancle the search.")
            if aYear == "_exit":
                exit()
            if aYear == '':
                pass
            else:
                for values in dataSet:
                    dataSet[:] = [x for x in dataSet if aYear <= x[1]]

            bYear = input("Type in the upper range(the later year) of the publish year. No need for quotation marks. Press enter to skip. Type _exit to cancle the search.")
            if bYear == "_exit":
                exit()
            if bYear == '':
                pass
            else:
                for values in dataSet:
                    dataSet[:] = [x for x in dataSet if bYear >= x[1]]
            if not ((aTitle == '') and (aAuthor == '') and (aYear == '') and (bYear == '')):
                for lists in dataSet:
                    bookList.append(lists[0])

    if len(bookList) == 0:
        bookList.append("Sorry, there are no matches. Please check the spelling, capitalization, and spacing. Type --help for more information.")
    return bookList
    

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
# nargs is the number of arguments needed


args = parser.parse_args()

if args.title: #prints all the books containing the string title
    bookList = findBooks(filename, "title", args.title[0])
elif args.author: #prints all the authors containing the string author and their books
    bookList = findBooks(filename, "author", args.author[0])
elif args.multiSearch:
    bookList = findBooks(filename, "ms" )
elif args.year: #prints all the books between the start publish year and the end publish year
    bookList = findBooks(filename, "year", int(args.year[0]), int(args.year[1]))

for item in bookList:
        print(item)



    















