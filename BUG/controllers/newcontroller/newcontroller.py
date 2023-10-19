"""建议把快进打开，不然在复杂地图跑完全程会需要很长时间"""
from controller import Robot
import numpy as np
from controller import InertialUnit
import math

def calculate_angle(start_point, destination):
    temp = 0
    if destination[0] - start_point[0] < 0:
        if destination[1] - start_point[1] < 0:
            temp = np.arctan((destination[0] - start_point[0]) / (destination[1] - start_point[1]))
        else:
            temp = np.pi - np.arctan(-(destination[0] - start_point[0]) / (destination[1] - start_point[1]))
    elif destination[0] - start_point[0] > 0:
        if destination[1] - start_point[1] < 0:
            temp = np.arctan((destination[0] - start_point[0]) / (destination[1] - start_point[1]))
        else:
            temp = np.arctan((destination[0] - start_point[0]) / (destination[1] - start_point[1])) - np.pi
    elif destination[0] - start_point[0] == 0:
        temp = np.pi/2
    return temp


def point_on_m_line(a, b, c):
    x0,y0,_ = a
    x1,y1,_= b
    x2,y2,_ = c
    distance = abs((x2 - x1) * (y1 - y0) - (x1 - x0) * (y2 - y1)) / np.sqrt(np.square(x2 - x1) + np.square(y2 - y1))
    return distance < 0.24

def detect_obstacle(dis_sensors):
    for i in range(len(dis_sensors)):
        if i == 3 or i == 4:
            continue
        if dis_sensors[i].getValue() > 90:
            return True
    return False


def select_current_direction(sensed_direction, five_prev_directions):
    if abs(abs(np.average(five_prev_directions)) - abs(sensed_direction)) < 0.4:
        return sensed_direction
    else:
        return five_prev_directions[0]


def update_prev_directions_list(new_value, five_prev_directions):
    for i in range(0, 4):
        five_prev_directions[i + 1] = five_prev_directions[i]
    five_prev_directions[0] = new_value
    return five_prev_directions

def euclid_distance(point1, point2):
    distance = np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    return distance


def run(robot,timestep):
    max_speed = 6.28
    left_motor = robot.getDevice('left wheel motor')
    right_motor = robot.getDevice('right wheel motor')
    left_motor.setPosition(float('inf'))
    right_motor.setPosition(float('inf'))
    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)

    gps = robot.getDevice('gps')
    gps.enable(timestep)

    dis_sensors = []
    for i in range(8):
        sensor_name = 'ps' + str(i)
        dis_sensors.append(robot.getDevice(sensor_name))
        dis_sensors[i].enable(timestep)
    inertial = robot.getDevice("inertial unit")
    inertial.enable(timestep)

    mode = 0
    wall_detected = False
    right_wall_sensors = False
    last_hit_is_valid = False
    five_prev_directions = [0, 0, 0, 0, 0]
    last_hit = [float('inf'), float('inf'), float('inf')]
    count = 0
    last_hit_time = 0;
    follow_num = 0;
    
    while robot.step(timestep) != -1:
        if count == 0:
            temp = gps.getValues()
            start_point = (temp[0],temp[1],0)
            destination = (-temp[0],-temp[1],0)
            desired = calculate_angle(start_point, destination)
        count+=1
        gps_val = gps.getValues()
        
        left_wall =  dis_sensors[5].getValue() > 90
        right_wall =  dis_sensors[2].getValue() > 90
        front_left_wall = dis_sensors[7].getValue() > 90 or dis_sensors[6].getValue() >90 
        front_right_wall = dis_sensors[0].getValue() > 90 or dis_sensors[1].getValue() > 90 
        
        left_speed = 0
        right_speed = 0
        
        current_direction = select_current_direction(inertial.getRollPitchYaw()[2], five_prev_directions)
        five_prev_directions = update_prev_directions_list(current_direction, five_prev_directions)
        if np.sqrt((gps_val[0] - destination[0]) ** 2 + (gps_val[1] - destination[1]) ** 2) < 0.5:
            print("OK,we reach the destination!")
            left_speed = 0
            right_speed = 0
        elif mode == 0:
            mode = 1
        elif mode == 1:
            last_hit_is_valid = True
            if abs(desired - current_direction) < 0.05 :
                print("found the correct direction!")
                mode = 2
            else:
                left_speed = -max_speed/4
                right_speed = max_speed/4
                print("finding direction")
        elif mode == 2:
            if detect_obstacle(dis_sensors):
                left_speed = 0
                right_speed = 0
                last_hit = gps_val
                last_hit_is_valid = False
                #last_hit_time = count;
                print("wall detected")
                print("follow the wall")
                mode = 3
            else:
                print("follow the m-line...")
                left_speed = max_speed
                right_speed = max_speed
        elif mode == 3:
            if point_on_m_line(gps_val, start_point, destination)and euclid_distance(
                    destination, last_hit) > euclid_distance(destination, gps_val):
                print("line found")
                mode = 1
            else:
                if not wall_detected and front_left_wall:
                    wall_detected = True
                    right_wall_sensors = True
                    left_speed = -max_speed
                    right_speed = max_speed
                elif not wall_detected and front_right_wall:
                    wall_detected = True
                    right_wall_sensors = False
                    left_speed = max_speed
                    right_speed = -max_speed
                elif wall_detected and not right_wall_sensors and (front_right_wall or front_left_wall):
                    left_speed = max_speed
                    right_speed = -max_speed
                elif wall_detected and right_wall_sensors and (front_right_wall or front_left_wall):
                    left_speed = -max_speed
                    right_speed = max_speed
                elif left_wall or right_wall:
                    last_hit_is_valid = True
                    left_speed = max_speed
                    right_speed = max_speed
                else:
                    if right_wall_sensors:
                        right_speed = max_speed / 8
                        left_speed = max_speed
                    else:
                        right_speed = max_speed
                        left_speed = max_speed / 8

        left_motor.setVelocity(left_speed)
        right_motor.setVelocity(right_speed)


if __name__ == "__main__":
    robot = Robot()
    timestep = 32
    run(robot,timestep)

