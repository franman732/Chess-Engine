#pragma once

#include <QObject>
#include <QString>
#include <QVariantList>
#include <QProcess>

class EngineManager : public QObject {
    Q_OBJECT

    Q_PROPERTY(QString bestMove
               READ getBestMove
               NOTIFY bestMoveChanged)

    Q_PROPERTY(double bestEval
               READ getBestEval
               NOTIFY bestEvalChanged)

public:
    explicit EngineManager(QObject *parent = nullptr);

    Q_INVOKABLE void findBestMove(const QVariantList &boardState);

    QString getBestMove() const
    {
        return bestMoveVar;
    }

    double getBestEval() const
    {
        return bestEvalVar;
    }

signals:
    void bestMoveChanged();
    void bestEvalChanged();

private:
    QProcess pythonProcess;

    QString bestMoveVar = "";
    double bestEvalVar = 0;
};