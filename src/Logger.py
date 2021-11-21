from datetime import date, datetime

def added(msg:str):
    print(_current_time() + ': ADDED - ' +msg)
    _sep()

def changed(msg:str):
    print(_current_time() + ': CHANGED - ' +msg)
    _sep()

def info(msg:str):
    print(_current_time() + ': INFO - ' +msg)
    _sep()

def error(msg:str):
    print(_current_time() + ': ERROR - ' +msg)
    _sep()

def _current_time():
    return date.strftime(datetime.now(),'%H:%M')

def _sep():
    print('-'*10)