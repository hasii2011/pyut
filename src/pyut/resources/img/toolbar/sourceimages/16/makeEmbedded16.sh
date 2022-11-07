#!/usr/bin/env bash


pip3 list > /dev/null 2>&1
STATUS=$?

#if [[ ${STATUS} -ne 0 ]] ; then
#    echo "You are not in a virtual environment"
#    exit 1

img2py -n embeddedImage -i ToolboxActor.png                     ../../embedded16/ImgToolboxActor.py
img2py -n embeddedImage -i ToolboxArrow.png                     ../../embedded16/ImgToolboxArrow.py
img2py -n embeddedImage -i ToolboxClass.png                     ../../embedded16/ImgToolboxClass.py
img2py -n embeddedImage -i ToolboxNewClassDiagram.png           ../../embedded16/ImgToolboxNewClassDiagram.py
img2py -n embeddedImage -i ToolboxNewProject.png                ../../embedded16/ImgToolboxNewProject.py
img2py -n embeddedImage -i ToolboxNewSequenceDiagram.png        ../../embedded16/ImgToolboxNewSequenceDiagram.py
img2py -n embeddedImage -i ToolboxNewUseCaseDiagram.png         ../../embedded16/ImgToolboxNewUseCaseDiagram.py
img2py -n embeddedImage -i ToolboxNote.png                      ../../embedded16/ImgToolboxNote.py
img2py -n embeddedImage -i ToolboxOpenFile.png                  ../../embedded16/ImgToolboxOpenFile.py
img2py -n embeddedImage -i ToolboxRedo.png                      ../../embedded16/ImgToolboxRedo.py
img2py -n embeddedImage -i ToolboxRelationshipAggregation.png   ../../embedded16/ImgToolboxRelationshipAggregation.py
img2py -n embeddedImage -i ToolboxRelationshipAssociation.png   ../../embedded16/ImgToolboxRelationshipAssociation.py
img2py -n embeddedImage -i ToolboxRelationshipComposition.png   ../../embedded16/ImgToolboxRelationshipComposition.py
img2py -n embeddedImage -i ToolboxRelationshipInheritance.png   ../../embedded16/ImgToolboxRelationshipInheritance.py
img2py -n embeddedImage -i ToolboxRelationshipNote.png          ../../embedded16/ImgToolboxRelationshipNote.py
img2py -n embeddedImage -i ToolboxRelationshipRealization.png   ../../embedded16/ImgToolboxRelationshipRealization.py
img2py -n embeddedImage -i ToolboxSaveDiagram.png               ../../embedded16/ImgToolboxSaveDiagram.py
img2py -n embeddedImage -i ToolboxSequenceDiagramInstance.png   ../../embedded16/ImgToolboxSequenceDiagramInstance.py
img2py -n embeddedImage -i ToolboxSequenceDiagramMessage.png    ../../embedded16/ImgToolboxSequenceDiagramMessage.py
img2py -n embeddedImage -i ToolboxText.png                      ../../embedded16/ImgToolboxText.py
img2py -n embeddedImage -i ToolboxUndo.png                      ../../embedded16/ImgToolboxUndo.py
img2py -n embeddedImage -i ToolboxUseCase.png                   ../../embedded16/ImgToolboxUseCase.py
img2py -n embeddedImage -i ToolboxZoomIn.png                    ../../embedded16/ImgToolboxZoomIn.py
img2py -n embeddedImage -i ToolboxZoomOut.png                   ../../embedded16/ImgToolboxZoomOut.py


