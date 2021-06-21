SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

USE `review`;

DROP TABLE IF EXISTS `comment`;
CREATE TABLE IF NOT EXISTS `comment` (
    `comment_id` int(11) NOT NULL AUTO_INCREMENT,
    `review_id` int(11) NOT NULL,
    `user_id` int(8) NOT NULL,
    `user_name` varchar(32) NOT NULL,
    `comment_text` varchar(500) NOT NULL,
    `comment_likes` int(10) NOT NULL,
    `comment_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `comment_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`comment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

INSERT INTO `comment` (`review_id`, `user_id`, `user_name`, `comment_text`, `comment_likes`) 
VALUES (1, 1, "Apple TAN", "I love McGriddles too!", 20);

INSERT INTO `comment` (`review_id`, `user_id`, `user_name`, `comment_text`, `comment_likes`) 
VALUES (2, 2, "Orange LEE", "Hello oppa!", 23);

COMMIT