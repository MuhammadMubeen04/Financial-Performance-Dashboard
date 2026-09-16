-- ============================================================
-- Financial Performance - Key SQL Queries (MySQL)
-- ============================================================

USE financial_analytics;

-- 1. OVERALL KPIs
SELECT 
    ROUND(SUM(CASE WHEN Type = 'Revenue' THEN Actual ELSE 0 END), 2) AS total_revenue,
    ROUND(SUM(CASE WHEN Type = 'Expense' THEN Actual ELSE 0 END), 2) AS total_expenses,
    ROUND(SUM(CASE WHEN Type = 'Revenue' THEN Actual ELSE 0 END) -
          SUM(CASE WHEN Type = 'Expense' THEN Actual ELSE 0 END), 2) AS net_profit,
    ROUND(
        (SUM(CASE WHEN Type = 'Revenue' THEN Actual ELSE 0 END) -
         SUM(CASE WHEN Type = 'Expense' THEN Actual ELSE 0 END)) /
        NULLIF(SUM(CASE WHEN Type = 'Revenue' THEN Actual ELSE 0 END), 0) * 100
    , 2) AS profit_margin_pct
FROM financials;


-- 2. MONTHLY P&L TREND
SELECT 
    YearMonth,
    ROUND(SUM(CASE WHEN Type = 'Revenue' THEN Actual ELSE 0 END), 2) AS revenue,
    ROUND(SUM(CASE WHEN Type = 'Expense' THEN Actual ELSE 0 END), 2) AS expenses,
    ROUND(SUM(CASE WHEN Type = 'Revenue' THEN Actual ELSE 0 END) -
          SUM(CASE WHEN Type = 'Expense' THEN Actual ELSE 0 END), 2) AS profit
FROM financials
GROUP BY YearMonth
ORDER BY YearMonth;


-- 3. REVENUE BY CATEGORY
SELECT 
    Category,
    ROUND(SUM(Actual), 2) AS actual_revenue,
    ROUND(SUM(Budget), 2) AS budget_revenue,
    ROUND(SUM(Actual) - SUM(Budget), 2) AS variance
FROM financials
WHERE Type = 'Revenue'
GROUP BY Category
ORDER BY actual_revenue DESC;


-- 4. EXPENSES BY CATEGORY
SELECT 
    Category,
    ROUND(SUM(Actual), 2) AS actual_expense,
    ROUND(SUM(Budget), 2) AS budget_expense,
    ROUND(SUM(Actual) - SUM(Budget), 2) AS variance
FROM financials
WHERE Type = 'Expense'
GROUP BY Category
ORDER BY actual_expense DESC;


-- 5. EXPENSES BY DEPARTMENT
SELECT 
    Department,
    ROUND(SUM(Actual), 2) AS actual_expense,
    ROUND(SUM(Budget), 2) AS budget_expense,
    ROUND(SUM(Actual) - SUM(Budget), 2) AS variance
FROM financials
WHERE Type = 'Expense'
GROUP BY Department
ORDER BY actual_expense DESC;


-- 6. BUDGET VS ACTUAL (OVERALL)
SELECT 
    Type,
    ROUND(SUM(Actual), 2) AS total_actual,
    ROUND(SUM(Budget), 2) AS total_budget,
    ROUND(SUM(Actual) - SUM(Budget), 2) AS variance,
    ROUND((SUM(Actual) - SUM(Budget)) / NULLIF(SUM(Budget), 0) * 100, 2) AS variance_pct
FROM financials
GROUP BY Type;


-- 7. YEARLY SUMMARY
SELECT 
    Year,
    ROUND(SUM(CASE WHEN Type = 'Revenue' THEN Actual ELSE 0 END), 2) AS revenue,
    ROUND(SUM(CASE WHEN Type = 'Expense' THEN Actual ELSE 0 END), 2) AS expenses,
    ROUND(SUM(CASE WHEN Type = 'Revenue' THEN Actual ELSE 0 END) -
          SUM(CASE WHEN Type = 'Expense' THEN Actual ELSE 0 END), 2) AS profit
FROM financials
GROUP BY Year
ORDER BY Year;


-- 8. TOP EXPENSE DEPARTMENTS WITH MARGIN CONTEXT
SELECT 
    Department,
    ROUND(SUM(CASE WHEN Type = 'Expense' THEN Actual ELSE 0 END), 2) AS expenses
FROM financials
GROUP BY Department
ORDER BY expenses DESC;
