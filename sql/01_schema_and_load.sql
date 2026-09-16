-- ============================================================
-- Financial Performance Dashboard - MySQL Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS financial_analytics;
USE financial_analytics;

CREATE TABLE IF NOT EXISTS financials (
    RecordID     VARCHAR(20) PRIMARY KEY,
    Date         DATE,
    Year         INT,
    Month        INT,
    YearMonth    VARCHAR(10),
    Type         VARCHAR(20),      -- Revenue or Expense
    Category     VARCHAR(50),
    Department   VARCHAR(50),
    Actual       DECIMAL(14,2),
    Budget       DECIMAL(14,2),
    Variance     DECIMAL(14,2)
);

-- Import: data/financial_data.csv → financials table
