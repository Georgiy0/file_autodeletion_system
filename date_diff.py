from datetime import datetime

"""
This module contains different functions that compute
the difference between two dates mesuared in days.
"""

def standard(d1, d2):
    """ standard function that accepts two datetime arguments """
    return abs((d1 - d2).days)

def date_dif_loops(years_1, month_1, day_1, years_2, month_2, day_2):
    """ custom function that computes the difference between two dates """
    #array that contains the ammount of days in each month (Jan - Dec)
    month_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    # checks weather end years are leap years
    leap_1 = years_1 % 4 == 0
    leap_2 = years_2 % 4 == 0
    if years_1 == years_2:
        if month_1 == month_2:
            return day_1 - day_2
        else:
            days_num = day_1 + (month_day[month_2 - 1] - day_2)
            for month in range(month_2 + 1, month_1):
                days_num += month_day[month-1]
            if leap_1 and month_2 <= 2 and month_1 > 2:
                days_num += 1
            return days_num
    else:
        leap_num = (years_1 - 1)//4 - (years_2 - 1)//4
        if leap_2:
            leap_num -= 1
        # the difference between two dates not considering end years
        full_year_diff = (years_1 - years_2 - 1)*365 + leap_num
        days_in_year_2 = month_day[month_2-1] - day_2
        if leap_2 and month_2 <= 2:
            days_in_year_2 += 1
        for month in range(month_2+1, 13):
            days_in_year_2 += month_day[month-1]
        days_in_year_1 = day_1
        if leap_1 and month_1 > 2:
            days_in_year_1 += 1
        for month in range(1, month_1):
            days_in_year_1 += month_day[month-1]
        total_diff = full_year_diff + days_in_year_1 + days_in_year_2
        return total_diff

def date_dif_precomputed(years_1, month_1, day_1, years_2, month_2, day_2):
    """
    Enhanced version of date_dif_loops function that uses precomputed array which
    contains ammount of dates between two months.
    """
    month_day = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    month_list = (
        (0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365),
        (0, 0, 28, 59, 89, 120, 150, 181, 212, 242, 273, 303, 334),
        (0, 0, 0, 31, 61, 92, 122, 153, 184, 214, 245, 275, 306),
        (0, 0, 0, 0, 30, 61, 91, 122, 153, 183, 214, 244, 275),
        (0, 0, 0, 0, 0, 31, 61, 92, 123, 153, 184, 214, 245),
        (0, 0, 0, 0, 0, 0, 30, 61, 92, 122, 153, 183, 214),
        (0, 0, 0, 0, 0, 0, 0, 31, 62, 92, 123, 153, 184),
        (0, 0, 0, 0, 0, 0, 0, 0, 31, 61, 92, 122, 153),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 30, 61, 91, 122),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 31, 61, 92),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 30, 61),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 31),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        )
    leap_1 = years_1 % 4 == 0
    leap_2 = years_2 % 4 == 0
    if years_1 == years_2:
        if month_1 == month_2:
            return day_1 - day_2
        else:
            days_num = day_1 + (month_day[month_2 - 1] - day_2)
            days_num += month_list[month_2][month_1-2]
            if leap_1 and month_2 <= 2 and month_1 > 2:
                days_num += 1
            return days_num
    else:
        leap_num = (years_1 - 1)//4 - (years_2 - 1)//4
        if leap_2:
            leap_num -= 1
        full_year_diff = (years_1 - years_2 - 1)*365 + leap_num
        days_in_year_2 = month_day[month_2-1] - day_2
        if leap_2 and month_2 <= 2:
            days_in_year_2 += 1
        days_in_year_2 += month_list[month_2][12]
        days_in_year_1 = day_1
        if leap_1 and month_1 > 2:
            days_in_year_1 += 1
        days_in_year_1 += month_list[0][month_1-1]
        return full_year_diff + days_in_year_1 + days_in_year_2

def day_num(y, m, d):
    """ computes the ammount of days from A.D. to the provided date (Y-m-d) """
    m = (m + 9) % 12
    y = y - m//10
    return 365*y + y//4 - y//100 + y //400 + (m*306 + 5)//10 + (d - 1)

def days_sum_dif(year_1, month_1, day_1, year_2, month_2, day_2):
    """ computes the difference between two dates as substitution of the ammount of days in them """
    return day_num(year_1, month_1, day_1) - day_num(year_2, month_2, day_2)
