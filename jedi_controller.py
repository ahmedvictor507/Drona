#!/usr/bin/env python3

import sys
import cv2
import mediapipe as mp

# Try importing ROS components, but provide a mock if unavailable for testing on Windows
class MockRospy:
    def init_node(self, *args, **kwargs): pass
    def loginfo(self, msg): print(f"[INFO] {msg}")
    def logwarn(self, msg): print(f"[WARN] {msg}")
    def logerr(self, msg): print(f"[ERR] {msg}")
    def wait_for_service(self, *args, **kwargs): raise self.ROSException("No ROS")
    def is_shutdown(self): return False
    def signal_shutdown(self, msg): print(f"[SHUTDOWN] {msg}")
    def ServiceProxy(self, *args, **kwargs): return None
    class ROSException(Exception): pass
    class ServiceException(Exception): pass
    class ROSInterruptException(Exception): pass

try:
    import rospy
    try:
        from drona.srv import SetVelocity
    except ImportError:
        try:
            from clover.srv import SetVelocity
        except ImportError:
            SetVelocity = None
except ImportError:
    print("ROS (rospy) not found! Running in offline webcam test mode.")
    rospy = MockRospy()
    SetVelocity = None

def main():
    # Initialize the ROS node
    rospy.init_node('jedi_controller')
    
    rospy.loginfo("Waiting for set_velocity service...")
    try:
        rospy.wait_for_service('set_velocity', timeout=3.0)
        set_velocity = rospy.ServiceProxy('set_velocity', SetVelocity)
        rospy.loginfo("Connected to set_velocity service.")
    except rospy.ROSException:
        rospy.logwarn("Service set_velocity not available. Proceeding in test mode.")
        set_velocity = None

    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )
    mp_draw = mp.solutions.drawing_utils

    # Open the default webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        rospy.logerr("Cannot open webcam")
        return

    rospy.loginfo("Starting Jedi Controller... Press 'q' in the video window to quit.")
    
    try:
        while not rospy.is_shutdown():
            ret, frame = cap.read()
            if not ret:
                rospy.logerr("Failed to read from webcam")
                break
                
            # Flip the image horizontally for a selfie-view display
            frame = cv2.flip(frame, 1)
            
            # Convert BGR to RGB for MediaPipe processing
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb_frame)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    
                    # Extract y-coordinates for wrist (0) and middle finger tip (12)
                    wrist_y = hand_landmarks.landmark[0].y
                    middle_finger_tip_y = hand_landmarks.landmark[12].y
                    
                    # In OpenCV/MediaPipe, y=0 is at the top of the image.
                    # So wrist_y - middle_finger_tip_y > 0 means the finger tip is ABOVE the wrist.
                    if (wrist_y - middle_finger_tip_y) >= 0.2:
                        print("OPEN PALM: Force Push Up")
                        if set_velocity:
                            try:
                                # Trigger upward push (vx=0, vy=0, vz=1.0)
                                set_velocity(vx=0.0, vy=0.0, vz=1.0, frame_id='body')
                            except rospy.ServiceException as e:
                                print(f"Service call failed: {e}")
                    else:
                        print("CLOSED FIST: Hover")
                        if set_velocity:
                            try:
                                # Trigger hover (vx=0, vy=0, vz=0)
                                set_velocity(vx=0.0, vy=0.0, vz=0.0, frame_id='body')
                            except rospy.ServiceException as e:
                                print(f"Service call failed: {e}")

            # Show the video feed
            cv2.imshow('Jedi Controller', frame)
            
            # Break the loop if 'q' is pressed using cv2.waitKey
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Quitting Jedi Controller...")
                break
                
    except KeyboardInterrupt:
        print("Caught KeyboardInterrupt, shutting down...")
    finally:
        # Clean up camera and close windows
        cap.release()
        cv2.destroyAllWindows()
        rospy.signal_shutdown("User requested exit")

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
