'''Functions that help with random stuff that's used across multiple different files.'''
from aqt.utils import showInfo
from aqt import mw
import time
from .errors import *
from abc import ABC, abstractmethod
# typechecking
from typing import Optional
from math import floor

class CalenderDate:
    def __init__(self, YMD:list['year-####':int, 'month-##':int, 'day-##':int]) -> None:
        if type(YMD) != list:
            if YMD == 'None' or YMD == None:
                YMD = [2001, 1, 1]
            else:
                raise Exception(f'{YMD} is not a list')
        
        
        self._year = YMD[0]
        self._month = YMD[1]
        self._day = YMD[2]
        #Convert the YMD to unix, than to local time, to get the day of the week.
        self._day_of_the_week = time.localtime(time.mktime((self._year, self._month, self._day, 0, 0, 0, 0, 0, -1))).tm_wday
    
        if self._year < 2000 or type(self._year) is not int:
            raise ValueError(f'Calender Date Type (year) must be a integer and over 1999. Value passed is {str(self._year)}. The type is {str(type(self._year))}')
        if self._month not in range(1, 12) or type(self._month) is not int:
            raise ValueError(f'Calender Date Type (month) must be a integer and between 1-12. Value passed is {str(self._month)}. The type is {str(type(self._month))}')
        if self._day not in range(1, 31) or type(self._day) is not int:
            raise ValueError(f'Calender Date Type (day) must be a integer and between 1-31. Value passed is {str(self._day)}. The type is {str(type(self._day))}')
    
    def withinStreak(self, arg:'CalenderDate') -> bool:
        try:
            self._epoch = time.mktime((self._year, self._month, self._day, 0, 0, 0, 0, 0, -1))
            if type(arg) is list:
                arg = CalenderDate([arg[0], arg[1], arg[2]])
            arg_epoch = time.mktime((arg._year, arg._month, arg._day, 0, 0, 0, 0, 0, -1))
            diff = self._epoch - arg_epoch
            diff_in_days = diff // 86400
            if diff_in_days >= 1 and diff_in_days < 2:
                return True
            else:
                return False
        except Exception:
            raise Exception(f'Arg Type: {type(arg)} String: {arg.__str__()}')
        
    def withinWeek(self, arg:'CalenderDate') -> bool:
        try:
            self._epoch = time.mktime((self._year, self._month, self._day, 0, 0, 0, 0, 0, -1))
            if type(arg) is list:
                arg = CalenderDate([arg[0], arg[1], arg[2]])
            arg_epoch = time.mktime((arg._year, arg._month, arg._day, 0, 0, 0, 0, 0, -1))
            diff = self._epoch - arg_epoch
            diff_in_days = diff // 86400
            if diff_in_days <= 6 and diff_in_days >= -6:
                return True
            else:
                return False
        except Exception:
            raise Exception(f'Arg Type: {type(arg)} String: {arg.__str__()}') 

    def addDay(self, arg:'CalenderDate') -> 'CalenderDate':
        #If the argument comes straight from the json file, than make it a CalenderDate Object
        if type(arg) is list:
            arg = CalenderDate([arg[0], arg[1], arg[2]])
        #Convert to Epoch Time
        arg_epoch = time.mktime((arg._year, arg._month, arg._day, 0, 0, 0, 0, 0, -1))
        #Add a days worth of Epoch Time to the date
        arg_epoch += 86400
        #Convert the epoch date to the time tuple
        to_return = time.localtime(arg_epoch)
        #Convert it back into a calender date to be able to return it
        to_return = CalenderDate([to_return.tm_year, to_return.tm_mon, to_return.tm_mday])
        return to_return
            
    def getYMD(self):
        return [self._year, self._month, self._day]
    
    def __eq__(self, arg:'CalenderDate') -> bool:
        if type(arg) is list:
                arg = CalenderDate([arg[0], arg[1], arg[2]])
                
        if self._year is arg._year:
            if self._month is arg._month:
                if self._day is arg._day:
                    return True
        return False
    
    def __ne__(self, arg:'CalenderDate') -> bool:
        if type(arg) is list:
                arg = CalenderDate([arg[0], arg[1], arg[2]])
        if self._year is not arg._year:
            return True
        if self._month is not arg._month:
            return True
        if self._day is not arg._day:
            return True
        return False
    
    def __gt__(self, arg:'CalenderDate') -> bool:
        '''Returns true if the left hand side is more 'in the future' than the right hand side.'''
        if type(arg) is list:
                arg = CalenderDate([arg[0], arg[1], arg[2]])
        if self._year > arg._year:
            return True
        if self._year == arg._year and self._month > arg._month:
            return True
        if self._year == arg._year and self._month == arg._month and self._day > arg._day:
            return True
        return False
    
    def __lt__(self, arg:'CalenderDate') -> bool:
        '''Returns true if the left hand side is more ancient than the right hand side.'''
        if type(arg) is list:
                arg = CalenderDate([arg[0], arg[1], arg[2]])
        if self._year < arg._year:
            return True
        if self._year == arg._year and self._month < arg._month:
            return True
        if self._year == arg._year and self._month == arg._month and self._day < arg._day:
            return True
        return False

class DateType:
    def __init__(self, time) -> None:
        if any(time is t for t in (int, float)):
            self.v = time
        else:
            raise ValueError("Date Type can only take ")

