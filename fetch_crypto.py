import requests
import pandas as pd
from datetime import datetime
import os

def fetch_data():
    # API lấy giá thị trường của các đồng coin top đầu
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": "bitcoin,ethereum,solana,cardano,ripple",
        "order": "market_cap_desc"
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status() # Kiểm tra lỗi
        data = response.json()
        
        df = pd.DataFrame(data)
        # Chỉ lấy một vài cột quan trọng
        df = df[['id', 'symbol', 'name', 'current_price', 'market_cap', 'total_volume']]
        df['extracted_at'] = datetime.now()
        
        # Lưu vào tầng Bronze (Thô)
        file_path = f"data/raw_crypto_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
        df.to_csv(file_path, index=False)
        print(f"✅ Đã tải dữ liệu thành công: {file_path}")
        
    except Exception as e:
        print(f"❌ Lỗi khi lấy dữ liệu: {e}")

if __name__ == "__main__":
    fetch_data()