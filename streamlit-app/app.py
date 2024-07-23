import streamlit as st
import requests
from urllib.parse import urlencode
import time
import cv2
from ultralytics import YOLO
import PIL
import webbrowser
import streamlit as st
from streamlit_cookies_controller import CookieController

cookie_controller = CookieController()


class App:  
    def __init__(self):
        st.title('Face Recognition App')
        query_params = st.query_params
        token = query_params.get('sessionId', None)
        is_valid = False
        self.token = token
        
        if token:
            validation_response = self.validate_token(token)
            if validation_response.get('valid'):
                st.session_state[token] = {'valid': True, 'expires': validation_response.get('expires'), token: token}
                is_valid = True
                cookie_controller.set('sessionId', token)

        if not is_valid:
            st.write('Redirecting...')
            time.sleep(2)  # Add a delay for demonstration purposes
            redirect_url = 'http://localhost:8000'
            st.markdown(f'<meta http-equiv="refresh" content="0;URL={redirect_url}">', unsafe_allow_html=True)

    def _display_detected_frames(self, conf, model, st_frame, image, is_display_tracking=None, tracker=None):
        """
        Display the detected objects on a video frame using the YOLOv8 model.

        Args:
        - conf (float): Confidence threshold for object detection.
        - model (YoloV8): A YOLOv8 object detection model.
        - st_frame (Streamlit object): A Streamlit object to display the detected video.
        - image (numpy array): A numpy array representing the video frame.
        - is_display_tracking (bool): A flag indicating whether to display object tracking (default=None).

        Returns:
        None
        """

        # Resize the image to a standard size
        image = cv2.resize(image, (720, int(720*(9/16))))

        # Display object tracking, if specified
        if is_display_tracking:
            res = model.track(image, conf=conf, persist=True, tracker=tracker)
        else:
            # Predict the objects in the image using the YOLOv8 model
            res = model.predict(image, conf=conf)

        # # Plot the detected objects on the video frame
        res_plotted = res[0].plot()
        st_frame.image(res_plotted,
                    caption='Detected Video',
                    channels="BGR",
                    use_column_width=True
                    )



    def play_webcam(self, conf, model):
        """
        Plays a webcam stream. Detects Objects in real-time using the YOLOv8 object detection model.

        Parameters:
            conf: Confidence of YOLOv8 model.
            model: An instance of the `YOLOv8` class containing the YOLOv8 model.

        Returns:
            None

        Raises:
            None
        """
        source_webcam = 0
        is_display_tracker, tracker = True, "bytetrack.yaml"
        
        try:
            vid_cap = cv2.VideoCapture(source_webcam)
            st_frame = st.empty()
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    self._display_detected_frames(conf,
                                            model,
                                            st_frame,
                                            image,
                                            True,
                                            "bytetrack.yaml",
                                            )
                else:
                    vid_cap.release()
                    break
        except Exception as e:
            st.error(f"Error occurred while opening the webcam: {e}")
            pass

    def play_rtsp_stream(self, conf, model):
        """
        Plays an rtsp stream. Detects Objects in real-time using the YOLOv8 object detection model.

        Parameters:
            conf: Confidence of YOLOv8 model.
            model: An instance of the `YOLOv8` class containing the YOLOv8 model.

        Returns:
            None

        Raises:
            None
        """
        source_rtsp = "rtsp://807e9439d5ca.entrypoint.cloud.wowza.com:1935/app-rC94792j/068b9c9a_stream2"
        st.sidebar.caption('Example URL: rtsp://admin:12345@192.168.1.210:554/Streaming/Channels/101')
        is_display_tracker, tracker = True, "bytetrack.yaml"
        try:
            vid_cap = cv2.VideoCapture(source_rtsp)
            st_frame = st.empty()
            while (vid_cap.isOpened()):
                success, image = vid_cap.read()
                if success:
                    self._display_detected_frames(conf,
                                            model,
                                            st_frame,
                                            image,
                                            is_display_tracker,
                                            tracker
                                            )
                else:
                    vid_cap.release()
                    # vid_cap = cv2.VideoCapture(source_rtsp)
                    # time.sleep(0.1)
                    # continue
                    break
        except Exception as e:
            vid_cap.release()
            st.sidebar.error("Error loading RTSP stream: " + str(e))


    def facial_code(self):
        btn_radio_op = st.selectbox('Select an option', ['do_nothing','with_url', 'with_video', 'with_image'])

        # Add a button to take a photo from the integrated camera
        if btn_radio_op == 'do_nothing':
            st.write('do_nothing')
        elif btn_radio_op == 'with_url':
            print('with_url')
            self.play_rtsp_stream(0.5, YOLO('./media/yolov8n.pt'))
        elif btn_radio_op == 'with_video':
            print('with_video')
            # Add your code to capture an image from the integrated camera
            self.play_webcam(0.5, YOLO('./media/yolov8n.pt'))
        
        else:
            # Add a file uploader widget
            uploaded_file = st.file_uploader("Upload or take a photo", type=["jpg", "jpeg", "png"])

            if uploaded_file is not None:
                # Process the uploaded file
                st.image(uploaded_file, caption='Uploaded Image', use_column_width=True)

                uploaded_image = PIL.Image.open(uploaded_file)
                model = YOLO('./media/yolov8n.pt')
                res = model.predict(uploaded_image,
                                        conf=0.5
                                        )
                
                res_plotted = res[0].plot()[:, :, ::-1]
                st.image(res_plotted, caption='Detected Image',
                            use_column_width=True)            
        
        st.button('logout', on_click=self.logout)

    def logout(self):
        st.session_state.clear()
        time.sleep(2)
        print('ddjdjfndn')
        print(self.token)
        redirect_url = 'http://localhost:8000/api/continue-session/?'+ urlencode({'sessionId': self.token})
        st.markdown(f'<meta http-equiv="refresh" content="0;URL={redirect_url}">', unsafe_allow_html=True)
    
    def run(self):
        self.facial_code()
    
    @staticmethod
    def validate_token(token):
        response = requests.get('http://localhost:8000/api/validate-token/?'+ urlencode({'session_token': token}))
        return response.json()

if __name__ == '__main__':
    st.sidebar = st.empty()
    App().run()
