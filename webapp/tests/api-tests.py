'''
   api-tests.py
   Aiden Chang, 18 Feb 2021
   Testing api for covid website project 
   CS257 winter2021
'''

import #whatever the covid api program will look like
import unittest

class ApiEndpointTester(unittest.TestCase):
    def setUp(self):
        self.api_endpoint = #not sure what to put here yet, we don't know yet right? since we don't have the api code
    def tearDown(self):
        pass

    '''
    testing for api endpoints
    '''
    
    #testing REQUEST: /total_cases?region_contains={state_keyword}
    def test_get_cases(self):
        self.assertTrue(self.api_endpoint.get_total_cases(), 0)
        self.assertIsNotNone(self.api_endpoint.get_total_cases())
        self.assertTrue(self.api_endpoint.get_total_cases('california')) #empty lists or dics evaluate to false
        self.assertIsTrue(self.api_endpoint.get_total_cases("california"))
        self.assertRaise(ValueError,api_endpoint.gettotal_cases,'californiaadadada')

    #testing REQUEST: /total_vaccinations?region_contains={state_keyword}
    def test_get_vaccinations(self):
        self.assertTrue(self.api_endpoint.get_total_cases(), 0)
        self.assertIsNotNone(self.api_endpoint.get_total_cases())
        self.assertTrue(self.api_endpoint.get_total_cases('california')) #empty lists or dics evaluate to false
        self.assertIsTrue(self.api_endpoint.get_total_cases('california'))
        self.assertRaise(ValueError,api_endpoint.gettotal_cases,'californiaadadada')


    #testing REQUEST: /cases_by_date?region_name={state}
    def test_get_cases_by_date(self):
        