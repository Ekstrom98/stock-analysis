CREATE TABLE IF NOT EXISTS companies (
    id SERIAL PRIMARY KEY,
    company_name varchar,
    company_symbol varchar(32)
);
CREATE TABLE IF NOT EXISTS company_data (
    id SERIAL PRIMARY KEY,
    company_name varchar,
    company_symbol varchar(32),
    industry varchar(100),
    sector varchar(100),
    full_time_employees int,
    return_on_assets float,
    return_on_equity float,
    market_cap bigint,
    current_price float,
    trailing_eps float,
    current_pe float
);