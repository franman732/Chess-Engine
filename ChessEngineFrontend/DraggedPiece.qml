import QtQuick

Image {
    property string dir
    property int pieceIndex

    source: dir
    id: dragged

    z: 10000

//    x: 1000
//    y: 50

    // Optional layout properties
    width: 96
    height: 96
    fillMode: Image.PreserveAspectFit
}