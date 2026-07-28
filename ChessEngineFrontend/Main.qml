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
    property int startX: 500
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
            pieceComponent: pieceComponent
            window: window
        }
    }

    Component.onCompleted: {
        var bB = pieceComponent.createObject(window)
        bB.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/blackBishop.png"
        bB.x = startX
        bB.y = startY
        bB.board = board

        var bKn = pieceComponent.createObject(window)
        bKn.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/blackKnight.png"
        bKn.x = startX
        bKn.y = startY + offset
        bKn.board = board

        var bR = pieceComponent.createObject(window)
        bR.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/blackRook.png"
        bR.x = startX
        bR.y = startY + offset * 2
        bR.board = board

        var bP = pieceComponent.createObject(window)
        bP.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/blackPawn.png"
        bP.x = startX
        bP.y = startY + offset * 3
        bP.board = board

        var bK = pieceComponent.createObject(window)
        bK.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/blackKing.png"
        bK.x = startX
        bK.y = startY + offset * 4
        bK.board = board

        var bQ = pieceComponent.createObject(window)
        bQ.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/blackQueen.png"
        bQ.x = startX
        bQ.y = startY + offset * 5
        bQ.board = board

        var wK = pieceComponent.createObject(window)
        wK.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/whiteKing.png"
        wK.x = startX + 1500
        wK.y = startY + offset * 4
        wK.board = board

        var draggedPiece = draggedPieceComponent.createObject(window)
        draggedPiece.visible = false

        bB.dragged = draggedPiece
        bKn.dragged = draggedPiece
        bR.dragged = draggedPiece
        bP.dragged = draggedPiece
        bK.dragged = draggedPiece
        bQ.dragged = draggedPiece
        wK.dragged = draggedPiece
   }
}
