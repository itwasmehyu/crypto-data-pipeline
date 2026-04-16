{{ config(materialized='table') }}

WITH latest_prices AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (
            PARTITION BY coin_id 
            ORDER BY extracted_at DESC
        ) as rn
    FROM {{ ref('stg_crypto') }}
)

SELECT
    coin_id,
    symbol,
    name,
    price_usd,
    market_cap,
    total_volume,
    extracted_at
FROM latest_prices
WHERE rn = 1