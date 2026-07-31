#include "EngineManager.h"

#include <QObject>
#include <QDebug>
#include <QString>
#include <array>
#include <QVariant>
#include <QVariantList>

EngineManager::EngineManager(QObject *parent)
    : QObject(parent)
{
}

void EngineManager::findBestMove(const QVariantList& boardState) {
    std::array<int, 64> board;

    qDebug() << "EngineManager created";

    for (int i = 0; i < 64; i++) {
        board[i] = boardState[i].toInt();
    }

    qDebug() << board;
};