class Debug:
    debug_txt = ""
    def msg(self, txt:str, error:str="None") -> None:
        if error != "None":
            showInfo(f'DEBUG: {txt} || {error}')
        else:
            showInfo(f'DEBUG: {txt}')
                
    def __str__(self):
        return self.debug_txt
            
class Consts:
    def __init__(self) -> None:
        self.addon_package = mw.addonManager.addonFromModule(__name__)
        self.base_url = f'/_addons/{self.addon_package}'

class Date_Calc:
    def __init__(self) -> None:
        self._local_time = time.localtime()
        self._year = self._local_time.tm_year
        self._month = self._local_time.tm_mon
        self._day = self._local_time.tm_mday
        self._day_of_the_week = self._local_time.tm_wday
        self._date: CalenderDate = CalenderDate([self._year, self._month, self._day])
    
    def getDayWeek(self, arg=-1) -> str:
        #Anki uses Python 3.9, meaning match isn't an option :(
        if self._day_of_the_week == 0 or arg == 0:
            to_return = "M"
        if self._day_of_the_week == 1 or arg == 1:
            to_return = "T"
        if self._day_of_the_week == 2 or arg == 2:
            to_return = "W"
        if self._day_of_the_week == 3 or arg == 3:
            to_return = "Th"
        if self._day_of_the_week == 4 or arg == 4:
            to_return = "F"
        if self._day_of_the_week == 5 or arg == 5:
            to_return = "Sa"
        if self._day_of_the_week == 6 or arg == 6:
            to_return = "S"
        return to_return
    
class DataHandler:
    def __init__(self) -> None:
        self.config = mw.addonManager.getConfig(__name__ + '/user_data')

    def save(self):
        '''Saves changes made to the config.'''
        mw.addonManager.writeConfig(__name__ + '/user_data', self.config)
    
    def changeVar(self, var, data):
        if var == None or var == "None":
            raise Exception(f'{var} is equal to None. It contains: {data}')
        try:
            self.config[var] = data
            self.save()
        except Exception as e:
            raise Exception(e)

class UserData():
    def __init__(self, CONFIG_DATA) -> None:
        self.data = CONFIG_DATA
        self.date = Date_Calc()._date
        if CONFIG_DATA:
            self._last_anki_use = CalenderDate(CONFIG_DATA['lastankiuse']) # Unix time
            self._start_date_use = CalenderDate(CONFIG_DATA['startdateuse']) # Unix time
            self._debug = CONFIG_DATA['debug'] # 0 or 1
            self._streak = CONFIG_DATA['streak']
            self._frozen = CalenderDate(CONFIG_DATA['frozen'])
        else:
            raise CollectionError("Anki data was not ready to be read, and thus caused an error in the Streak Addon when attempted to access too early.")
    
    def getDebug(self) -> bool:
        if self._debug == 0: return False
        elif self._debug == 1: return True
        else: raise ParameterError("Debug data is not a 0 or a 1. To fix this, change the config file.")
        
    def getToday(self) -> CalenderDate:
        to_return = Date_Calc()
        return to_return._date
    
    def getStart(self) -> CalenderDate:
        if type(self._start_date_use) != CalenderDate: 
            self.setStart()
            return self._start_date_use
        return self._start_date_use
        
    def setStart(self) -> None:
        self._start_date_use = self.date.getYMD()
        DATA = DataHandler()
        DATA.changeVar('startdateuse', self._start_date_use)
        DATA.save()
    
    def getLastUse(self) -> CalenderDate:
        if type(self._last_anki_use) != CalenderDate: 
            self.setLastUse()
            return self._last_anki_use
        return self._last_anki_use
    
    def setLastUse(self) -> None:
        self._last_anki_use = self.date.getYMD()
        DATA = DataHandler()
        DATA.changeVar('lastankiuse', self._last_anki_use)
        DATA.save()
    
    def getStreak(self) -> int:
        if self.date.withinStreak(self.getLastUse()):
            self._streak += 1
            self.setLastUse()
            DATA = DataHandler()
            DATA.changeVar('streak', self._streak)
            DATA.save()
            return self._streak
        elif self.date == self.getLastUse():
            return self._streak
        else:
            self._streak = 0
            self.setLastUse()
            self.setStart()
            DATA = DataHandler()
            DATA.changeVar('streak', self._streak)
            DATA.save()
            return self._streak

    def getTomorrow(self) -> CalenderDate:
        tomorrow = self.date.addDay(self.date)
        return tomorrow
    
    def getFrozen(self) -> CalenderDate:
        if type(self._frozen) != CalenderDate:
            if type(self._frozen) == list:
                self._frozen = CalenderDate(self._frozen[0], self._frozen[1], self._frozen[2])
            else:
                self._frozen = CalenderDate([2001,1,1])
        return self._frozen
    
    def setFreeze(self) -> None:
        DATA = DataHandler()
        if self.getFrozen() == self.getTomorrow():
            self._frozen = CalenderDate([2002, 1, 1])
        else:  
            tomorrow = self.getTomorrow()
            self._frozen = tomorrow.getYMD()
        DATA.changeVar('frozen', self._frozen)
        DATA.save()
        # The Graphical portion of the addon is handled by streak.js
        