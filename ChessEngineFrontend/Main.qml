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

    property var draggedPiece
    property var draggedPiece2

    Button {
           text: "Determine Best Move"
           font.pointSize: 15

           palette.button: "white"

           height: 50
           width: 300

           x: boardBoarder.x + boardBoarder.width + 50
           y: boardBoarder.y + boardBoarder.height - height

           // Handle the click event
           onClicked: {
               engineManager.findBestMove(board.buildCPPPieceList())
           }
       }

    Text {
        id: bestMoveText

        font.pointSize: 15

        height: 50
        width: 300

        text: engineManager.bestMove

        x: boardBoarder.x + boardBoarder.width + 50
        y: boardBoarder.y + boardBoarder.height - height - 100 // 50 is just there for the gap

       // Text: "Best Move: "
    }

    Text {
        id: bestEvalText

        font.pointSize: 15

        height: 50
        width: 300

        text: engineManager.bestEval

        x: boardBoarder.x + boardBoarder.width + 50
        y: boardBoarder.y + boardBoarder.height - height - 50 // 50 is just there for the gap

        //Text: "Best Eval: "
    }

    Rectangle {
        id: boardBoarder

        x: 795
        y: 165

        width: 1050
        height: 1050

        color: "transparent"

        border.width: 60
        border.color: "gray"

        property var textLabels: ["a", "b", "c", "d", "e", "f", "g", "h"]
        property var numLabels: ["8", "7", "6", "5", "4", "3", "2", "1"]

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

        Repeater {
            model: 8

            Text {
                    text: boardBoarder.textLabels[index]

                    font.pixelSize: 30
                    x: 60 + (120 * index) + 45 - (width / 2)
                    y: 960 + 8 + 45 - (height / 4)
                    z: 75

                    color: "white"
            }
        }

        Repeater {
            model: 8

            Text {
                    text: boardBoarder.numLabels[index]

                    font.pixelSize: 30
                    x: 23 - (width / 2)
                    y: 45 + 60 + (120 * index) - (height / 2)
                    z: 75

                    color: "white"
            }
        }
    }

    Rectangle {
            id: wPTs

            width: 890
            height: 125

            x: boardBoarder.x + (boardBoarder.width - width) / 2
            y: window.height - 25 - height

            color: "gray"

            property int topAndBottomGap: 10
            property int sideGap: 20

            property real squareWidth: (width - sideGap * 6) / 5
            property real squareHeight: height - topAndBottomGap * 2

            Repeater {
                model: 5

                Rectangle {
                    width: wPTs.squareWidth
                    height: wPTs.squareHeight

                    x: wPTs.sideGap * (index + 1)
                       + wPTs.squareWidth * index

                    y: wPTs.topAndBottomGap

                    color: "lightGray"
                }
            }

            Component.onCompleted: {
                    var wP = pieceComponent.createObject(wPTs)
                    wP.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/whitePawn.png"
                    wP.x = wPTs.sideGap + squareWidth / 2 - (wP.width / 2)
                    wP.y = wPTs.topAndBottomGap + (wPTs.squareHeight - wP.height) / 2
                    wP.z = 50
                    wP.board = board
                    wP.pieceIndex = 17

                    var wKn = pieceComponent.createObject(wPTs)
                    wKn.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/whiteKnight.png"
                    wKn.x = wPTs.sideGap * 2 + squareWidth / 2 - (wKn.width / 2) + squareWidth
                    wKn.y = wPTs.topAndBottomGap + (wPTs.squareHeight - wKn.height) / 2
                    wKn.board = board
                    wKn.z = 50
                    wKn.pieceIndex = 26

                    var wB = pieceComponent.createObject(wPTs)
                    wB.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/whiteBishop.png"
                    wB.x = wPTs.sideGap * 3 + squareWidth / 2 - (wB.width / 2) + squareWidth * 2
                    wB.y = wPTs.topAndBottomGap + (wPTs.squareHeight - wB.height) / 2
                    wB.board = board
                    wB.z = 50
                    wB.pieceIndex = 27

                    var wR = pieceComponent.createObject(wPTs)
                    wR.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/whiteRook.png"
                    wR.x = wPTs.sideGap * 4 + squareWidth / 2 - (wR.width / 2) + squareWidth * 3
                    wR.y = wPTs.topAndBottomGap + (wPTs.squareHeight - wR.height) / 2
                    wR.board = board
                    wR.z = 50
                    wR.pieceIndex = 25

                    var wQ = pieceComponent.createObject(wPTs)
                    wQ.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/whiteQueen.png"
                    wQ.x = wPTs.sideGap * 5 + squareWidth / 2 - (wQ.width / 2) + squareWidth * 4
                    wQ.y = wPTs.topAndBottomGap + (wPTs.squareHeight - wQ.height) / 2
                    wQ.board = board
                    wQ.z = 50
                    wQ.pieceIndex = 28

                    draggedPiece = draggedPieceComponent.createObject(window)
                    draggedPiece.visible = false

                    wP.dragged = draggedPiece
                    wKn.dragged = draggedPiece
                    wB.dragged = draggedPiece
                    wR.dragged = draggedPiece
                    wQ.dragged = draggedPiece
            }
    }

    Rectangle {
        id: bPTs

        x: boardBoarder.x + (boardBoarder.width - width) / 2
        y: 25

        width: 890
        height: 125

        color: "gray"

        property int topAndBottomGap: 10
        property int sideGap: 20

        property real squareWidth: (width - sideGap * 6) / 5
        property real squareHeight: height - topAndBottomGap * 2

        Repeater {
            model: 5

            Rectangle {
                width: bPTs.squareWidth
                height: bPTs.squareHeight

                x: bPTs.sideGap * (index + 1)
                   + bPTs.squareWidth * index

                y: bPTs.topAndBottomGap

                color: "lightGray"
            }
        }

        Component.onCompleted: {
                var bB = pieceComponent.createObject(bPTs)
                bB.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/blackBishop.png"
                bB.x = bPTs.sideGap + squareWidth / 2 - (bB.width / 2)
                bB.y = bPTs.topAndBottomGap + (bPTs.squareHeight - bB.height) / 2
                bB.board = board
                bB.z = 50
                bB.pieceIndex = 11

                var bKn = pieceComponent.createObject(bPTs)
                bKn.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/blackKnight.png"
                bKn.x = bPTs.sideGap * 2 + squareWidth / 2 - (bKn.width / 2) + squareWidth
                bKn.y = bPTs.topAndBottomGap + (bPTs.squareHeight - bKn.height) / 2
                bKn.board = board
                bKn.z = 50
                bKn.pieceIndex = 10

                var bR = pieceComponent.createObject(bPTs)
                bR.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/blackRook.png"
                bR.x = bPTs.sideGap * 3 + squareWidth / 2 - (bR.width / 2) + squareWidth * 2
                bR.y = bPTs.topAndBottomGap + (bPTs.squareHeight - bR.height) / 2
                bR.board = board
                bR.z = 50
                bR.pieceIndex = 9

                var bP = pieceComponent.createObject(bPTs)
                bP.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/blackPawn.png"
                bP.x = bPTs.sideGap * 4 + squareWidth / 2 - (bP.width / 2) + squareWidth * 3
                bP.y = bPTs.topAndBottomGap + (bPTs.squareHeight - bP.height) / 2
                bP.board = board
                bP.z = 50
                bP.pieceIndex = 1

                var bQ = pieceComponent.createObject(bPTs)
                bQ.dir = "qrc:/qt/qml/ChessEngineFrontend/pieceImages/blackQueen.png"
                bQ.x = bPTs.sideGap * 5 + squareWidth / 2 - (bQ.width / 2) + squareWidth * 4
                bQ.y = bPTs.topAndBottomGap + (bPTs.squareHeight - bQ.height) / 2
                bQ.board = board
                bQ.z = 50
                bQ.pieceIndex = 12

                draggedPiece2 = draggedPieceComponent.createObject(window)
                draggedPiece2.visible = false

                bB.dragged = draggedPiece2
                bKn.dragged = draggedPiece2
                bR.dragged = draggedPiece2
                bP.dragged = draggedPiece2
                bQ.dragged = draggedPiece2

                board.resetPiecePositions()
        }
    }
}
