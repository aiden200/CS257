'''
    api.py
    Aiden Chang, Silas Zhao
    22 Febuary 2021

    API to support covid-19 website
'''
import sys
import flask
import json
import config
import psycopg2 
import datetime
import json

api = flask.Blueprint('api', __name__)

@api.route("/total_cases")
def get_total_cases():
    ''' 
        REQUEST: /total_cases?region_contains={state_keyword}

        GET parameters:
            region_contains(optional, default: USA)

        RESPONSE: a JSON int of the total number of covid cases in America if no optional arguments are specified. 
        If an optional argument is specified, this will return a JSON dictionary with each state containing the 
        state_keyword parameter as a key(string), and the value as the cases for that state.
    '''
    contain_string = flask.request.args.get('region_contains', 'USA')
    connection = connect_to_database()

    user_input = '%' + contain_string + '%'
    
    query = "\
        SELECT DISTINCT cases_and_vaccination_in_US.states, cases_and_vaccination_in_US.cases\
        FROM cases_and_vaccination_in_US\
        WHERE cases_and_vaccination_in_US.state LIKE '%s'\
        ORDER BY cases_and_vaccination_in_US.state;\
        "

    cursor = getCursor(query, connection, user_input)
    return_list = []

    for row in cursor:
        row_dic = {}
        row_dic['region_name'] = row[0]
        row_dic['cases'] = row[1]
        return_list.append(row_dic)
    
    connection.close()

    return json.dumps(return_list)

@api.route("/total_vaccinations")
def get_total_vaccinations():
    ''' 
        REQUEST: /total_vaccinations?region_contains={state_keyword}

        GET parameters: 
            region_contains(optional, default: USA)

        RESPONSE: a JSON int of the total number of vaccination cases in America if no optional arguments are specified. 
        If an optional argument is specified, this will return a JSON dictionary with each state containing the state_keyword 
        parameter as a key(string), and the value as the vaccinations for that state.
    '''
    contain_string = flask.request.args.get('region_contains', 'USA') #The second argument is the default argument
    connection = connect_to_database()

    user_input = '%' + contain_string + '%'
    query = "\
        SELECT DISTINCT cases_and_vaccination_in_US.states, cases_and_vaccination_in_US.vaccination\
        FROM cases_and_vaccination_in_US\
        WHERE cases_and_vaccination_in_US.state LIKE '%s'\
        ORDER BY cases_and_vaccination_in_US.state;\
        "

    cursor = getCursor(query, connection, user_input)
    return_list = []

    for row in cursor:
        row_dic = {}
        row_dic['region_name'] = row[0]
        row_dic['vaccinations'] = row[1]
        return_list.append(row_dic)
    
    connection.close()

    return json.dumps(return_list)

@api.route("/cases_by_date")
def get_cases_by_date():
    '''
        REQUEST: /cases_by_date?[region_name={state},given_date={date}]

        GET parameters:
            region_contains(optional, default:USA)

        RESPONSE: A JSON list of dictionaries, each of which represents a dataset in one day, sorted by date. If no optional arguments are given, 
        the dictionary will contain cases by day for the United States with the following fields. 
            name -- (string) the region name                                                
            cases_dates -- (list) list that contains the date and the case of the date given with the format of each value in the list as date:case
            
        If only the state optional argument is given, the dictionary will contain cases by day for the specified state. The dictionary will have the following fields.
            name -- (string) the region name
            cases_dates -- (list) list that contains the date and the case of the date given with the format of each value in the list as date:case

        If both optional arguments are given, the dictionary will contain the case of the specified date with the following fields.
            name -- (string) the region name
            date -- (string) the requested date
            case -- (int) the cases on the date
    '''
    region_name = flask.request.args.get('region_name', default = 'USA')
    given_date = flask.request.args.get('given_date','0')
    connection = connect_to_database()
    region_name = region_name.lower() # lowercase
    query = ''
    return_list = []
    if given_date == '0': #case 1 and 2
        if region_name == 'USA':
            query = "SELECT DISTINCT cases_date.day, cases_date.cases\
                FROM cases_date\
                WHERE cases_date.states = '%s'\
                ORDER BY cases_date.day;"
        else:
            query = "SELECT DISTINCT cases_date.day, cases_date.cases\
                FROM cases_date\
                WHERE cases_date.states = '%s'\
                ORDER BY cases_date.day;"
        cursor = getCursor(query, connection, region_name)
        in_list = []
        for row in cursor:
            in_list.append(str(row[0]) + ':' + row[1])
        in_dic = {}
        in_dic["name"] = region_name
        in_dic["cases_dates"] = in_list
        return_list.append(in_dic)
        connection.close()
        return json.dumps(return_list)
    else: #case 3
        query = "\
            SELECT DISTINCT cases_date.day, cases_date.cases\
            FROM cases_date\
            WHERE cases_date.states = '%s'\
            AND cases_date.day = '%s'\
            ORDER BY cases_date.day;"
        cursor = getCursor(query, connection, region_name, given_date)
        for row in cursor:
            row_dic = {}
            row_dic['name'] = row[0]
            row_dic['date'] = str(row[1])
            row_dic['case'] = row[2]
            return_list.append(row_dic)
        connection.close()
        return json.dumps(return_list)
    


def connect_to_database():
    '''
    Will establish a connection to the database.
    If an error ocurs, it will be printed out ten the code will exit

    Returns:
        connection: the connection object to the database
    '''
    try:
        connection = psycopg2.connect(database=config.database, user=config.user, password=config.password)
        return connection
    except Exception as e:
        print(e)
        exit()

def getCursor(query, connection, region_search_string = None, date_search_string = None):
    '''
    Query the database, creating a cursor object allowing you to use to iterate over the rows generated by your query.

    Parameters:
        query: the query you would like your cursor to iterate over
        connection: the connection object to your database
        search_string: optional argument. If a search string is specified, the cursor will execute the query with the userinput( the search string)
    Returns:
        cursor: the cursor object that can be used to iterate rows over the specified query
    '''
    try:
        cursor = connection.cursor()
        if region_search_string != None and date_search_string == None:
            cursor.execute(query, (region_search_string,))
        elif region_search_string != None and date_search_string != None:
            cursor.execute(query, (region_search_string,date_search_string,)) # Not 100% confident this is how you put two variables maybe take out the comma?
        else:
            cursor.execute(query)
        return cursor
    except Exception as e:
        print(e)
        exit()

