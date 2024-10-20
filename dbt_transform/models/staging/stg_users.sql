WITH users_dedup AS (
    SELECT *
    FROM ({{ remove_duplicates('raw_users', 'customer_id') }}) as base_dedup
)
SELECT      customer_id,
            customer_name,
            customer_email,
            CASE
                WHEN customer_name IS NOT NULL THEN 1
                ELSE 0
            END AS valid_name
FROM        users_dedup
