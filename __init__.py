# import the main window object (mw) from aqt and get hooks
from aqt import mw, gui_hooks
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *
# import auxillary functions
from .auxillary import *
# import HTML and CSS elements for inserting into the ANKI document
from .gui import *

# Errors for debugging
from .errors import *
     
def main(db, content):
    '''Handles the general logic of the addon.'''
    #db and content are auto passed by 'gui_hooks.deck_browser_will_render_content', but the addon only uses content.
    DEBUG_INFO = ""
    data = UserData(CONFIG_DATA)
    if data.getDebug():
        TODAY = data.getToday()
        DEBUG_INFO += ("<br><span style='text-align:left;width:486px;display:block;margin-inline:1rem;'><b>Loaded Anki Streak Addon in Debug mode</b></span>")
        DEBUG_INFO_GRID_CONTENT = "".join([
            f"<span>TODAY:</span>", f"{'-'.join([str(TODAY._year), str(TODAY._month), str(TODAY._day)])}</span>",
            f"<span>CURRENT STREAK:</span>", f"{data.getStreak()}</span>",
            f"<span>DEBUG MODE:</span>", f"{data.getDebug()}</span>",
            f"<span>__NAME__</span>", f"<span>{__name__}</span>"
        ])
        DEBUG_INFO_GRID = f'<br><style>.debug-grid {{display:grid;grid-template-columns:1fr 1fr;max-width:486px;margin:1rem;text-align:left;}}</style><div class="debug-grid">{DEBUG_INFO_GRID_CONTENT}</div>'
        DEBUG_INFO += DEBUG_INFO_GRID
        

    #Builds the core part of the application
    current_streak = 0
    
    if data._streak: current_streak = data.getStreak()
    streak = BuildDisplay('styles.css', 'fire.png', 'streak.js', current_streak)
    content.stats += streak.core(data.getDebug())
    
    #Adds any debug info to the main screen instead of throwing something that would cause a crash.
    content.stats += DEBUG_INFO
    
    
if __name__ != "__main__":
    # CONFIG_DATA has to be loaded before the main function intializes or things will fail to work
    CONFIG_DATA = mw.addonManager.getConfig(__name__)
    # Gets permission to access png, css, and js files needed for the addon to work.
    mw.addonManager.setWebExports(__name__, r'.+\.(png|css|js)')
    # When Anki renders the main menu, it will connect the main function to part of it's executed methods.
    gui_hooks.deck_browser_will_render_content.append(main)