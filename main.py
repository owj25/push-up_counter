#libraries used: opencv, mediapipe
#Initially written in python 3.8 on 7/17/22
#owj25 on github, PROFILE: https://github.com/owj25 PROJECT REPO: https://github.com/owj25/push-up_counter
#GNU GPL 3 license

import cv2 #OpenCV
import mediapipe as mp #MediaPipe
import os #Operating System

# defining various MediaPipe built in methods

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

count = 0

#create the video feed through the built in webcam
capture = cv2.VideoCapture(0)

#set the starting position of the pushup to "up"
position = "up"
said = False

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
                    position = "down" #declare that you are in the "down" state
                    if not said: #make sure it won't repeatedly say 'down'
                        os.system('say -v "karen" "down"') #say 'down' using terminal
                        said = True #also to ensure it won't repeate 'down'
                elif imlist[12][2] and imlist[11][2] <= imlist[13][2] and imlist[14][2] and position == "down": #check if you are in the "up" state and you were previously in the down state
                    position = "up" #declare that you are in the "up" state
                    count += 1 #increment the count of pushups
                    print("pushups completed:", count) #print num of pushups
                    os.system('say -v "karen" "% s"' % count) #say the number of complete pushups
                    said = False #reset so that it can say 'down' again
        posit = ((int)(image.shape[1] / 3 - 268 / 2), (int)(image.shape[0] / 4 - 36 / 2)) #determine where to write the count of the pushups on the output window
        cv2.putText(image, 'Push-ups completed: % s' % count, posit, 0, 2, (255, 0, 0), 3, 15) #write the count on the output window
        cv2.imshow("pushup counter", image) #show the video feed
        key = cv2.waitKey(1)
        if key == 27: #create an exit condition: the 'esc' key, previously 'q'
            break
            cv2.destroyAllWindows() #destroy all OpenCV windows on esc key

cv2.destroyAllWindows() #when the loop ends, destroy all OpenCV windows


