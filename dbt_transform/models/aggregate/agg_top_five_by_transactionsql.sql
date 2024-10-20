{{ config(
    materialized='materialized_view'
) }}

SELECT 	customer_id,
		SUM(total) AS sum_transactions
FROM {{ ref('stg_transactions') }}
GROUP BY 1
ORDER BY 2 DESC
LIMIT 5