from enum import Enum


class Action(Enum):

    SELECTOR             = 'Selector'
    NEW_CLASS            = 'NewClass'
    NEW_ACTOR            = 'NewActor'
    NEW_USECASE          = 'NewUseCase'
    NEW_NOTE             = 'NewNote'
    NEW_IMPLEMENT_LINK   = 'NewImplementLink'
    NEW_INTERFACE        = 'NewInterface'
    NEW_INHERIT_LINK     = 'NewInheritLink'
    NEW_AGGREGATION_LINK = 'NewAggregationLink',
    NEW_COMPOSITION_LINK = 'NewCompositionLink'
    NEW_ASSOCIATION_LINK = 'NewAssociationLink'
    NEW_NOTE_LINK        = 'NewNoteLink'
    NEW_TEXT             = 'NewText'

    DESTINATION_IMPLEMENT_LINK   = 'DestinationImplementLink'
    DESTINATION_INHERIT_LINK     = 'DestinationInheritLink'
    DESTINATION_AGGREGATION_LINK = 'DestinationAggregationLink'
    DESTINATION_COMPOSITION_LINK = 'DestinationCompositionLink'
    DESTINATION_ASSOCIATION_LINK = 'DestinationAssociationLink'
    DESTINATION_NOTE_LINK        = 'DestinationNoteLink'
    NEW_SD_INSTANCE              = 'NewSDInstance'
    NEW_SD_MESSAGE               = 'NewSDMessage'
    DESTINATION_SD_MESSAGE       = 'DestinationSDMessage'
    ZOOM_IN                      = 'ZoomIn'
    ZOOM_OUT                     = 'ZoomOut'
    NO_ACTION                    = 'NoAction'

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.name

