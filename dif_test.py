import time
from datetime import datetime
from date_diff import standard, date_dif_loops, date_dif_precomputed, days_sum_dif
from parse_date_str import parse_date_str
from inspect import signature

"""
This module performs testing of functions from date_diff.py
This module is not compatible with python version 2.7 and lower.
"""

# sets weather to parse arguments on each test function callable
# or parse the arguments set only once for each function
DO_PARSE = True
# number of execution of each function
LOOP_NUM = 100000
# set of dates to test the functions on (end_date, start_date)
TEST_DATA_SET = [
    ("2017-7-13", "2014-1-13")
]

# list of function to test
TEST_FUNC_SET = [date_dif_precomputed, date_dif_loops, standard, days_sum_dif]
# the output of testing function is compared to the output of
# this function.
CHECKING_FUNC = standard

def get_2_argset(D1, D2):
    PARAM_1 = datetime.strptime(D1, "%Y-%m-%d")
    PARAM_2 = datetime.strptime(D2, "%Y-%m-%d")
    return (PARAM_1, PARAM_2)

def get_6_argset(D1, D2):
    PARAM_1 = parse_date_str(D1, '-', 0, 1, 2)
    PARAM_2 = parse_date_str(D2, '-', 0, 1, 2)
    return (PARAM_1[0], PARAM_1[1], PARAM_1[2], PARAM_2[0], PARAM_2[1], PARAM_2[2])

# dictionary of functions that return valid arguments set based
# on function's signature
GET_ARGS = {    
    2: get_2_argset,
    6: get_6_argset
    }

# main testing cycles
for data_set in TEST_DATA_SET:
    print("\nData set: from {} to {}".format(data_set[1], data_set[0]))
    for func in TEST_FUNC_SET:
        sig = signature(func)
        param_num = len(sig.parameters)
        print("Testing {}".format(func.__name__))
        get_args_func = GET_ARGS[param_num]
        if not DO_PARSE:
            args = get_args_func(*data_set)
            start = time.time()
            for i in range(0, LOOP_NUM):
                func(*args)
            end = time.time()
            print("Time elapsed {}".format(end - start))
            print("Diff = {}".format(func(*get_args_func(*data_set))))
            if func(*get_args_func(*data_set)) != CHECKING_FUNC(*get_2_argset(*data_set)):
                print("{} != {}".format(func(*get_args_func(*data_set)), CHECKING_FUNC(*get_2_argset(*data_set))))
                raise ValueError('Wrong return value')
        else:
            start = time.time()
            for i in range(0, LOOP_NUM):
                func(*get_args_func(*data_set))
            end = time.time()
            print("Time elapsed {}".format(end - start))
            print("Diff = {}".format(func(*get_args_func(*data_set))))
            if func(*get_args_func(*data_set)) != CHECKING_FUNC(*get_2_argset(*data_set)):
                print("{} != {}".format(func(*get_args_func(*data_set)), CHECKING_FUNC(*get_2_argset(*data_set))))
                raise ValueError('Wrong return value')
