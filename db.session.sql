SELECT bangazon_api_product.name AS product, bangazon_api_product.price AS price, bangazon_api_store.name AS store
FROM bangazon_api_product
JOIN bangazon_api_store
    ON bangazon_api_product.store_id = bangazon_api_store.id
WHERE price >= 500;

SELECT
                user.id AS customer_id
                ( user.first_name || " " || user.last_name ) AS customer_name,
                store.name AS seller_name
            FROM bangazon_api_favorite AS fav
            JOIN auth_user AS user
                ON fav.customer_id = user.id
            JOIN bangazon_api_store AS store
                ON fav.store_id = store.id

