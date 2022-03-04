SELECT bangazon_api_product.name AS product, bangazon_api_product.price AS price, bangazon_api_store.name AS store
FROM bangazon_api_product
JOIN bangazon_api_store
    ON bangazon_api_product.store_id = bangazon_api_store.id
WHERE price >= 500