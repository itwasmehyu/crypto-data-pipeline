{{ config(materialized='view') }}

WITH source_data AS (
    SELECT * FROM {{ source('external_source', 'raw_crypto') }}
)

SELECT
    id as coin_id,
    symbol,
    name,
    current_price as price_usd,
    market_cap,
    total_volume,
    extracted_at
FROM source_data