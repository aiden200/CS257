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

@api.route("/total_cases") # always USA?
def get_total_cases():
    ''' 
        REQUEST: /total_cases?region_contains={state_keyword}

        GET parameters:x


            region_contains(optional, default: USA)

        RESPONSE: a JSON int of the total number of covid cases in America if no optional arguments are specified. 
        If an optional argument is specified, this will return a JSON dictionary with each state containing the 
        state_keyword parameter as a key(string), and the value as the cases for that state.
        
        make it case insensitive:
        """
        SELECT DISTINCT states_code.states, cases_date.cases
        FROM cases_date, states_code
        WHERE day = (SELECT MAX(day) FROM cases_date)
        AND UPPER(states_code.states) LIKE UPPER(%s)
        AND states_code.code = cases_date.states;
        """
    '''
    contain_string = flask.request.args.get('region_contains', 'USA')
    connection = connect_to_database()
    
    user_input = '%' + contain_string + '%'
    if contain_string == 'USA':
        query = "SELECT cases\
                FROM cases_in_US\
                WHERE day = (SELECT MAX(day) FROM cases_in_US);"
        cursor = getCursor(query, connection)
        return_str = '' 
        for line in cursor:
            return_str = line[0]
        connection.close()
        return json.dumps(return_str)#WORKS
    else:
        query = "SELECT DISTINCT states_code.states, cases_date.cases\
                FROM cases_date, states_code\
                WHERE day = (SELECT MAX(day) FROM cases_date)\
                AND UPPER(states_code.states) LIKE UPPER(%s) AND states_code.code = cases_date.states;"
        cursor = getCursor(query, connection, user_input)
        return_list = []

        for row in cursor:
            row_dic = {}
            row_dic['region_name'] = row[0]
            row_dic['cases'] = row[1]
            return_list.append(row_dic)
        
        connection.close()

        return json.dumps(return_list)#WORKS

