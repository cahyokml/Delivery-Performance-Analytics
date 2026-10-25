-- ==========================================
-- DELIVERY PERFORMANCE ANALYTICS QUERIES
-- ==========================================

-- 1. KPI OVERALL (On-Time Delivery Rate, Avg Delay, Total Late Orders)
SELECT 
    COUNT(order_id) AS total_orders,
    ROUND(AVG(delay_days), 2) AS avg_delay_days,
    SUM(CASE WHEN is_late = 1 THEN 1 ELSE 0 END) AS total_late_orders,
    ROUND((SUM(CASE WHEN is_on_time = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(order_id)), 2) AS otd_rate_percentage
FROM fact_orders;

-- 2. PERFORMA PENGIRIMAN PER NEGARA BAGIAN (STATE) TERBURUK
SELECT 
    customer_state,
    COUNT(order_id) AS total_orders,
    SUM(CASE WHEN is_late = 1 THEN 1 ELSE 0 END) AS late_orders,
    ROUND((SUM(CASE WHEN is_late = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(order_id)), 2) AS late_rate_percentage,
    ROUND(AVG(delay_days), 2) AS avg_delay_days
FROM fact_orders
GROUP BY customer_state
HAVING total_orders > 50 -- Filter agar data statistik valid
ORDER BY late_rate_percentage DESC
LIMIT 10;

-- 3. DAMPAK KETERLAMBATAN TERHADAP SKOR ULASAN (REVIEW)
SELECT 
    CASE 
        WHEN is_late = 1 THEN 'Late Delivery'
        ELSE 'On-Time Delivery'
    END AS delivery_status,
    COUNT(order_id) AS total_orders,
    ROUND(AVG(review_score), 2) AS avg_review_score,
    SUM(CASE WHEN review_score <= 2 THEN 1 ELSE 0 END) AS bad_reviews_count
FROM fact_orders
WHERE review_score IS NOT NULL
GROUP BY is_late;

-- 4. PERFORMA BERDASARKAN TIPE PEMBAYARAN
SELECT 
    payment_type,
    COUNT(order_id) AS total_orders,
    ROUND(AVG(delay_days), 2) AS avg_delay_days,
    ROUND(AVG(review_score), 2) AS avg_review_score
FROM fact_orders
WHERE payment_type IS NOT NULL
GROUP BY payment_type
ORDER BY total_orders DESC;