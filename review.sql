SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+08:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS `review` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `review`;

DROP TABLE IF EXISTS `review`;
CREATE TABLE IF NOT EXISTS `review` (
    `review_id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(8) NOT NULL,
    `user_name` varchar(32) NOT NULL,
    `place_id` varchar(255) NOT NULL,
    `place_name` varchar(255) NOT NULL,
    `rating` int(10) NOT NULL,
    `review_title` varchar(50) NOT NULL,
    `review_text` varchar(5000) NOT NULL,
    `likes` int(10) NOT NULL,
    `views` int(10) NOT NULL,
    `imageurl` varchar(255) NOT NULL,
    `created` timestamp DEFAULT CURRENT_TIMESTAMP NOT NULL,
    `modified` timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP  NOT NULL,
    PRIMARY KEY (`review_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

INSERT INTO `review` (`user_id`, `user_name`, `place_id`, `place_name`, `rating`, `review_title`, `review_text`, `likes`, `views`, `imageurl`) VALUES
(1, "Apple TAN", "ChIJ5-RO0h8X2jERJjpGocFQ3Qw", "McDonald's Bishan Park", 4, "I love McGriddles!", "My love for McGriddles", 204, 504, "https://esd-image.s3.amazonaws.com/r/1.jpg");

INSERT INTO `review` (`user_id`, `user_name`, `place_id`, `place_name`, `rating`, `review_title`, `review_text`, `likes`, `views`, `imageurl`) VALUES
(2, "Orange LEE", "ChIJ5RI1hM0Z2jERbO48YRVTOJM", "Wildfire Burgers", 5, "Truffle burger is so juicy!", "Juicy patty uwu", 103, 303, "https://esd-image.s3.amazonaws.com/r/2.jpg");

COMMIT