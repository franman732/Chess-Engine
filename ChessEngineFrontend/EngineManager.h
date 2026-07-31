#pragma once

#include <QObject>
#include <QString>

class EngineManager : public QObject {
    Q_OBJECT

public:
    explicit EngineManager(QObject *parent = nullptr);

    Q_INVOKABLE void testPrint(QString testString);
};