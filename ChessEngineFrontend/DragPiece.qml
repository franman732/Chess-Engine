import QtQuick

Image {
    id: dragPiece

    visible: false

    width: 120
    height: 120

    z: 1000

    property int pieceID: -1
    property int startSquare: -1
}