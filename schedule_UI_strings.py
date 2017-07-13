#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
This module contains a set of python dictionaries which contains text strings for UserWarning
interfaces in different languages
"""

ENG = {
    'greeting': "SCHEDULER version 1.0\nKulicov Dmitriy\nKubrin Georgiy\n2017, IBKS",
    'menu_option_list': "Operations: \n1) Add directory for cleaning \n2) Delete directory from cleaning list\n3) Print cleaning list\n4) Stop editing of the list\n",
    'menu_operation1_input': "input directory for cleaning ( format: [way] [time format for cleaning ( hours, minutes, days)] [count of times] [file age]): \n",
    'menu_operation2_input': "input directory which will be deleted from cleaning list\n",
    'double_directory_assertion': "This directory already in cleaning list\n",
    'hours': 'hours',
    'minutes': 'minutes',
    'days': 'days',
    'directory': 'directory',
    'not_found': 'not found',
    'starting_cleaning': 'starting cleaning',
    'TIME_FORMAT': {
        'hours': 'hours',
        'minutes': 'minutes',
        'days': 'days'
    }
}

RUS = {
    'greeting': "ПЛИНИРОВЩИК версия 1.0\nКуликов Дмитрий\nКубрин Георгий\n2017, ИБКС",
    'menu_option_list': "Функции: \n1) Добавить папку для отчистки\n2) Удалить папку из списка отчищаемых\n3) Вывести список отчищаемых папок\n4) Закончить настройку списка\n",
    'menu_operation1_input': "Введите путь к отчищаемой директории ( формат: [путь] [формат времени (часы, минуты, дни)] [количество] [возраст удаляемых файлов]): \n",
    'menu_operation2_input': "Введите директорию для удаления из списка\n",
    'double_directory_assertion': "Эта дириктория уже содержится в списке!\n",
    'hours': 'часы',
    'minutes': 'минуты',
    'days': 'дни',
    'directory': 'дириктория',
    'not_found': 'не найдена',
    'starting_cleaning': 'начало отчистки',
    'TIME_FORMAT': {
        'часы': 'hours',
        'минуты': 'minutes',
        'дни': 'days'
    }
}