@api.route("/total_cases_and_vaccination") 
def get_total_cases_and_vaccination():
    ''' 
        REQUEST: /total_cases?region_contains={state_keyword}

        GET parameters:x


            region_contains(optional, default: USA)

        RESPONSE: a JSON int of the total number of covid cases in America if no optional arguments are specified. 
        If an optional argument is specified, this will return a JSON dictionary with each state containing the 
        state_keyword parameter as a key(string), and the value as the cases for that state.
        
        make it case insensitive:
        """
        SELECT DISTINCT states_code.states, cases_date.cases
        FROM cases_date, states_code
        WHERE day = (SELECT MAX(day) FROM cases_date)
        AND UPPER(states_code.states) LIKE UPPER(%s)
        AND states_code.code = cases_date.states;
        """
    '''
    connection = connect_to_database() 
    query = "SELECT DISTINCT vaccinations_region.region, vaccinations_region.people_with_1_or_more_doses, cases_date.cases\
            FROM cases_date, vaccinations_region,states_code\
            WHERE UPPER(cases_date.states) = UPPER(states_code.code)\
            AND UPPER(states_code.states) = UPPER(vaccinations_region.region)\
            AND cases_date.day = (SELECT MAX(day) FROM cases_date)\
            ORDER BY cases_date.cases;"
    cursor = getCursor(query, connection)
    return_list = []

    for row in cursor:
        row_dic = {}
        row_dic['region_name'] = row[0]
        row_dic['vaccination'] = row[1]
        row_dic['cases'] = row[2]
        return_list.append(row_dic)
    connection.close()

    return json.dumps(return_list)#WORKS
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
    contain_string = flask.request.args.get('region_contains', 'USA')
    connection = connect_to_database()

    user_input = '%' + contain_string + '%'
    if contain_string == 'USA':
        query = "\
            SELECT DISTINCT vaccinations_region.people_with_1_or_more_doses\
            FROM vaccinations_region;"
        cursor = getCursor(query, connection)
        return_str = '' 
        for line in cursor:
            return_str = line[0]
        connection.close()
        return json.dumps(int(return_str)) #WORKS
        
    else:
        query = "SELECT DISTINCT region, people_with_1_or_more_doses\
        FROM vaccinations_region\
        WHERE UPPER(region) LIKE UPPER(%s);"

        cursor = getCursor(query, connection, user_input)
        return_list = []

        for row in cursor:
            row_dic = {}
            row_dic['region_name'] = row[0]
            row_dic['vaccinations'] = row[1]
            return_list.append(row_dic)
        
        connection.close()

        return json.dumps(return_list)#WORKS

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
    print(given_date)
    connection = connect_to_database()
    #region_name = region_name.lower() # lowercase
    query = ''
    return_list = []
    if given_date == '0': #case 1 and 2
        if region_name == 'USA':
            query = "SELECT DISTINCT cases_in_US.day, cases_in_US.cases\
                FROM cases_in_US\
                ORDER BY cases_in_US.day;"
            cursor = getCursor(query, connection)
            in_list = []
            for row in cursor:
                in_list.append(str(row[0]) + ':' + str(row[1]))
            in_dic = {}
            in_dic["name"] = region_name
            in_dic["cases_dates"] = in_list
            return_list.append(in_dic)
            connection.close()
            return json.dumps(return_list)#WORKS
        else:
            query = "SELECT DISTINCT cases_date.day, cases_date.cases\
                FROM cases_date\
                WHERE cases_date.states = %s\
                ORDER BY cases_date.day;"
            cursor = getCursor(query, connection, region_name)
            in_list = []
            for row in cursor:
                in_list.append(str(row[0]) + ':' + str(row[1]))
            in_dic = {}
            in_dic["name"] = region_name
            in_dic["cases_dates"] = in_list
            return_list.append(in_dic)
            connection.close()
            return json.dumps(return_list) #works
    else: #case 3
        """
        "\
            SELECT DISTINCT cases_date.day, cases_date.cases\
            FROM cases_date\
            WHERE cases_date.states = %s\
            AND cases_date.day = DATE(%s)\
            ORDER BY cases_date.day;"
            SELECT DISTINCT cases_date.day, cases_date.states, cases_date.cases
            FROM cases_date, states_code
            WHERE UPPER(states_code.states) LIKE UPPER('California')
            AND states_code.code = cases_date.states
            AND cases_date.day = '2021-02-20'
            ORDER BY cases_date.day;
            SELECT DISTINCT cases_date.states, cases_date.day, cases_date.cases
            FROM cases_date
            WHERE UPPER(cases_date.states) LIKE UPPER('CA')
            AND cases_date.day = '2021-02-25'
            ORDER BY cases_date.day;
        """
        query = "SELECT DISTINCT cases_date.states, cases_date.day, cases_date.cases\
            FROM cases_date\
            WHERE UPPER(cases_date.states) LIKE UPPER(%s)\
            AND cases_date.day = %s\
            ORDER BY cases_date.day;"

        cursor = getCursor(query, connection, region_name, given_date)
        for row in cursor:
            row_dic = {}
            row_dic['name'] = row[0]
            row_dic['date'] = str(row[1])
            row_dic['case'] = row[2]
            return_list.append(row_dic)
        connection.close()
        return json.dumps(return_list) # working
    
