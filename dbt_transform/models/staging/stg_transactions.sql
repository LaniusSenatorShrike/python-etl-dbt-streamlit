WITH transactions_dedup AS (
    SELECT *
    FROM ({{ remove_duplicates('raw_transactions', 'transaction_id') }}) as base_dedup
)
SELECT      date_utc,
            transaction_id,
            customer_id,
            subscription_id,
            total,
            UPPER(currency) AS currency
FROM        transactions_dedup

