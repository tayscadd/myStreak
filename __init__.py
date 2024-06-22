# import the main window object (mw) from aqt and get hooks
from aqt import mw, gui_hooks
from aqt.utils import showInfo
from aqt.qt import *
# import auxillary functions
from .auxillary import *
# import HTML and CSS elements for inserting into the ANKI document
from .gui import *
# Errors for debugging
from .errors import *

CONTENT = None

def main(db, content):
    '''Handles the general logic of the addon.'''
    #db and content are auto passed by 'gui_hooks.deck_browser_will_render_content', but the addon only uses content.
    
    #When debug is on, information used to help debug will be displayed.
    DEBUG_INFO = ""
    data = UserData(CONFIG_DATA)
    if data.getDebug():
        TODAY = data.getToday()
        TOMORROW = data.getTomorrow()
        LASTUSE = data.getLastUse()
        STARTUSE = data.getStart()
        FROZEN = data.getFrozen()
        DEBUG_INFO += ("<br><span style='text-align:left;width:486px;display:block;margin-inline:1rem;'><b>Loaded Anki Streak Addon in Debug mode</b></span>")
        DEBUG_INFO_GRID_CONTENT = "".join([
            f"<span>TODAY:</span>", f"<span>{'-'.join(str(item) for item in TODAY.getYMD())}</span>",
            f"<span>CURRENT STREAK:</span>", f"<span>{data.getStreak()}</span>",
            f"<span>DEBUG MODE:</span>", f"<span>{data.getDebug()}</span>",
            f"<span>FROZEN DATE:</span>", f"<span>{'-'.join(str(item) for item in FROZEN.getYMD())}</span>",
            f"<span>TOMORROW:</span>", f"<span>{'-'.join(str(item) for item in TOMORROW.getYMD())}</span>",
            f"<span>STARTUSE:</span>", f"<span>{'-'.join(str(item) for item in STARTUSE.getYMD())}</span>",
            f"<span>LASTUSE:</span>", f"<span>{'-'.join(str(item) for item in LASTUSE.getYMD())}</span>",
            f"<span>__NAME__</span>", f"<span>{__name__}</span>"
        ])
        DEBUG_INFO_GRID = f'<br><style>.debug-grid {{display:grid;grid-template-columns:1fr 1fr;max-width:486px;margin:1rem;text-align:left;}}</style><div class="debug-grid">{DEBUG_INFO_GRID_CONTENT}</div>'
        DEBUG_INFO += DEBUG_INFO_GRID
        
    #Builds the core part of the application  
    current_streak:int  
    if data._streak: 
        current_streak = data.getStreak()
    else: 
        current_streak = 0
    frozen_date = CalenderDate([2000, 1, 1])
    if data._frozen:
        frozen_date = data._frozen
    streak = BuildDisplay('styles.css', 'fire.png', 'streak.js', current_streak, frozen_date)
    
    #Displays the content.
    content.stats += streak.core(data.getDebug())
    
    #Adds the freeze btn
    '''freezeBtn = QAction("Freeze Tomorrow", mw)
    qconnect(freezeBtn.triggered, data.freezeTomorrow)
    mw.form.menuaddWidget(freezeBtn)'''
    #Adds any debug info to the main screen instead of throwing something that would cause a crash.
    
    content.stats += DEBUG_INFO
    CONTENT = content.stats
    
#Handles any button clicked events.
def handleButtons(handled, msg, ctxt):
    if msg == "freeze-tomorrow":
        data = UserData(CONFIG_DATA)
        data.setFreeze()
        # Has to return something so Anki doesn't think there was an error.
        return (True, None)
    else:
        #Auto passed by Anki.
        return handled
    
    
if __name__ != "__main__":
    # CONFIG_DATA has to be loaded before the main function intializes or things will fail to work
    CONFIG_DATA = mw.addonManager.getConfig(__name__)
    # Gets permission to access png, css, and js files needed for the addon to work.
    mw.addonManager.setWebExports(__name__, r'.+\.(png|css|js)')
    # When Anki renders the main menu, it will connect the main function to part of it's executed methods.
    gui_hooks.deck_browser_will_render_content.append(main)
    #When a button is pressed, Anki will send a JS message. 
    #When it detects one, the function "handleButtons" will handle it.
    gui_hooks.webview_did_receive_js_message.append(handleButtons)
    