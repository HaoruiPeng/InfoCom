CREATE DATABASE IF NOT EXISTS `RaspberryPiuserDB` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `RaspberryPiuserDB`;

CREATE TABLE IF NOT EXISTS `RaspberryPiusers` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
    `serialnumber` VARCHAR(511) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `email` VARCHAR(100) NOT NULL,
    `x` float(10,10) NOT NULL,
    `y` float(10,10) NOT NULL,
    PRIMARY KEY (`id`)
)  ENGINE=INNODB AUTO_INCREMENT=2 DEFAULT CHARSET=UTF8;

INSERT INTO `RaspberryPiusers` (`id`, `serialnumber`, `password`, `email`, `x`, `y`) VALUES (000000, '1000000000000000' , 'test', 'test@test.com', 0.0, 0.0);