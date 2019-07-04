# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 20:42:54 2019

@author: sbtithzy
"""
import dlib         # 人脸处理的库 Dlib
import numpy as np  # 数据处理的库 Numpy
import cv2          # 图像处理的库 OpenCv
import os           # 读写文件
import shutil       # 读写文件
# Dlib 正向人脸检测器 / frontal face detector
detector = dlib.get_frontal_face_detector()
#detector = dlib.cnn_face_detection_model_v1()
# Dlib 68 点特征预测器 / 68 points features predictor
predictor = dlib.shape_predictor('data/data_dlib/shape_predictor_68_face_landmarks.dat')
# OpenCv 调用摄像头 use camera
cap = cv2.VideoCapture(0)
# 设置视频参数 set camera
cap.set(3, 480)
# 人脸截图的计数器 the counter for screen shoot
cnt_ss = 0
# 存储人脸的文件夹 the folder to save faces
current_face_dir = ""
# 保存 faces images 的路径 the directory to save images of faces
path_photos_from_camera = "data/data_faces_from_camera/"
# 新建保存人脸图像文件和数据CSV文件夹
# mkdir for saving photos and csv
def pre_work_mkdir():
    # 新建文件夹 / make folders to save faces images and csv
    if os.path.isdir(path_photos_from_camera):
        pass
    else:
        os.mkdir(path_photos_from_camera)
pre_work_mkdir()
##### optional/可选, 默认关闭 #####
# 删除之前存的人脸数据文件夹
# delete the old data of faces
def pre_work_del_old_face_folders():
    # 删除之前存的人脸数据文件夹
    # 删除 "/data_faces_from_camera/person_x/"...
    folders_rd = os.listdir(path_photos_from_camera)
    for i in range(len(folders_rd)):
        shutil.rmtree(path_photos_from_camera+folders_rd[i])
    if os.path.isfile("data/features_all.csv"):
        os.remove("data/features_all.csv")
# 这里在每次程序录入之前, 删掉之前存的人脸数据
# 如果这里打开，每次进行人脸录入的时候都会删掉之前的人脸图像文件夹 person_1/,person_2/,person_3/...
# If enable this function, it will delete all the old data in dir person_1/,person_2/,/person_3/...
# pre_work_del_old_face_folders()
##################################
# 如果有之前录入的人脸 / if the old folders exists
# 在之前 person_x 的序号按照 person_x+1 开始录入 / start from person_x+1
if os.listdir("data/data_faces_from_camera/"):
    # 获取已录入的最后一个人脸序号 / get the num of latest person
    person_list = os.listdir("data/data_faces_from_camera/")
    person_num_list = []
    for person in person_list:
        person_num_list.append(int(person.split('_')[-1]))
    person_cnt = max(person_num_list)
# 如果第一次存储或者没有之前录入的人脸, 按照 person_1 开始录入
# start from person_1
else:
    person_cnt = 0
# 之后用来控制是否保存图像的 flag / the flag to control if save
save_flag = 1
# 之后用来检查是否先按 'n' 再按 's' / the flag to check if press 'n' before 's'
press_n_flag = 0
while cap.isOpened():
    flag, img_rd = cap.read()
    # print(img_rd.shape)
    # It should be 480 height * 640 width
    kk = cv2.waitKey(1)
    img_gray = cv2.cvtColor(img_rd, cv2.COLOR_RGB2GRAY)    
    # 人脸数 faces
    faces = detector(img_gray, 0)
    # 待会要写的字体 / font to write
    font = cv2.FONT_HERSHEY_COMPLEX
    # 按下 'n' 新建存储人脸的文件夹 / press 'n' to create the folders for saving faces
    if kk == ord('n'):
        person_cnt += 1
        name = input("Enter your name: ")
        person_list = os.listdir("data/data_faces_from_camera/")
        person_name = []
        for person in person_list:
            person_name.append(str(person.split('_')[0]))
        if name in person_name:
            print ("用户照片已存在,无需重复录入!!！")
            print("请重新键盘输入'N'来新建人脸文件夹！")
            person_cnt -= 1
            continue
        else:
            current_face_dir = path_photos_from_camera + name + '_'+ str(person_cnt)
            os.makedirs(current_face_dir)
            print('\n')
            print("新建的人脸文件夹: ", current_face_dir)
            print("键盘输入'S'保存照片")
        cnt_ss = 0              # 将人脸计数器清零 / clear the cnt of faces
        press_n_flag = 1        # 已经按下 'n' / have pressed 'n'
    # 检测到人脸 / if face detected
    if len(faces) != 0:
        # 矩形框 / show the rectangle box
        for k, d in enumerate(faces):
            # 计算矩形大小
            # we need to compute the width and height of the box
            # (x,y), (宽度width, 高度height)
            pos_start = tuple([d.left(), d.top()])
            pos_end = tuple([d.right(), d.bottom()])
            # 计算矩形框大小 / compute the size of rectangle box
            height = (d.bottom() - d.top())
            width = (d.right() - d.left())
            hh = int(height/2)
            ww = int(width/2)
            # 设置颜色 / the color of rectangle of faces detected
            color_rectangle = (255, 255, 255)
            # 判断人脸矩形框是否超出 480x640
            if (d.right()+ww) > 640 or (d.bottom()+hh > 480) or (d.left()-ww < 0) or (d.top()-hh < 0):
                cv2.putText(img_rd, "OUT OF RANGE", (20, 300), font, 0.8, (0, 0, 255), 1, cv2.LINE_AA)
                color_rectangle = (0, 0, 255)
                save_flag = 0
                if kk == ord('s'):
                    print("请调整位置 / Please adjust your position")
            else:
                color_rectangle = (255, 255, 255)
                save_flag = 1
            cv2.rectangle(img_rd,
                          tuple([d.left() - ww, d.top() - hh]),
                          tuple([d.right() + ww, d.bottom() + hh]),
                          color_rectangle, 2)
            # 根据人脸大小生成空的图像 / create blank image according to the size of face detected
            im_blank = np.zeros((int(height*2), width*2, 3), np.uint8)
            if save_flag:
                # 按下 's' 保存摄像头中的人脸到本地 / press 's' to save faces into local images
                if kk == ord('s'):
                    # 检查有没有先按'n'新建文件夹 / check if you have pressed 'n'
                    if press_n_flag:
                        cnt_ss += 1
                        for ii in range(height*2):
                            for jj in range(width*2):
                                im_blank[ii][jj] = img_rd[d.top()-hh + ii][d.left()-ww + jj]
                        #cv2.imwrite(current_face_dir + "/img_face_" + str(cnt_ss) + ".jpg", im_blank)
                        #cv2.imwrite("我//h.jpg", frame) #该方法不成功
                        cv2.imencode('.jpg', im_blank)[1].tofile(current_face_dir + "/" + name +'_'+ str(cnt_ss)+ ".jpg") #正确方法
                        
                        print("保存照片：", str(current_face_dir) + "/" + name +'_' + str(cnt_ss) + ".jpg")
                    else:
                        print("请在按 'S' 之前先按 'N' 来建文件夹 / Please press 'N' before 'S'")
    # 显示人脸数 / show the numbers of faces detected
    cv2.putText(img_rd, "Faces: " + str(len(faces)), (20, 100), font, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
    # 添加说明 / add some statements
    cv2.putText(img_rd, "Face Register", (20, 40), font, 1, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(img_rd, "N: New face folder", (20, 350), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(img_rd, "S: Save current face", (20, 400), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
    cv2.putText(img_rd, "Q: Quit", (20, 450), font, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
    # 按下 'q' 键退出 / press 'q' to exit
    if kk == ord('q'):
        break
    # 如果需要摄像头窗口大小可调 / uncomment this line if you want the camera window is resizeable
    # cv2.namedWindow("camera", 0)
    cv2.imshow("camera", img_rd)
# 释放摄像头 / release camera
cap.release()
cv2.destroyAllWindows()
