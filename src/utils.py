#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__version__ = "$Revision: 1.4 $"
__author__ = "C.Dutoit"
__date__ = "2003-01-11"

"""
This file provides external PyUt utilities.

functions :
  - validateXML(xmlFile)

:author: C.Dutoit
:contact: <dutoitc@hotmail.com>
"""
import sys

from xml.parsers.xmlproc import xmlproc,dtdparser,utils,xmldtd


def validateXML(xmlFile):
    """
    Validate the given xml file.
    @author C.Dutoit
    """
    # Init
    parser=dtdparser.DTDParser()
    dtd = xmldtd.CompleteDTD(parser)
    parser.set_dtd_consumer(dtd)
    parser.set_error_handler(utils.ErrorPrinter(parser))

    # Parse
    parser.parse_resource(xmlFile)

validateXML(sys.argv[1])
