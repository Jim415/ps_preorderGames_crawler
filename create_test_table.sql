-- Create test table for PlayStation Store Crawler
-- This table has the same structure as the existing preorder_games table

USE playstation_crawler;

-- Drop the test table if it exists
DROP TABLE IF EXISTS `preorder_games_test`;

-- Create the test table with the same structure as the original table
CREATE TABLE `preorder_games_test` (
  `id` int NOT NULL AUTO_INCREMENT,
  `crawl_date` date NOT NULL,
  `region` varchar(10) NOT NULL,
  `game_name` text NOT NULL,
  `display_rank` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_crawl_date` (`crawl_date`),
  KEY `idx_region` (`region`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Add a unique constraint to prevent duplicate entries for the same date/region combination
ALTER TABLE `preorder_games_test` 
ADD UNIQUE KEY `unique_date_region` (`crawl_date`, `region`);

-- Verify the table was created successfully
SELECT 'Test table preorder_games_test created successfully!' as status; 