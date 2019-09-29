INSERT INTO `groups` (`number`) VALUES (1) ;
INSERT INTO `groups` (`number`) VALUES (2) ;
INSERT INTO `groups` (`number`,`description`) VALUES (3,'almost everything') ;

INSERT INTO `users` (`name`,`MAC`,`username`,`password`,`group_number`) VALUES ('Kid','123','kid12','pass12',1) ;
INSERT INTO `users` (`name`,`MAC`,`username`,`password`,`group_number`) VALUES ('Boy','456','boy_me','123456',1) ;
INSERT INTO `users` (`name`,`MAC`,`username`,`password`,`group_number`) VALUES ('Girl','123','girlie_girl','girlwithg',1) ;
INSERT INTO `users` (`name`,`MAC`,`username`,`password`,`group_number`) VALUES ('Dog','101112','doge23','barkroof',2) ;
INSERT INTO `users` (`name`,`MAC`,`username`,`password`,`group_number`) VALUES ('Cat','131415','concat','ilovemilk',2) ;
INSERT INTO `users` (`name`,`MAC`,`username`,`password`,`group_number`) VALUES ('Sir','161718','Alex','godsavethequeen',3) ;

INSERT INTO `facilities` (`name`) VALUES ('kitchen') ;
INSERT INTO `facilities` (`name`) VALUES ('lobby') ;
INSERT INTO `facilities` (`name`) VALUES ('heaven') ;
INSERT INTO `facilities` (`name`) VALUES ('hell') ;
INSERT INTO `facilities` (`name`) VALUES ('castle') ;
INSERT INTO `facilities` (`name`) VALUES ('yard') ;
INSERT INTO `facilities` (`name`) VALUES ('playground') ;
INSERT INTO `facilities` (`name`) VALUES ('pool') ;

INSERT INTO `access` (`group_number`, `facility_name`) VALUES (1, 'kitchen') ;
INSERT INTO `access` (`group_number`, `facility_name`) VALUES (1, 'lobby') ;
INSERT INTO `access` (`group_number`, `facility_name`) VALUES (1, 'hell') ;
INSERT INTO `access` (`group_number`, `facility_name`) VALUES (1, 'yard') ;
INSERT INTO `access` (`group_number`, `facility_name`) VALUES (2, 'playground') ;
INSERT INTO `access` (`group_number`, `facility_name`) VALUES (2, 'heaven') ;
INSERT INTO `access` (`group_number`, `facility_name`) VALUES (2, 'lobby') ;
INSERT INTO `access` (`group_number`, `facility_name`) VALUES (3, 'kitchen') ;
INSERT INTO `access` (`group_number`, `facility_name`) VALUES (3, 'lobby') ;
INSERT INTO `access` (`group_number`, `facility_name`) VALUES (3, 'heaven') ;
INSERT INTO `access` (`group_number`, `facility_name`) VALUES (3, 'hell') ;
INSERT INTO `access` (`group_number`, `facility_name`) VALUES (3, 'yard') ;
INSERT INTO `access` (`group_number`, `facility_name`) VALUES (3, 'playground') ;
INSERT INTO `access` (`group_number`, `facility_name`) VALUES (3, 'pool') ;