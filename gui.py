from .auxillary import Consts, Date_Calc
from typing import (
    TYPE_CHECKING,
    Dict,
    List
)

'''HTML Elements that can be used to insert content into the ANKI document'''
class HTML_Elements:
    def bold(self, txt) -> str:
        return f'<b>{txt}</b>'

    def italize(self, txt) -> str:
        return f'<i>{txt}</i>'

    def span(self, txt, cls="", id_thing="") -> str:
        return f'<span class="{cls}" id="{id_thing}">{txt}</span>'

    def div(self, txt, cls="", id_thing="") -> str:
        return f'<div class="{cls}" id="{id_thing}">{txt}</div>'

    def img(self, src, alt="", cls="", id_thing="") -> str:
        return f'''<img src="{src}" alt="{alt}" id="{id_thing}" class="img_default {cls}" height="68px" width="40px">'''
    
    def stylesheet(self, href) -> str:
        return f'''<link rel="stylesheet" type="text/css" href="{href}"/>'''
    
    def jsLink(self, href) -> str:
        return f'<script src="{href}"></script>'
    
    def br(self) -> str:
        return f'<br>'
    
    def section(self, content, cls="") -> str:
        return f'<section class="{cls}">{content}</section>'
    
    def p(self, txt, cls="") -> str:
        return f'<p class="{cls}">{txt}</p>'
    
    def btn(self, text, cls="", onclick="") -> str:
        return f'<button class="{cls}" onclick="{onclick}">{text}</button>'
'''Prebuilt CSS classes to reduce duplicating the same thing.'''  
class CSS_Classes:
    def defaultCssTxt(self) -> str:
        '''txt-white'''
        return f'txt-white'
    def defaultCssSection(self) -> str:
        '''w-full section-default'''
        return f'w-full section-default'
    def defaultCssHeader(self) -> str:
        '''header border-bottom'''
        return f'header border-bottom'
    def streakCssImage(self) -> str:
        '''img_default'''
        return f'img-default img-streak'
    def streakCssDiv(self) -> str:
        '''div-streak'''
        return f'div-streak'
    def streakCssSpan(self) -> str:
        '''span-streak '''
        return f'span-streak '
    def weekCss(self) -> str:
        '''week-container'''
        return f'week-container'

class BuildDisplay(HTML_Elements, CSS_Classes):
    def __init__(self, style_file_name, image_file_name, script_file_name, streak=0, frozen=None) -> None:
        self.url = Consts().base_url
        self.stylesheet_path = f'{self.url}/{style_file_name}'
        self.img_path = f'{self.url}/icons/{image_file_name}'
        self.js_path = f'{self.url}/{script_file_name}'
        self.streak = streak
        self.frozen = frozen

    def core(self, debug:bool) -> str:
        # Header
        streak_icon_css = self.streakCssImage()
        if self.streak > 0: streak_icon_css += ' img-streak-active'
        streak_icon = self.img(self.img_path, "streak icon", streak_icon_css)
        streak_text = self.span(self.streak, self.streakCssSpan(), "streakCounter")
        header_icon = self.div(streak_icon + streak_text, self.streakCssDiv())
        header_text = self.span("Anki Streak", 'w-full block')
        header = self.div(header_text + header_icon, self.defaultCssHeader() + ' grid')
        
        #Days
        days_of_the_week = self.weekIcons()
        
        #Buttons
        btn_freeze = self.btn('Freeze', '', "freeze();return pycmd('freeze-tomorrow');")
        btn_increase = self.btn('DEBUG: Streak Increase', '', 'increaseCounter()')
        btn_decrease = self.btn('DEBUG: Streak Decrease', '', 'decreaseCounter()')
        
        #Combine Core
        core = self.div(header + days_of_the_week)
        if debug is True: core += btn_freeze+btn_increase+btn_decrease
        else: core += btn_freeze
        
        container = self.container(core, self.defaultCssSection())
        return container

    def container(self, content, cls="") -> str:
        elements = [
            self.stylesheet(self.stylesheet_path),
            self.jsLink(self.js_path),
            self.section(content, cls)
        ]
        to_return = "".join(elements)
        return to_return
    
    def dayIcon(self, day) -> str:
        days = ["S","M","T","W","Th","F","Sa"]
        to_return_css = 'week'
        date = Date_Calc()
        date._today = date.getDayWeek()
        if self.streak >= 1:
            if date._today == day:
                to_return_css += ' ongoing-streak'
                
            elif days.index(day) <= days.index(date._today):
                range_end = days.index(date.getDayWeek())
                range_start = days.index(date.getDayWeek()) - (self.streak) + 1
                if range_start < -7: 
                    range_start = -7
                if days.index(day) in list(range(range_start, range_end)):
                   to_return_css += ' ongoing-streak'
        elif date._today == day:
            to_return_css += ' day-current'
        elif self.frozen.withinWeek(date._date) and date.getDayWeek(self.frozen._day_of_the_week) == day:
            to_return_css += ' day-frozen'
            
        to_return = self.div(
            self.div(
                self.span(day, "", f'date_{day}')
                ),
            to_return_css)
        return to_return
    
    def weekIcons(self) -> str:
        day_icons = ""
        days = ["S","M","T","W","Th","F","Sa"]
        for day in days:
            day_icons += f'{self.dayIcon(day)} '
        to_return = self.div(day_icons, self.weekCss())
        return to_return
    
    '''
    Find a way to store the current streak
        See how the heatmap does it to implement it "correctly"
    Maybe add a freezing method?
    Look at requirements and see if you can implement them.
    '''