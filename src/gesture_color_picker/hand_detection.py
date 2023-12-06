import mediapipe as mp
import cv2
import numpy as np

class HandDetector():
    def __init__(self, static_mode=False, max_hands=2,
                 model_complexity=1, 
                 detect_confidence=0.5, 
                 track_confidence=0.5) -> None:
        
        self.static_mode = static_mode
        self.max_hands = max_hands
        self.model_complexity = model_complexity
        self.detect_confidence = detect_confidence
        self.track_confidence = track_confidence

        self.FINGURE_TIP = [4, 8, 12, 16, 20]

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(static_image_mode=self.static_mode, 
                                         max_num_hands=self.max_hands, 
                                         model_complexity=self.model_complexity, 
                                         min_detection_confidence=self.detect_confidence,
                                         min_tracking_confidence=self.track_confidence)

        self.mp_draw = mp.solutions.drawing_utils
    
    def find_hand(self, image, draw=True):
        img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        if self.results.multi_hand_landmarks:
            if draw:
                for hand in self.results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(image, hand, self.mp_hands.HAND_CONNECTIONS)
        return image, self.results
    
    def find_position(self, image):
        h, w, c = image.shape
        lst_position = []
        if self.results.multi_hand_landmarks:
            for hand in self.results.multi_hand_landmarks:
                for id, mark in enumerate(hand.landmark):
                    lst_position.append([id, mark.x, mark.y])
        return lst_position
    
    def fingerUp(self, lst_mark):
        fingure_status = list()
        if lst_mark[4][1] < lst_mark[4 -1][1]:
            fingure_status.append(1)
        else:
            fingure_status.append(0)
        for id in self.FINGURE_TIP[1:]:
            if lst_mark[id][2] < lst_mark[id -1][2]:
                fingure_status.append(1)
            else:
                fingure_status.append(0)
        return fingure_status
   
    def angle_between_vectors(self, vector1, vector2):
        dot_product = np.dot(vector1, vector2)
        magnitude_product = np.linalg.norm(vector1) * np.linalg.norm(vector2)
        if magnitude_product == 0:
            return 0
        else:
            cosine_similarity = dot_product / magnitude_product
            return np.degrees(np.arccos(np.clip(cosine_similarity, -1.0, 1.0)))

    def is_pointing(self, lst_position):
        if len(lst_position) >= 21:
            wrist = lst_position[0]
            thumb_base = lst_position[1]
            index_finger_base = lst_position[5]
            index_finger_tip = lst_position[8]

            vector_thumb = np.array([thumb_base[1] - wrist[1], thumb_base[2] - wrist[2]])
            vector_index_finger = np.array([index_finger_tip[1] - index_finger_base[1],
                                            index_finger_tip[2] - index_finger_base[2]])

            angle_x = self.angle_between_vectors(vector_thumb, vector_index_finger)

            rotated_vector_thumb = np.array([-vector_thumb[1], vector_thumb[0]])
            rotated_vector_index_finger = np.array([-vector_index_finger[1], vector_index_finger[0]])

            angle_y = self.angle_between_vectors(rotated_vector_thumb, rotated_vector_index_finger)

            return (80 <= angle_x <= 100) and (80 <= angle_y <= 100)

        return False
