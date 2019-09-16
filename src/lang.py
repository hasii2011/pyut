#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__  = "Laurent Burgbacher <lb@alawa.ch>"
__version__ = "$Revision: 1.14 $"
__date__    = "2001-07-29"

from PyutPreferences import *
import gettext

import wx


# Constants
DEFAULT_LANG = "en"
LANGUAGES = {
        DEFAULT_LANG: ("English", wx.LANGUAGE_ENGLISH),
        "da": ("Danish", wx.LANGUAGE_DANISH),
        "de": ("Deutsch", wx.LANGUAGE_GERMAN),
        "eo": ("Esperanto",wx.LANGUAGE_ESPERANTO),
        "es": ("Spanish", wx.LANGUAGE_SPANISH),
        "fr": ("Francais", wx.LANGUAGE_FRENCH),
        "id": ("Indonesian",wx.LANGUAGE_INDONESIAN),
        "pl": ("Polish", wx.LANGUAGE_POLISH),
        "ci": ("chinese-utf8", wx.LANGUAGE_CHINESE_TRADITIONAL),
        }

def importLanguage():
    # Get language from preferences
    prefs = PyutPreferences()
    language = prefs['I18N']

    # Set default language?
    if language not in LANGUAGES:
        # Use default language
        language = DEFAULT_LANG

    # Set language for all application
    print("Installing language <", language, ">")
    try:
        # Latest test 20050308
        #langid=wx.LANGUAGE_CHINESE_TRADITIONAL
        wxLangID = LANGUAGES[language][1]
        domain="Pyut"
        localedir="." #"./locale"
        #print "langid=", wxLangID

        method=0
        if method==0:
            # Possibility to load all languages, then do an install on fly
            tr = gettext.translation(domain, localedir, languages=[language])
            tr.install(unicode=True)
            #gettext.install(domain, localedir, unicode=True)
        elif method==1:

            # Set locale for wxWidget
            loc = wx.Locale(wxLangID)
            loc.AddCatalogLookupPathPrefix(localedir)
            loc.AddCatalog(domain)

            # Set up python's gettext
            print("Encoding name is ", loc.GetCanonicalName())
            mytrans = gettext.translation(domain, localedir,
                    [loc.GetCanonicalName()], fallback=True)
            mytrans.install(unicode=True)
            #import __builtin__
            #__builtin__.__dict__['_'] = lambda x:wx.GetTranslation(x).encode("UTF-8")
            #__builtin__.__dict__['_'] = wx.GetTranslation
            #print "importL=", _("Untitled.put")



            #gettext.install('Pyut', '.', unicode=True)
            #trad = gettext.translation("Pyut", ".", [language])
            #trad.install()
            #loc = wx.Locale(wx.LANGUAGE_CHINESE_TRADITIONAL)
            #loc.setLocale(locale.LC_ALL, 'ci')
            #gettext.translation("Pyut", ".", [language]).install()




            #gettext.translation("Pyut", ".", languages=[language]).install()

            #loc = wxLocale(wxLANGUAGE_POLISH)
            #loc.AddCatalog("pl/LC_MESSAGES/Pyut.mo")
            #print wxGetTranslation("Untitled.put")
            #_ = wxGetTranslation
            #import __builtin__
            #__builtin__.__dict__['_'] = _
    except:
        # If there has been a problem with i18n
        print("Warning: problem with gettext, i18n not used")
        import sys, traceback
        errMsg ="The following error occured : %s" % str(sys.exc_info()[1])
        errMsg += "\n\n---------------------------\n"
        if sys.exc_info()[0] is not None:
            errMsg += "Error : %s" % sys.exc_info()[0] + "\n"
        if sys.exc_info()[1] is not None:
            errMsg += "Msg   : %s" % sys.exc_info()[1] + "\n"
        if sys.exc_info()[2] is not None:
            errMsg += "Trace :\n"
            for el in traceback.extract_tb(sys.exc_info()[2]):
                errMsg = errMsg + str(el) + "\n"
        print(errMsg)

        # Redefining '_' function
        # def _(string):
        #     return unicode(string)

        ## Put function '_' in globals (builtin)
        # import __builtin__
        # __builtin__.__dict__['_'] = _

importLanguage()
#print "**************"
#print _("Untitled.put")
#print wx.GetTranslation("Untitled.put")
