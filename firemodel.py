from imageai.Detection.Custom import CustomObjectDetection, CustomVideoObjectDetection
import os
import cv2
#import uuid


execution_path = os.getcwd()

def detect_from_image(input_img,detected_img):
    prediction=[]
    confidence=[]
    box_points=[]
    width=[]
    height=[]
    level=[]
    
    detector = CustomObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(detection_model_path=os.path.join(execution_path, "detection_model-ex-33--loss-4.97.h5"))
    detector.setJsonPath(configuration_json=os.path.join(execution_path, "detection_config.json"))
    detector.loadModel()


    detections = detector.detectObjectsFromImage(input_image= os.path.join(execution_path, "\\Users\\Adhisha\\Projects\\Anemoi Technologies\\Django_Project\\visionai\\media\\"+ str(input_img)),
                                                 output_image_path=os.path.join(execution_path, "\\Users\\Adhisha\\Projects\\Anemoi Technologies\\Django_Project\\visionai\\media\\"+ detected_img),
                                                 minimum_percentage_probability=40)

    for iteration,detection in enumerate(detections):
        prediction.append(detection["name"]), 
        confidence.append(detection["percentage_probability"])
        box_points.append(detection["box_points"])
        width.append(box_points[iteration][2] - box_points[iteration][0])
        height.append(box_points[iteration][3] - box_points[iteration][1])
       
        if (width[iteration] <= 150 and height[iteration] <= 150):
            level.append("Small")
        elif (width[iteration] > 150 and width[iteration] < 350 and height[iteration] > 150 and height[iteration] < 350):
            level.append("Intermediate")
        elif (width[iteration] > 350 or height[iteration] > 350):
            level.append("Dangerous")

    return detected_img,iteration+1,prediction,confidence,box_points,width,height,level,input_img



def detect_from_video(input_video,detected_video,folder_name):
    detector = CustomVideoObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(detection_model_path=os.path.join(execution_path, "detection_model-ex-33--loss-4.97.h5"))
    detector.setJsonPath(configuration_json=os.path.join(execution_path, "detection_config.json"))
    detector.loadModel()


    #Making a seperate directory
    #filename = input_video
    #dir_name = os.path.splitext(filename)[0]
    #global dir_name
    dir_name = folder_name
    parent_dir = "C:\\Users\\Adhisha\\Projects\\Anemoi Technologies\\Django_Project\\visionai\\media\\Fire_Video_Frames"
    directory = os.path.join(parent_dir, dir_name) 
    os.mkdir(directory)
    seconds = 1


    cap=cv2.VideoCapture(os.path.join(execution_path, "\\Users\\Adhisha\\Projects\\Anemoi Technologies\\Django_Project\\visionai\\media\\"+ str(input_video)))
    fps=round(cap.get(cv2.CAP_PROP_FPS))
    multiplier = fps*seconds
    frame_count=cap.get(cv2.CAP_PROP_FRAME_COUNT)

    detected_video_path = detector.detectObjectsFromVideo(input_file_path=os.path.join(execution_path, "\\Users\\Adhisha\\Projects\\Anemoi Technologies\\Django_Project\\visionai\\media\\"+ str(input_video)), frames_per_second=fps, output_file_path=os.path.join(execution_path, "\\Users\\Adhisha\\Projects\\Anemoi Technologies\\Django_Project\\visionai\\media\\"+ detected_video), minimum_percentage_probability=10, log_progress=True, frame_detection_interval=multiplier)


    def show():

        #filename = "Video.mp4"
        #dir_name = os.path.splitext(filename)[0]

        cap = cv2.VideoCapture("C:\\Users\\Adhisha\\Projects\\Anemoi Technologies\\Django_Project\\visionai\\media\\"+ detected_video+".mp4")
        count = -1
        seconds = 1
        fps = round(cap.get(cv2.CAP_PROP_FPS)) 
        multiplier = fps*seconds

        while cap.isOpened():
            ret, frame = cap.read()

            if ret:
                cv2.imwrite('C:\\Users\\Adhisha\\Projects\\Anemoi Technologies\\Django_Project\\visionai\\media\\Fire_Video_Frames\\%s\\Frame{:f}.jpg'.format(count)%(dir_name),frame)
                count += multiplier 
                cap.set(1, count)
            else:
                cap.release()
                break
            
    show()

    v_frames = os.listdir('C:/Users/Adhisha/Projects/Anemoi Technologies/Django_Project/visionai/media/Fire_Video_Frames/'+folder_name)
    frame_no = len(v_frames)
    frames_data= {}
    for i in range(1,frame_no+1,1):
        frames_data['f' + str(i)] = "Fire_Video_Frames/"+folder_name+"/"+v_frames[i-1]
 
    locals().update(frames_data)

    my_list = []
    key_list = []
    for key,value in frames_data.items() :
        my_list.append(value)
        key_list.append(key)


    return input_video,detected_video,fps,frame_count, my_list,frame_no,key_list
    







