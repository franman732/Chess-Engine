import QtQuick

Image {
    id: placedPiece


    // Optional layout properties
    width: 92
    height: 92
    z:500
    fillMode: Image.PreserveAspectFit

    property var board
    property var dir
    property int pieceIndex

    source: dir

    MouseArea {
        anchors.fill: parent

        onPressed: function(mouse) {
            var p = placedPiece.mapToItem(window.contentItem, mouse.x - 46, mouse.y - 46)
            placedPiece.x = p.x
            placedPiece.y = p.y
        }

        onPositionChanged: function(mouse) {
            if (pressed) {
                var p = placedPiece.mapToItem(window.contentItem, mouse.x, mouse.y)

                placedPiece.x = p.x - width / 2
                placedPiece.y = p.y - height / 2
            }
        }

        onReleased: {
            var coordinates = board.getCoordinates(placedPiece.x, placedPiece.y, placedPiece)

            if ((coordinates.x !== -1) && (coordinates.y !== -1)) {
                placedPiece.x = coordinates.x
                placedPiece.y = coordinates.y
            }
        }
    }
}
