SELECT bangazon_api_product.name AS product, bangazon_api_product.price AS price, bangazon_api_store.name AS store
FROM bangazon_api_product
JOIN bangazon_api_store
    ON bangazon_api_product.store_id = bangazon_api_store.id
WHERE price >= 500;

SELECT 
    bangazon_api_order.id AS orderId,
    (auth_user.first_name || " " || auth_user.last_name) AS CustomerName,
    sum(price) as totalPaid,
    bangazon_api_paymenttype.merchant_name,
    bangazon_api_paymenttype.acct_number
FROM bangazon_api_order
JOIN auth_user
    ON bangazon_api_order.user_id = auth_user.id
JOIN bangazon_api_paymenttype
    ON bangazon_api_order.payment_type_id = bangazon_api_paymenttype.id
JOIN bangazon_api_orderproduct
    ON bangazon_api_order.id = bangazon_api_orderproduct.order_id
JOIN bangazon_api_product
    ON bangazon_api_orderproduct.product_id = bangazon_api_product.id

WHERE bangazon_api_order.completed_on NOT NULL;

SELECT *
FROM bangazon_api_paymenttype

SELECT
    bangazon_api_order.id AS orderId,
    (auth_user.first_name || " " || auth_user.last_name) AS CustomerName,
    bangazon_api_paymenttype.merchant_name,
    bangazon_api_paymenttype.acct_number,
    bangazon_api_product.price
FROM bangazon_api_order
JOIN auth_user
    ON bangazon_api_order.user_id = auth_user.id
JOIN bangazon_api_paymenttype
    ON bangazon_api_order.payment_type_id = bangazon_api_paymenttype.id
JOIN bangazon_api_orderproduct
    ON bangazon_api_order.id = bangazon_api_orderproduct.order_id
JOIN bangazon_api_product
    ON bangazon_api_orderproduct.product_id = bangazon_api_product.id
WHERE payment_type_id NOT NULL