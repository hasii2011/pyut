
from logging import Logger
from logging import getLogger

import gettext

import wx

from PyutPreferences import PyutPreferences
from org.pyut.PyutUtils import getErrorInfo

# Constants
DEFAULT_LANG = "en"
LANGUAGES = {
        DEFAULT_LANG: (
            "English",              wx.LANGUAGE_ENGLISH),
            "da": ("Danish",        wx.LANGUAGE_DANISH),
            "de": ("Deutsch",       wx.LANGUAGE_GERMAN),
            "eo": ("Esperanto",     wx.LANGUAGE_ESPERANTO),
            "es": ("Spanish",       wx.LANGUAGE_SPANISH),
            "fr": ("Francais",      wx.LANGUAGE_FRENCH),
            "id": ("Indonesian",    wx.LANGUAGE_INDONESIAN),
            "pl": ("Polish",        wx.LANGUAGE_POLISH),
            "ci": ("chinese-utf8",  wx.LANGUAGE_CHINESE_TRADITIONAL),
        }


def importLanguage():

    moduleLogger: Logger = getLogger(__name__)
    # Get language from preferences
    prefs = PyutPreferences()
    language = prefs['I18N']

    # Set default language?
    if language not in LANGUAGES:
        # Use default language
        language = DEFAULT_LANG

    # Set language for all application
    moduleLogger.info(f'Installing language <{language}>')
    try:
        # Latest test 20050308
        # langid=wx.LANGUAGE_CHINESE_TRADITIONAL
        wxLangID   = LANGUAGES[language][1]
        domain    = "Pyut"
        localedir = "src"  # "./locale"     TODO: look this up via a resource directory
        # print "langid=", wxLangID

        method = 0          # Really ?
        if method == 0:
            # Possibility to load all languages, then do an install on fly
            tr = gettext.translation(domain, localedir, languages=[language])
            # Python 3 update
            # tr.install(unicode=True)
            tr.install(True)
            # gettext.install(domain, localedir, unicode=True)
        elif method == 1:

            # Set locale for wxWidget
            loc = wx.Locale(wxLangID)
            loc.AddCatalogLookupPathPrefix(localedir)
            loc.AddCatalog(domain)

            # Set up python's gettext
            moduleLogger.info(f'Encoding name is {loc.GetCanonicalName()}')
            mytrans = gettext.translation(domain, localedir, [loc.GetCanonicalName()], fallback=True)
            mytrans.install(unicode=True)
    except (ValueError, Exception) as e:
        # If there has been a problem with i18n
        moduleLogger.error(f'Warning: problem with gettext, i18n not used.  Error: {e}')
        errMsg = getErrorInfo()
        moduleLogger.error(errMsg)


importLanguage()
# print "**************"
# print _("Untitled.put")
# print wx.GetTranslation("Untitled.put")
