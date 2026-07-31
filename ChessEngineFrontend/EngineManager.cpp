#include "EngineManager.h"

#include <QObject>
#include <QDebug>
#include <QString>

EngineManager::EngineManager(QObject *parent)
    : QObject(parent)
{
}

void EngineManager::testPrint(QString testString) {
    qDebug() << "EngineManager created";
    qDebug() << "Test string: ";
    qDebug() << testString;
};