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

    property real squareWidth: 120
    property real squareHeight: 120

    function getCoordinates (pieceX, pieceY, piece) { // piece is the piece that I want to replicate. It is simply used to get width and height of the piece to center it properly.
        var boardPos = board.mapToItem(window.contentItem, 0, 0)

        var centerX = pieceX + piece.width / 2
        var centerY = pieceY + piece.height / 2

        var finalCoords = {x: -1, y: -1, i: -1}

        if (((centerX > boardPos.x) && (centerX < (boardPos.x + board.width))) && ((centerY > boardPos.y) && (centerY < (boardPos.y + board.height)))) {

            var row = Math.floor((centerY - boardPos.y) / squareWidth)
            var col = Math.floor((centerX - boardPos.x) / squareHeight)

            var newPieceX = (col * squareWidth) + 15 + boardPos.x - 1
            var newPieceY = (row * squareHeight) + 15 + boardPos.y - 1 // 15 is the board offsets for the outline. I do not know how to get it through member access, so I hard coded it.

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

    function resetPiecePositions() {
        piecePositions = ({})
        var boardPos = board.mapToItem(window.contentItem, 0, 0)


        // this section creates the black starting pieces


        var p_BR1 = placedPieceComponent.createObject(window)
        p_BR1.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/blackRook.png"
        p_BR1.x = 15 + boardPos.x - 1
        p_BR1.y = 15 + boardPos.y - 1
        p_BR1.board = board
        p_BR1.pieceIndex = 9
        addPiece(0, p_BR1)

        var p_BK1 = placedPieceComponent.createObject(window)
        p_BK1.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/blackKnight.png"
        p_BK1.x = (1 * squareWidth) + 15 + boardPos.x - 1
        p_BK1.y = 15 + boardPos.y - 1
        p_BK1.board = board
        p_BK1.pieceIndex = 10
        addPiece(1, p_BK1)

        var p_BB1 = placedPieceComponent.createObject(window)
        p_BB1.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/blackBishop.png"
        p_BB1.x = (2 * squareWidth) + 15 + boardPos.x - 1
        p_BB1.y = 15 + boardPos.y - 1
        p_BB1.board = board
        p_BB1.pieceIndex = 11
        addPiece(2, p_BB1)

        var p_BQ = placedPieceComponent.createObject(window)
        p_BQ.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/blackQueen.png"
        p_BQ.x = (3 * squareWidth) + 15 + boardPos.x - 1
        p_BQ.y = 15 + boardPos.y - 1
        p_BQ.board = board
        p_BQ.pieceIndex = 12
        addPiece(3, p_BQ)

        var p_BK = placedPieceComponent.createObject(window)
        p_BK.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/blackKing.png"
        p_BK.x = (4 * squareWidth) + 15 + boardPos.x - 1
        p_BK.y = 15 + boardPos.y - 1
        p_BK.board = board
        p_BK.pieceIndex = 13
        addPiece(4, p_BK)

        var p_BB2 = placedPieceComponent.createObject(window)
        p_BB2.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/blackBishop.png"
        p_BB2.x = (5 * squareWidth) + 15 + boardPos.x - 1
        p_BB2.y = 15 + boardPos.y - 1
        p_BB2.board = board
        p_BB2.pieceIndex = 11
        addPiece(5, p_BB2)

        var p_BK2 = placedPieceComponent.createObject(window)
        p_BK2.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/blackKnight.png"
        p_BK2.x = (6 * squareWidth) + 15 + boardPos.x - 1
        p_BK2.y = 15 + boardPos.y - 1
        p_BK2.board = board
        p_BK2.pieceIndex = 10
        addPiece(6, p_BK2)

        var p_BR2 = placedPieceComponent.createObject(window)
        p_BR2.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/blackRook.png"
        p_BR2.x = (7 * squareWidth) + 15 + boardPos.x - 1
        p_BR2.y = 15 + boardPos.y - 1
        p_BR2.board = board
        p_BR2.pieceIndex = 9
        addPiece(7, p_BR2)

        for (var i = 0; i < 8; i++) {
            var p_BP = placedPieceComponent.createObject(window)
            p_BP.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/blackPawn.png"
            p_BP.x = (i * squareWidth) + 15 + boardPos.x - 1
            p_BP.y = squareHeight + 15 + boardPos.y - 1
            p_BP.board = board
            p_BP.pieceIndex = 1
            addPiece(i + 8, p_BP)
        }


        // This next section creates the white starting pieces


        var p_WR1 = placedPieceComponent.createObject(window)
        p_WR1.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/whiteRook.png"
        p_WR1.x = 15 + boardPos.x - 1
        p_WR1.y = (7 * squareHeight) + 15 + boardPos.y - 1
        p_WR1.board = board
        p_WR1.pieceIndex = 25
        addPiece(56, p_WR1)

        var p_WK1 = placedPieceComponent.createObject(window)
        p_WK1.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/whiteKnight.png"
        p_WK1.x = (1 * squareWidth) + 15 + boardPos.x - 1
        p_WK1.y = (7 * squareHeight) + 15 + boardPos.y - 1
        p_WK1.board = board
        p_WK1.pieceIndex = 26
        addPiece(57, p_BK1)

        var p_WB1 = placedPieceComponent.createObject(window)
        p_WB1.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/whiteBishop.png"
        p_WB1.x = (2 * squareWidth) + 15 + boardPos.x - 1
        p_WB1.y = (7 * squareHeight) + 15 + boardPos.y - 1
        p_WB1.board = board
        p_WB1.pieceIndex = 27
        addPiece(58, p_WB1)

        var p_WQ = placedPieceComponent.createObject(window)
        p_WQ.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/whiteQueen.png"
        p_WQ.x = (3 * squareWidth) + 15 + boardPos.x - 1
        p_WQ.y = (7 * squareHeight) + 15 + boardPos.y - 1
        p_WQ.board = board
        p_WQ.pieceIndex = 28
        addPiece(59, p_WQ)

        var p_WK = placedPieceComponent.createObject(window)
        p_WK.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/whiteKing.png"
        p_WK.x = (4 * squareWidth) + 15 + boardPos.x - 1
        p_WK.y = (7 * squareHeight) + 15 + boardPos.y - 1
        p_WK.board = board
        p_WK.pieceIndex = 29
        addPiece(60, p_WK)

        var p_WB2 = placedPieceComponent.createObject(window)
        p_WB2.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/whiteBishop.png"
        p_WB2.x = (5 * squareWidth) + 15 + boardPos.x - 1
        p_WB2.y = (7 * squareHeight) + 15 + boardPos.y - 1
        p_WB2.board = board
        p_WB2.pieceIndex = 27
        addPiece(61, p_WB2)

        var p_WK2 = placedPieceComponent.createObject(window)
        p_WK2.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/whiteKnight.png"
        p_WK2.x = (6 * squareWidth) + 15 + boardPos.x - 1
        p_WK2.y = (7 * squareHeight) + 15 + boardPos.y - 1
        p_WK2.board = board
        p_WK2.pieceIndex = 26
        addPiece(62, p_WK2)

        var p_WR2 = placedPieceComponent.createObject(window)
        p_WR2.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/whiteRook.png"
        p_WR2.x = (7 * squareWidth) + 15 + boardPos.x - 1
        p_WR2.y = (7 * squareHeight) + 15 + boardPos.y - 1
        p_WR2.board = board
        p_WR2.pieceIndex = 25
        addPiece(63, p_WR2)

        for (var j = 0; j < 8; j++) {
            var p_WP = placedPieceComponent.createObject(window)
            p_WP.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/whitePawn.png"
            p_WP.x = (j * squareWidth) + 15 + boardPos.x - 1
            p_WP.y = (6 * squareHeight) + 15 + boardPos.y - 1
            p_WP.board = board
            p_WP.pieceIndex = 17
            addPiece(j + 48, p_WP)
        }
    }
}