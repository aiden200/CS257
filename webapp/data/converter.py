import csv 
def openfile(filename):
    csvFile =open(filename, "r")
    reader = csv.reader(csvFile)
    return reader

def writefile_cases(reader, case_date):
    #table1:
    csvFile1 = open(case_date, "w")
    case_date_w= csv.writer(csvFile1)
    #check redundancy
    for row in reader:
        if reader.line_num == 1:
            continue
        case_date = []
        for i in range(len(row)):
            if in_case_date(i):
                if row[i] == '':
                    row[i] = 'Null'
                case_date.append(row[i])
        case_date_w.writerow(case_date)
        
def writefile_vaccine(reader, file):
    #table1:
    csvFile1 = open(file, "w")
    case_date_w= csv.writer(csvFile1)

    for row in reader:
        if reader.line_num == 1:
            continue
        case_date = []
        for i in range(len(row)):
            if in_case_vaccine(i):
                if row[i] == 'N/A':
                    row[i] = 'Null'
                case_date.append(row[i])
        case_date_w.writerow(case_date)
def writefile_US(reader, file):
    #table1:
    csvFile1 = open(file, "w")
    case_date_w= csv.writer(csvFile1)

    for row in reader:
        if reader.line_num == 1:
            continue
        case_date = []
        for i in range(len(row)):
            if in_US(i):
                if row[i] == 'N/A':
                    row[i] = 'Null'
                case_date.append(row[i])
        case_date_w.writerow(case_date)

def in_US(index):
    if index <=1 or index == 12 or index == 13:
        return True
    else:
        return False
def in_case_date(index):
    if index <= 1 or index == 19 or index == 21:
        return True
    else:
        return False

def in_case_vaccine(index):
    if index < 1:
        return True
    elif index >=5 and index <=8:
        return True
    else:
        return False

def main():
    reader = openfile("all-states-history.csv")
    writefile_cases(reader,"case_date.csv")
    reader = openfile("national-history.csv")
    writefile_US(reader,"case_state_date.csv")

main()