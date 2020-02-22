from enum import Enum


class OglLinkType(Enum):
    """
     Types of OGL Links

     TODO:  No such thing as Ogl Link type;  Link types are embedded only the PyutData model; So
            this enumeration should be part of the data model and named accordingly
    """
    OGL_ASSOCIATION = 0
    OGL_AGGREGATION = 1
    OGL_COMPOSITION = 2
    OGL_INHERITANCE = 3
    OGL_INTERFACE   = 4
    OGL_NOTELINK    = 5
    OGL_SD_MESSAGE  = 6

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.name

    @staticmethod
    def toEnum(strValue: str) -> 'OglLinkType':
        """
        Converts the input string to the link type enum
        Args:
            strValue:   The serialized string representation

        Returns:  The visibility enumeration
        """
        canonicalStr: str = strValue.lower().strip(' ')
        if canonicalStr == 'ogl_association':
            return OglLinkType.OGL_ASSOCIATION
        elif canonicalStr == 'ogl_aggregation':
            return OglLinkType.OGL_AGGREGATION
        elif canonicalStr == 'ogl_composition':
            return OglLinkType.OGL_COMPOSITION
        elif canonicalStr == 'ogl_inheritance':
            return OglLinkType.OGL_INHERITANCE
        elif canonicalStr == 'ogl_interface':
            return OglLinkType.OGL_INTERFACE
        elif canonicalStr == 'ogl_notelink':
            return OglLinkType.OGL_NOTELINK
        elif canonicalStr == 'ogl_sd_message':
            return OglLinkType.OGL_SD_MESSAGE
        else:
            print(f'Warning: did not recognize this link type: {canonicalStr}')
            return OglLinkType.OGL_ASSOCIATION
