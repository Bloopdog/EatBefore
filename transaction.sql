SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS `transaction` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `transaction`;
/* changed transaction id to auto incremental */;
DROP TABLE IF EXISTS `transaction`;
CREATE TABLE IF NOT EXISTS `transaction` (
    `transaction_id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(8) NOT NULL,
    `transaction_type` varchar(8) NOT NULL,
    `transaction_amount` float(4) NOT NULL,
    `transaction_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`transaction_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

INSERT INTO `transaction` (`user_id`, `transaction_type`, `transaction_amount`) 
VALUES (0, 'withdraw', 10.0);

INSERT INTO `transaction` (`user_id`, `transaction_type`, `transaction_amount`) 
VALUES (1, 'deposit', 3.0);

COMMIT