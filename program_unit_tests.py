import sys
import os
import unittest
import platform
import Assimilation_Tool as at
from datetime import datetime

class Test_Setup(unittest.TestCase):

    def test_python_version(self):
        ver = sys.version_info.major
        self.assertTrue(ver == 3)

    def test_work_dir(self):
        if platform.system() in "Windows":
            file_path = 'G:\\users\\COASTAL\\Hydrocoast\\Data Assimilation\\Data\\data_assimilation'
        elif platform.system() in "Linux":
            file_path = '/home/sogood/Documents/Python/LPBF/Data Assimilation/Data/data_assimilation'
        self.assertTrue(os.getcwd() == file_path)

class Test_calculations(unittest.TestCase):

    def test_average(self):
        num = [1,2,3,4,5]
        num_check = at.calculations.average(num)
        self.assertTrue(num_check == 3)

# class Test_Data_Collection(unittest.TestCase):
#
#     def test_scrape_gauges_dict(self):

class Test_Tool_Filters(unittest.TestCase):

    def test_make_monday(self):
        dict = {
            'test day1': [2018, 11, 2, '20181029'],
            'test day2': [2017, 1, 1, '20161226'],
        }

        for key in dict:
            year = dict[key][0]
            month = dict[key][1]
            day = dict[key][2]
            day = datetime(year, month, day)

            monday_check = at.tool_filters.make_monday(day)
            self.assertEqual(monday_check, dict[key][3])

    def test_date_subtract_adjustment(self):

        start_date = datetime(year=2018, month=11, day=2)
        end_date_test1 = at.tool_filters.date_adjustment(start_date, day = -7)
        end_date_test2 = at.tool_filters.date_adjustment(start_date, month = -7)
        end_date_test3 = at.tool_filters.date_adjustment(start_date, year = -7)
        end_date_test4 = at.tool_filters.date_adjustment(start_date, year = -7, month=-7)
        end_date_test5 = at.tool_filters.date_adjustment(start_date, year = -7, month=-7, day=-7)
        end_date_test6 = at.tool_filters.date_adjustment(start_date, month = -28)
        end_date_test7 = at.tool_filters.date_adjustment(start_date, day=-365)

        self.assertTrue(end_date_test1 == datetime(year=2018, month=10, day=26))
        self.assertTrue(end_date_test2 == datetime(year=2018, month=4, day=2))
        self.assertTrue(end_date_test3 == datetime(year=2011, month=11, day=2))
        self.assertTrue(end_date_test4 == datetime(year=2011, month=4, day=2))
        self.assertTrue(end_date_test5 == datetime(year=2011, month=3, day=26))
        self.assertTrue(end_date_test6 == datetime(year=2016, month=7, day=2))
        self.assertTrue(end_date_test7 == datetime(year=2017, month=11, day=2))

    def test_date_addition_adjustment(self):
        start_date = datetime(year=2017, month=1, day=1)
        end_date_test1 = at.tool_filters.date_adjustment(start_date, day = 7)
        end_date_test2 = at.tool_filters.date_adjustment(start_date, month = 7)
        end_date_test3 = at.tool_filters.date_adjustment(start_date, year = 7)
        end_date_test4 = at.tool_filters.date_adjustment(start_date, year = 7, month=7)
        end_date_test5 = at.tool_filters.date_adjustment(start_date, year = 7, month=7, day=7)
        end_date_test6 = at.tool_filters.date_adjustment(start_date, month=28)
        end_date_test7 = at.tool_filters.date_adjustment(start_date, day=365)

        self.assertTrue(end_date_test1 == datetime(year=2017, month=1, day=8))
        self.assertTrue(end_date_test2 == datetime(year=2017, month=8, day=1))
        self.assertTrue(end_date_test3 == datetime(year=2024, month=1, day=1))
        self.assertTrue(end_date_test4 == datetime(year=2024, month=8, day=1))
        self.assertTrue(end_date_test5 == datetime(year=2024, month=8, day=8))
        self.assertTrue(end_date_test6 == datetime(year=2019, month=5, day=1))
        self.assertTrue(end_date_test7 == datetime(year=2018, month=1, day=1))



if __name__ == '__main__':
   test_file = 'test_log.txt'
   f = open(test_file, "w")
   runner = unittest.TextTestRunner(f)
   print(runner)
   unittest.main(testRunner=runner)
   f.close()