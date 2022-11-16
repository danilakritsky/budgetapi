-- ####### Тестовое задание SQL #######   
-- Вам дана база данных ноутбуков, которая содержит две таблицы.
-- Таблица notebooks\_brand содержит данные о наименовании брендов ноутбуков.
-- Таблица notebooks\_notebook содержит данные о наименовании ноутбука,
-- его диагонали, ширине, глубине и высоте, а также имеет ссылку на бренд,
-- к которому относится данная модель.   
   
-- ####### Задание: 1. ######
-- Напишите запрос, который подсчитает какое количество ноутбуков
-- представлено в каждом бренде.
-- Отсортируйте данные по убыванию.   

SELECT
    b.title AS brand,
    COUNT(*) AS notebook_count
FROM notebooks_notebook AS n
    LEFT JOIN notebooks_brand AS b
        ON n.brand_id = b.id
GROUP BY b.title
ORDER BY
    notebook_count DESC;

-- ####### Задание: 2. ######
-- Вам необходимо выделить группы ноутбуков по размерам.
-- Для этого размеры предварительно нужно округлить в большую сторону
-- до ближайшего 0 или 5 и затем сгруппировать по одинаковым размерам,
-- подсчитав количество ноутбуков в каждой группе.
-- Отсортируйте данные по размерам.

WITH rounded(width, depth, height) AS (
    SELECT
        CEILING(width / 5) * 5,
        CEILING(depth / 5) * 5,
        CEILING(height / 5) * 5
    FROM notebooks_notebook
)
SELECT
    width, depth, height, COUNT(*) AS notebook_count
FROM rounded
GROUP BY width, depth, height
ORDER BY width , depth, height;
