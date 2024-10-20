WITH raw_data AS (
    SELECT      *
    FROM        ({{raw_data_layer('transactions')}}) AS base_table
)
SELECT      date_utc,
            transaction_id,
            customer_id,
            subscription_id,
            total,
            currency
FROM        raw_data