@api.route("/increased_cases_by_date")
def get_increased_cases_by_date():
    '''
        REQUEST: /increased_cases_by_date?[region_name={state},given_date={date}]

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
    print(given_date)
    connection = connect_to_database()
    #region_name = region_name.lower() # lowercase
    query = ''
    return_list = []
    if given_date == '0': #case 1 and 2
        if region_name == 'USA':
            query = "SELECT DISTINCT cases_in_US.day, cases_in_US.cases_increased\
                FROM cases_in_US\
                ORDER BY cases_in_US.day;"
            cursor = getCursor(query, connection)
            in_list = []
            for row in cursor:
                in_dic = {}
                in_dic["day"] = str(row[0])
                in_dic["increased_cases"] = row[1]              
                return_list.append(in_dic)
            connection.close()
            return json.dumps(return_list)#WORKS
        else:
            query = "SELECT DISTINCT cases_date.day, cases_date.cases_increased\
                FROM cases_date\
                WHERE cases_date.states = %s\
                ORDER BY cases_date.day;"
            cursor = getCursor(query, connection, region_name)
            
            for row in cursor:
                in_dic = {}
                in_dic["day"] = str(row[0])
                in_dic["increased_cases"] = row[1]              
                return_list.append(in_dic)
            connection.close()
            return json.dumps(return_list)#WORKS
    else: #case 3
        """
        "\
            SELECT DISTINCT cases_date.day, cases_date.cases\
            FROM cases_date\
            WHERE cases_date.states = %s\
            AND cases_date.day = DATE(%s)\
            ORDER BY cases_date.day;"
            SELECT DISTINCT cases_date.day, cases_date.states, cases_date.cases
            FROM cases_date, states_code
            WHERE UPPER(states_code.states) LIKE UPPER('California')
            AND states_code.code = cases_date.states
            AND cases_date.day = '2021-02-20'
            ORDER BY cases_date.day;
            SELECT DISTINCT cases_date.states, cases_date.day, cases_date.cases
            FROM cases_date
            WHERE UPPER(cases_date.states) LIKE UPPER('CA')
            AND cases_date.day = '2021-02-25'
            ORDER BY cases_date.day;
            CREATE TABLE vaccinations_region(
                region text,
                people_with_1_or_more_doses integer,
                people_with_1_or_more_doses_per_100K integer,
                people_with_2_doses integer,
                people_with_2_doses_per_100K integer,
            );
            
            SELECT DISTINCT vaccinations_region.region, vaccinations_region.people_with_1_or_more_doses, cases_date.cases
            FROM cases_date, vaccinations_region,states_code
            WHERE UPPER(cases_date.states) = UPPER(states_code.code)
            AND UPPER(states_code.states) = UPPER(vaccinations_region.region)
            AND cases_date.day = (SELECT MAX(day) FROM cases_date)
            ORDER BY cases_date.cases;
        """
        query = "SELECT DISTINCT cases_date.states, cases_date.day, cases_date.cases_increased\
            FROM cases_date\
            WHERE UPPER(cases_date.states) LIKE UPPER(%s)\
            AND cases_date.day = %s\
            ORDER BY cases_date.day;"

        cursor = getCursor(query, connection, region_name, given_date)
        for row in cursor:
            row_dic = {}
            row_dic['name'] = row[0]
            row_dic['date'] = str(row[1])
            row_dic['increased_case'] = row[2]
            return_list.append(row_dic)
        connection.close()
        return json.dumps(return_list) # working
    


@api.route("/vaccinations_by_date")
def get_vaccinations_by_date():
    '''
        REQUEST: /vaccinations_by_date?[region_name={state},given_date={date}]

        GET parameters:
            region_contains(optional, default:USA)

        RESPONSE: A JSON list of dictionaries, each of which represents a dataset in one day, sorted by date. If no optional arguments are given, 
        the dictionary will contain cases by day for the United States with the following fields. 
            name -- (string) the region name                                                
            cases_dates -- (list) list that contains the date and the vaccinations of the date given with the format of each value in the list as date:vaccinations
            
        If only the state optional argument is given, the dictionary will contain vaccinations by day for the specified state. The dictionary will have the following fields.
            name -- (string) the region name
            vaccination_dates -- (list) list that contains the date and the vaccinations of the date given with the format of each value in the list as date:vaccinations

        If both optional arguments are given, the dictionary will contain the vaccinations of the specified date with the following fields.
            name -- (string) the region name
            date -- (string) the requested date
            vaccinations -- (int) the vaccinations on the date
    '''
    region_name = flask.request.args.get('region_name', default = 'USA')
    given_date = flask.request.args.get('given_date','0')
    connection = connect_to_database()
    #region_name = region_name.lower() # lowercase
    query = ''
    return_list = []
    if given_date == '0': #case 1 and 2
        if region_name == 'USA':
            query = "SELECT DISTINCT vaccinations_in_US.day, vaccinations_in_US.people_with_1_or_more_doses\
                FROM vaccinations_in_US\
                ORDER BY vaccinations_in_US.people_with_1_or_more_doses;"
            cursor = getCursor(query, connection)
            in_list = []
            for row in cursor:
                row_dic = {}
                row_dic['region'] = "USA"
                row_dic['date'] = str(row[0])
                row_dic['vaccinations'] = row[1]
                return_list.append(row_dic)
            connection.close()
            return json.dumps(return_list)
        else: # WE DONT HAVE ANYTHING FROM HERE
            query = "SELECT DISTINCT cases_date.day, cases_date.cases\
                FROM cases_date\
                WHERE cases_date.states = '%s'\
                ORDER BY cases_date.day;"
            cursor = getCursor(query, connection, region_name)
            for row in cursor:
                row_dic = {}
                row_dic['date'] = row[0]
                row_dic['case'] = row[1]
                return_list.append(row_dic)
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
            row_dic['vaccinations'] = row[2]
            return_list.append(row_dic)
        connection.close()
        return json.dumps(return_list)# Not working
@api.route("/increased_vaccinations_by_date")
def get_increased_vaccination_by_date():
    '''
        REQUEST: /increased_cases_by_date?given_date={date}

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
    given_date = flask.request.args.get('given_date','0')
    print(given_date)
    connection = connect_to_database()
    #region_name = region_name.lower() # lowercase
    query = ''
    return_list = []
    if given_date == '0':
            query = "SELECT DISTINCT day, total_doses_administered_daily\
                FROM vaccinations_in_US\
                ORDER BY  day;"
            cursor = getCursor(query, connection)
            for row in cursor:
                row_dic = {}
                row_dic['date'] = str(row[0])
                row_dic['increased_vaccination'] = row[1]
                return_list.append(row_dic)
            connection.close()
            return json.dumps(return_list) #works
    else: #case 2
        """
        "\
            SELECT DISTINCT cases_date.day, cases_date.cases\
            FROM cases_date\
            WHERE cases_date.states = %s\
            AND cases_date.day = DATE(%s)\
            ORDER BY cases_date.day;"
            SELECT DISTINCT cases_date.day, cases_date.states, cases_date.cases
            FROM cases_date, states_code
            WHERE UPPER(states_code.states) LIKE UPPER('California')
            AND states_code.code = cases_date.states
            AND cases_date.day = '2021-02-20'
            ORDER BY cases_date.day;
            SELECT DISTINCT cases_date.states, cases_date.day, cases_date.cases
            FROM cases_date
            WHERE UPPER(cases_date.states) LIKE UPPER('CA')
            AND cases_date.day = '2021-02-25'
            ORDER BY cases_date.day;
        """
        query = "SELECT DISTINCT day, total_doses_administered_daily\
                FROM vaccinations_in_US\
                WHERE day = %s\
                ORDER BY  day;"

        cursor = getCursor(query, connection, given_date)
        for row in cursor:
            row_dic = {}
            row_dic['date'] = str(row[0])
            row_dic['increased_vaccination'] = row[1]
            return_list.append(row_dic)
        connection.close()
        return json.dumps(return_list) # working

@api.route("/us_information")
def get_us_information():
    '''
        REQUEST: /increased_cases_by_date?[region_name={state},given_date={date}]

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
    connection = connect_to_database()
    query = ''
    return_list = []
    query = "SELECT DISTINCT cases_in_US.day, cases_in_US.cases, cases_in_US.cases_increased, vaccinations_in_US.people_with_1_or_more_doses,\
        vaccinations_in_US.total_doses_administered_daily, vaccinations_in_US.people_with_2_doses\
        FROM cases_in_US, vaccinations_in_US\
        WHERE cases_in_US.day = vaccinations_in_US.day\
        ORDER BY cases_in_US.day;"
    cursor = getCursor(query, connection)
    in_list = []
    for row in cursor:
        in_dic = {}
        in_dic["day"] = str(row[0])
        in_dic["total_cases"] = row[1]
        in_dic["increased_cases"] = row[2]  
        in_dic["people_with_1_or_more_doses"] = row[3]
        in_dic["total_doses_administered_daily"] = row[4]
        in_dic["people_with_2_doses"] = row[5]
        return_list.append(in_dic)
    connection.close()
    return json.dumps(return_list)#WORKS
    
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

