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
    property string dir
    property int pieceIndex

    source: dir

    MouseArea {
        anchors.fill: parent

        onPressed: function(mouse) {
            var p = testImage.mapToItem(window.contentItem, mouse.x - 46, mouse.y - 46)

            dragged.visible = true
            dragged.x = p.x
            dragged.y = p.y
            dragged.dir = dir
            dragged.pieceIndex = pieceIndex
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
            var coordinates = board.getCoordinates(dragged.x, dragged.y, dragged)
            if (((coordinates.x !== -1) && (coordinates.y !== -1)) && (board.piecePositions[coordinates.i]?.pieceIndex !== 13) && (board.piecePositions[coordinates.i]?.pieceIndex !== 29)) {
                if (coordinates.i in board.piecePositions) {
                    board.piecePositions[coordinates.i].destroy()
                    delete board.piecePositions[coordinates.i]
                    console.log("WE ARE OVERRIDING in PIECE")
                    board.printPieces()
                }

                var newPiece = board.placedPieceComponent.createObject(window)
                newPiece.dir = dragged.dir
                newPiece.x = coordinates.x
                newPiece.y = coordinates.y
                newPiece.board = board
                newPiece.pieceIndex = pieceIndex
                board.addPiece(coordinates.i, newPiece)
                console.log("WE ARE CREATING NEW in PIECE")
                board.printPieces()

                newPiece.startCoordinates = coordinates
            }
        }
    }
}