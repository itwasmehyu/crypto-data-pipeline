import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

# Cấu hình trang
st.set_page_config(page_title="Crypto Real-time Dashboard", layout="wide")

st.title("🚀 Crypto Data Pipeline Dashboard")
st.markdown(f"Dữ liệu được cập nhật tự động mỗi **15 phút** bởi Airflow")

# Hàm lấy dữ liệu từ DuckDB
def get_data():
    # Trỏ đúng đường dẫn đến file db của bạn
    con = duckdb.connect(database='data/crypto_data.db', read_only=True)
    query = """
        SELECT 
            extracted_at as timestamp, 
            symbol, 
            price_usd,
            price_usd / FIRST_VALUE(price_usd) OVER (PARTITION BY symbol ORDER BY timestamp) - 1 as return_pct
        FROM fct_crypto_prices
        ORDER BY timestamp DESC
    """
    df = con.execute(query).df()
    con.close()
    return df

try:
    df = get_data()

    # Hiển thị các chỉ số quan trọng (Metrics)
    latest_time = df['timestamp'].max()
    st.info(f"Dữ liệu mới nhất tính đến: {latest_time}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Biến động giá theo thời gian")
        fig_price = px.line(df, x='timestamp', y='price_usd', color='symbol', 
                            title="Giá Crypto (USD)", template="plotly_dark")
        st.plotly_chart(fig_price, use_container_width=True)

    with col2:
        st.subheader("Bảng dữ liệu chi tiết")
        st.dataframe(df.head(10), use_container_width=True)

    # Nút refresh thủ công
    if st.button('Cập nhật dữ liệu mới'):
        st.rerun()

except Exception as e:
    st.error(f"Đang đợi dữ liệu từ Airflow... Lỗi: {e}")