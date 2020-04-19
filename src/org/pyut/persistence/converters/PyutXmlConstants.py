
class PyutXmlConstants:
    """
    A `no method` class that just hosts the strings that represent the Pyut XML strings
    """

    TOP_LEVEL_ELEMENT:           str = 'PyutProject'
    ELEMENT_GRAPHIC_CLASS:       str = 'GraphicClass'
    ELEMENT_GRAPHIC_NOTE:        str = 'GraphicNote'
    ELEMENT_GRAPHIC_ACTOR:       str = 'GraphicActor'
    ELEMENT_GRAPHIC_USE_CASE:    str = 'GraphicUseCase'
    ELEMENT_GRAPHIC_LINK:        str = 'GraphicLink'
    ELEMENT_GRAPHIC_SD_INSTANCE: str = 'GraphicSDInstance'
    ELEMENT_GRAPHIC_SD_MESSAGE:  str = 'GraphicSDMessage'

    ELEMENT_DOCUMENT:          str = 'PyutDocument'
    ELEMENT_MODEL_CLASS:       str = 'Class'
    ELEMENT_MODEL_METHOD:      str = 'Method'
    ELEMENT_MODEL_NOTE:        str = 'Note'
    ELEMENT_MODEL_ACTOR:       str = 'Actor'
    ELEMENT_MODEL_USE_CASE:    str = 'UseCase'
    ELEMENT_MODEL_LINK:        str = 'Link'
    ELEMENT_MODEL_FIELD:       str = 'Field'
    ELEMENT_MODEL_PARAM:       str = 'Param'
    ELEMENT_MODEL_RETURN:      str = 'Return'
    ELEMENT_MODEL_MODIFIER:    str = 'Modifier'

    ELEMENT_MODEL_SD_INSTANCE:   str = 'SDInstance'
    ELEMENT_MODEL_SD_MESSAGE:    str = 'SDMessage'
    ELEMENT_MODEL_CONTROL_POINT: str = 'ControlPoint'

    ELEMENT_ASSOC_CENTER_LABEL:      str = 'LabelCenter'
    ELEMENT_ASSOC_SOURCE_LABEL:      str = 'LabelSrc'
    ELEMENT_ASSOC_DESTINATION_LABEL: str = 'LabelDst'

    ATTR_VERSION: str = 'version'

    ATTR_ID: str = 'id'

    ATTR_WIDTH:  str = 'width'
    ATTR_HEIGHT: str = 'height'

    ATTR_X: str = 'x'
    ATTR_Y: str = 'y'

    ATTR_STEREOTYPE:  str = 'stereotype'
    ATTR_DESCRIPTION: str = 'description'
    ATTR_VISIBILITY:  str = 'visibility'

    ATTR_FILENAME: str = 'filename'
    ATTR_NAME:     str = 'name'
    ATTR_CONTENT:  str = 'content'
    ATTR_TYPE:     str = 'type'
    ATTR_TITLE:    str = 'title'

    ATTR_DEFAULT_VALUE:   str = 'defaultValue'
    ATTR_SHOW_STEREOTYPE: str = 'showStereotype'
    ATTR_SHOW_METHODS:    str = 'showMethods'
    ATTR_SHOW_FIELDS:     str = 'showFields'

    ATTR_LINK_SOURCE_ANCHOR_X: str = 'srcX'
    ATTR_LINK_SOURCE_ANCHOR_Y: str = 'srcY'

    ATTR_LINK_DESTINATION_ANCHOR_X: str = 'dstX'
    ATTR_LINK_DESTINATION_ANCHOR_Y: str = 'dstY'

    ATTR_SPLINE:        str = 'spline'
    ATTR_BIDIRECTIONAL: str = 'bidir'

    ATTR_SOURCE_ID:      str = 'sourceId'
    ATTR_DESTINATION_ID: str = 'destId'

    ATTR_CARDINALITY_SOURCE:      str = 'cardSrc'
    ATTR_CARDINALITY_DESTINATION: str = 'cardDestination'

    ATTR_INSTANCE_NAME:    str = 'instanceName'
    ATTR_LIFE_LINE_LENGTH: str = 'lifeLineLength'

    ATTR_MESSAGE:               str = 'message'
    ATTR_SOURCE_TIME_LINE:      str = 'srcTime'
    ATTR_DESTINATION_TIME_LINE: str = 'dstTime'

    ATTR_SD_MESSAGE_SOURCE_ID:      str = 'srcID'
    ATTR_SD_MESSAGE_DESTINATION_ID: str = 'dstID'

    V9_LINK_PREFIX: str = 'OGL_'

    ATTR_CODE_PATH: str = 'CodePath'

    ATTR_SCROLL_POSITION_X: str = 'scrollPositionX'
    ATTR_SCROLL_POSITION_Y: str = 'scrollPositionY'
    ATTR_PIXELS_PER_UNIT_X: str = 'pixelsPerUnitX'
    ATTR_PIXELS_PER_UNIT_Y: str = 'pixelsPerUnitY'
