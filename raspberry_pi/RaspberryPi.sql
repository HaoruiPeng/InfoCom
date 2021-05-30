CREATE DATABASE IF NOT EXISTS `RaspberryPi` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `RaspberryPi`;

CREATE TABLE IF NOT EXISTS `raspberries` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `serialnumber` INT(50) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `x` float(10,10) NOT NULL,
    `y` float(10,10) NOT NULL,
    PRIMARY KEY (`id`)
)  ENGINE=INNODB AUTO_INCREMENT=2 DEFAULT CHARSET=UTF8;

INSERT INTO `raspberries` (`id`, `serialnumber`, `password`, `email`, `x`, `y`) VALUES (000000, 111111, 'test', 'test@test.com', 0.0, 0.0);