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
                if (line.startsWith("MOVE:")) {
                    QString bestMove = line.mid(5);

                    qDebug() << "Best move: " << bestMove;
                }

                else if (line.startsWith("EVAL:")) {
                    double bestEval = line.mid(5).toDouble();

                    qDebug() << "Best eval: " << bestEval;
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