import QtQuick
import QtQuick.Layouts


GridLayout {
    anchors.centerIn: parent

    id: board

    rows: 8
    columns: 8
    rowSpacing: 0
    columnSpacing: 0
    z:10

    property var placedPieceComponent
    property var window

    property var piecePositions: ({})

    Repeater {
        model: 64

        Rectangle {
            required property int index

            width: 120
            height: 120

            property int row: Math.floor(index / 8)
            property int col: index % 8

            color: (row + col) % 2 === 0 ? "beige" : "green"
        }
    }

    function getCoordinates (pieceX, pieceY, piece) { // piece is the piece that I want to replicate. It is simply used to get width and height of the piece to center it properly.
        var boardPos = board.mapToItem(window.contentItem, 0, 0)

        var centerX = pieceX + piece.width / 2
        var centerY = pieceY + piece.height / 2

        var finalCoords = {x: -1, y: -1, i: -1}

        if (((centerX > boardPos.x) && (centerX < (boardPos.x + board.width))) && ((centerY > boardPos.y) && (centerY < (boardPos.y + board.height)))) {

            var row = Math.floor((centerY - boardPos.y) / 120)
            var col = Math.floor((centerX - boardPos.x) / 120)

            var newPieceX = (col * 120) + 15 + boardPos.x - 1
            var newPieceY = (row * 120) + 15 + boardPos.y - 1 // 15 is the board offsets for the outline. I do not know how to get it through member access, so I hard coded it.

            finalCoords.x = newPieceX
            finalCoords.y = newPieceY
            finalCoords.i = (col + (row * 8))
        } else {
            piece.visible = false
        }

        return finalCoords // If the piece is held off the board, or later over an existing piece, finalCoords = {-1, -1}. Otherwise it equals the final coordinates of the position.
    }

    function addPiece (index, piece) {
        piecePositions[index] = piece
    }

    function isCapturable_By (index, piece) { // index is the piece in piecePositions were checking to be captured by piece
        var capturedPiece = piecePositions[index]

        var capturedPieceColor = capturedPiece.pieceIndex >= 17 ? 1: 0
        var capturingPieceColor = piece.pieceIndex >= 17 ? 1: 0

        if (capturedPieceColor !== capturingPieceColor) {
            return true
        }
    }

    function printPieces() {
        console.log("=== Piece Positions ===")

        for (var key in piecePositions) {
            var piece = piecePositions[key]
            console.log(
                "Square", key,
                "Dir:", piece.dir,
                "Pos:", piece.x + ", " + piece.y
            )
        }

        console.log("=======================")
    }
}