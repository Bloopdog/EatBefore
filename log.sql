SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+08:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS `log` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `log`;

DROP TABLE IF EXISTS `log`;
CREATE TABLE IF NOT EXISTS `log` (
    `log_id` int(16) NOT NULL AUTO_INCREMENT,
    `microservice` varchar(32) NOT NULL,
    `userid` int(8) NOT NULL,
    `action` varchar(32) NOT NULL,
    `data` varchar(32) NOT NULL,
    `description` varchar(512) NOT NULL,
    `status` varchar(16) NOT NULL,
    `log_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`log_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

INSERT INTO `log` (`microservice`, `userid`, `action`, `data`, `description`, `status`, `log_timestamp`) 
VALUES ("user", 0, "create", "user", 'Successful creation of user 1 at user microservice', 'success','2020-02-12 02:14:58');

INSERT INTO `log` (`microservice`, `userid`, `action`, `data`, `description`, `status`, `log_timestamp`) 
VALUES ("user", 0, "create", "user", 'Successful creation of user 2 at user microservice', 'success','2021-01-11 02:14:57');

COMMIT