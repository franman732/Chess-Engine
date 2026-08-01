#pragma once

#include <QObject>
#include <QString>
#include <QVariantList>
#include <QProcess>

class EngineManager : public QObject {
    Q_OBJECT

public:
    explicit EngineManager(QObject *parent = nullptr);

    Q_INVOKABLE void findBestMove(const QVariantList &boardState);

private:
    QProcess pythonProcess;
};