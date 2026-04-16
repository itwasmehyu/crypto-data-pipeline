# 🚀 Crypto Data Pipeline: End-to-End Automated ELT

Hệ thống tự động hóa thu thập, xử lý và kiểm soát chất lượng dữ liệu tiền điện tử theo thời gian thực, xây dựng dựa trên mô hình **Modern Data Stack**.

## 📌 Tổng quan dự án
Dự án này là một Data Pipeline hoàn chỉnh (End-to-End) thực hiện quy trình **ELT (Extract - Load - Transform)**. Hệ thống tự động lấy dữ liệu thô từ API, lưu trữ vào kho dữ liệu và áp dụng các quy tắc biến đổi dữ liệu chuyên nghiệp để sẵn sàng cho việc phân tích.

## 🛠 Tech Stack & Kiến trúc
Dự án áp dụng kiến trúc **Medallion Architecture** (Bronze - Silver - Gold):

* **Orchestrator:** [Apache Airflow](https://airflow.apache.org/) - Điều phối và lập lịch chạy các task tự động.
* **Transformation:** [dbt (Data Build Tool)](https://www.getdbt.com/) - Quản lý logic biến đổi dữ liệu bằng SQL và kiểm soát chất lượng (Data Quality).
* **Database:** [DuckDB](https://duckdb.org/) - OLAP Database hiệu năng cao cho dữ liệu dạng bảng.
* **Infrastructure:** [Docker](https://www.docker.com/) - Đóng gói toàn bộ hệ thống để vận hành nhất quán trên mọi môi trường.
* **Language:** Python (Requests, Pandas) - Thu thập dữ liệu từ **CoinGecko API**.

## 🏗 Quy trình vận hành (Data Flow)
1.  **Extract & Load (Bronze):** Python script lấy dữ liệu từ API và lưu thành các file CSV thô kèm timestamp vào thư mục `data/`.
2.  **Transform (Silver):** dbt chuẩn hóa dữ liệu từ CSV (Schema mapping, Casting types) và lưu vào DuckDB dưới dạng các Staging Views.
3.  **Refine (Gold):** dbt tạo ra các bảng Fact (`fct_crypto_prices`) chứa dữ liệu sạch, duy nhất và sẵn sàng để phân tích xu hướng.
4.  **Data Quality:** Hệ thống áp dụng **dbt-test** (Unique, Not-null) để đảm bảo tính toàn vẹn của dữ liệu trước khi hoàn tất chu trình.

## 📂 Cấu trúc thư mục
```text
.
├── dags/                   # Airflow DAGs (Định nghĩa workflow)
├── my_crypto_project/      # Dự án dbt (Models, Macros, Tests)
│   ├── models/             # Logic biến đổi dữ liệu SQL
│   ├── schema.yml          # Cấu hình Data Quality tests
│   └── profiles.yml        # Kết nối Database (Docker environment)
├── data/                   # Lưu trữ CSV thô và file database (.db)
├── docker-compose.yaml     # Hạ tầng Docker
└── .gitignore              # Loại bỏ các file rác và dữ liệu nặng
```

## 🚀 Hướng dẫn khởi chạy

Để vận hành hệ thống này trên máy cục bộ, bạn chỉ cần thực hiện các bước sau (Yêu cầu đã cài đặt **Docker** và **Docker Compose**):

1. **Clone repository:**
   ```bash
   git clone [https://github.com/huynguyen/crypto_pipeline.git](https://github.com/huynguyen/crypto_pipeline.git)
   cd crypto_pipeline
   ```
2. **Khởi động hệ thống:**
   ```bash
   docker compose up -d
   ```
3. **Cấu hình môi trường (Lần đầu chạy):**

   Do dbt được cài đặt trong môi trường chạy (runtime), bạn cần cài đặt dbt-duckdb vào container Airflow:
   ```bash
   docker exec -u airflow -it crypto_pipeline-airflow-1 python3 -m pip install --user dbt-duckdb pandas requests
   ```
4. **Vận hành và Theo dõi:**

* Truy cập giao diện Airflow: http://localhost:8080 (Tài khoản: airflow / Mật khẩu: airflow).
* Tìm DAG có tên crypto_daily_pipeline.
* Gạt nút Pause/Unpause sang màu xanh để kích hoạt Pipeline.
