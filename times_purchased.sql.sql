SELECT
    p1.product_name AS product_1,
    p2.product_name AS product_2,
    COUNT(*) AS times_purchased_together
FROM
    Order_Items oi1
JOIN
    Order_Items oi2 ON oi1.order_id = oi2.order_id AND oi1.product_id < oi2.product_id
JOIN
    Products p1 ON oi1.product_id = p1.product_id
JOIN
    Products p2 ON oi2.product_id = p2.product_id
GROUP BY
    product_1, product_2
ORDER BY
    times_purchased_together DESC
LIMIT 10;