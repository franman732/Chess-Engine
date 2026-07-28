import QtQuick

Image {
    id: testImage

//    x: 1000
//    y: 50

    // Optional layout properties
    width: 92
    height: 92
    fillMode: Image.PreserveAspectFit

    property var dragged
    property var board
    property var dir

    source: dir

    MouseArea {
        anchors.fill: parent

        onPressed: function(mouse) {
            var p = testImage.mapToItem(window.contentItem, mouse.x - 46, mouse.y - 46)

            dragged.visible = true
            dragged.x = p.x
            dragged.y = p.y
            dragged.dir = dir
        }

        onPositionChanged: function(mouse) {
                if (pressed) {
                    var p = testImage.mapToItem(window.contentItem, mouse.x, mouse.y)

                    dragged.x = p.x - dragged.width / 2
                    dragged.y = p.y - dragged.height / 2
                }
            }

        onReleased: {
            dragged.visible = false
            board.addPiece(dragged)
        }
    }
}