import cv2 #OpenCV
import mediapipe as mp #MediaPipe

# defining various MediaPipe built in methods

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

count = 0

pos = None

#create the video feed through the built in webcam
capture = cv2.VideoCapture(0)

#set the starting position of the pushup to "up"
position = "up"

#the body of the code

with mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7) as pose:
    while capture.isOpened(): #while the video feed is running
        success, image = capture.read()
        if not success: # if there is nothing from the video feed, end the loop
            print("empty camera")
            break
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB) 
        result = pose.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #the previous three lines have been to switch the color from BGR to RGB
        imlist = [] #this will be the list of the (x, y) coords of the various landmarks on the body

        if result.pose_landmarks:
            mp_drawing.draw_landmarks(
                image, result.pose_landmarks, mp_pose.POSE_CONNECTIONS) #this will overlay the points of all the landmarks as well as lines connecting them in the output video
            for id, im in enumerate(result.pose_landmarks.landmark):
                h, w, _ = image.shape
                X, Y = int(im.x*w), int(im.y*h)
                imlist.append([id, X, Y]) #adding all the coords of the landmarks as well as ids to the list 'imlist'

            if len(imlist) != 0: #check to make sure that there are in fact coordinates that are found.
                if imlist[12][2] and imlist[11][2] >= imlist[13][2] and imlist[14][2]: #check if you are in the "down" state
                    position = "down"
                elif imlist[12][2] and imlist[11][2] <= imlist[13][2] and imlist[14][2] and position == "down": #check if you are in the "up" state and you were previously in the down state
                    position = "up"
                    count += 1 #increment the count of pushups
                    print("pushups completed:", count)
        posit = ((int)(image.shape[1] / 3 - 268 / 2), (int)(image.shape[0] / 4 - 36 / 2)) #determine where to write the count of the pushups on the output window
        cv2.putText(image, 'Push-ups completed: % s' % count, posit, 0, 2, (255, 0, 0), 3, 15) #write the count on the output window
        cv2.imshow("pushup counter", image) #show the video feed
        key = cv2.waitKey(1)
        if key == ord('q'): #create an exit condition: press q to end the code
            break
capture.release() #when the loop ends, release the video


