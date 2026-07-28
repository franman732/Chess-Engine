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

    property var startCoordinates

    source: dir

    MouseArea {
        anchors.fill: parent

        onPressed: function(mouse) {
            startCoordinates = board.getCoordinates(placedPiece.x, placedPiece.y, placedPiece)

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
            var capturedPieceIndex = board.piecePositions[coordinates.i]?.pieceIndex ?? -1;

            if ((board.piecePositions[coordinates.i] !== placedPiece) && ((capturedPieceIndex !== 13) && (capturedPieceIndex !== 29))) {
                if (((coordinates.x !== -1) && (coordinates.y !== -1)) && (coordinates.i in board.piecePositions)) {
                    board.piecePositions[coordinates.i].destroy()
                    delete board.piecePositions[coordinates.i]
                    console.log("WE ARE OVERRIDING")
                    board.printPieces()
                }

                if ((coordinates.x !== -1) && (coordinates.y !== -1)) {
                    placedPiece.x = coordinates.x
                    placedPiece.y = coordinates.y
                    delete board.piecePositions[startCoordinates.i]
                    board.piecePositions[coordinates.i] = placedPiece
                }

                if ((coordinates.x === -1) && (coordinates.y === -1) && ((pieceIndex === 13) || (pieceIndex === 29))) {
                    placedPiece.x = startCoordinates.x
                    placedPiece.y = startCoordinates.y // This moves the king back to start position if it is dragged outside of the range of the board
                }
            } else {
                placedPiece.x = startCoordinates.x
                placedPiece.y = startCoordinates.y // This was just for fixing when you let go of the mouse while still on top of the same square, hence board.piecePositions[coordinates.i] !== placedPiece
            }
        }
    }
}
