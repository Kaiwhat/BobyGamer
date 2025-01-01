import mediapipe as mp
import cv2
from math import hypot


class myPose():
    def __init__(self):

         # 初始化 mediapipe 姿勢類別
        self.mp_pose = mp.solutions.pose

        # 設置圖片模式下的姿勢檢測
        self.pose_image = self.mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5, model_complexity=1)

          # 設置視頻模式下的姿勢檢測
        self.pose_video = self.mp_pose.Pose(static_image_mode=False, model_complexity=1, min_detection_confidence=0.7,
                                            min_tracking_confidence=0.7)

        # 初始化 mediapipe 畫圖類別
        self.mp_drawing = mp.solutions.drawing_utils

    def detectPose(self, image, pose, draw=False, display=False):
        """
        This function performs the pose detection on the most prominent person in an image.
        Args:
            image: The input image with a prominent person whose pose landmarks needs to be detected.
            pose: The pose function required to perform the pose detection.
            draw: A boolean value that is if set to true the function draw pose landmarks on the output image.
            display: A boolean value that is if set to true the function displays the original input image, and the
                 resultant image and returns nothing.

        Returns:
            output_image: The input image with the detected pose landmarks drawn if it was specified.
            results:      The output of the pose landmarks detection on the input image.

        """

         # 創建輸入圖像的副本
        output_image = image.copy()

        # 將圖像從 BGR 轉換為 RGB 格式
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 執行姿勢檢測.
        results = pose.process(imageRGB)

         # 檢查是否檢測到任何標誌，並且是否要求繪製
        if results.pose_landmarks and draw:
             # 在輸出圖像上繪製姿勢標誌
            self.mp_drawing.draw_landmarks(image=output_image, landmark_list=results.pose_landmarks,
                                      connections=self.mp_pose.POSE_CONNECTIONS,
                                      landmark_drawing_spec=self.mp_drawing.DrawingSpec(color=(255, 255, 255),
                                                                                   thickness=3, circle_radius=3),
                                      connection_drawing_spec=self.mp_drawing.DrawingSpec(color=(49, 125, 237),
                                                                                     thickness=2, circle_radius=2))

        # 檢查是否需要顯示原始圖像和結果圖像
        if display:
            # Display the original input image and the resultant image.
            plt.figure(figsize=[22, 22])
            plt.subplot(121);
            plt.imshow(image[:, :, ::-1]);
            plt.title("Original Image");
            plt.axis('off');
            plt.subplot(122);
            plt.imshow(output_image[:, :, ::-1]);
            plt.title("Output Image");
            plt.axis('off');

        # Otherwise
        else:
            # Return the output image and the results of pose landmarks detection.
            return output_image, results

    def checkPose_LRC(self, image, results, draw=False, display=False):
        """
        This function finds the horizontal position (left, center, right) of the person in an image.
        Args:
            image:   The input image with a prominent person whose the horizontal position needs to be found.
            results: The output of the pose landmarks detection on the input image.
            draw:    A boolean value that is if set to true the function writes the horizontal position on the output image.
            display: A boolean value that is if set to true the function displays the resultant image and returns nothing.
        Returns:
            output_image:         The same input image but with the horizontal position written, if it was specified.
            horizontal_position:  The horizontal position (left, center, right) of the person in the input image.

        """

        # 聲明一個變數來存儲人物的水平位置（左、中、右）
        horizontal_position = None

        # 獲取圖像的高度和寬度
        height, width, _ = image.shape

        # 創建輸入圖像的副本，用於繪製水平位置
        output_image = image.copy()

        # 獲取左肩膀標誌的 x 坐標
        left_x = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].x * width)

        # 獲取右肩膀標誌的 x 坐標
        right_x = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER].x * width)

        # 檢查人物是否位於左邊，即當兩個肩膀標誌的 x 坐標都小於或等於圖像中心的 x 坐標
        if (right_x <= width // 2 and left_x <= width // 2):

            horizontal_position = 'Left'

        # 檢查人物是否位於右邊，即當兩個肩膀標誌的 x 坐標都大於或等於圖像中心的 x 坐標
        elif (right_x >= width // 2 and left_x >= width // 2):

            horizontal_position = 'Right'

        # 檢查人物是否位於中間，即當右肩膀標誌的 x 坐標大於或等於圖像中心，並且左肩膀標誌的 x 坐標小於或等於圖像中心
        elif (right_x >= width // 2 and left_x <= width // 2):

            # Set the person's position to center.
            horizontal_position = 'Center'

        # 檢查是否需要在圖像上繪製水平位置和中線
        if draw:
            cv2.putText(output_image, horizontal_position, (5, height - 10), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255),3)

            cv2.line(output_image, (width // 2, 0), (width // 2, height), (255, 255, 255), 2)

        # 檢查是否需要顯示結果圖像
        if display:

            # Display the output image.
            plt.figure(figsize=[10, 10])
            plt.imshow(output_image[:, :, ::-1]);
            plt.title("Output Image");
            plt.axis('off');

        # Otherwise
        else:

            # Return the output image and the person's horizontal position.
            return output_image, horizontal_position

    def checkPose_JSD(self, image, results, MID_Y=250, draw=False, display=False):
        """
        This function checks the posture (Jumping, Crouching or Standing) of the person in an image.
        Args:
            image:   The input image with a prominent person whose the posture needs to be checked.
            results: The output of the pose landmarks detection on the input image.
            MID_Y:   The intial center y-coordinate of both shoulders landmarks of the person recorded during starting
                 the game. This will give the idea of the person's height when he is standing straight.
            draw:    A boolean value that is if set to true the function writes the posture on the output image.
            display: A boolean value that is if set to true the function displays the resultant image and returns nothing.
        Returns:
            output_image: The input image with the person's posture written, if it was specified.
            posture:      The posture (Jumping, Crouching or Standing) of the person in an image.

        """
        # 獲取圖像的高度和寬度
        height, width, _ = image.shape

        # 創建輸入圖像的副本，用於繪製姿勢標註
        output_image = image.copy()

        # 獲取左肩膀標誌的 y 坐標
        left_y = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_SHOULDER].y * height)

        # 獲取右肩膀標誌的 y 坐標
        right_y = int(results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_SHOULDER].y * height)

        # 計算左右肩膀的中點 y 坐標
        actual_mid_y = abs(right_y + left_y) // 2

        # 計算上限和下限的閾值
        lower_bound = MID_Y - 15
        upper_bound = MID_Y + 100

        #跳躍
        if (actual_mid_y < lower_bound):

            # Set the posture to jumping.
            posture = 'Jumping'

        #蹲下
        elif (actual_mid_y > upper_bound):

            # Set the posture to crouching.
            posture = 'Crouching'

        #站著
        else:

            # Set the posture to Standing straight.
            posture = 'Standing'

        # 檢查是否需要在圖像上繪製姿勢標註
        if draw:
            # Write the posture of the person on the image.
            cv2.putText(output_image, posture, (5, height - 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)

            # Draw a line at the intial center y-coordinate of the person (threshold).
            cv2.line(output_image, (0, MID_Y), (width, MID_Y), (255, 255, 255), 2)

        # 檢查是否需要顯示結果圖像
        if display:

            plt.figure(figsize=[10, 10])
            plt.imshow(output_image[:, :, ::-1]);
            plt.title("Output Image");
            plt.axis('off');
        
        else:
            return output_image, posture

    def checkHandsJoined(self, image, results, draw=False, display=False):
        """
        This function checks whether the hands of the person are joined or not in an image.
        Args:
            image:   The input image with a prominent person whose hands status (joined or not) needs to be classified.
            results: The output of the pose landmarks detection on the input image.
            draw:    A boolean value that is if set to true the function writes the hands status &amp; distance on the output image.
            display: A boolean value that is if set to true the function displays the resultant image and returns nothing.

        Returns:
            output_image: The same input image but with the classified hands status written, if it was specified.
            hand_status:  The classified status of the hands whether they are joined or not.

        """

        # 獲取輸入圖像的高度和寬度
        height, width, _ = image.shape

        # 創建輸入圖像的副本，用來寫上手部狀態標註
        output_image = image.copy()

        # 獲取左手腕標誌的 x 和 y 坐標
        left_wrist_landmark = (results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST].x * width,
                               results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.LEFT_WRIST].y * height)

        # 獲取右手腕標誌的 x 和 y 坐標
        right_wrist_landmark = (results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST].x * width,
                                results.pose_landmarks.landmark[self.mp_pose.PoseLandmark.RIGHT_WRIST].y * height)

        # 計算左手腕和右手腕之間的歐幾里得距離
        euclidean_distance = int(hypot(left_wrist_landmark[0] - right_wrist_landmark[0],
                                       left_wrist_landmark[1] - right_wrist_landmark[1]))

        # 比較手腕之間的距離和適當的閾值來檢查雙手是否接觸
        if euclidean_distance < 100:

            # 設置手部狀態為雙手合併
            hand_status = 'Hands Joined'
            color = (0, 255, 0)

        else:

            hand_status = 'Hands Not Joined'

            color = (0, 0, 255)

        if draw:

            cv2.putText(output_image, hand_status, (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, color, 3)


            cv2.putText(output_image, f'Distance: {euclidean_distance}', (10, 70),
                        cv2.FONT_HERSHEY_PLAIN, 2, color, 3)

        if display:

            plt.figure(figsize=[10, 10])
            plt.imshow(output_image[:, :, ::-1]);
            plt.title("Output Image");
            plt.axis('off');


        else:
            return output_image, hand_status

