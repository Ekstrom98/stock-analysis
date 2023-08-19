CREATE TABLE IF NOT EXISTS companies (
    company_id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR,
    symbol VARCHAR(32) UNIQUE,
    description TEXT
);
CREATE TABLE IF NOT EXISTS industries (
    industry_id SERIAL PRIMARY KEY NOT NULL,
    industry VARCHAR(200)
);
CREATE TABLE IF NOT EXISTS sectors (
    sector_id SERIAL PRIMARY KEY NOT NULL,
    sector VARCHAR(200)
);
CREATE TABLE IF NOT EXISTS stock_data (
    id SERIAL PRIMARY KEY NOT NULL,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    price FLOAT,
    ema_34 FLOAT,
    ema_200 FLOAT,
    return_on_assets FLOAT,
    return_on_equity FLOAT,
    trailing_earnings_per_share FLOAT,
    price_earnings_ratio FLOAT,
    market_capitalization FLOAT,
    company_id BIGINT REFERENCES companies(company_id) ON DELETE NO ACTION ON UPDATE CASCADE,
    industry_id BIGINT REFERENCES industries(industry_id) ON DELETE SET NULL ON UPDATE CASCADE,
    sector_id BIGINT REFERENCES sectors(sector_id) ON DELETE SET NULL ON UPDATE CASCADE
);