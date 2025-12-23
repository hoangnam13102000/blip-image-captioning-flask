# BLIP Image Captioning Web Application (Flask)

## Giới thiệu
Đây là đồ án môn **Phân tích dữ liệu**, tập trung xây dựng **ứng dụng web Flask** cho phép **tự động chú thích hình ảnh (Image Captioning)** dựa trên mô hình **BLIP (Bootstrapped Language-Image Pretraining)** của Salesforce.

Ứng dụng cho phép người dùng:
- Tải lên một hình ảnh
- Hệ thống tự động sinh chú thích mô tả nội dung ảnh
- Hiển thị kết quả trực quan ngay trên giao diện web

---

## Mục tiêu của đồ án
- Nghiên cứu bài toán **Image Captioning**
- Ứng dụng mô hình **BLIP pre-trained + fine-tuning**
- Triển khai mô hình học sâu vào **ứng dụng web Flask**
- Kết hợp kiến thức **Phân tích dữ liệu + Deep Learning + Web**

---

## Công nghệ sử dụng
- **Python 3.9+**
- **Flask**
- **PyTorch**
- **HuggingFace Transformers**
- **BLIP Image Captioning Model**
- **HTML / CSS / JavaScript**
- **Matplotlib** (trực quan kết quả)

---

##  Cấu trúc thư mục
```text
FinalProject/
│
├── app.py                     # Flask backend
├── requirements.txt           # Thư viện cần cài
├── README.md                  # Mô tả project
├── .gitignore
│
├── model/
│   ├── blip_model.pkl         # (KHÔNG upload GitHub)
│   └── blip_processor.pkl     # (KHÔNG upload GitHub)
│
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── script.js
│   └── uploads/               # Lưu ảnh upload tạm
│
└── templates/
    ├── index.html             # Trang upload ảnh
    └── result.html            # Trang hiển thị kết quả
