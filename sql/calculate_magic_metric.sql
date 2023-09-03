WITH screened_table AS (
    SELECT *
    FROM stock_analytics
    WHERE (price_earnings_ratio IS NOT NULL) AND (price_earnings_ratio > 0)
    AND (return_on_assets IS NOT NULL) AND (return_on_assets > 0) 
), 
magic_table AS (
    SELECT fetched_at, price, ema_34, ema_200, return_on_assets, return_on_equity, price_earnings_ratio,
    market_capitalization, name, symbol, description,
    DENSE_RANK() OVER (ORDER BY price_earnings_ratio DESC) pe_score,
    DENSE_RANK() OVER (ORDER BY return_on_assets) roa_score
    FROM screened_table
)
SELECT fetched_at, price, ema_34, ema_200, return_on_assets, return_on_equity, price_earnings_ratio,
    market_capitalization, name, symbol, description,
   (pe_score+roa_score) magic_score 
FROM magic_table;