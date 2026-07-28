import QtQuick
import QtQuick.Layouts


GridLayout {
    anchors.centerIn: parent

    id: board

    rows: 8
    columns: 8
    rowSpacing: 0
    columnSpacing: 0

    property var pieceComponent
    property var window

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

    function addPiece (piece) {
        var boardPos = board.mapToItem(window.contentItem, 0, 0)

        var centerX = piece.x + piece.width / 2
        var centerY = piece.y + piece.height / 2

        if (((centerX > boardPos.x) && (centerX < (boardPos.x + board.width))) && ((centerY > boardPos.y) && (centerY < (boardPos.y + board.height)))) {
            var newPiece = pieceComponent.createObject(window)

            var row = Math.floor((centerY - boardPos.y) / 120)
            var col = Math.floor((centerX - boardPos.x) / 120)

            console.log(row)
            console.log(col)

            newPiece.dir = piece.dir
            newPiece.x = (col * 120) + 15 + boardPos.x - 1
            newPiece.y = (row * 120) + 15 + boardPos.y - 1 // 15 is the board offsets for the outline. I do not know how to get it through member access.
        }
    }
}