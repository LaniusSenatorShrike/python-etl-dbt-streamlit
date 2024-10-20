WITH products_dedup AS (
    SELECT *
    FROM ({{ remove_duplicates('raw_products', 'surrogate_key') }}) as base_dedup
)
SELECT  subscription_id,
        plan,
        product,
        interval,
        amount,
        status,
        surrogate_key
FROM    products_dedup

