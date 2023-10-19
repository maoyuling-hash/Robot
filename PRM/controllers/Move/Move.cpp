w#include <webots/Robot.hpp>
#include <webots/Motor.hpp>
#include <webots/Keyboard.hpp>

#include <iostream>
#include <algorithm>
#include <limits>
#include <string>

using namespace std;
using namespace webots;

int main()
{
    Robot *robot = new Robot();
    int timeStep = (int)robot->getBasicTimeStep();
    cout << timeStep << endl;

    Keyboard keyboard;
    keyboard.enable(1);

    Motor *motors[4];
    char wheelsNames[4][8] = {"motor1", "motor2", "motor3", "motor4"};
    double speed[4];
    double v = 10;
    for (int i = 0; i < 4; i++)
    {
        motors[i] = robot->getMotor(wheelsNames[i]);
        motors[i]->setPosition(std::numeric_limits<double>::infinity());
        motors[i]->setVelocity(0.0);
        speed[i] = 0;
    }

    double speedForward[4] = {v, v, v, v};
    double speedBackward[4] = {-v, -v, -v, -v};
    double speedRightward[4] = {0.5 * v, 0.5 * v, -0.5*v, -0.5*v};
    double speedLeftward[4] = {-0.5*v, -0.5*v, 0.5 * v, 0.5 * v};

    while (robot->step(timeStep) != -1)
    {
        int keyValue = 0;
        keyValue = keyboard.getKey();
        if (keyValue == 'W')
        {
            for (int i = 0; i < 4; ++i)
            {
                speed[i] = speedForward[i];
            }
        }
        else if (keyValue == 'S')
        {
            for (int i = 0; i < 4; ++i)
            {
                speed[i] = speedBackward[i];
            }
        }
        else if (keyValue == 'A')
        {
            for (int i = 0; i < 4; ++i)
            {
                speed[i] = speedLeftward[i];
            }
        }
        else if (keyValue == 'D')
        {
            for (int i = 0; i < 4; ++i)
            {
                speed[i] = speedRightward[i];
            }
        }
        else
        {
            for (int i = 0; i < 4; ++i)
            {
                speed[i] = 0;
            }
        }

        for (int i = 0; i < 4; ++i)
        {
            motors[i]->setVelocity(speed[i]);
        }
    }

    delete robot;
    return 0;
}
