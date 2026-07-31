#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include "EngineManager.h"

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    QQmlApplicationEngine engine;
    QObject::connect(
        &engine,
        &QQmlApplicationEngine::objectCreationFailed,
        &app,
        []() { QCoreApplication::exit(-1); },
        Qt::QueuedConnection);

    EngineManager testManager;

    engine.rootContext()->setContextProperty(
        "engineManager",
        &testManager
        );

    engine.loadFromModule("ChessEngineFrontend", "Main");

    return QGuiApplication::exec();
}
