#import the necesary packages
import argparse
import imutils
import cv2

#construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help = "path to the (optional) video file")
args = vars(ap.parse_args())

#define the color ranges
colorRanges = [
	((80, 90, 88), (140, 148, 150), "orange")]

if not args.get("video", False):
	camera = cv2.VideoCapture(0)

#otherwise, grab a reference to the video file
else:
	#camera = cv2.VideoCapture(args["video", False]):
	camera = cv2.VideoCapture(args["image"])

#keep looping
while True:
	#grab the current frame
	(grabbed, frame) = camera.read()

	#if we are viewing a video and we did not grab a frame, then we have
	#reached the end of the video
	if args.get("video") and not grabbed:
		break

	#resize the frame, blur it, and convert it to the HSV color space
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	#loop over the color ranges
	for (lower, upper, colorName) in colorRanges:
		#construct a mask for all oclors in the current HSV range, then
		#perform a series of dilarions and erosions to remove any small
		#blobs left in the mask
		mask = cv2.inRange(hsv, lower, upper)
		mask = cv2.erode(mask, None, iterations = 2)
		mask = cv2.dilate(mask, None, iterations = 2)

		#find contours in the mask
		cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
			cv2.CHAIN_APPROX_SIMPLE)
		cnts = cnts[0] if imutils.is_cv2() else cnts[1]

		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		
	# show the frame to our screen and increment the frame counter
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	counter += 1
 
	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break
 
# if we are not using a video file, stop the camera video stream
if not args.get("video", False):
	vs.stop()
 
# otherwise, release the camera
else:
	vs.release()
 
# close all windows
cv2.destroyAllWindows()
 



