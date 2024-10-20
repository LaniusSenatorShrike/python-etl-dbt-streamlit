{{ config(
    materialized='materialized_view'
) }}

SELECT DATE_TRUNC('month', date_utc) AS month
		,AVG(total) AS avg_transaction_amount
FROM {{ ref('stg_transactions') }}
WHERE date_utc >= NOW() - INTERVAL '5 months'
GROUP BY 1
