# push-up_counter
v1 of a python based cv push-up counter using OpenCV and MediaPipe.

GENERAL:

This is a project that I am working on to help me develop my skills with computer vision, OpenCV, and to introduce myself to MediaPipe (a Google product for computer vision). 

I have been developing this program in PyCharm, and it is written entirely in python using OpenCV 2 and MediaPipe's pose model. Because of the nature of the project as well as the MediaPipe model, there are no training sets required, and effectively all you need to run the program is a python environment, OpenCV and MediaPipe installed, and a functioning webcam. 

This was a program that took a few hours to write as it is my first project using MediaPipe, but I am quite happy with the outcome.

USAGE:

The program checks whether your shoulders are below your elbows; when the shoulders are below, you are in the "down" state, and when your elbows are above the shoulders you are in the "up" state. If you are detected to be in the "down" state, and you were previously in the "up" state, then the count is incremented by 1 and you are set to the down state. 

Please note that the way it functions is by reading both elbows/shoulders, so the camera must be pointed such that you are facing it and it is angled nearly parallell to the ground. 

I highly reccomend using headphones if you are on a mac – it will let you know when you reach the down position as well as count out loud.
