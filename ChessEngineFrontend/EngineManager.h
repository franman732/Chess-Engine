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

    Q_PROPERTY(QString bestEval
               READ getBestEval
               NOTIFY bestEvalChanged)

public:
    explicit EngineManager(QObject *parent = nullptr);

    Q_INVOKABLE void findBestMove(const QVariantList &boardState);

    QString getBestMove() const
    {
        return bestMoveVar;
    }

    QString getBestEval() const
    {
        return bestEvalVar;
    }

signals:
    void bestMoveChanged();
    void bestEvalChanged();

private:
    QProcess pythonProcess;

    QString bestMoveVar = "Best Move: --";
    QString bestEvalVar = "Best Eval: --";

    QHash<int, QString> columnDictionary {{0, "a"}, {1, "b"}, {2, "c"}, {3, "d"}, {4, "e"}, {5, "f"}, {6, "g"}, {7, "h"}};
    QHash<int, QString> rowDictionary {{0, "8"}, {1, "7"}, {2, "6"}, {3, "5"}, {4, "4"}, {5, "3"}, {6, "2"}, {7, "1"}};
};