{{ config(
    materialized='materialized_view'
) }}

WITH monthly_revenue_cte AS (
	SELECT
		DATE_TRUNC('month', date_utc) AS month,
		SUM(total) AS monthly_revenue
	FROM {{ ref('stg_transactions') }}
	WHERE date_utc >= NOW() - INTERVAL '7 months'
	GROUP BY 1
	ORDER BY 1 ASC
)
SELECT
	month,
	monthly_revenue,
	LAG(monthly_revenue) OVER (ORDER BY month) AS previous_month_revenue,
	ROUND(COALESCE( ((monthly_revenue - LAG(monthly_revenue) OVER (ORDER BY month)) /
			LAG(monthly_revenue) OVER (ORDER BY month)) * 100, 0)::numeric, 2) AS revenue_growth_percent
FROM monthly_revenue_cte
WHERE month >= DATE_TRUNC('month', NOW()) - INTERVAL '6 months'
