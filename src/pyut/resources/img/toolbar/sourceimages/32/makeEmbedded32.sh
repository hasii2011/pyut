#!/usr/bin/env bash


pip3 list > /dev/null 2>&1
STATUS=$?

#if [[ ${STATUS} -ne 0 ]] ; then
#    echo "You are not in a virtual environment"
#    exit 1

img2py -n embeddedImage -i ToolboxActor.png                     ../../embedded32/ImgToolboxActor.py
img2py -n embeddedImage -i ToolboxArrow.png                     ../../embedded32/ImgToolboxArrow.py
img2py -n embeddedImage -i ToolboxClass.png                     ../../embedded32/ImgToolboxClass.py
img2py -n embeddedImage -i ToolboxNewClassDiagram.png           ../../embedded32/ImgToolboxNewClassDiagram.py
img2py -n embeddedImage -i ToolboxNewProject.png                ../../embedded32/ImgToolboxNewProject.py
img2py -n embeddedImage -i ToolboxNewSequenceDiagram.png        ../../embedded32/ImgToolboxNewSequenceDiagram.py
img2py -n embeddedImage -i ToolboxNewUseCaseDiagram.png         ../../embedded32/ImgToolboxNewUseCaseDiagram.py
img2py -n embeddedImage -i ToolboxNote.png                      ../../embedded32/ImgToolboxNote.py
img2py -n embeddedImage -i ToolboxOpenFile.png                  ../../embedded32/ImgToolboxOpenFile.py
img2py -n embeddedImage -i ToolboxRedo.png                      ../../embedded32/ImgToolboxRedo.py
img2py -n embeddedImage -i ToolboxRelationshipAggregation.png   ../../embedded32/ImgToolboxRelationshipAggregation.py
img2py -n embeddedImage -i ToolboxRelationshipAssociation.png   ../../embedded32/ImgToolboxRelationshipAssociation.py
img2py -n embeddedImage -i ToolboxRelationshipComposition.png   ../../embedded32/ImgToolboxRelationshipComposition.py
img2py -n embeddedImage -i ToolboxRelationshipInheritance.png   ../../embedded32/ImgToolboxRelationshipInheritance.py
img2py -n embeddedImage -i ToolboxRelationshipNote.png          ../../embedded32/ImgToolboxRelationshipNote.py
img2py -n embeddedImage -i ToolboxRelationshipRealization.png   ../../embedded32/ImgToolboxRelationshipRealization.py
img2py -n embeddedImage -i ToolboxSaveDiagram.png               ../../embedded32/ImgToolboxSaveDiagram.py
img2py -n embeddedImage -i ToolboxSequenceDiagramInstance.png   ../../embedded32/ImgToolboxSequenceDiagramInstance.py
img2py -n embeddedImage -i ToolboxSequenceDiagramMessage.png    ../../embedded32/ImgToolboxSequenceDiagramMessage.py
img2py -n embeddedImage -i ToolboxText.png                      ../../embedded32/ImgToolboxText.py
img2py -n embeddedImage -i ToolboxUndo.png                      ../../embedded32/ImgToolboxUndo.py
img2py -n embeddedImage -i ToolboxUseCase.png                   ../../embedded32/ImgToolboxUseCase.py
img2py -n embeddedImage -i ToolboxZoomIn.png                    ../../embedded32/ImgToolboxZoomIn.py
img2py -n embeddedImage -i ToolboxZoomOut.png                   ../../embedded32/ImgToolboxZoomOut.py


