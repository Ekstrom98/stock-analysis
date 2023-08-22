WITH ranked_by_date AS (
SELECT 
*,
DENSE_RANK() OVER (PARTITION BY s.company_id ORDER BY s.fetched_at DESC) rank
FROM stock_data s
),
most_recent_data AS (
SELECT 
DATE(fetched_at) fetched_at, price, ema_34, ema_200, return_on_assets, return_on_equity,
trailing_earnings_per_share, price_earnings_ratio, market_capitalization, company_id,
industry_id, sector_id
FROM ranked_by_date
WHERE rank = 1
)
SELECT
r.fetched_at, r.price, r.ema_34, r.ema_200, r.return_on_assets, r.return_on_equity,
r.trailing_earnings_per_share, r.price_earnings_ratio, r.market_capitalization,
c.name, c.symbol, i.industry, s.sector, c.description
FROM most_recent_data r
LEFT JOIN companies c ON r.company_id = c.company_id
LEFT JOIN industries i ON r.industry_id = i.industry_id
LEFT JOIN sectors s ON r.sector_id = s.sector_id;