import time
import pyautogui
import os
import math
import pypot.dynamixel
import socket
import numpy as np


def angle(v1,v2,v3):
	#Takes 3 Points. Returns Angles via Cos Inverse
	p1 = [v2[0]-v1[0],v2[1]-v1[1],v2[2]-v1[2]]
	p2 = [v3[0]-v2[0],v3[1]-v2[1],v3[2]-v2[2]]
		
	dot = p1[0]*p2[0] + p1[1]*p2[1] + p1[2]*p2[2]
	mag1 = math.sqrt(p1[0]**2 + p1[1]**2 + p1[2]**2)
	mag2 = math.sqrt(p2[0]**2 + p2[1]**2 + p2[2]**2)
	rad = math.acos(dot/(mag1*mag2))
	deg = rad * 180 /math.pi
	return deg 

def vangle(p1,p2):
	#Takes two vectors. Returns Cos Theta
	dot = p1[0]*p2[0] + p1[1]*p2[1] + p1[2]*p2[2]
	mag1 = math.sqrt(p1[0]**2 + p1[1]**2 + p1[2]**2) + 0.0001
	mag2 = math.sqrt(p2[0]**2 + p2[1]**2 + p2[2]**2) + 0.0001
	return dot/(mag1*mag2)


def theta(p1,p2,p3,flip):
	#Takes Two Points. Return angles via Slope
	m1 = (p2[1] -p1[1])/(p2[0]-p1[0]+0.000001)
	m2 = (p3[1] -p2[1])/(p3[0]-p2[0]+0.000001)
	if flip:
		tan = (m1-m2)/abs((1+m1*m2))
	else:
		tan = (m1-m2)/(1+m1*m2)
	theta = math.atan(tan) * 180/math.pi
	return theta 

#Motor Code ------------------------------------------
ports = pypot.dynamixel.get_available_ports()
if not ports:
    raise IOError('no port found!')

print('ports found', ports)
ports.sort()
print('connecting on the first available port:', ports[0])
dxl_io = pypot.dynamixel.DxlIO(ports[0])
ids = dxl_io.scan(range(10))
print(ids)

for i in range(len(ids)):
	dxl_io.set_moving_speed({ids[i]:85})
	dxl_io.set_moving_speed({7:200,8:200})
	pass
#Socket Code ------------------------------------------

#Kinect Code ------------------------------------------
'''

os.system("start test.pde")
time.sleep(4)

pyautogui.keyDown('ctrl')
pyautogui.press('r')
pyautogui.keyUp('ctrl')
time.sleep(5)
'''
#Main Code ----------------------------------------------
j = raw_input("Start")
current = list((16.84, -8.4, 8.04, -23.6, 2.33, 3.65, 92.82, 3.08))
while True:
	pyautogui.press('r')
	time.sleep(0.005)
	try:
		f = open('angles.txt','r')
	except:
		continue
	z = f.readlines()
	f.close()
	points = []
	for point in z:
		y = [float(x) for x in point.split(',')]
		points.append(y)

	t1 =  theta(points[0],points[1],points[2],False) #ls
	t2 =  angle(points[1],points[2],points[3]) #le
	t3 =  theta(points[0],points[4],points[5],True) #rs
	t4 = angle(points[4],points[5],points[6]) #re
	
	v1 = [points[1][0]-points[2][0],points[1][1]-points[2][1],abs(points[1][2]-points[2][2])]
	a1 = vangle(v1,[0,0,1])
	v1 = [v1[0]*a1,v1[1]*a1,v1[2]*a1]
	a1 = vangle(v1,[0,1,0])
	t5 = math.acos(a1)*180/math.pi #l3d
	
	v1 = [points[4][0]-points[5][0],points[4][1]-points[5][1],abs(points[4][2]-points[5][2])]
	a1 = vangle(v1,[0,0,1])
	v1 = [v1[0]*a1,v1[1]*a1,v1[2]*a1]
	a1 = vangle(v1,[0,1,0])
	t6 = math.acos(a1)*180/math.pi #r3d

	t1 = 90-abs(t1)
	t3 = 90-abs(t3)
	#current = dxl_io.get_present_position(ids)
	thetas = [(t1+10),-t5,(t4*-1)+28,t2-26,(10-t3),t6]
	offset = [-3 if x[0] > x[1] else 3 for x in zip(current,thetas)]
	current = [x[0] + x[1] for x in zip(current,offset)]
	print current
	dxl_io.set_goal_position(dict(zip(ids,current)))
	time.sleep(0.005)