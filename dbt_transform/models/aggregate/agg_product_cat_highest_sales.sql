{{ config(
    materialized='materialized_view'
) }}

WITH RANKS AS (
SELECT		pro.product,
			RANK() OVER (ORDER BY SUM(tra.total) DESC) AS rank
FROM		{{ ref('stg_products') }} pro
LEFT JOIN	{{ ref('stg_transactions') }} tra ON pro.subscription_id = tra.subscription_id
GROUP BY	1
)
SELECT		product
FROM		RANKS
WHERE		rank = 1