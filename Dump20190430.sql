-- MySQL dump 10.13  Distrib 5.7.25, for Linux (x86_64)
--
-- Host: eecslab-9.case.edu    Database: team_6
-- ------------------------------------------------------
-- Server version	5.7.25-0ubuntu0.18.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Caterers`
--

create user 'team6'@'localhost' identified by '5adad0da';
grant all on team_6.* to 'team6'@'localhost';
flush privileges;

DROP TABLE IF EXISTS `Caterers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Caterers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Caterers`
--

LOCK TABLES `Caterers` WRITE;
/*!40000 ALTER TABLE `Caterers` DISABLE KEYS */;
INSERT INTO `Caterers` VALUES (1,'Chipotle'),(2,'Bon Apple Tea'),(3,'Bon Appetit'),(4,'Chopstick'),(5,'Barrio'),(6,'Qdoba'),(7,'Starbucks'),(8,'Mitchells'),(9,'McDonalds'),(10,'Den');
/*!40000 ALTER TABLE `Caterers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Events`
--

DROP TABLE IF EXISTS `Events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Events` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) DEFAULT NULL,
  `dates` datetime DEFAULT NULL,
  `price` decimal(2,0) DEFAULT '0',
  `location_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idEvents_UNIQUE` (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`),
  KEY `event_location_idx` (`location_id`),
  CONSTRAINT `event_location` FOREIGN KEY (`location_id`) REFERENCES `Locations` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Events`
--

LOCK TABLES `Events` WRITE;
/*!40000 ALTER TABLE `Events` DISABLE KEYS */;
INSERT INTO `Events` VALUES (2,'CORE CRAM','2019-04-11 00:00:00',0,NULL),(3,'Night Market','2018-11-09 00:00:00',0,NULL),(4,'La Fiesta','2018-04-17 00:00:00',0,NULL),(5,'Spring Fest','2019-05-17 00:00:00',0,NULL);
/*!40000 ALTER TABLE `Events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Locations`
--

DROP TABLE IF EXISTS `Locations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Locations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `hub` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Locations`
--

LOCK TABLES `Locations` WRITE;
/*!40000 ALTER TABLE `Locations` DISABLE KEYS */;
INSERT INTO `Locations` VALUES (1,'Village House 2','North'),(2,'Village House 3','North'),(3,'Village House 5','North'),(4,'Village House 6','North'),(5,'Village House 7','North'),(6,'Village House 1','North'),(7,'Thwing','Center'),(8,'KSL','Center'),(9,'Leutner','North'),(10,'STJ','North'),(11,'Freshman Housing','North'),(12,'Tink','Center');
/*!40000 ALTER TABLE `Locations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Organizations`
--

DROP TABLE IF EXISTS `Organizations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Organizations` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Organizations`
--

LOCK TABLES `Organizations` WRITE;
/*!40000 ALTER TABLE `Organizations` DISABLE KEYS */;
INSERT INTO `Organizations` VALUES (1,'La Alianza'),(2,'AAA'),(3,'Taiwanese American Student Association'),(4,'Glee Club'),(5,'Johnson Fan Club'),(6,'UDC'),(7,'USG'),(8,'Film Society'),(9,'Juggling Club');
/*!40000 ALTER TABLE `Organizations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `password` varchar(20) NOT NULL,
  `is_organizer` tinyint(4) NOT NULL DEFAULT '0',
  `locations_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`),
  KEY `location_id_fk_idx` (`locations_id`),
  CONSTRAINT `location_id_fk` FOREIGN KEY (`locations_id`) REFERENCES `Locations` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
INSERT INTO `Users` VALUES (1,'Austin Guo','asdafa',1,1),(2,'Justin Shearson','bbones225',1,1),(3,'2kewl4skewl','abc123',1,10),(4,'s3xygur1','catfish',1,10),(5,'andrewfong','12344',1,10);
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `catered_by`
--

DROP TABLE IF EXISTS `catered_by`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `catered_by` (
  `event_id` int(11) NOT NULL,
  `caterer_id` int(11) NOT NULL,
  KEY `caterer_idx` (`caterer_id`),
  KEY `hosting event_idx` (`event_id`),
  CONSTRAINT `caterer` FOREIGN KEY (`caterer_id`) REFERENCES `Caterers` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `hosting event` FOREIGN KEY (`event_id`) REFERENCES `Events` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Relational Table between event and caterer determined by who caters the event';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `catered_by`
--

LOCK TABLES `catered_by` WRITE;
/*!40000 ALTER TABLE `catered_by` DISABLE KEYS */;
/*!40000 ALTER TABLE `catered_by` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lead_by`
--

DROP TABLE IF EXISTS `lead_by`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lead_by` (
  `event_id` int(11) NOT NULL,
  `organization_id` int(11) NOT NULL,
  KEY `event_id_idx` (`event_id`),
  KEY `organization id_idx` (`organization_id`),
  CONSTRAINT `event id` FOREIGN KEY (`event_id`) REFERENCES `Events` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `organization id` FOREIGN KEY (`organization_id`) REFERENCES `Organizations` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Relational Table for events and Organizations';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lead_by`
--

LOCK TABLES `lead_by` WRITE;
/*!40000 ALTER TABLE `lead_by` DISABLE KEYS */;
INSERT INTO `lead_by` VALUES (3,3),(4,1),(5,6),(5,7),(5,3);
/*!40000 ALTER TABLE `lead_by` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `member_of`
--

DROP TABLE IF EXISTS `member_of`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `member_of` (
  `user_id` int(11) NOT NULL,
  `organization_id` int(11) NOT NULL,
  KEY `user_id_idx` (`user_id`),
  KEY `organization id_idx` (`organization_id`),
  CONSTRAINT `organizations id` FOREIGN KEY (`organization_id`) REFERENCES `Organizations` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `user id` FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='Relation between Organizations and Users which describes what organizations User is a member of';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `member_of`
--

LOCK TABLES `member_of` WRITE;
/*!40000 ALTER TABLE `member_of` DISABLE KEYS */;
/*!40000 ALTER TABLE `member_of` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prefers`
--

DROP TABLE IF EXISTS `prefers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `prefers` (
  `user_id` int(11) NOT NULL,
  `caterer_id` int(11) DEFAULT NULL,
  KEY `user id_idx` (`user_id`),
  KEY `preferred caterer_idx` (`caterer_id`),
  CONSTRAINT `preferred caterer` FOREIGN KEY (`caterer_id`) REFERENCES `Caterers` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `user preference` FOREIGN KEY (`user_id`) REFERENCES `Users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COMMENT='What caterers the user prefers';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prefers`
--

LOCK TABLES `prefers` WRITE;
/*!40000 ALTER TABLE `prefers` DISABLE KEYS */;
/*!40000 ALTER TABLE `prefers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-04-30 12:51:09
