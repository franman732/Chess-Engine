import QtQuick

Image {
    property string dir

    source: dir
    id: dragged

//    x: 1000
//    y: 50

    // Optional layout properties
    width: 96
    height: 96
    fillMode: Image.PreserveAspectFit
}