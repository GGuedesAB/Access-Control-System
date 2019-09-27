CREATE DATABASE IF NOT EXISTS `accontrol` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `accontrol`;

CREATE TABLE `groups` (
  `number` int(10) NOT NULL,
  `description` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `users` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `MAC` varchar(45) DEFAULT NULL,
  `username` varchar(45) DEFAULT NULL,
  `password` blob,
  `group_number` int(10) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username_UNIQUE` (`username`),
  FOREIGN KEY (`group_number`) REFERENCES `groups`(`number`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;


CREATE TABLE `facilities` (
  `name` varchar(45) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `access` (
  `group_number` int(10) NOT NULL,
  `facility_name` varchar(45) NOT NULL,
  PRIMARY KEY (`group_number`, `facility_name`),
  FOREIGN KEY (`group_number`) REFERENCES `groups`(`number`),
  FOREIGN KEY (`facility_name`) REFERENCES `facilities`(`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
