import QtQuick

QtObject {
    property bool dragging: false
    property int pieceID: -1
    property int startIndex: -1
    property var dragPiece

    function startDragging(ID, start) {
        dragging = true
        pieceID = ID
        startIndex = start
    }

    function stopDragging() {
        dragging = false
    }
}