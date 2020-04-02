graph [
comment "This is a simple graph" directed 1
IsPlanar 1
node
[
    id	1
    label	"(279, 255)"
    graphics
    [
        x	279.0
        y	255.0
        w	10.0
        h	10.0
        type	"ellipse"
        fill	"#1F78B4"
        outline	"#000000"
    ]
    LabelGraphics
    [
        text	"(279, 255)"
        fontSize	12
        fontName	"Dialog"
        visible	0
        anchor	"c"
    ]
]
node
[
    id	2
    label	"(367, 255)"
    graphics
    [
        x	367.0
        y	255.0
        w	10.0
        h	10.0
        type	"ellipse"
        fill	"#1F78B4"
        outline	"#000000"
    ]
    LabelGraphics
    [
        text	"(367, 255)"
        fontSize	12
        fontName	"Dialog"
        visible	0
        anchor	"c"
    ]
]
node
[
    id	3
    label	"(1667, 255)"
    graphics
    [
        x	1667.0
        y	255.0
        w	10.0
        h	10.0
        type	"ellipse"
        fill	"#1F78B4"
        outline	"#000000"
    ]
    LabelGraphics
    [
        text	"(1667, 255)"
        fontSize	12
        fontName	"Dialog"
        visible	0
        anchor	"c"
    ]
]

edge [
    source 1
    target 2
    label "Edge from node 1 to node 2"
]
edge [
    source 2
    target 3
    label "Edge from node 2 to node 3"
]
edge [
source 3
target 1 label
"Edge from node 3 to node 1"
]
]
