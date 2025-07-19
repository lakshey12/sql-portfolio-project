SELECT
    DATE_FORMAT(o.order_date, '%Y-%m') AS sales_month,
    ROUND(SUM(oi.quantity * oi.price_per_unit), 2) AS monthly_revenue
FROM
    Orders o
JOIN
    Order_Items oi ON o.order_id = oi.order_id
GROUP BY
    sales_month
ORDER BY
    sales_month;