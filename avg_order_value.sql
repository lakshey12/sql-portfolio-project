SELECT
    ROUND(SUM(oi.quantity * oi.price_per_unit) / COUNT(DISTINCT o.order_id), 2) AS average_order_value
FROM
    Orders o
JOIN
    Order_Items oi ON o.order_id = oi.order_id;