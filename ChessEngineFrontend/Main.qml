import QtQuick
import QtQuick.Layouts
import QtQuick.Controls.Basic


ApplicationWindow {
    id: window
    width: 2560
    height: 1440
    minimumWidth: 200
    minimumHeight: 250
    visible: true
    title: qsTr("Hello World")
    property bool lightMode: Application.styleHints.colorScheme === Qt.Light
    color: "lightgray"

    property int offset: 150
    property int startBX: 500
    property int startWX: 2060
    property int startY: 200

    Rectangle {
        id: boardBoarder

        x: 785
        y: 205

        width: 990
        height: 990

        color: "transparent"

        border.width: 15
        border.color: "gray"

        Component {
            id: placedPieceComponent

            PlacedPiece { }
        }

        Component {
            id: pieceComponent

            Piece { }
        }

        Component {
            id: draggedPieceComponent

            DraggedPiece { }
        }

        Board {
            id: board
            anchors.centerIn: parent
            placedPieceComponent: placedPieceComponent
            window: window
        }
    }

    Component.onCompleted: { // This section is entirely dedicated to creating the template pieces.
        var bB = pieceComponent.createObject(window)
        bB.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/blackBishop.png"
        bB.x = startBX
        bB.y = startY
        bB.board = board
        bB.pieceIndex = 11

        var bKn = pieceComponent.createObject(window)
        bKn.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/blackKnight.png"
        bKn.x = startBX
        bKn.y = startY + offset
        bKn.board = board
        bKn.pieceIndex = 10

        var bR = pieceComponent.createObject(window)
        bR.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/blackRook.png"
        bR.x = startBX
        bR.y = startY + offset * 2
        bR.board = board
        bR.pieceIndex = 9

        var bP = pieceComponent.createObject(window)
        bP.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/blackPawn.png"
        bP.x = startBX
        bP.y = startY + offset * 3
        bP.board = board
        bP.pieceIndex = 1

        var bK = pieceComponent.createObject(window)
        bK.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/blackKing.png"
        bK.x = startBX
        bK.y = startY + offset * 4
        bK.board = board
        bK.pieceIndex = 13

        var bQ = pieceComponent.createObject(window)
        bQ.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/blackQueen.png"
        bQ.x = startBX
        bQ.y = startY + offset * 5
        bQ.board = board
        bQ.pieceIndex = 12


        var wB = pieceComponent.createObject(window)
        wB.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/whiteBishop.png"
        wB.x = startWX
        wB.y = startY
        wB.board = board
        wB.pieceIndex = 27

        var wKn = pieceComponent.createObject(window)
        wKn.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/whiteKnight.png"
        wKn.x = startWX
        wKn.y = startY + offset
        wKn.board = board
        wKn.pieceIndex = 26

        var wR = pieceComponent.createObject(window)
        wR.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/whiteRook.png"
        wR.x = startWX
        wR.y = startY + offset * 2
        wR.board = board
        wR.pieceIndex = 25

        var wP = pieceComponent.createObject(window)
        wP.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/whitePawn.png"
        wP.x = startWX
        wP.y = startY + offset * 3
        wP.board = board
        wP.pieceIndex = 17

        var wK = pieceComponent.createObject(window)
        wK.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/whiteKing.png"
        wK.x = startWX
        wK.y = startY + offset * 4
        wK.board = board
        wK.pieceIndex = 29

        var wQ = pieceComponent.createObject(window)
        wQ.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/whiteQueen.png"
        wQ.x = startWX
        wQ.y = startY + offset * 5
        wQ.board = board
        wQ.pieceIndex = 28


        var draggedPiece = draggedPieceComponent.createObject(window)
        draggedPiece.visible = false
        draggedPiece.z = 1000 // simply makes draggedPiece show above every other object.

        bB.dragged = draggedPiece
        bKn.dragged = draggedPiece
        bR.dragged = draggedPiece
        bP.dragged = draggedPiece
        bK.dragged = draggedPiece
        bQ.dragged = draggedPiece

        wB.dragged = draggedPiece
        wKn.dragged = draggedPiece
        wR.dragged = draggedPiece
        wP.dragged = draggedPiece
        wK.dragged = draggedPiece
        wQ.dragged = draggedPiece


        board.resetPiecePositions()
   }
}
