
#include <webots/Robot.hpp>
#include <webots/Motor.hpp>
#include <webots/Keyboard.hpp>
#include <iostream> 
#include <webots/Camera.hpp>
#include <algorithm>
#include <iostream>
#include <limits>
#include <string>
#include <webots/GPS.hpp>
#include <vector>
#include <ctime>
#include <cmath>
using namespace std;
using namespace webots;

int main() {
	Motor *motors[4];//�����ͼ��̶�Ҫ��webots��������
	webots::Keyboard keyboard;
	char wheels_names[4][8] = { "motor1","motor2","motor3","motor4" };//���ڷ������������õ�����

	Robot *robot = new Robot();//ʹ��webots�Ļ���������
	keyboard.enable(1);//���м�����������Ƶ����1ms��ȡһ��

	double speed1[4];
	double speed2[4];
	double velocity = 4;
	int otime,ntime;
	otime = 0;
	ntime = 0;
	vector<double> lf,rf,lb,rb,mistake;
	

	//��ʼ��
	for (int i = 0; i < 4; i++)
	{
		motors[i] = robot->getMotor(wheels_names[i]);//�������ڷ������������õ����ֻ�ȡ����
		motors[i]->setPosition(std::numeric_limits<double>::infinity());
		motors[i]->setVelocity(0.0);

		speed1[i] = 0;
		speed2[i] = 0;
	}
	int timeStep = (int)robot->getBasicTimeStep();
       Camera *camera;
       int w,h;
       camera=robot->getCamera("camera");
       camera->enable (timeStep);
       w = camera->getWidth();
       h = camera->getHeight();
       //GPS *gps = robot->getGPS("gps");
       //gps->enable(timeStep);
       
       double carpos[3];

	//������һ��С���񣬵��ĸ����Ӱ�����������ת��ʱ�򣬳��ӿ�������ǰ�����ң�תȦ
	//б������ǰ��+����  ������ͬʱ��
	double speed_forward[4] = { velocity ,velocity ,velocity ,velocity };
	double speed_backward[4] = { -velocity ,-velocity ,-velocity ,-velocity };
	double speed_leftward[4] = { velocity ,-velocity ,velocity ,-velocity };
	double speed_rightward[4] = { -velocity ,velocity ,-velocity ,velocity };

	double speed_leftCircle[4] = { velocity ,-velocity ,-velocity ,velocity };
	double speed_rightCircle[4] = { -velocity ,velocity ,velocity ,-velocity };

       for(int i = 0;i <4;i++){
	speed1[i] = speed_forward[i];
	}
	//int timeStep = (int)robot->getBasicTimeStep();//��ȡ����webots����һ֡��ʱ��
	cout << timeStep << endl;

	while (robot->step(timeStep) != -1){
  
	
	const unsigned char* img = camera->getImage();
	int right=0,left=0;
       for(int i = 0;i < 4*h/5;i++){
       for(int j = 0;j<w/2;j++){
       right +=camera->imageGetRed(img,w,i,j);
       right +=camera->imageGetGreen(img,w,i,j);
       right +=camera->imageGetBlue(img,w,i,j);
       }}
       for(int i = 0;i < 4*h/5;i++){
       for(int j = w/2;j<w;j++){
       left +=camera->imageGetRed(img,w,i,j);
       left +=camera->imageGetGreen(img,w,i,j);
       left +=camera->imageGetBlue(img,w,i,j);
       }}
       if(left-right > w*255){
       for(int i = 0;i < 4;i++){
       speed2[i] = speed_forward[i];
       
       }
       for(int i = 0;i < 4;i++){
       speed1[i] = speed_rightCircle[i];}}
       
       if(right-left > w*255){
       for(int i = 0;i < 4;i++){
       speed2[i] = speed_forward[i];
       }
       for(int i = 0;i < 4;i++){
       speed1[i] = speed_leftCircle[i];}
       }
       if(right-left == w*255){
       for(int i = 0;i < 4;i++){
       speed2[i] = speed_forward[i];
       }
       for(int i = 0;i < 4;i++){
       speed1[i] = speed_forward[i];}
       }
       for(int i = 0;i <4;i++){
       motors[i]->setVelocity(speed1[i]+speed2[i]);
       if(i == 0){
       lf.push_back(speed1[i]+speed2[i]);
       }
       if(i == 1){
       rf.push_back(speed1[i]+speed2[i]);
       }
       if(i == 2){
       lb.push_back(speed1[i]+speed2[i]);
       }
       if(i == 3){
       rb.push_back(speed1[i]+speed2[i]);
       }
       }
       }
      	while (robot->step(timeStep) != -1) //∑¬’Ê‘À––“ª÷°
	{



		//ªÒ»°º¸≈Ã ‰»Î£¨’‚—˘–¥ø…“‘ªÒµ√Õ¨ ±∞¥œ¬µƒ∞¥º¸£®◊Ó∂‡÷ß≥÷7∏ˆ£©
		int keyValue1 = keyboard.getKey();
		int keyValue2 = keyboard.getKey();
		cout << keyValue1 << ":" << keyValue2 << endl;

		//∏˘æ›∞¥º¸æˆ∂®µÁª˙‘ı√¥—˘◊™∂Ø
		if (keyValue1 == 'W')
		{
			for (int i = 0; i < 4; i++)
			{
				speed1[i] = speed_forward[i];
			}
		}
		else if (keyValue1 == 'S')
		{
			for (int i = 0; i < 4; i++)
			{
				speed1[i] = speed_backward[i];
			}
		}
		else if (keyValue1 == 'A')
		{
			for (int i = 0; i < 4; i++)
			{
				speed1[i] = speed_leftward[i];
			}
		}
		else if (keyValue1 == 'D')
		{
			for (int i = 0; i < 4; i++)
			{
				speed1[i] = speed_rightward[i];
			}
		}
		else if (keyValue1 == 'Q')
		{
			for (int i = 0; i < 4; i++)
			{
				speed1[i] = speed_leftCircle[i];
			}
		}
		else if (keyValue1 == 'E')
		{
			for (int i = 0; i < 4; i++)
			{
				speed1[i] = speed_rightCircle[i];
			}
		}
		else
		{
			for (int i = 0; i < 4; i++)
			{
				speed1[i] = 0;
			}
		}




		if (keyValue2 == 'W')
		{
			for (int i = 0; i < 4; i++)
			{
				speed2[i] = speed_forward[i];
			}
		}
		else if (keyValue2 == 'S')
		{
			for (int i = 0; i < 4; i++)
			{
				speed2[i] = speed_backward[i];
			}
		}
		else if (keyValue2 == 'A')
		{
			for (int i = 0; i < 4; i++)
			{
				speed2[i] = speed_leftward[i];
			}
		}
		else if (keyValue2 == 'D')
		{
			for (int i = 0; i < 4; i++)
			{
				speed2[i] = speed_rightward[i];
			}
		}
		else
		{
			for (int i = 0; i < 4; i++)
			{
				speed2[i] = 0;
			}
		}


		//»√µÁª˙÷¥––
		for (int i = 0; i < 4; i++)
		{
			motors[i]->setVelocity(speed1[i] + speed2[i]);
		}

		//wb_motor_set_velocity(wheels[0],right_speed);
	}


      
	return 0;
}



