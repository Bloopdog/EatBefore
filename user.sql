SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS `user` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `user`;

DROP TABLE IF EXISTS `user`;
CREATE TABLE IF NOT EXISTS `user` (
    `user_id` int(8) NOT NULL AUTO_INCREMENT,
    `user_name` varchar(32) NOT NULL,
    `password` varchar(32) NOT NULL,
    `email` varchar(32) NOT NULL,
    `wallet_balance` float(10) NOT NULL,
    `total_views` int(10) NOT NULL,
    PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

INSERT INTO `user` (`user_name`, `password`, `email`, `wallet_balance`, `total_views`) 
VALUES ("Apple TAN", "ronaldmcdonald", "xenophitez@gmail.com", 500.0, 1000);

INSERT INTO `user` (`user_name`, `password`, `email`, `wallet_balance`, `total_views`) 
VALUES ("Orange LEE", "woaitruffle", "xenzpaya@gmail.com", 300.20, 800);

COMMIT