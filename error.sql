SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+08:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS `error` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `error`;

DROP TABLE IF EXISTS `error`;
CREATE TABLE IF NOT EXISTS `error` (
    `error_id` int(16) NOT NULL AUTO_INCREMENT,
    `microservice` varchar(32) NOT NULL,
    `userid` int(8) NOT NULL,
    `action` varchar(32) NOT NULL,
    `data` varchar(32) NOT NULL,
    `description` varchar(512) NOT NULL,
    `status` varchar(16) NOT NULL,
    `error_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`error_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

INSERT INTO `error` (`microservice`, `userid`, `action`, `data`, `description`, `status`, `error_timestamp`) 
VALUES ("user", 1, "view", "user", "Failed viewing of user 1's wallet balance at user microservice, User not found", "error", '2020-06-12 02:14:58');

COMMIT