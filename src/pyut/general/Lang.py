
from logging import Logger
from logging import getLogger

from os import sep as osSep

import gettext

from wx import LANGUAGE_CHINESE_TRADITIONAL
from wx import LANGUAGE_DANISH
from wx import LANGUAGE_ENGLISH
from wx import LANGUAGE_ESPERANTO
from wx import LANGUAGE_FRENCH
from wx import LANGUAGE_GERMAN
from wx import LANGUAGE_INDONESIAN
from wx import LANGUAGE_POLISH
from wx import LANGUAGE_SPANISH
from wx import Locale

from pyut.preferences.PyutPreferences import PyutPreferences
from pyut.PyutUtils import PyutUtils

from pyut.errorcontroller.ErrorManager import ErrorManager

# Constants
DEFAULT_LANG = "en"
LANGUAGES = {
        DEFAULT_LANG: (
            "English",              LANGUAGE_ENGLISH),
            "da": ("Danish",        LANGUAGE_DANISH),
            "de": ("Deutsch",       LANGUAGE_GERMAN),
            "eo": ("Esperanto",     LANGUAGE_ESPERANTO),
            "es": ("Spanish",       LANGUAGE_SPANISH),
            "fr": ("Francais",      LANGUAGE_FRENCH),
            "id": ("Indonesian",    LANGUAGE_INDONESIAN),
            "pl": ("Polish",        LANGUAGE_POLISH),
            "ci": ("chinese-utf8",  LANGUAGE_CHINESE_TRADITIONAL),
        }


class Lang:

    LOCALE_DIRECTORY: str = f'{PyutUtils.RESOURCES_PATH}{osSep}locale'

    @staticmethod
    def importLanguage():

        moduleLogger: Logger = getLogger(__name__)
        prefs: PyutPreferences = PyutPreferences()
        language = prefs.i18n

        if language not in LANGUAGES:
            language = DEFAULT_LANG

        # Set the language for the application
        moduleLogger.debug(f'Installing language <{language}>')
        try:
            wxLangID:     int  = LANGUAGES[language][1]
            domain:       str = "Pyut"
            orgDirectory: str = prefs.orgDirectory

            moduleLogger.debug(f'orgDirectory: {orgDirectory}')

            localedir: str = f'{orgDirectory}{osSep}{Lang.LOCALE_DIRECTORY}'
            method = 1          # Really ?
            if method == 0:
                # Possibility to load all languages, then do an install on the fly
                tr = gettext.translation(domain, localedir, languages=[language])
                tr.install(True)    # type: ignore
            elif method == 1:
                # Set locale for wxWidget
                loc = Locale(wxLangID)
                loc.AddCatalogLookupPathPrefix(localedir)
                loc.AddCatalog(domain)

                moduleLogger.info(f'Encoding name is {loc.GetCanonicalName()}')
                myTrans = gettext.translation(domain, localedir, [loc.GetCanonicalName()], fallback=True)
                myTrans.install()
        except (ValueError, Exception) as e:
            # If there has been a problem with i18n
            moduleLogger.error(f'Problem with language setting.  Error: {e}')
            errMsg = ErrorManager.getErrorInfo()
            moduleLogger.error(errMsg)
