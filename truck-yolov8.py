import tkinter as tk
from tkinter import font, messagebox
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
from ultralytics import YOLO
import cv2
import numpy as np
from firebase_admin import credentials, storage, initialize_app, db

window = tk.Tk()
window.title("Vehicle Detection System")
window.geometry("900x600")
window.configure(bg="#F5F5F5")  # Background

# Tạo font chữ tùy chỉnh
title_font = font.Font(family="Helvetica", size=16, weight="bold")
label_font = font.Font(family="Helvetica", size=12)
button_font = font.Font(family="Helvetica", size=12, weight="bold")

# Load model YOLOv8
model = YOLO('yolov8s.pt')  # Load YOLOv8 small model
classes = model.names  # Các lớp COCO đã tích hợp sẵn trong model YOLOv8

cap = cv2.VideoCapture(0)  # Đối tượng video

# Hàm tiền xử lý ảnh
def preprocess_image(frame):
    # Chuyển đổi ảnh sang màu xám
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Áp dụng Gaussian Blur để giảm nhiễu
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Sử dụng CLAHE để cải thiện độ tương phản
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(blurred)

    # Chuyển đổi về định dạng BGR để đưa vào mô hình YOLO
    bgr_image = cv2.cvtColor(enhanced, cv2.COLOR_GRAY2BGR)

    return bgr_image

# Cấu hình Firebase
cred = credentials.Certificate("C:/Users/ACER/PycharmProjects/trunks/firebase.json")
initialize_app(cred, {
    'storageBucket': 'fir-demo-df6f7.appspot.com',
    'databaseURL': 'https://fir-demo-df6f7-default-rtdb.firebaseio.com/'
})


# Hàm lấy danh sách ảnh từ Firebase Storage
def list_files_from_firebase():
    bucket = storage.bucket()  # Kết nối đến Firebase Storage
    blobs = bucket.list_blobs(prefix="data/")  # Lấy các file trong thư mục 'data/'

    files = []
    for blob in blobs:
        files.append(blob.name.replace("data/", ""))  # Lấy tên file
    return files
# Hàm để đẩy số lượng xe lên Firebase
def push_vehicle_count_to_firebase(vehicle_count):
    ref = db.reference('vehicle_count')  # Tạo tham chiếu đến node 'vehicle_count' trong Firebase Realtime Database
    ref.set(vehicle_count)

def open_selected_image_from_firebase(image_name):
    bucket = storage.bucket()  # Kết nối đến Firebase Storage
    blob = bucket.blob(f"data/{image_name}")  # Lấy blob ảnh đã chọn từ Firebase
    image_data = blob.download_as_bytes()  # Tải ảnh dưới dạng byte

    np_array = np.frombuffer(image_data, np.uint8)  # Chuyển byte thành numpy array
    frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)  # Đọc ảnh bằng OpenCV

    if frame is not None:
        # Tiền xử lý ảnh trước khi phát hiện xe
        frame = preprocess_image(frame)

        # Phát hiện và đếm xe
        vehicle_count, detected_vehicles = detect_and_count_vehicles(frame)

        # Hiển thị số lượng xe và danh sách các loại xe đã phát hiện
        soluong.delete("1.0", tk.END)
        soluong.insert(tk.END, vehicle_count)
        xe_detected.delete("1.0", tk.END)
        xe_detected.insert(tk.END, "\n".join(detected_vehicles))

        # Thay đổi kích thước ảnh cho phù hợp với giao diện
        frame_resized = cv2.resize(frame, (450, 350))  # Điều chỉnh kích thước ảnh

        # Chuyển đổi ảnh từ OpenCV (BGR) sang RGBA để hiển thị trên Tkinter
        cv2image = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGBA)
        img = ImageTk.PhotoImage(image=Image.fromarray(cv2image))

        # Cập nhật ảnh lên Label trong giao diện
        la4.imgtk = img
        la4.configure(image=img)
        # Hiển thị số lượng xe và danh sách các loại xe đã phát hiện
        print(vehicle_count)  # In ra số lượng xe phát hiện
        push_vehicle_count_to_firebase(vehicle_count)

# Tạo cửa sổ mới cho việc chọn ảnh
def load_image_from_firebase():
    files = list_files_from_firebase()  # Lấy danh sách ảnh từ Firebase
    if not files:
        messagebox.showerror("Lỗi", "Không có ảnh trong thư mục.")
        return

    # Hiển thị danh sách ảnh để người dùng chọn
    def on_select_image(image_name):
        open_selected_image_from_firebase(image_name)  # Tải ảnh đã chọn từ Firebase
        window_new.destroy()  # Đóng cửa sổ chọn ảnh

    # Tạo cửa sổ mới cho việc chọn ảnh
    window_new = tk.Toplevel(window)  # Tạo cửa sổ con mới
    window_new.title("Chọn ảnh từ Firebase")

    listbox = tk.Listbox(window_new, height=10, width=50)
    listbox.grid(row=0, column=0, pady=20)  # Dùng grid thay vì pack

    for file in files:
        listbox.insert(tk.END, file)  # Thêm các ảnh vào Listbox

    # Nút chọn ảnh
    button_select = tk.Button(window_new, text="Chọn ảnh", command=lambda: on_select_image(listbox.get(tk.ACTIVE)))
    button_select.grid(row=1, column=0)  # Dùng grid thay vì pack


