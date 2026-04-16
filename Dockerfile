# # Sử dụng chính xác bản Airflow bạn đang dùng
# FROM apache/airflow:2.7.2

# # Chuyển sang user airflow để cài thư viện
# USER airflow

# # Copy danh sách thư viện vào container
# COPY requirements.txt .

# # Cài đặt thư viện
# RUN pip install --no-cache-dir -r requirements.txt

# # Tự động thêm đường dẫn dbt vào PATH để không bao giờ bị lỗi "Command not found"
# ENV PATH="${PATH}:/home/airflow/.local/bin"





FROM apache/airflow:2.7.1-python3.10

USER airflow

# Cài đặt các thư viện cần thiết trực tiếp vào image
RUN pip install --no-cache-dir dbt-duckdb pandas requests

# Tự động thêm PATH để gọi được lệnh dbt ở bất cứ đâu
ENV PATH="${PATH}:/home/airflow/.local/bin"