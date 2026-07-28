cmake_minimum_required(VERSION 3.16)

project(ChessEngineFrontend VERSION 0.1 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 REQUIRED COMPONENTS Quick)

qt_standard_project_setup(REQUIRES 6.10)

# Content of downloaded design from Figma to Qt or similar
if (EXISTS "${CMAKE_CURRENT_LIST_DIR}/importedcontent/CMakeLists.txt")
    add_subdirectory(${CMAKE_CURRENT_LIST_DIR}/importedcontent)
endif()

qt_add_executable(appChessEngineFrontend
    main.cpp
)

qt_add_qml_module(appChessEngineFrontend
    URI ChessEngineFrontend
    QML_FILES
        Main.qml

    RESOURCES
        pieceImages/blackBishop.png
        pieceImages/blackKnight.png
        pieceImages/blackRook.png
        pieceImages/blackPawn.png
        pieceImages/blackKing.png
        pieceImages/blackQueen.png

        pieceImages/whiteKing.png

        QML_FILES
        QML_FILES
        QML_FILES
        QML_FILES Piece.qml
        QML_FILES DraggedPiece.qml
        QML_FILES Board.qml
)

# Qt for iOS sets MACOSX_BUNDLE_GUI_IDENTIFIER automatically since Qt 6.1.
# If you are developing for iOS or macOS you should consider setting an
# explicit, fixed bundle identifier manually though.
set_target_properties(appChessEngineFrontend PROPERTIES
#    MACOSX_BUNDLE_GUI_IDENTIFIER com.example.appChessEngineFrontend
    MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
    MACOSX_BUNDLE_SHORT_VERSION_STRING ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}
    MACOSX_BUNDLE TRUE
    WIN32_EXECUTABLE TRUE
)

target_link_libraries(appChessEngineFrontend
    PRIVATE Qt6::Quick
)

install(TARGETS appChessEngineFrontend
    BUNDLE DESTINATION .
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