# Hàm chọn file image
def open_image_file():
    filepath = askopenfilename(
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete("1.0", tk.END)
    txt_edit.insert(tk.END, filepath)

    # Đọc và hiển thị hình ảnh
    frame = cv2.imread(filepath)
    if frame is not None:

        frame = preprocess_image(frame) # Gọi đến hàm Tiền xử lý ảnh
        vehicle_count, detected_vehicles = detect_and_count_vehicles(frame)

        # Hiển thị số lượng xe và danh sách xe
        soluong.delete("1.0", tk.END)
        soluong.insert(tk.END, vehicle_count)
        xe_detected.delete("1.0", tk.END)
        xe_detected.insert(tk.END, "\n".join(detected_vehicles))

        # Thay đổi kích thước ảnh để vừa khung hiển thị
        frame_resized = cv2.resize(frame, (450, 350))  # Kích thước khung hiển thị
        # Chuyển đổi màu sắc và hiển thị hình ảnh
        cv2image = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGBA)
        img = ImageTk.PhotoImage(image=Image.fromarray(cv2image))
        la4.imgtk = img
        la4.configure(image=img)

# Hàm phát hiện và đếm xe sử dụng YOLOv8
def detect_and_count_vehicles(frame):
    results = model(frame)  # Dự đoán với YOLOv8
    vehicle_count = 0
    detected_vehicles = []

    for result in results:
        boxes = result.boxes
        for box in boxes:
            class_id = int(box.cls[0])  # Lấy class ID
            label = classes[class_id]
            confidence = box.conf[0]  # Độ tin cậy

            # Kiểm tra nếu đối tượng là xe (car, truck, bus, ...)
            if label in ["car", "truck", "bus", "motorbike"]:
                vehicle_count += 1
                detected_vehicles.append(label)
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Lấy tọa độ bounding box
                color = (0, 255, 0)
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame, f"{label} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    return vehicle_count, detected_vehicles

# Hàm chọn file video
def openfile():
    filepath = askopenfilename(
        filetypes=[("MP4 Files", "*.mp4"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete("1.0", tk.END)
    txt_edit.insert(tk.END, filepath)
    cap.open(filepath)
    window.title(f"Vehicle Detection System - {filepath}")

# Hàm hiển thị video từ file
frame_id = 0

def showvideo():
    if cap.isOpened():
        window.after(10, videostream)  # Thay vì gọi trực tiếp videostream(), sử dụng after với window

# Hàm xử lý video stream và đếm xe
def videostream():
    if not cap.isOpened():  # Nếu video chưa mở, thoát khỏi hàm
        return

    ret, frame = cap.read()
    if not ret:
        cap.release()  # Đóng video nếu không còn frame nào
        return

    global frame_id
    frame_id += 1

    # Thay đổi kích thước khung hình ở đây
    frame = cv2.resize(frame, (400, 300))  # Kích thước mới

    vehicle_count, detected_vehicles = detect_and_count_vehicles(frame)

    soluong.delete("1.0", tk.END)
    soluong.insert(tk.END, vehicle_count)
    xe_detected.delete("1.0", tk.END)
    xe_detected.insert(tk.END, "\n".join(detected_vehicles))

    # Chuyển đổi màu sắc và hiển thị hình ảnh
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = ImageTk.PhotoImage(image=Image.fromarray(cv2image))
    la4.imgtk = img
    la4.configure(image=img)

    # Sử dụng after để gọi lại hàm videostream sau 10 ms
    window.after(10, videostream)

# Giao diện người dùng

frame1 = tk.Frame(window, width=250, height=600, bg="#C4E1F6", padx=10, pady=10)
frame1.grid(row=0, column=0, rowspan=2, sticky="nsw")
frame1.grid_propagate(False)

la1 = tk.Label(frame1, text='Mục Tùy Chọn', font=title_font, bg="#C4E1F6", fg="#003161")
txt_edit = tk.Text(frame1, padx=5, pady=5, width=25, height=1, font=label_font)
button1 = tk.Button(frame1, width=20, height=2, text='Chọn File Video', font=button_font, bg="#4A628A", fg="#ffffff", command=openfile)
button2 = tk.Button(frame1, width=20, height=2, text='Hiển Thị Video', font=button_font, bg="#4A628A", fg="#ffffff", command=showvideo)
button4 = tk.Button(frame1, width=20, height=2, text='Chọn Hình Ảnh', font=button_font, bg="#4A628A", fg="#ffffff", command=open_image_file)
button5 = tk.Button(frame1, width=20, height=2, text='Load từ Firebase', font=button_font, bg="#4A628A", fg="#ffffff", command=load_image_from_firebase)


la1.pack(pady=10)
txt_edit.pack(pady=10)
button1.pack(pady=10)
button2.pack(pady=10)
button4.pack(pady=10)
button5.pack(pady=10)

la6 = tk.Label(frame1, text='Số Lượng Xe', font=title_font, bg="#C4E1F6", fg="#003161")
soluong = tk.Text(frame1, padx=5, pady=5, width=25, height=1, font=label_font)

la6.pack(pady=10)
soluong.pack()

frame2 = tk.Frame(window, width=600, height=400, bg="#4A628A", padx=10, pady=10)
frame2.grid(row=0, column=1, sticky="nsew")
frame2.grid_propagate(False)

la2 = tk.Label(frame2, text='Ảnh sau khi tiền sử lí', font=title_font, bg="#4A628A", fg="#ffffff")
la4 = tk.Label(frame2, width=450, height=350)
la2.pack()
la4.pack()

frame4 = tk.Frame(window, width=600, height=200, bg="#4A628A", padx=10, pady=10)
frame4.grid(row=1, column=1, sticky="nsew")
frame4.grid_propagate(False)

la7 = tk.Label(frame4, text='Danh Sách Xe Đã Đếm', font=title_font, bg="#4A628A", fg="#ffffff")
xe_detected = tk.Text(frame4, padx=5, pady=5, width=40, height=8, font=label_font)

la7.pack(pady=5)
xe_detected.pack()

window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
window.columnconfigure(1, weight=1)
window.mainloop()