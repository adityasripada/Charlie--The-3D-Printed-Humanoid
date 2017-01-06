import time
import pyautogui
import os
import math
import pypot.dynamixel
import numpy as np

def angle(v1,v2,v3):
	p1 = [v2[0]-v1[0],v2[1]-v1[1],v2[2]-v1[2]]
	p2 = [v3[0]-v2[0],v3[1]-v2[1],v3[2]-v2[2]]
		
	dot = p1[0]*p2[0] + p1[1]*p2[1] + p1[2]*p2[2]
	mag1 = math.sqrt(p1[0]**2 + p1[1]**2 + p1[2]**2)
	mag2 = math.sqrt(p2[0]**2 + p2[1]**2 + p2[2]**2)
	rad = math.acos(dot/(mag1*mag2))
	deg = rad * 180 /math.pi
	return deg 

def vangle(p1,p2):
	dot = p1[0]*p2[0] + p1[1]*p2[1] + p1[2]*p2[2]
	mag1 = math.sqrt(p1[0]**2 + p1[1]**2 + p1[2]**2) + 0.0001
	mag2 = math.sqrt(p2[0]**2 + p2[1]**2 + p2[2]**2) + 0.0001
	return dot/(mag1*mag2)


def theta(p1,p2,p3,flip):
	m1 = (p2[1] -p1[1])/(p2[0]-p1[0]+0.000001)
	m2 = (p3[1] -p2[1])/(p3[0]-p2[0]+0.000001)
	if flip:
		tan = (m1-m2)/abs((1+m1*m2))
	else:
		tan = (m1-m2)/(1+m1*m2)
	theta = math.atan(tan) * 180/math.pi
	return theta 

ports = pypot.dynamixel.get_available_ports()
ports.sort()
if not ports:
    raise IOError('no port found!')

print('ports found', ports)

print('connecting on the first available port:', ports[0])
dxl_io = pypot.dynamixel.DxlIO(ports[0])
ids = dxl_io.scan(range(10))
print(ids)

for i in range(len(ids)):
	dxl_io.set_moving_speed({ids[i]:45})
	pass
'''

os.system("start test.pde")
time.sleep(4)

pyautogui.keyDown('ctrl')
pyautogui.press('r')
pyautogui.keyUp('ctrl')
time.sleep(5)
'''
j = raw_input("Start")
lista = [0,0,0,0,0,0]
listb = [0,0,0,0,0,0]
listc = [0,0,0,0,0,0]
listd = [0,0,0,0,0,0]
liste = [0,0,0,0,0,0]
listf = [0,0,0,0,0,0]
while True:
	pyautogui.press('r')
	time.sleep(0.01)
	f = open('angles.txt','r')
	z = f.readlines()
	f.close()
	points = []
	for point in z:
		y = [float(x) for x in point.split(',')]
		points.append(y)
	for i in range(len(lista)-1):
		lista[i] = lista[i+1]
		listb[i] = listb[i+1]
		listc[i] = listc[i+1]
		listd[i] = listd[i+1]
		liste[i] = liste[i+1]
		listf[i] = listf[i+1]

	lista[5] =  theta(points[0],points[1],points[2],False) #ls
	listb[5] =  angle(points[1],points[2],points[3]) #le
	listc[5] =  theta(points[0],points[4],points[5],True) #rs
	listd[5] = angle(points[4],points[5],points[6]) #re
	
	v1 = [points[1][0]-points[2][0],points[1][1]-points[2][1],abs(points[1][2]-points[2][2])]
	a1 = vangle(v1,[0,0,1])
	v1 = [v1[0]*a1,v1[1]*a1,v1[2]*a1]
	a1 = vangle(v1,[0,1,0])
	liste[5] = math.acos(a1)*180/math.pi
	
	v1 = [points[4][0]-points[5][0],points[4][1]-points[5][1],abs(points[4][2]-points[5][2])]
	a1 = vangle(v1,[0,0,1])
	v1 = [v1[0]*a1,v1[1]*a1,v1[2]*a1]
	a1 = vangle(v1,[0,1,0])
	listf[5] = math.acos(a1)*180/math.pi

	t1 = 90-abs(sum(lista)/6)
	t2 = sum(listb)/6
	t3 = 90-abs(sum(listc)/6)
	t4 = sum(listd)/6
	t5 = sum(liste)/6
	t6 = sum(listf)/6
	
	if lista[0] ==0:
		continue
	thetas = [(t1+10),-t5,(t4*-1)+28,t2-26,(10-t3),t6]
	dxl_io.set_goal_position(dict(zip(ids,thetas)))
	time.sleep(0.01)