from datetime import date, datetime

level = 0
date_format = '%H:%M'

def added(msg:str):
    if level <= 1:
        print(_current_time() + ': ADDED - ' +msg)
        _sep()

def changed(msg:str):
    if level <= 1:
        print(_current_time() + ': CHANGED - ' +msg)
        _sep()

def info(msg:str):
    if level <= 0:
        print(_current_time() + ': INFO - ' +msg)
        _sep()

def error(msg:str):
    if level <= 2:
        print(_current_time() + ': ERROR - ' +msg)
        _sep()

def _current_time():
    return date.strftime(datetime.now(), date_format)

def _sep():
    print('-'*10)