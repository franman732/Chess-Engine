#include "EngineManager.h"

#include <QProcess>
#include <QObject>
#include <QDebug>
#include <QString>
#include <QVariant>
#include <QVariantList>

EngineManager::EngineManager(QObject *parent)
    : QObject(parent)
{

    pythonProcess.start(
        "C:/Users/Nathaniel/Documents/GitHub/Chess_Engine/ChessEngine.venv/Scripts/python.exe",
        QStringList() << "C:/Users/Nathaniel/Documents/GitHub/Chess_Engine/Python_engine/Main.py"
    );


    if(!pythonProcess.waitForStarted())
    {
        qDebug() << "Failed to start Python engine";
    }

    qDebug() << "Started:" << pythonProcess.waitForStarted();
    qDebug() << "State:" << pythonProcess.state();

    connect(
        &pythonProcess,
        &QProcess::finished,
        this,
        [](int exitCode, QProcess::ExitStatus status)
        {
            qDebug() << "Python exited";
            qDebug() << "Exit code:" << exitCode;
            qDebug() << "Status:" << status;
        }
        );

    connect(
        &pythonProcess,
        &QProcess::readyReadStandardOutput,
        this,
        [this]()
        {
            QString output = pythonProcess.readAllStandardOutput();

            QStringList lines = QString(output).split("\n");

            for (QString line : lines)
            {
                qDebug() << line;

                if (line.startsWith("BEST MOVE:")) {
                    QString bestMoveString = line.mid(10).trimmed();
                    QStringList bestMoveStringList = bestMoveString.split(',');

                    for (QString& string : bestMoveStringList) {
                        string = string.remove(0, 1); // removes index 0 of the string, which is either a parenthesis or a space
                    }

                    bestMoveStringList[bestMoveStringList.length() - 1].chop(1); // removes the last character of the final part of the move string, which is ). This is for convenience sake so converting every value in the list to an int doesnt break the program.

                    int start = bestMoveStringList[0].toInt();
                    int end = bestMoveStringList[1].toInt();

                    int startRow = start / 8;
                    int startCol = start & 7;

                    int endRow = end / 8;
                    int endCol = end & 7;

                    QString bestMoveStart = columnDictionary[startCol] + rowDictionary[startRow];
                    QString bestMoveEnd = columnDictionary[endCol] + rowDictionary[endRow];

                    bestMoveVar = "Best Move: " + bestMoveStart + " " + "->" + " " + bestMoveEnd;
                    emit bestMoveChanged();
                    qDebug() << "Best move: |" << bestMoveVar;
                }

                else if (line.startsWith("BEST EVAL:")) {
                    bestEvalVar = "Best Eval: " + line.mid(10).trimmed();
                    emit bestEvalChanged();
                    qDebug() << "Best eval: |" << bestEvalVar;
                }
                else {
                    QString time = line;

                    qDebug() << "time: "<< time;
                }
            }
        }
        );

    connect(
        &pythonProcess,
        &QProcess::readyReadStandardError,
        this,
        [this]()
        {
            qDebug() << "Python stderr:";
            qDebug().noquote() << pythonProcess.readAllStandardError();
        }
        );
}

void EngineManager::findBestMove(const QVariantList& boardState) {
    QString message;


    for(int i = 0; i < 64; i++)
    {
        message += QString::number(boardState[i].toInt());

        if(i != 63)
            message += ",";
    }


    message += "\n";

    qDebug() << "MESSAGE SENT";

    pythonProcess.write(message.toUtf8());
};