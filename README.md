# Vehicle Counting System

## 📌 Project Overview

This project is a Smart Vehicle Counting System that uses YOLOv8 for object detection, combined with Firebase for data management and Arduino (ESP32-CAM) for real-time camera input. The application is built using Python and developed in PyCharm.

## 🔧 Technologies Used

YOLOv8 – Object detection model for vehicle recognition.

PyCharm – IDE for developing the Python application.

Firebase – Cloud database for storing and retrieving vehicle count data.

Arduino ESP32-CAM – Capturing real-time images for vehicle detection.

Tkinter – GUI framework for building the application interface.

OpenCV (cv2) – Image processing and real-time video frame handling.

NumPy – Efficient numerical computations.

## 🏗 Project Structure

├── app/
│   ├── main.py           # Main application file
│   ├── gui.py            # Tkinter GUI implementation
│   ├── detector.py       # YOLOv8 vehicle detection module
│   ├── firebase.py       # Firebase integration
│   ├── arduino.py        # ESP32-CAM communication handler
│   ├── config.py         # Configuration settings
│
├── models/
│   ├── yolov8_model.pt   # Pretrained YOLOv8 model
│
├── assets/
│   ├── test_videos/      # Sample test videos
│   ├── test_images/      # Sample test images
│
├── requirements.txt      # Dependencies
├── README.md             # Project documentation


## 🚀 Features

✔️ Real-time vehicle detection using YOLOv8✔️ Live streaming from ESP32-CAM✔️ Data synchronization with Firebase✔️ User-friendly GUI with Tkinter✔️ Offline & Online processing modes

## 📡 ESP32-CAM & Firebase Integration

The ESP32-CAM captures images and sends them to Firebase.

The Python application retrieves images from Firebase and performs YOLOv8-based vehicle detection.

Detected vehicle counts are updated back in Firebase for real-time monitoring.

## 📝 Future Improvements

🔹 Improve accuracy with custom-trained YOLOv8 models.🔹 Add vehicle classification (e.g., car, bus, truck).🔹 Deploy the system on an embedded device (e.g., Raspberry Pi).🔹 Integrate real-time traffic analytics.
## 🎨 UI Screenshots
Main page:
![image](https://github.com/user-attachments/assets/2b635cc9-6de0-4ee1-b957-698645f338ac)
Select to count and classify vehicles from local images:
![image](https://github.com/user-attachments/assets/10f50067-c235-4507-8e4e-3c759ba1c79d)
Counting cars from Video:
![image](https://github.com/user-attachments/assets/cc957c8b-b0d3-4678-8b22-c9da5510215e)




## 📞 Contact

For any inquiries, feel free to reach out:

📧 Email: laikhacminhquang24032002@gmail.com

🔗 GitHub: Tommy240302
