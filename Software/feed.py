import cv2
cap = cv2.VideoCapture(2)
while True:
	_, frame = cap.read()
	cv2.imshow("Left",frame)
	cv2.imshow("Right",frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	
#Release everything if job is finished
