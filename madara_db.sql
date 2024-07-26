-- MySQL dump 10.13  Distrib 8.0.37, for Linux (x86_64)
--
-- Host: localhost    Database: madara_db
-- ------------------------------------------------------
-- Server version	8.0.37-0ubuntu0.22.04.3

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add configuration',7,'add_configuration'),(26,'Can change configuration',7,'change_configuration'),(27,'Can delete configuration',7,'delete_configuration'),(28,'Can view configuration',7,'view_configuration'),(29,'Can add broker details',8,'add_brokerdetails'),(30,'Can change broker details',8,'change_brokerdetails'),(31,'Can delete broker details',8,'delete_brokerdetails'),(32,'Can view broker details',8,'view_brokerdetails'),(33,'Can add order book',9,'add_orderbook'),(34,'Can change order book',9,'change_orderbook'),(35,'Can delete order book',9,'delete_orderbook'),(36,'Can view order book',9,'view_orderbook'),(37,'Can add index details',10,'add_indexdetails'),(38,'Can change index details',10,'change_indexdetails'),(39,'Can delete index details',10,'delete_indexdetails'),(40,'Can view index details',10,'view_indexdetails'),(41,'Can add job details',11,'add_jobdetails'),(42,'Can change job details',11,'change_jobdetails'),(43,'Can delete job details',11,'delete_jobdetails'),(44,'Can view job details',11,'view_jobdetails'),(45,'Can add payment details',12,'add_paymentdetails'),(46,'Can change payment details',12,'change_paymentdetails'),(47,'Can delete payment details',12,'delete_paymentdetails'),(48,'Can view payment details',12,'view_paymentdetails'),(49,'Can add configuration',13,'add_configuration'),(50,'Can change configuration',13,'change_configuration'),(51,'Can delete configuration',13,'delete_configuration'),(52,'Can view configuration',13,'view_configuration'),(53,'Can add broker details',14,'add_brokerdetails'),(54,'Can change broker details',14,'change_brokerdetails'),(55,'Can delete broker details',14,'delete_brokerdetails'),(56,'Can view broker details',14,'view_brokerdetails'),(57,'Can add order book',15,'add_orderbook'),(58,'Can change order book',15,'change_orderbook'),(59,'Can delete order book',15,'delete_orderbook'),(60,'Can view order book',15,'view_orderbook'),(61,'Can add index details',16,'add_indexdetails'),(62,'Can change index details',16,'change_indexdetails'),(63,'Can delete index details',16,'delete_indexdetails'),(64,'Can view index details',16,'view_indexdetails'),(65,'Can add job details',17,'add_jobdetails'),(66,'Can change job details',17,'change_jobdetails'),(67,'Can delete job details',17,'delete_jobdetails'),(68,'Can view job details',17,'view_jobdetails'),(69,'Can add payment details',18,'add_paymentdetails'),(70,'Can change payment details',18,'change_paymentdetails'),(71,'Can delete payment details',18,'delete_paymentdetails'),(72,'Can view payment details',18,'view_paymentdetails'),(73,'Can add scalper details',19,'add_scalperdetails'),(74,'Can change scalper details',19,'change_scalperdetails'),(75,'Can delete scalper details',19,'delete_scalperdetails'),(76,'Can view scalper details',19,'view_scalperdetails'),(77,'Can add candle data',20,'add_candledata'),(78,'Can change candle data',20,'change_candledata'),(79,'Can delete candle data',20,'delete_candledata'),(80,'Can view candle data',20,'view_candledata');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$720000$TrRCp4ZEcCaTlJwjDlgH4n$bXk1dvyXOBkHUCj4N2oz2av/RSJgPbv2aSX+u6Z+Daw=','2024-07-13 07:49:51.933995',1,'admin','','','madara@plutus.com',1,1,'2024-06-15 12:09:57.133766'),(2,'pbkdf2_sha256$720000$su9jHjriTejd7pUVflaCpW$zYqJtpAqxjfNEVZEVupo4bhWZI2XlrAvdVoIugS7MM4=','2024-07-13 07:48:56.265093',0,'antonyrajan.d','antonyrajan.d','','antonyrajan.d@gmail.com',0,1,'2024-06-15 12:19:09.052744');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(8,'madaraApp','brokerdetails'),(7,'madaraApp','configuration'),(10,'madaraApp','indexdetails'),(11,'madaraApp','jobdetails'),(9,'madaraApp','orderbook'),(12,'madaraApp','paymentdetails'),(14,'plutusAI','brokerdetails'),(20,'plutusAI','candledata'),(13,'plutusAI','configuration'),(16,'plutusAI','indexdetails'),(17,'plutusAI','jobdetails'),(15,'plutusAI','orderbook'),(18,'plutusAI','paymentdetails'),(19,'plutusAI','scalperdetails'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=96 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-06-15 12:02:20.084320'),(2,'auth','0001_initial','2024-06-15 12:03:05.244407'),(3,'admin','0001_initial','2024-06-15 12:03:15.119429'),(4,'admin','0002_logentry_remove_auto_add','2024-06-15 12:03:15.325262'),(5,'admin','0003_logentry_add_action_flag_choices','2024-06-15 12:03:15.637149'),(6,'contenttypes','0002_remove_content_type_name','2024-06-15 12:03:21.877062'),(7,'auth','0002_alter_permission_name_max_length','2024-06-15 12:03:27.939462'),(8,'auth','0003_alter_user_email_max_length','2024-06-15 12:03:28.471649'),(9,'auth','0004_alter_user_username_opts','2024-06-15 12:03:28.800176'),(10,'auth','0005_alter_user_last_login_null','2024-06-15 12:03:33.421193'),(11,'auth','0006_require_contenttypes_0002','2024-06-15 12:03:33.985967'),(12,'auth','0007_alter_validators_add_error_messages','2024-06-15 12:03:34.747565'),(13,'auth','0008_alter_user_username_max_length','2024-06-15 12:03:40.350750'),(14,'auth','0009_alter_user_last_name_max_length','2024-06-15 12:03:46.485267'),(15,'auth','0010_alter_group_name_max_length','2024-06-15 12:03:47.223014'),(16,'auth','0011_update_proxy_permissions','2024-06-15 12:03:48.089320'),(17,'auth','0012_alter_user_first_name_max_length','2024-06-15 12:03:53.620107'),(18,'madaraApp','0001_initial','2024-06-15 12:03:55.626302'),(19,'madaraApp','0002_levels_remove_configuration_target_and_more','2024-06-15 12:04:26.236798'),(20,'madaraApp','0003_configuration_trailing_points_and_more','2024-06-15 12:04:31.008526'),(21,'madaraApp','0004_remove_configuration_levels_configuration_levels','2024-06-15 12:04:33.870250'),(22,'madaraApp','0005_delete_levels_configuration_user_id','2024-06-15 12:04:38.192991'),(23,'madaraApp','0006_configuration_start_scheduler','2024-06-15 12:04:40.835549'),(24,'madaraApp','0007_configuration_stage_configuration_strike','2024-06-15 12:04:46.791665'),(25,'madaraApp','0008_brokerdetails_orderbook','2024-06-15 12:04:51.436069'),(26,'madaraApp','0009_brokerdetails_is_demo_trading_enabled','2024-06-15 12:04:53.774299'),(27,'madaraApp','0010_alter_brokerdetails_user_id_and_more','2024-06-15 12:04:54.081200'),(28,'madaraApp','0011_brokerdetails_broker_api_token_and_more','2024-06-15 12:04:59.023843'),(29,'madaraApp','0012_indexdetails_jobdetails_and_more','2024-06-15 12:05:04.731802'),(30,'madaraApp','0013_brokerdetails_index_group','2024-06-15 12:05:07.228864'),(31,'madaraApp','0014_paymentdetails','2024-06-15 12:05:09.833452'),(32,'madaraApp','0015_jobdetails_terminate_job','2024-06-15 12:05:11.464829'),(33,'madaraApp','0016_alter_jobdetails_terminate_job','2024-06-15 12:05:17.943298'),(34,'madaraApp','0017_remove_jobdetails_terminate_job','2024-06-15 12:05:19.954183'),(35,'madaraApp','0018_indexdetails_index_ltp_indexdetails_index_token','2024-06-15 12:05:23.404805'),(36,'madaraApp','0019_rename_index_ltp_indexdetails_ltp_and_more','2024-06-15 12:05:26.593994'),(37,'madaraApp','0020_configuration_lots','2024-06-15 12:05:29.311089'),(38,'madaraApp','0021_indexdetails_qty','2024-06-15 12:05:31.329100'),(39,'madaraApp','0022_alter_configuration_lots','2024-06-15 12:05:31.549297'),(40,'madaraApp','0023_indexdetails_current_expiry_indexdetails_next_expiry','2024-06-15 12:05:34.506065'),(41,'madaraApp','0024_rename_time_orderbook_entry_time_orderbook_exit_time_and_more','2024-06-15 12:05:39.447613'),(42,'madaraApp','0025_supportedbrokers','2024-06-15 12:05:42.216629'),(43,'madaraApp','0026_alter_supportedbrokers_instruments','2024-06-15 12:05:42.543369'),(44,'madaraApp','0027_alter_supportedbrokers_instruments','2024-06-15 12:05:42.772467'),(45,'madaraApp','0028_alter_supportedbrokers_instruments','2024-06-15 12:05:42.948876'),(46,'madaraApp','0029_delete_supportedbrokers','2024-06-15 12:05:45.208042'),(47,'madaraApp','0030_alter_orderbook_exit_price_alter_orderbook_exit_time','2024-06-15 12:05:53.532372'),(48,'madaraApp','0031_orderbook_cumulative_p_l','2024-06-15 12:05:56.106308'),(49,'madaraApp','0032_rename_cumulative_p_l_orderbook_total','2024-06-15 12:05:57.373743'),(50,'madaraApp','0033_alter_orderbook_entry_time_alter_orderbook_exit_time','2024-06-15 12:06:07.645784'),(51,'madaraApp','0034_alter_orderbook_entry_time','2024-06-15 12:06:07.814832'),(52,'madaraApp','0035_alter_orderbook_entry_time_alter_orderbook_exit_time','2024-06-15 12:06:18.955808'),(53,'sessions','0001_initial','2024-06-15 12:06:22.209235'),(54,'plutusAI','0001_initial','2024-06-28 11:25:32.152488'),(55,'plutusAI','0002_levels_remove_configuration_target_and_more','2024-06-28 11:25:40.327923'),(56,'plutusAI','0003_configuration_trailing_points_and_more','2024-06-28 11:25:41.546149'),(57,'plutusAI','0004_remove_configuration_levels_configuration_levels','2024-06-28 11:25:42.421099'),(58,'plutusAI','0005_delete_levels_configuration_user_id','2024-06-28 11:25:43.398115'),(59,'plutusAI','0006_configuration_start_scheduler','2024-06-28 11:25:43.997191'),(60,'plutusAI','0007_configuration_stage_configuration_strike','2024-06-28 11:25:45.804286'),(61,'plutusAI','0008_brokerdetails_orderbook','2024-06-28 11:25:47.088906'),(62,'plutusAI','0009_brokerdetails_is_demo_trading_enabled','2024-06-28 11:25:47.744083'),(63,'plutusAI','0010_alter_brokerdetails_user_id_and_more','2024-06-28 11:25:47.833230'),(64,'plutusAI','0011_brokerdetails_broker_api_token_and_more','2024-06-28 11:25:49.122124'),(65,'plutusAI','0012_indexdetails_jobdetails_and_more','2024-06-28 11:25:51.448043'),(66,'plutusAI','0013_brokerdetails_index_group','2024-06-28 11:25:51.889756'),(67,'plutusAI','0014_paymentdetails','2024-06-28 11:25:52.521700'),(68,'plutusAI','0015_jobdetails_terminate_job','2024-06-28 11:25:53.110337'),(69,'plutusAI','0016_alter_jobdetails_terminate_job','2024-06-28 11:25:54.962080'),(70,'plutusAI','0017_remove_jobdetails_terminate_job','2024-06-28 11:25:55.802918'),(71,'plutusAI','0018_indexdetails_index_ltp_indexdetails_index_token','2024-06-28 11:25:57.420723'),(72,'plutusAI','0019_rename_index_ltp_indexdetails_ltp_and_more','2024-06-28 11:25:58.849286'),(73,'plutusAI','0020_configuration_lots','2024-06-28 11:25:59.539261'),(74,'plutusAI','0021_indexdetails_qty','2024-06-28 11:26:00.002390'),(75,'plutusAI','0022_alter_configuration_lots','2024-06-28 11:26:00.127633'),(76,'plutusAI','0023_indexdetails_current_expiry_indexdetails_next_expiry','2024-06-28 11:26:01.151605'),(77,'plutusAI','0024_rename_time_orderbook_entry_time_orderbook_exit_time_and_more','2024-06-28 11:26:01.970431'),(78,'plutusAI','0025_supportedbrokers','2024-06-28 11:26:02.951083'),(79,'plutusAI','0026_alter_supportedbrokers_instruments','2024-06-28 11:26:03.037508'),(80,'plutusAI','0027_alter_supportedbrokers_instruments','2024-06-28 11:26:03.136228'),(81,'plutusAI','0028_alter_supportedbrokers_instruments','2024-06-28 11:26:03.236543'),(82,'plutusAI','0029_delete_supportedbrokers','2024-06-28 11:26:03.716101'),(83,'plutusAI','0030_alter_orderbook_exit_price_alter_orderbook_exit_time','2024-06-28 11:26:05.800617'),(84,'plutusAI','0031_orderbook_cumulative_p_l','2024-06-28 11:26:06.335256'),(85,'plutusAI','0032_rename_cumulative_p_l_orderbook_total','2024-06-28 11:26:07.082821'),(86,'plutusAI','0033_alter_orderbook_entry_time_alter_orderbook_exit_time','2024-06-28 11:26:12.186488'),(87,'plutusAI','0034_alter_orderbook_entry_time','2024-06-28 11:26:12.265476'),(88,'plutusAI','0035_alter_orderbook_entry_time_alter_orderbook_exit_time','2024-06-28 11:26:15.701922'),(89,'plutusAI','0036_orderbook_strategy','2024-06-28 11:26:16.840524'),(90,'plutusAI','0037_jobdetails_strategy','2024-06-28 11:57:45.886402'),(91,'plutusAI','0038_scalperdetails','2024-06-29 15:47:23.836694'),(92,'plutusAI','0039_scalperdetails_is_demo_trading_enabled_and_more','2024-06-29 15:50:41.640121'),(93,'plutusAI','0040_scalperdetails_target','2024-06-29 16:00:13.207342'),(94,'plutusAI','0041_scalperdetails_lots','2024-07-04 05:26:34.514852'),(95,'plutusAI','0042_candledata_remove_scalperdetails_capital','2024-07-13 16:16:23.086358');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('2y3j1qgxtrfo7qt8u9o9xy6gmozfj5jb','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sOqZg:L7UpklxZ8coWp1fxwexKp_k4U9iwVlO8G7f-an7RK1E','2024-07-17 03:22:28.848509'),('4i7k3evdhzkw2bjbhzn67a5wvd11ni1k','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sISNf:rz6C4so4auNahvUBVexX7mUnT8Uh7NF_VZphUnIyTe0','2024-06-29 12:19:39.087860'),('bdjy3no66rzpty31tuu9xnxh05z1x9cu','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sOqUz:OG5lpOn-rrIauTNOkGy_xFaOM7VbpreV11eo20DDUSQ','2024-07-17 03:17:37.045572'),('e7xtiz2ut1w0yucfu03vgrsbz4z05hc8','.eJxVjMsOwiAQRf-FtSEMjwIu3fcbyAyMUjU0Ke3K-O_apAvd3nPOfYmE21rT1nlJUxFnAeL0uxHmB7cdlDu22yzz3NZlIrkr8qBdjnPh5-Vw_w4q9vqtjQUqSpkcQUfGQNYYnSEzqODY2-KjxoEhKBc8KWs9XS37HHkghxTE-wPFnTdt:1sISEn:5nqopMDP56toJY3cYxaLEnijZ6ZUnr7qjgQaloiEvj4','2024-06-29 12:10:29.755173'),('erzt5xhhv8q2xtn39y916jqf7udng727','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sN9hB:D1vdKi-9csGFODYjMBpLOLH8_xC7Y0OLVoc96Fgwtxo','2024-07-12 11:23:13.012241'),('hm6j77v8buwthal25sp5aca2g0qky4fs','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sSXV2:WSf9sq2KX8edcN1vRh4FVbUsLGzy0KpG53bYjl5wbpo','2024-07-27 07:48:56.531386'),('i3tqnzk8ozeaiieudd07j3og5pwy6uhd','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sOqZi:0_WbPAA4NT6xUUyRQyU8s4r3C169iInAGVNWnT8NSJ8','2024-07-17 03:22:30.107491'),('jitu9suzvax750ht855s812gk0ftu0zk','.eJxVjMsOwiAQRf-FtSEMjwIu3fcbyAyMUjU0Ke3K-O_apAvd3nPOfYmE21rT1nlJUxFnAeL0uxHmB7cdlDu22yzz3NZlIrkr8qBdjnPh5-Vw_w4q9vqtjQUqSpkcQUfGQNYYnSEzqODY2-KjxoEhKBc8KWs9XS37HHkghxTE-wPFnTdt:1sSXVw:6KwTYkQVEq0Sfk5pgJG4EjgOqR_Tjr-mip1dWHkYN5w','2024-07-27 07:49:52.089921'),('kyhmnhkv0fdvv07yhcx54piocuqnc6qc','.eJxVjMsOwiAQRf-FtSEMjwIu3fcbyAyMUjU0Ke3K-O_apAvd3nPOfYmE21rT1nlJUxFnAeL0uxHmB7cdlDu22yzz3NZlIrkr8qBdjnPh5-Vw_w4q9vqtjQUqSpkcQUfGQNYYnSEzqODY2-KjxoEhKBc8KWs9XS37HHkghxTE-wPFnTdt:1sISQz:tPKj-ClanmA-Dk7Aww1zqQ-VKfssykyIPVFAvv-Dmhw','2024-06-29 12:23:05.675170'),('pri82v6cbnqk4f7pmw20s8ixrvhtctvb','.eJxVjMsOwiAQRf-FtSEMjwIu3fcbyAyMUjU0Ke3K-O_apAvd3nPOfYmE21rT1nlJUxFnAeL0uxHmB7cdlDu22yzz3NZlIrkr8qBdjnPh5-Vw_w4q9vqtjQUqSpkcQUfGQNYYnSEzqODY2-KjxoEhKBc8KWs9XS37HHkghxTE-wPFnTdt:1sQej6:NIuFBRq1gRdkCB5zOuZE2omH0TWQ2HM33LMSMjUn2mA','2024-07-22 03:07:40.182675'),('t4jf4e0169nktmzyid1bsiu3ph7mjcgy','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sOqUx:rooxrBXoGRwZEolrVt-InZ1MTHaZREBRK370suc8WHU','2024-07-17 03:17:35.795418'),('tyil8duo5kku5utumjo9yhjx6t61837o','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sOqZf:a6Bt-5mMNluq-kMmH2IQyEL5aLzA1jJhHpj4c7o4nSQ','2024-07-17 03:22:27.495393'),('vhao97j773azajvhq0plcvxxuku2g9i5','.eJxVjMsOwiAQRf-FtSEMjwIu3fcbyAyMUjU0Ke3K-O_apAvd3nPOfYmE21rT1nlJUxFnAeL0uxHmB7cdlDu22yzz3NZlIrkr8qBdjnPh5-Vw_w4q9vqtjQUqSpkcQUfGQNYYnSEzqODY2-KjxoEhKBc8KWs9XS37HHkghxTE-wPFnTdt:1sRkp0:4Od5ily03gLhP-JcethZxcrcDt-Yyhu8B0CrNgSbYGI','2024-07-25 03:50:18.311605');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plutusAI_brokerdetails`
--

DROP TABLE IF EXISTS `plutusAI_brokerdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plutusAI_brokerdetails` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` varchar(500) NOT NULL,
  `broker_user_id` varchar(250) NOT NULL,
  `broker_user_name` varchar(250) NOT NULL,
  `broker_name` varchar(250) NOT NULL,
  `token_status` varchar(250) NOT NULL,
  `is_demo_trading_enabled` tinyint(1) NOT NULL,
  `broker_api_token` varchar(250) NOT NULL,
  `broker_mpin` varchar(250) NOT NULL,
  `broker_qr` varchar(250) NOT NULL,
  `index_group` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_brokerdetails`
--

LOCK TABLES `plutusAI_brokerdetails` WRITE;
/*!40000 ALTER TABLE `plutusAI_brokerdetails` DISABLE KEYS */;
INSERT INTO `plutusAI_brokerdetails` VALUES (1,'antonyrajan.d@gmail.com','A58033497','ANTONY RAJAN DANIEL','angel_one','generated',1,'pOruxLYZ','1005','RQFCDA2ZX2DMFZ5GR6HXXPFITY','indian_index'),(2,'madara@plutus.com','S50761409','SAHAYARAJ  SAHAYARAJ','angel_one','generated',0,'Q12feFjR','1005','5TXNGVJEVZYMHCLF6HHOQHHTZ4','indian_index');
/*!40000 ALTER TABLE `plutusAI_brokerdetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plutusAI_candledata`
--

DROP TABLE IF EXISTS `plutusAI_candledata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plutusAI_candledata` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `index_name` varchar(50) NOT NULL,
  `token` varchar(50) NOT NULL,
  `time` varchar(50) NOT NULL,
  `open` varchar(50) NOT NULL,
  `high` varchar(50) NOT NULL,
  `low` varchar(50) NOT NULL,
  `close` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=697 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_candledata`
--

LOCK TABLES `plutusAI_candledata` WRITE;
/*!40000 ALTER TABLE `plutusAI_candledata` DISABLE KEYS */;
INSERT INTO `plutusAI_candledata` VALUES (81,'bank_nifty_fut','35165','12:52:00','52276.0','52280.0','52270.0','52278.9'),(82,'bank_nifty_fut','35165','12:53:00','52278.9','52288.95','52275.9','52284.15'),(83,'bank_nifty_fut','35165','12:54:00','52281.0','52295.0','52280.0','52290.0'),(84,'bank_nifty_fut','35165','12:55:00','52289.5','52289.5','52275.25','52280.4'),(85,'bank_nifty_fut','35165','12:56:00','52280.4','52295.0','52280.0','52280.0'),(86,'bank_nifty_fut','35165','12:57:00','52280.0','52283.9','52270.0','52270.35'),(87,'bank_nifty_fut','35165','12:58:00','52270.35','52274.45','52251.0','52251.95'),(88,'bank_nifty_fut','35165','12:59:00','52251.95','52251.95','52216.6','52218.95'),(89,'bank_nifty_fut','35165','13:00:00','52228.0','52240.05','52201.0','52240.05'),(90,'bank_nifty_fut','35165','13:01:00','52240.05','52250.0','52227.4','52250.0'),(91,'bank_nifty_fut','35165','13:02:00','52247.15','52268.9','52245.0','52266.95'),(92,'bank_nifty_fut','35165','13:03:00','52266.95','52268.9','52251.2','52261.2'),(93,'bank_nifty_fut','35165','13:04:00','52261.2','52269.0','52251.9','52251.9'),(94,'bank_nifty_fut','35165','13:05:00','52251.9','52275.0','52251.9','52274.85'),(95,'bank_nifty_fut','35165','13:06:00','52274.85','52281.0','52257.25','52272.3'),(96,'bank_nifty_fut','35165','13:07:00','52272.3','52276.85','52242.25','52246.85'),(97,'bank_nifty_fut','35165','13:08:00','52249.35','52254.9','52235.15','52242.05'),(98,'bank_nifty_fut','35165','13:09:00','52248.4','52257.45','52245.0','52253.0'),(99,'bank_nifty_fut','35165','13:10:00','52247.45','52256.2','52232.2','52237.0'),(100,'bank_nifty_fut','35165','13:11:00','52234.15','52237.0','52225.9','52229.75'),(101,'bank_nifty_fut','35165','13:12:00','52226.15','52236.1','52225.9','52228.15'),(102,'bank_nifty_fut','35165','13:13:00','52228.15','52241.05','52225.9','52229.1'),(103,'bank_nifty_fut','35165','13:14:00','52229.1','52254.0','52225.9','52254.0'),(104,'bank_nifty_fut','35165','13:15:00','52250.45','52250.45','52229.05','52249.55'),(105,'bank_nifty_fut','35165','13:16:00','52249.55','52249.9','52225.9','52231.1'),(106,'bank_nifty_fut','35165','13:17:00','52234.15','52247.85','52225.95','52247.1'),(107,'bank_nifty_fut','35165','13:18:00','52247.1','52247.1','52227.85','52227.95'),(108,'bank_nifty_fut','35165','13:19:00','52241.95','52244.4','52225.9','52225.9'),(109,'bank_nifty_fut','35165','13:20:00','52225.9','52251.7','52225.9','52244.0'),(110,'bank_nifty_fut','35165','13:21:00','52244.0','52251.7','52240.0','52240.2'),(111,'bank_nifty_fut','35165','13:22:00','52240.2','52279.65','52240.2','52279.0'),(112,'bank_nifty_fut','35165','13:23:00','52275.0','52298.5','52270.5','52288.95'),(113,'bank_nifty_fut','35165','13:24:00','52287.35','52304.55','52279.2','52303.4'),(114,'bank_nifty_fut','35165','13:25:00','52303.9','52340.0','52300.0','52332.15'),(115,'bank_nifty_fut','35165','13:26:00','52332.15','52344.9','52316.0','52320.3'),(116,'bank_nifty_fut','35165','13:27:00','52319.6','52321.1','52302.9','52305.35'),(117,'bank_nifty_fut','35165','13:28:00','52305.35','52319.6','52290.1','52313.0'),(118,'bank_nifty_fut','35165','13:29:00','52313.0','52320.0','52301.5','52316.0'),(119,'bank_nifty_fut','35165','13:30:00','52316.0','52338.0','52308.2','52337.25'),(120,'bank_nifty_fut','35165','13:31:00','52337.25','52347.55','52325.0','52335.05'),(121,'bank_nifty_fut','35165','13:32:00','52335.05','52348.3','52320.5','52335.2'),(122,'bank_nifty_fut','35165','13:33:00','52335.2','52340.4','52306.65','52308.2'),(123,'bank_nifty_fut','35165','2024-07-19 13:34:00','52314.75','52316.0','52310.0','52316.0'),(124,'bank_nifty_fut','35165','2024-07-19 13:35:00','52316.0','52348.8','52316.0','52343.0'),(125,'bank_nifty_fut','35165','2024-07-19 13:36:00','52343.0','52360.95','52340.0','52355.0'),(126,'bank_nifty_fut','35165','2024-07-19 13:37:00','52355.0','52355.35','52331.8','52343.7'),(127,'bank_nifty_fut','35165','2024-07-19 13:38:00','52343.7','52346.25','52322.9','52332.25'),(128,'bank_nifty_fut','35165','2024-07-19 13:39:00','52332.25','52336.0','52327.0','52336.0'),(129,'bank_nifty_fut','35165','2024-07-19 13:40:00','52336.0','52370.0','52336.0','52367.45'),(130,'bank_nifty_fut','35165','2024-07-19 13:41:00','52368.75','52370.0','52336.0','52346.9'),(131,'bank_nifty_fut','35165','2024-07-19 13:42:00','52346.9','52346.9','52322.9','52325.35'),(132,'bank_nifty_fut','35165','2024-07-19 13:43:00','52325.35','52332.3','52311.0','52314.75'),(133,'bank_nifty_fut','35165','2024-07-19 13:44:00','52314.75','52325.0','52308.75','52317.85'),(134,'bank_nifty_fut','35165','2024-07-19 13:45:00','52317.85','52334.0','52312.2','52334.0'),(135,'bank_nifty_fut','35165','2024-07-19 13:46:00','52334.0','52354.0','52330.0','52350.0'),(136,'bank_nifty_fut','35165','2024-07-19 13:47:00','52350.0','52351.0','52337.45','52342.0'),(137,'bank_nifty_fut','35165','2024-07-19 13:48:00','52342.0','52355.0','52342.0','52353.65'),(138,'bank_nifty_fut','35165','2024-07-19 13:49:00','52352.35','52358.15','52340.05','52358.15'),(139,'bank_nifty_fut','35165','2024-07-19 13:50:00','52352.1','52366.0','52345.3','52360.0'),(140,'bank_nifty_fut','35165','2024-07-19 13:51:00','52360.0','52375.0','52351.0','52374.35'),(141,'bank_nifty_fut','35165','2024-07-19 13:52:00','52358.25','52358.25','52326.7','52326.7'),(142,'bank_nifty_fut','35165','2024-07-19 13:53:00','52340.75','52350.2','52340.75','52345.0'),(143,'bank_nifty_fut','35165','2024-07-19 13:55:00','52348.65','52348.65','52345.2','52345.2'),(144,'bank_nifty_fut','35165','2024-07-19 13:56:00','52350.0','52352.1','52347.3','52347.3'),(145,'bank_nifty_fut','35165','2024-07-19 13:57:00','52338.25','52338.25','52338.25','52338.25'),(146,'bank_nifty_fut','35165','2024-07-19 13:58:00','52336.5','52336.5','52325.0','52330.15'),(147,'bank_nifty_fut','35165','2024-07-19 13:59:00','52330.15','52345.55','52330.15','52344.35'),(148,'bank_nifty_fut','35165','2024-07-19 14:00:00','52333.05','52365.0','52333.05','52352.4'),(149,'bank_nifty_fut','35165','2024-07-19 14:01:00','52352.4','52366.0','52340.2','52344.7'),(150,'bank_nifty_fut','35165','2024-07-19 14:02:00','52344.7','52357.4','52330.0','52330.0'),(151,'bank_nifty_fut','35165','2024-07-19 14:03:00','52330.0','52339.2','52311.0','52317.4'),(152,'bank_nifty_fut','35165','2024-07-19 14:04:00','52317.4','52320.8','52290.0','52290.0'),(153,'bank_nifty_fut','35165','2024-07-22 09:13:00','52270.65','52270.65','52100.4','52100.4'),(154,'bank_nifty_fut','35165','2024-07-22 09:15:00','52158.0','52185.25','51986.7','52017.0'),(155,'bank_nifty_fut','35165','2024-07-22 09:16:00','52000.45','52000.45','51935.55','51986.3'),(156,'bank_nifty_fut','35165','2024-07-22 09:17:00','51986.3','52080.6','51969.5','52046.8'),(157,'bank_nifty_fut','35165','2024-07-22 09:18:00','52046.8','52077.0','52014.7','52049.4'),(158,'bank_nifty_fut','35165','2024-07-22 09:19:00','52041.6','52050.5','52000.9','52013.95'),(159,'bank_nifty_fut','35165','2024-07-22 09:20:00','52013.9','52049.45','51986.3','51986.3'),(160,'bank_nifty_fut','35165','2024-07-22 09:21:00','51990.55','52063.15','51985.8','52040.45'),(161,'bank_nifty_fut','35165','2024-07-25 09:14:00','51401.1','51401.1','50966.0','50966.0'),(162,'bank_nifty_fut','35165','2024-07-25 09:15:00','50939.5','51088.35','50939.5','51006.55'),(163,'bank_nifty_fut','35165','2024-07-25 09:16:00','50997.25','50997.25','50836.05','50868.55'),(164,'bank_nifty_fut','35165','2024-07-25 09:17:00','50856.6','50918.55','50832.95','50890.2'),(165,'bank_nifty_fut','35165','2024-07-25 09:18:00','50889.7','50934.55','50889.0','50916.15'),(166,'bank_nifty_fut','35165','2024-07-25 09:19:00','50916.15','50918.85','50870.0','50880.0'),(167,'bank_nifty_fut','35165','2024-07-25 09:20:00','50870.0','50890.0','50850.0','50869.2'),(168,'bank_nifty_fut','35165','2024-07-25 09:21:00','50869.2','50907.5','50855.2','50877.85'),(169,'bank_nifty_fut','35165','2024-07-25 09:22:00','50877.85','50919.05','50873.2','50912.2'),(170,'bank_nifty_fut','35165','2024-07-25 09:23:00','50919.75','50975.0','50902.15','50967.4'),(171,'bank_nifty_fut','35165','2024-07-25 09:24:00','50967.4','50987.4','50908.05','50930.0'),(172,'bank_nifty_fut','35165','2024-07-25 09:25:00','50930.0','50948.95','50920.5','50947.45'),(173,'bank_nifty_fut','35165','2024-07-25 09:26:00','50947.45','50968.4','50907.7','50922.3'),(174,'bank_nifty_fut','35165','2024-07-25 09:27:00','50927.0','50927.0','50875.0','50901.95'),(175,'bank_nifty_fut','35165','2024-07-25 09:28:00','50901.95','50944.9','50895.5','50928.0'),(176,'bank_nifty_fut','35165','2024-07-25 09:29:00','50930.85','50952.05','50922.05','50938.8'),(177,'bank_nifty_fut','35165','2024-07-25 09:30:00','50938.8','50976.45','50931.05','50941.4'),(178,'bank_nifty_fut','35165','2024-07-25 09:31:00','50939.8','50950.0','50924.0','50949.0'),(179,'bank_nifty_fut','35165','2024-07-25 09:34:00','50984.8','50984.8','50951.0','50951.05'),(180,'bank_nifty_fut','35165','2024-07-25 09:35:00','50950.0','50957.05','50901.2','50924.45'),(181,'bank_nifty_fut','35165','2024-07-25 09:36:00','50924.45','50932.15','50901.2','50902.0'),(182,'bank_nifty_fut','35165','2024-07-25 09:37:00','50903.0','50907.15','50851.75','50866.95'),(183,'bank_nifty_fut','35165','2024-07-25 09:38:00','50869.95','50935.8','50866.8','50929.95'),(184,'bank_nifty_fut','35165','2024-07-25 09:39:00','50930.7','50978.75','50926.35','50973.65'),(185,'bank_nifty_fut','35165','2024-07-25 09:40:00','50968.9','50991.7','50956.15','50991.7'),(186,'bank_nifty_fut','35165','2024-07-25 09:41:00','50985.0','50985.0','50934.45','50946.4'),(187,'bank_nifty_fut','35165','2024-07-25 09:42:00','50946.4','50946.4','50905.2','50911.05'),(188,'bank_nifty_fut','35165','2024-07-25 09:43:00','50911.05','50936.05','50911.05','50924.5'),(189,'bank_nifty_fut','35165','2024-07-25 09:44:00','50924.5','50927.9','50891.45','50896.95'),(190,'bank_nifty_fut','35165','2024-07-25 09:45:00','50891.2','50891.2','50830.8','50835.7'),(191,'bank_nifty_fut','35165','2024-07-25 09:46:00','50829.15','50832.6','50704.05','50713.15'),(192,'bank_nifty_fut','35165','2024-07-25 09:47:00','50713.15','50748.25','50702.3','50712.65'),(193,'bank_nifty_fut','35165','2024-07-25 09:48:00','50712.65','50745.35','50704.8','50741.25'),(194,'bank_nifty_fut','35165','2024-07-25 09:49:00','50743.65','50772.5','50730.1','50753.5'),(195,'bank_nifty_fut','35165','2024-07-25 09:50:00','50750.0','50782.05','50725.05','50775.0'),(196,'bank_nifty_fut','35165','2024-07-25 09:51:00','50775.0','50783.05','50760.0','50775.0'),(197,'bank_nifty_fut','35165','2024-07-25 09:52:00','50775.0','50794.65','50768.05','50770.0'),(198,'bank_nifty_fut','35165','2024-07-25 09:53:00','50780.0','50784.05','50744.6','50745.45'),(199,'bank_nifty_fut','35165','2024-07-25 09:54:00','50745.45','50789.8','50745.45','50773.55'),(200,'bank_nifty_fut','35165','2024-07-25 09:55:00','50777.0','50798.8','50776.35','50789.8'),(201,'bank_nifty_fut','35165','2024-07-25 09:56:00','50789.95','50795.0','50737.5','50747.3'),(202,'bank_nifty_fut','35165','2024-07-25 09:57:00','50750.8','50777.7','50736.1','50736.1'),(203,'bank_nifty_fut','35165','2024-07-25 09:58:00','50741.3','50744.15','50711.0','50720.0'),(204,'bank_nifty_fut','35165','2024-07-25 09:59:00','50719.8','50745.75','50710.5','50717.05'),(205,'bank_nifty_fut','35165','2024-07-25 10:00:00','50705.8','50741.0','50654.85','50707.8'),(206,'bank_nifty_fut','35165','2024-07-25 10:01:00','50708.95','50724.5','50700.0','50706.2'),(207,'bank_nifty_fut','35165','2024-07-25 10:02:00','50709.9','50729.8','50690.1','50694.8'),(208,'bank_nifty_fut','35165','2024-07-25 10:03:00','50694.8','50720.0','50682.0','50713.45'),(209,'bank_nifty_fut','35165','2024-07-25 10:04:00','50713.45','50759.95','50695.35','50757.55'),(210,'bank_nifty_fut','35165','2024-07-25 10:05:00','50757.0','50758.15','50730.0','50730.0'),(211,'bank_nifty_fut','35165','2024-07-25 10:06:00','50730.0','50738.0','50713.55','50733.85'),(212,'bank_nifty_fut','35165','2024-07-25 10:07:00','50730.8','50744.35','50700.35','50700.35'),(213,'bank_nifty_fut','35165','2024-07-25 10:08:00','50714.85','50723.4','50700.0','50702.85'),(214,'bank_nifty_fut','35165','2024-07-25 10:09:00','50702.85','50722.5','50700.0','50709.0'),(215,'bank_nifty_fut','35165','2024-07-25 10:10:00','50709.0','50714.05','50690.65','50690.65'),(216,'bank_nifty_fut','35165','2024-07-25 10:11:00','50700.0','50733.8','50690.0','50711.75'),(217,'bank_nifty_fut','35165','2024-07-25 10:12:00','50711.75','50728.2','50710.0','50711.35'),(218,'bank_nifty_fut','35165','2024-07-25 10:13:00','50707.7','50721.0','50705.75','50711.9'),(219,'bank_nifty_fut','35165','2024-07-25 10:14:00','50711.9','50721.95','50694.0','50698.75'),(220,'bank_nifty_fut','35165','2024-07-25 10:15:00','50698.75','50765.95','50687.1','50739.6'),(221,'bank_nifty_fut','35165','2024-07-25 10:16:00','50739.2','50776.75','50735.0','50746.1'),(222,'bank_nifty_fut','35165','2024-07-25 10:17:00','50742.0','50745.85','50688.1','50697.5'),(223,'bank_nifty_fut','35165','2024-07-25 10:18:00','50699.95','50702.65','50650.0','50666.25'),(224,'bank_nifty_fut','35165','2024-07-25 10:19:00','50666.25','50685.0','50658.0','50680.8'),(225,'bank_nifty_fut','35165','2024-07-25 10:20:00','50680.8','50698.75','50660.0','50660.0'),(226,'bank_nifty_fut','35165','2024-07-25 10:21:00','50660.0','50675.75','50630.0','50675.75'),(227,'bank_nifty_fut','35165','2024-07-25 10:22:00','50675.75','50687.65','50661.2','50664.95'),(228,'bank_nifty_fut','35165','2024-07-25 10:23:00','50664.95','50673.65','50641.45','50641.45'),(229,'bank_nifty_fut','35165','2024-07-25 10:24:00','50641.45','50654.8','50610.0','50619.85'),(230,'bank_nifty_fut','35165','2024-07-25 10:25:00','50619.25','50650.0','50601.0','50617.15'),(231,'bank_nifty_fut','35165','2024-07-25 10:26:00','50617.15','50661.8','50617.15','50659.65'),(232,'bank_nifty_fut','35165','2024-07-25 10:27:00','50657.35','50665.0','50644.8','50647.5'),(233,'bank_nifty_fut','35165','2024-07-25 10:28:00','50647.4','50659.8','50640.3','50645.0'),(234,'bank_nifty_fut','35165','2024-07-25 10:29:00','50645.0','50647.95','50620.0','50621.65'),(235,'bank_nifty_fut','35165','2024-07-25 10:30:00','50615.3','50650.1','50615.3','50650.1'),(236,'bank_nifty_fut','35165','2024-07-25 10:31:00','50650.1','50696.95','50643.85','50679.8'),(237,'bank_nifty_fut','35165','2024-07-25 10:32:00','50678.5','50723.85','50670.0','50700.0'),(238,'bank_nifty_fut','35165','2024-07-25 10:33:00','50700.0','50714.6','50682.75','50692.5'),(239,'bank_nifty_fut','35165','2024-07-25 10:34:00','50689.8','50689.8','50669.8','50676.45'),(240,'bank_nifty_fut','35165','2024-07-25 10:35:00','50676.45','50727.7','50673.95','50694.05'),(241,'bank_nifty_fut','35165','2024-07-25 10:36:00','50694.05','50712.05','50694.05','50704.85'),(242,'bank_nifty_fut','35165','2024-07-25 10:37:00','50709.95','50722.95','50701.3','50721.2'),(243,'bank_nifty_fut','35165','2024-07-25 10:38:00','50721.2','50743.0','50710.0','50730.9'),(244,'bank_nifty_fut','35165','2024-07-25 10:39:00','50730.9','50730.9','50690.05','50691.85'),(245,'bank_nifty_fut','35165','2024-07-25 10:40:00','50691.85','50710.0','50680.0','50694.15'),(246,'bank_nifty_fut','35165','2024-07-25 10:41:00','50694.15','50716.95','50682.35','50715.3'),(247,'bank_nifty_fut','35165','2024-07-25 10:42:00','50715.3','50725.0','50702.4','50725.0'),(248,'bank_nifty_fut','35165','2024-07-25 10:43:00','50727.6','50734.3','50716.25','50732.95'),(249,'bank_nifty_fut','35165','2024-07-25 10:44:00','50732.95','50742.15','50721.9','50733.0'),(250,'bank_nifty_fut','35165','2024-07-25 10:45:00','50733.0','50750.0','50726.15','50745.0'),(251,'bank_nifty_fut','35165','2024-07-25 10:46:00','50745.0','50769.9','50744.25','50756.9'),(252,'bank_nifty_fut','35165','2024-07-25 10:47:00','50760.0','50780.0','50743.0','50745.6'),(253,'bank_nifty_fut','35165','2024-07-25 10:48:00','50745.6','50746.0','50717.05','50717.7'),(254,'bank_nifty_fut','35165','2024-07-25 10:49:00','50717.7','50747.75','50716.5','50747.75'),(255,'bank_nifty_fut','35165','2024-07-25 10:50:00','50739.95','50775.15','50739.95','50763.35'),(256,'bank_nifty_fut','35165','2024-07-25 10:51:00','50763.35','50763.35','50755.55','50760.0'),(257,'bank_nifty_fut','35165','2024-07-25 10:52:00','50760.0','50769.05','50755.55','50759.15'),(258,'bank_nifty_fut','35165','2024-07-25 10:53:00','50755.0','50755.0','50730.0','50730.0'),(259,'bank_nifty_fut','35165','2024-07-25 10:54:00','50729.95','50736.75','50717.65','50732.0'),(260,'bank_nifty_fut','35165','2024-07-25 10:55:00','50732.0','50760.0','50732.0','50760.0'),(261,'bank_nifty_fut','35165','2024-07-25 10:56:00','50760.0','50772.0','50752.85','50754.45'),(262,'bank_nifty_fut','35165','2024-07-25 10:57:00','50754.45','50795.0','50753.35','50774.15'),(263,'bank_nifty_fut','35165','2024-07-25 10:58:00','50774.15','50780.0','50765.1','50770.45'),(264,'bank_nifty_fut','35165','2024-07-25 10:59:00','50770.45','50778.7','50752.45','50775.4'),(265,'bank_nifty_fut','35165','2024-07-25 11:00:00','50775.45','50818.2','50760.4','50760.4'),(266,'bank_nifty_fut','35165','2024-07-25 11:01:00','50774.95','50787.4','50764.4','50785.0'),(267,'bank_nifty_fut','35165','2024-07-25 11:02:00','50785.0','50802.15','50775.65','50792.2'),(268,'bank_nifty_fut','35165','2024-07-25 11:03:00','50792.2','50805.2','50782.1','50793.1'),(269,'bank_nifty_fut','35165','2024-07-25 11:04:00','50793.1','50800.0','50771.0','50780.05'),(270,'bank_nifty_fut','35165','2024-07-25 11:05:00','50780.05','50796.2','50770.8','50770.8'),(271,'bank_nifty_fut','35165','2024-07-25 11:06:00','50770.8','50782.2','50760.0','50765.35'),(272,'bank_nifty_fut','35165','2024-07-25 11:07:00','50765.35','50780.0','50756.0','50769.9'),(273,'bank_nifty_fut','35165','2024-07-25 11:08:00','50769.9','50795.3','50764.05','50795.3'),(274,'bank_nifty_fut','35165','2024-07-25 11:09:00','50786.4','50796.15','50780.0','50789.6'),(275,'bank_nifty_fut','35165','2024-07-25 11:10:00','50786.25','50800.0','50780.0','50796.0'),(276,'bank_nifty_fut','35165','2024-07-25 11:11:00','50800.0','50802.15','50781.55','50790.7'),(277,'bank_nifty_fut','35165','2024-07-25 11:12:00','50790.7','50807.0','50790.05','50793.0'),(278,'bank_nifty_fut','35165','2024-07-25 11:13:00','50793.0','50810.0','50793.0','50804.0'),(279,'bank_nifty_fut','35165','2024-07-25 11:14:00','50804.0','50804.0','50783.0','50783.7'),(280,'bank_nifty_fut','35165','2024-07-25 11:15:00','50783.7','50796.8','50783.7','50787.5'),(281,'bank_nifty_fut','35165','2024-07-25 11:16:00','50787.5','50792.0','50763.45','50769.95'),(282,'bank_nifty_fut','35165','2024-07-25 11:17:00','50774.4','50784.95','50764.0','50776.3'),(283,'bank_nifty_fut','35165','2024-07-25 11:18:00','50776.3','50792.25','50774.5','50785.45'),(284,'bank_nifty_fut','35165','2024-07-25 11:19:00','50785.45','50785.45','50742.9','50747.45'),(285,'bank_nifty_fut','35165','2024-07-25 11:20:00','50747.45','50780.0','50747.45','50780.0'),(286,'bank_nifty_fut','35165','2024-07-25 11:21:00','50780.0','50800.0','50771.95','50799.95'),(287,'bank_nifty_fut','35165','2024-07-25 11:22:00','50798.95','50816.3','50780.0','50807.9'),(288,'bank_nifty_fut','35165','2024-07-25 11:23:00','50807.9','50821.0','50798.65','50819.0'),(289,'bank_nifty_fut','35165','2024-07-25 11:24:00','50819.0','50840.25','50808.8','50840.25'),(290,'bank_nifty_fut','35165','2024-07-25 11:25:00','50831.65','50846.5','50827.75','50828.0'),(291,'bank_nifty_fut','35165','2024-07-25 11:26:00','50828.0','50849.0','50821.55','50844.85'),(292,'bank_nifty_fut','35165','2024-07-25 11:27:00','50844.85','50865.95','50844.05','50849.05'),(293,'bank_nifty_fut','35165','2024-07-25 11:28:00','50856.3','50880.9','50853.9','50866.05'),(294,'bank_nifty_fut','35165','2024-07-25 11:29:00','50866.1','50871.0','50852.0','50865.0'),(295,'bank_nifty_fut','35165','2024-07-25 11:30:00','50857.6','50868.0','50846.65','50860.0'),(296,'bank_nifty_fut','35165','2024-07-25 11:31:00','50860.0','50874.9','50852.7','50860.25'),(297,'bank_nifty_fut','35165','2024-07-25 11:32:00','50860.25','50885.0','50850.5','50870.0'),(298,'bank_nifty_fut','35165','2024-07-25 11:33:00','50870.0','50880.0','50865.2','50875.1'),(299,'bank_nifty_fut','35165','2024-07-25 11:34:00','50875.0','50892.5','50870.05','50875.0'),(300,'bank_nifty_fut','35165','2024-07-25 11:35:00','50875.0','50890.0','50869.4','50890.0'),(301,'bank_nifty_fut','35165','2024-07-25 11:36:00','50890.0','50916.05','50888.65','50901.0'),(302,'bank_nifty_fut','35165','2024-07-25 11:37:00','50901.0','50910.0','50900.0','50908.25'),(303,'bank_nifty_fut','35165','2024-07-25 11:38:00','50906.25','50910.0','50893.95','50910.0'),(304,'bank_nifty_fut','35165','2024-07-25 11:39:00','50910.0','50910.2','50888.95','50905.0'),(305,'bank_nifty_fut','35165','2024-07-25 11:40:00','50895.2','50930.0','50895.2','50917.85'),(306,'bank_nifty_fut','35165','2024-07-25 11:41:00','50917.15','50964.1','50915.05','50953.7'),(307,'bank_nifty_fut','35165','2024-07-25 11:42:00','50956.0','50959.75','50930.0','50930.0'),(308,'bank_nifty_fut','35165','2024-07-25 11:43:00','50930.0','50940.0','50911.8','50920.2'),(309,'bank_nifty_fut','35165','2024-07-25 11:44:00','50922.5','50949.35','50922.5','50938.65'),(310,'bank_nifty_fut','35165','2024-07-25 11:45:00','50938.65','50950.2','50935.0','50945.2'),(311,'bank_nifty_fut','35165','2024-07-25 11:46:00','50942.4','50942.4','50921.5','50930.25'),(312,'bank_nifty_fut','35165','2024-07-25 11:47:00','50930.25','50937.6','50920.2','50930.25'),(313,'bank_nifty_fut','35165','2024-07-25 11:48:00','50937.3','50949.75','50930.2','50945.6'),(314,'bank_nifty_fut','35165','2024-07-25 11:49:00','50937.85','50962.5','50924.7','50952.85'),(315,'bank_nifty_fut','35165','2024-07-25 11:50:00','50952.85','50953.2','50927.9','50928.8'),(316,'bank_nifty_fut','35165','2024-07-25 11:51:00','50928.8','50937.7','50913.65','50925.55'),(317,'bank_nifty_fut','35165','2024-07-25 11:52:00','50924.2','50929.0','50911.2','50918.0'),(318,'bank_nifty_fut','35165','2024-07-25 11:53:00','50914.0','50936.1','50907.5','50929.3'),(319,'bank_nifty_fut','35165','2024-07-25 11:54:00','50929.3','50937.75','50915.0','50929.25'),(320,'bank_nifty_fut','35165','2024-07-25 11:55:00','50929.25','50945.0','50922.25','50945.0'),(321,'bank_nifty_fut','35165','2024-07-25 11:56:00','50948.95','50960.0','50942.1','50947.85'),(322,'bank_nifty_fut','35165','2024-07-25 11:57:00','50947.85','50963.75','50940.65','50940.65'),(323,'bank_nifty_fut','35165','2024-07-25 11:58:00','50940.65','50947.7','50920.05','50920.05'),(324,'bank_nifty_fut','35165','2024-07-25 11:59:00','50920.05','50929.95','50915.45','50928.85'),(325,'bank_nifty_fut','35165','2024-07-25 12:00:00','50928.85','50940.35','50911.3','50913.15'),(326,'bank_nifty_fut','35165','2024-07-25 12:01:00','50913.1','50919.6','50900.25','50906.65'),(327,'bank_nifty_fut','35165','2024-07-25 12:02:00','50906.65','50920.0','50901.1','50901.1'),(328,'bank_nifty_fut','35165','2024-07-25 12:03:00','50909.3','50910.0','50893.0','50910.0'),(329,'bank_nifty_fut','35165','2024-07-25 12:04:00','50910.0','50940.0','50905.25','50935.0'),(330,'bank_nifty_fut','35165','2024-07-25 12:05:00','50935.0','50947.85','50925.0','50936.2'),(331,'bank_nifty_fut','35165','2024-07-25 12:06:00','50936.2','50936.75','50914.8','50914.8'),(332,'bank_nifty_fut','35165','2024-07-25 12:07:00','50914.8','50922.8','50903.45','50903.45'),(333,'bank_nifty_fut','35165','2024-07-25 12:08:00','50903.45','50918.95','50901.0','50910.7'),(334,'bank_nifty_fut','35165','2024-07-25 12:09:00','50910.7','50911.6','50878.6','50885.55'),(335,'bank_nifty_fut','35165','2024-07-25 12:10:00','50885.55','50908.9','50885.55','50891.45'),(336,'bank_nifty_fut','35165','2024-07-25 12:11:00','50891.45','50900.0','50884.2','50899.95'),(337,'bank_nifty_fut','35165','2024-07-25 12:12:00','50899.95','50913.85','50895.2','50909.2'),(338,'bank_nifty_fut','35165','2024-07-25 12:13:00','50909.2','50921.95','50895.0','50905.45'),(339,'bank_nifty_fut','35165','2024-07-25 12:14:00','50900.0','50915.1','50900.0','50907.9'),(340,'bank_nifty_fut','35165','2024-07-25 12:15:00','50907.9','50919.65','50904.95','50909.8'),(341,'bank_nifty_fut','35165','2024-07-25 12:16:00','50909.8','50917.7','50891.25','50910.15'),(342,'bank_nifty_fut','35165','2024-07-25 12:17:00','50910.15','50913.95','50901.0','50901.0'),(343,'bank_nifty_fut','35165','2024-07-25 12:18:00','50901.0','50910.0','50900.25','50906.65'),(344,'bank_nifty_fut','35165','2024-07-25 12:19:00','50906.65','50910.0','50900.0','50909.95'),(345,'bank_nifty_fut','35165','2024-07-25 12:20:00','50909.95','50925.7','50908.2','50915.25'),(346,'bank_nifty_fut','35165','2024-07-25 12:21:00','50915.25','50923.9','50910.0','50916.1'),(347,'bank_nifty_fut','35165','2024-07-25 12:22:00','50916.15','50916.85','50892.65','50900.0'),(348,'bank_nifty_fut','35165','2024-07-25 12:23:00','50900.0','50916.0','50892.4','50916.0'),(349,'bank_nifty_fut','35165','2024-07-25 12:24:00','50916.0','50931.75','50910.25','50925.4'),(350,'bank_nifty_fut','35165','2024-07-25 12:25:00','50924.95','50929.0','50914.75','50928.25'),(351,'bank_nifty_fut','35165','2024-07-25 12:26:00','50928.25','50931.75','50919.15','50927.5'),(352,'bank_nifty_fut','35165','2024-07-25 12:27:00','50927.5','50930.0','50908.4','50915.05'),(353,'bank_nifty_fut','35165','2024-07-25 12:28:00','50915.05','50920.0','50912.25','50917.65'),(354,'bank_nifty_fut','35165','2024-07-25 12:29:00','50917.65','50917.65','50901.1','50905.0'),(355,'bank_nifty_fut','35165','2024-07-25 12:30:00','50905.0','50930.0','50905.0','50923.7'),(356,'bank_nifty_fut','35165','2024-07-25 12:31:00','50923.7','50942.9','50922.05','50937.0'),(357,'bank_nifty_fut','35165','2024-07-25 12:32:00','50936.5','50939.0','50929.8','50939.0'),(358,'bank_nifty_fut','35165','2024-07-25 12:33:00','50939.0','50939.25','50923.15','50930.1'),(359,'bank_nifty_fut','35165','2024-07-25 12:34:00','50934.0','50934.0','50914.0','50917.8'),(360,'bank_nifty_fut','35165','2024-07-25 12:35:00','50917.8','50926.45','50907.5','50925.95'),(361,'bank_nifty_fut','35165','2024-07-25 12:36:00','50925.95','50929.0','50920.8','50924.0'),(362,'bank_nifty_fut','35165','2024-07-25 12:37:00','50924.0','50930.0','50912.2','50914.05'),(363,'bank_nifty_fut','35165','2024-07-25 12:38:00','50914.05','50916.6','50905.0','50905.0'),(364,'bank_nifty_fut','35165','2024-07-25 12:39:00','50905.0','50908.35','50870.0','50870.6'),(365,'bank_nifty_fut','35165','2024-07-25 12:40:00','50872.0','50878.0','50845.4','50845.4'),(366,'bank_nifty_fut','35165','2024-07-25 12:41:00','50845.4','50874.0','50843.05','50873.95'),(367,'bank_nifty_fut','35165','2024-07-25 12:42:00','50873.95','50873.95','50841.05','50841.05'),(368,'bank_nifty_fut','35165','2024-07-25 12:43:00','50841.05','50862.0','50840.4','50840.4'),(369,'bank_nifty_fut','35165','2024-07-25 12:44:00','50840.4','50854.25','50833.7','50841.7'),(370,'bank_nifty_fut','35165','2024-07-25 12:45:00','50841.7','50875.65','50841.7','50868.15'),(371,'bank_nifty_fut','35165','2024-07-25 12:46:00','50868.15','50889.85','50860.2','50881.0'),(372,'bank_nifty_fut','35165','2024-07-25 12:47:00','50881.0','50908.9','50880.05','50899.75'),(373,'bank_nifty_fut','35165','2024-07-25 12:48:00','50899.75','50904.6','50881.85','50903.35'),(374,'bank_nifty_fut','35165','2024-07-25 12:49:00','50903.35','50908.15','50894.9','50899.75'),(375,'bank_nifty_fut','35165','2024-07-25 12:50:00','50899.75','50899.75','50879.3','50885.0'),(376,'bank_nifty_fut','35165','2024-07-25 12:51:00','50885.0','50915.85','50885.0','50915.85'),(377,'bank_nifty_fut','35165','2024-07-25 12:52:00','50915.85','50915.85','50888.65','50897.5'),(378,'bank_nifty_fut','35165','2024-07-25 12:53:00','50897.5','50910.0','50892.7','50910.0'),(379,'bank_nifty_fut','35165','2024-07-25 12:54:00','50910.0','50910.0','50894.15','50904.85'),(380,'bank_nifty_fut','35165','2024-07-25 12:55:00','50904.85','50910.1','50885.05','50895.0'),(381,'bank_nifty_fut','35165','2024-07-25 12:56:00','50895.0','50899.95','50880.65','50899.95'),(382,'bank_nifty_fut','35165','2024-07-25 12:57:00','50899.95','50910.4','50887.6','50907.8'),(383,'bank_nifty_fut','35165','2024-07-25 12:58:00','50903.65','50915.0','50903.65','50913.6'),(384,'bank_nifty_fut','35165','2024-07-25 12:59:00','50913.6','50930.15','50912.45','50930.15'),(385,'bank_nifty_fut','35165','2024-07-25 13:00:00','50930.15','50930.35','50917.3','50925.0'),(386,'bank_nifty_fut','35165','2024-07-25 13:01:00','50925.0','50942.95','50911.35','50938.7'),(387,'bank_nifty_fut','35165','2024-07-25 13:02:00','50938.8','50945.15','50921.0','50925.0'),(388,'bank_nifty_fut','35165','2024-07-25 13:03:00','50925.0','50941.05','50920.95','50939.05'),(389,'bank_nifty_fut','35165','2024-07-25 13:04:00','50937.3','50937.8','50900.0','50912.0'),(390,'bank_nifty_fut','35165','2024-07-25 13:05:00','50912.0','50912.0','50889.05','50903.8'),(391,'bank_nifty_fut','35165','2024-07-25 13:06:00','50903.8','50911.0','50890.05','50908.85'),(392,'bank_nifty_fut','35165','2024-07-25 13:07:00','50908.45','50927.65','50908.45','50927.65'),(393,'bank_nifty_fut','35165','2024-07-25 13:08:00','50927.65','50934.2','50915.75','50915.75'),(394,'bank_nifty_fut','35165','2024-07-25 13:09:00','50915.75','50938.2','50915.75','50938.2'),(395,'bank_nifty_fut','35165','2024-07-25 13:10:00','50938.2','50939.75','50918.5','50918.5'),(396,'bank_nifty_fut','35165','2024-07-25 13:11:00','50918.4','50923.95','50905.75','50912.0'),(397,'bank_nifty_fut','35165','2024-07-25 13:12:00','50912.0','50913.15','50901.05','50905.35'),(398,'bank_nifty_fut','35165','2024-07-25 13:13:00','50905.35','50915.0','50897.95','50897.95'),(399,'bank_nifty_fut','35165','2024-07-25 13:14:00','50899.0','50902.75','50881.0','50881.0'),(400,'bank_nifty_fut','35165','2024-07-25 13:15:00','50881.0','50900.0','50881.0','50894.5'),(401,'bank_nifty_fut','35165','2024-07-25 13:16:00','50894.5','50896.3','50890.0','50892.95'),(402,'bank_nifty_fut','35165','2024-07-25 13:17:00','50892.95','50894.25','50891.0','50891.0'),(403,'bank_nifty_fut','35165','2024-07-25 13:18:00','50890.0','50893.0','50890.0','50892.25'),(404,'bank_nifty_fut','35165','2024-07-25 13:19:00','50892.25','50894.25','50879.95','50879.95'),(405,'bank_nifty_fut','35165','2024-07-25 13:20:00','50879.95','50885.95','50873.05','50875.1'),(406,'bank_nifty_fut','35165','2024-07-25 13:21:00','50875.1','50881.7','50860.1','50881.7'),(407,'bank_nifty_fut','35165','2024-07-25 13:22:00','50881.7','50884.0','50860.1','50865.15'),(408,'bank_nifty_fut','35165','2024-07-25 13:23:00','50865.15','50882.0','50865.15','50882.0'),(409,'bank_nifty_fut','35165','2024-07-25 13:24:00','50882.0','50894.2','50877.5','50889.05'),(410,'bank_nifty_fut','35165','2024-07-25 13:25:00','50889.05','50893.0','50888.0','50892.5'),(411,'bank_nifty_fut','35165','2024-07-25 13:26:00','50894.25','50900.0','50890.45','50898.85'),(412,'bank_nifty_fut','35165','2024-07-25 13:27:00','50898.85','50916.65','50898.0','50910.0'),(413,'bank_nifty_fut','35165','2024-07-25 13:28:00','50910.0','50913.0','50880.05','50880.05'),(414,'bank_nifty_fut','35165','2024-07-25 13:29:00','50880.05','50884.05','50874.05','50884.0'),(415,'bank_nifty_fut','35165','2024-07-25 13:30:00','50884.0','50898.25','50878.5','50881.75'),(416,'bank_nifty_fut','35165','2024-07-25 13:31:00','50881.75','50888.0','50872.1','50874.25'),(417,'bank_nifty_fut','35165','2024-07-25 13:32:00','50874.25','50878.05','50841.0','50855.15'),(418,'bank_nifty_fut','35165','2024-07-25 13:33:00','50850.0','50850.0','50818.0','50837.85'),(419,'bank_nifty_fut','35165','2024-07-25 13:34:00','50837.85','50864.1','50837.85','50840.75'),(420,'bank_nifty_fut','35165','2024-07-25 13:35:00','50840.75','50856.75','50840.0','50849.95'),(421,'bank_nifty_fut','35165','2024-07-25 13:36:00','50849.95','50864.5','50842.05','50850.0'),(422,'bank_nifty_fut','35165','2024-07-25 13:37:00','50850.0','50854.65','50827.4','50854.65'),(423,'bank_nifty_fut','35165','2024-07-25 13:38:00','50854.65','50860.95','50848.4','50848.4'),(424,'bank_nifty_fut','35165','2024-07-25 13:39:00','50844.65','50852.85','50830.0','50835.0'),(425,'bank_nifty_fut','35165','2024-07-25 13:40:00','50843.15','50849.8','50837.7','50843.75'),(426,'bank_nifty_fut','35165','2024-07-25 13:41:00','50843.75','50850.0','50835.1','50849.8'),(427,'bank_nifty_fut','35165','2024-07-25 13:42:00','50850.0','50855.0','50840.0','50840.0'),(428,'bank_nifty_fut','35165','2024-07-25 13:43:00','50840.0','50841.0','50830.0','50838.35'),(429,'bank_nifty_fut','35165','2024-07-25 13:44:00','50838.35','50839.4','50806.0','50816.9'),(430,'bank_nifty_fut','35165','2024-07-25 13:45:00','50816.9','50826.25','50810.0','50820.0'),(431,'bank_nifty_fut','35165','2024-07-25 13:46:00','50820.0','50839.1','50815.55','50830.1'),(432,'bank_nifty_fut','35165','2024-07-25 13:47:00','50830.1','50848.3','50830.0','50846.9'),(433,'bank_nifty_fut','35165','2024-07-25 13:48:00','50846.9','50846.9','50825.0','50825.0'),(434,'bank_nifty_fut','35165','2024-07-25 13:49:00','50825.0','50835.25','50818.15','50818.15'),(435,'bank_nifty_fut','35165','2024-07-25 13:50:00','50827.5','50836.5','50816.55','50825.8'),(436,'bank_nifty_fut','35165','2024-07-25 13:51:00','50825.8','50845.45','50825.45','50844.75'),(437,'bank_nifty_fut','35165','2024-07-25 13:52:00','50844.75','50864.95','50840.0','50858.35'),(438,'bank_nifty_fut','35165','2024-07-25 13:53:00','50858.35','50860.2','50850.0','50860.2'),(439,'bank_nifty_fut','35165','2024-07-25 13:54:00','50851.0','50871.05','50847.05','50848.05'),(440,'bank_nifty_fut','35165','2024-07-25 13:55:00','50848.05','50875.0','50848.05','50873.9'),(441,'bank_nifty_fut','35165','2024-07-25 13:56:00','50873.9','50874.0','50856.0','50874.0'),(442,'bank_nifty_fut','35165','2024-07-25 13:57:00','50875.0','50883.0','50860.4','50874.2'),(443,'bank_nifty_fut','35165','2024-07-25 13:58:00','50874.2','50888.0','50872.6','50887.85'),(444,'bank_nifty_fut','35165','2024-07-25 13:59:00','50887.85','50892.85','50866.95','50889.3'),(445,'bank_nifty_fut','35165','2024-07-25 14:00:00','50889.3','50907.55','50885.2','50903.0'),(446,'bank_nifty_fut','35165','2024-07-25 14:01:00','50903.0','50912.65','50892.6','50911.65'),(447,'bank_nifty_fut','35165','2024-07-25 14:02:00','50909.0','50920.95','50900.0','50920.95'),(448,'bank_nifty_fut','35165','2024-07-25 14:03:00','50926.1','50986.0','50923.75','50964.95'),(449,'bank_nifty_fut','35165','2024-07-25 14:04:00','50964.95','50975.0','50957.0','50974.85'),(450,'bank_nifty_fut','35165','2024-07-25 14:05:00','50975.0','50975.0','50928.9','50937.9'),(451,'bank_nifty_fut','35165','2024-07-25 14:06:00','50937.9','50938.65','50910.5','50910.5'),(452,'bank_nifty_fut','35165','2024-07-25 14:07:00','50910.5','50938.7','50910.5','50938.4'),(453,'bank_nifty_fut','35165','2024-07-25 14:08:00','50923.85','50937.25','50920.6','50922.05'),(454,'bank_nifty_fut','35165','2024-07-25 14:09:00','50922.05','50940.0','50922.0','50937.6'),(455,'bank_nifty_fut','35165','2024-07-26 09:14:00','50934.2','50934.2','50658.85','50658.85'),(456,'bank_nifty_fut','35165','2024-07-26 09:15:00','50704.7','50829.7','50704.7','50765.0'),(457,'bank_nifty_fut','35165','2024-07-26 09:16:00','50765.0','50773.75','50714.05','50719.35'),(458,'bank_nifty_fut','35165','2024-07-26 09:17:00','50719.35','50759.25','50711.25','50755.35'),(459,'bank_nifty_fut','35165','2024-07-26 09:18:00','50755.35','50815.8','50750.35','50800.0'),(460,'bank_nifty_fut','35165','2024-07-26 09:19:00','50800.0','50846.2','50797.7','50845.25'),(461,'bank_nifty_fut','35165','2024-07-26 09:20:00','50845.25','50884.8','50839.0','50880.0'),(462,'bank_nifty_fut','35165','2024-07-26 09:21:00','50872.55','50902.0','50856.45','50895.4'),(463,'bank_nifty_fut','35165','2024-07-26 09:22:00','50891.1','50891.1','50839.5','50839.5'),(464,'bank_nifty_fut','35165','2024-07-26 09:23:00','50839.0','50850.15','50805.0','50813.1'),(465,'bank_nifty_fut','35165','2024-07-26 09:24:00','50813.1','50820.15','50761.4','50764.7'),(466,'bank_nifty_fut','35165','2024-07-26 09:25:00','50769.4','50798.0','50760.65','50797.2'),(467,'bank_nifty_fut','35165','2024-07-26 09:26:00','50790.05','50819.0','50789.0','50789.0'),(468,'bank_nifty_fut','35165','2024-07-26 09:27:00','50788.4','50800.0','50775.3','50783.65'),(469,'bank_nifty_fut','35165','2024-07-26 09:28:00','50783.65','50788.8','50770.0','50772.5'),(470,'bank_nifty_fut','35165','2024-07-26 09:29:00','50774.1','50778.6','50746.0','50752.3'),(471,'bank_nifty_fut','35165','2024-07-26 09:30:00','50756.55','50765.7','50732.7','50763.35'),(472,'bank_nifty_fut','35165','2024-07-26 09:31:00','50763.35','50796.2','50760.0','50776.25'),(473,'bank_nifty_fut','35165','2024-07-26 09:32:00','50776.25','50779.1','50748.0','50749.45'),(474,'bank_nifty_fut','35165','2024-07-26 09:33:00','50754.1','50758.55','50725.25','50735.55'),(475,'bank_nifty_fut','35165','2024-07-26 09:34:00','50734.95','50735.8','50715.0','50725.0'),(476,'bank_nifty_fut','35165','2024-07-26 09:35:00','50725.0','50765.0','50725.0','50764.8'),(477,'bank_nifty_fut','35165','2024-07-26 09:36:00','50765.0','50814.9','50756.7','50809.0'),(478,'bank_nifty_fut','35165','2024-07-26 09:37:00','50813.45','50875.0','50813.45','50860.85'),(479,'bank_nifty_fut','35165','2024-07-26 09:38:00','50863.9','50886.95','50844.5','50883.15'),(480,'bank_nifty_fut','35165','2024-07-26 09:39:00','50887.2','50896.0','50855.35','50865.0'),(481,'bank_nifty_fut','35165','2024-07-26 09:40:00','50865.0','50879.15','50845.0','50857.35'),(482,'bank_nifty_fut','35165','2024-07-26 09:41:00','50857.35','50857.35','50809.05','50811.05'),(483,'bank_nifty_fut','35165','2024-07-26 09:42:00','50811.05','50816.95','50775.4','50775.4'),(484,'bank_nifty_fut','35165','2024-07-26 09:43:00','50775.4','50790.55','50745.0','50745.0'),(485,'bank_nifty_fut','35165','2024-07-26 09:44:00','50745.0','50790.55','50745.0','50790.0'),(486,'bank_nifty_fut','35165','2024-07-26 09:45:00','50797.85','50806.85','50764.25','50787.8'),(487,'bank_nifty_fut','35165','2024-07-26 09:46:00','50787.8','50810.0','50782.25','50803.4'),(488,'bank_nifty_fut','35165','2024-07-26 09:47:00','50803.4','50811.75','50795.05','50799.2'),(489,'bank_nifty_fut','35165','2024-07-26 09:48:00','50799.2','50809.8','50784.1','50791.75'),(490,'bank_nifty_fut','35165','2024-07-26 09:49:00','50787.05','50795.0','50756.0','50758.2'),(491,'bank_nifty_fut','35165','2024-07-26 09:50:00','50758.2','50767.9','50751.0','50760.95'),(492,'bank_nifty_fut','35165','2024-07-26 09:51:00','50760.95','50760.95','50745.0','50745.0'),(493,'bank_nifty_fut','35165','2024-07-26 09:52:00','50745.65','50745.65','50632.15','50632.15'),(494,'bank_nifty_fut','35165','2024-07-26 09:53:00','50632.15','50689.7','50628.2','50689.7'),(495,'bank_nifty_fut','35165','2024-07-26 09:54:00','50689.7','50745.0','50689.7','50745.0'),(496,'bank_nifty_fut','35165','2024-07-26 09:55:00','50745.0','50764.85','50729.85','50750.0'),(497,'bank_nifty_fut','35165','2024-07-26 09:56:00','50751.0','50777.4','50750.85','50769.85'),(498,'bank_nifty_fut','35165','2024-07-26 09:57:00','50766.5','50768.8','50742.7','50745.9'),(499,'bank_nifty_fut','35165','2024-07-26 09:58:00','50745.9','50749.8','50715.0','50729.8'),(500,'bank_nifty_fut','35165','2024-07-26 09:59:00','50734.85','50772.35','50730.15','50766.85'),(501,'bank_nifty_fut','35165','2024-07-26 10:00:00','50769.0','50808.6','50769.0','50795.7'),(502,'bank_nifty_fut','35165','2024-07-26 10:01:00','50795.7','50821.4','50793.35','50807.4'),(503,'bank_nifty_fut','35165','2024-07-26 10:02:00','50817.2','50817.2','50787.55','50787.55'),(504,'bank_nifty_fut','35165','2024-07-26 10:03:00','50786.65','50794.75','50750.0','50750.0'),(505,'bank_nifty_fut','35165','2024-07-26 10:04:00','50750.0','50764.95','50734.8','50740.0'),(506,'bank_nifty_fut','35165','2024-07-26 10:06:00','50735.05','50742.4','50731.0','50738.9'),(507,'bank_nifty_fut','35165','2024-07-26 10:07:00','50738.9','50767.9','50738.9','50765.05'),(508,'bank_nifty_fut','35165','2024-07-26 10:08:00','50765.05','50769.0','50736.45','50737.15'),(509,'bank_nifty_fut','35165','2024-07-26 10:09:00','50737.15','50744.5','50715.95','50715.95'),(510,'bank_nifty_fut','35165','2024-07-26 10:10:00','50715.95','50727.25','50715.0','50717.05'),(511,'bank_nifty_fut','35165','2024-07-26 10:11:00','50717.05','50733.0','50707.0','50733.0'),(512,'bank_nifty_fut','35165','2024-07-26 10:12:00','50733.0','50752.0','50729.6','50749.45'),(513,'bank_nifty_fut','35165','2024-07-26 10:13:00','50749.45','50750.9','50723.15','50725.75'),(514,'bank_nifty_fut','35165','2024-07-26 10:14:00','50725.75','50730.0','50715.0','50730.0'),(515,'bank_nifty_fut','35165','2024-07-26 10:15:00','50721.3','50746.6','50720.0','50738.3'),(516,'bank_nifty_fut','35165','2024-07-26 10:16:00','50738.3','50743.85','50729.0','50740.1'),(517,'bank_nifty_fut','35165','2024-07-26 10:17:00','50740.0','50756.8','50740.0','50756.8'),(518,'bank_nifty_fut','35165','2024-07-26 10:18:00','50756.7','50775.7','50756.7','50763.0'),(519,'bank_nifty_fut','35165','2024-07-26 10:19:00','50763.0','50787.0','50761.0','50781.05'),(520,'bank_nifty_fut','35165','2024-07-26 10:20:00','50781.05','50790.0','50774.0','50775.0'),(521,'bank_nifty_fut','35165','2024-07-26 10:21:00','50775.0','50775.0','50753.65','50755.15'),(522,'bank_nifty_fut','35165','2024-07-26 10:22:00','50755.15','50765.0','50752.0','50752.0'),(523,'bank_nifty_fut','35165','2024-07-26 10:23:00','50752.0','50772.35','50752.0','50763.85'),(524,'bank_nifty_fut','35165','2024-07-26 10:24:00','50762.25','50772.3','50751.0','50770.0'),(525,'bank_nifty_fut','35165','2024-07-26 10:25:00','50770.0','50779.75','50754.0','50754.0'),(526,'bank_nifty_fut','35165','2024-07-26 10:26:00','50751.55','50761.85','50747.0','50747.0'),(527,'bank_nifty_fut','35165','2024-07-26 10:27:00','50743.85','50760.0','50737.95','50750.15'),(528,'bank_nifty_fut','35165','2024-07-26 10:28:00','50750.15','50760.0','50750.05','50760.0'),(529,'bank_nifty_fut','35165','2024-07-26 10:29:00','50760.0','50762.25','50741.05','50752.5'),(530,'bank_nifty_fut','35165','2024-07-26 10:30:00','50752.5','50762.25','50749.5','50762.25'),(531,'bank_nifty_fut','35165','2024-07-26 10:31:00','50762.25','50789.8','50762.25','50783.95'),(532,'bank_nifty_fut','35165','2024-07-26 10:32:00','50783.95','50784.4','50772.6','50778.0'),(533,'bank_nifty_fut','35165','2024-07-26 10:33:00','50778.0','50787.0','50765.75','50780.05'),(534,'bank_nifty_fut','35165','2024-07-26 10:34:00','50780.35','50781.6','50769.95','50771.0'),(535,'bank_nifty_fut','35165','2024-07-26 10:35:00','50771.0','50776.55','50760.7','50774.8'),(536,'bank_nifty_fut','35165','2024-07-26 10:36:00','50774.8','50780.25','50760.15','50767.4'),(537,'bank_nifty_fut','35165','2024-07-26 10:37:00','50767.4','50772.3','50761.5','50772.0'),(538,'bank_nifty_fut','35165','2024-07-26 10:38:00','50772.0','50781.6','50771.85','50775.0'),(539,'bank_nifty_fut','35165','2024-07-26 10:39:00','50775.0','50780.4','50770.05','50778.3'),(540,'bank_nifty_fut','35165','2024-07-26 10:40:00','50778.3','50778.3','50755.0','50763.6'),(541,'bank_nifty_fut','35165','2024-07-26 10:41:00','50763.6','50763.6','50750.0','50755.05'),(542,'bank_nifty_fut','35165','2024-07-26 10:42:00','50755.05','50756.4','50741.0','50742.6'),(543,'bank_nifty_fut','35165','2024-07-26 10:43:00','50742.6','50750.0','50741.0','50744.6'),(544,'bank_nifty_fut','35165','2024-07-26 10:44:00','50744.6','50755.4','50740.0','50740.0'),(545,'bank_nifty_fut','35165','2024-07-26 10:45:00','50740.0','50749.1','50707.0','50718.8'),(546,'bank_nifty_fut','35165','2024-07-26 10:46:00','50711.7','50741.25','50711.7','50739.0'),(547,'bank_nifty_fut','35165','2024-07-26 10:47:00','50739.0','50746.5','50732.75','50742.0'),(548,'bank_nifty_fut','35165','2024-07-26 10:48:00','50742.0','50742.6','50720.0','50720.05'),(549,'bank_nifty_fut','35165','2024-07-26 10:49:00','50720.05','50727.65','50710.0','50720.1'),(550,'bank_nifty_fut','35165','2024-07-26 10:50:00','50720.1','50736.9','50720.1','50724.2'),(551,'bank_nifty_fut','35165','2024-07-26 10:51:00','50724.2','50732.05','50715.5','50725.0'),(552,'bank_nifty_fut','35165','2024-07-26 10:52:00','50725.0','50734.8','50724.15','50732.7'),(553,'bank_nifty_fut','35165','2024-07-26 10:53:00','50732.7','50741.3','50730.0','50741.3'),(554,'bank_nifty_fut','35165','2024-07-26 10:54:00','50744.75','50759.35','50737.35','50742.5'),(555,'bank_nifty_fut','35165','2024-07-26 10:55:00','50742.5','50754.8','50742.5','50754.0'),(556,'bank_nifty_fut','35165','2024-07-26 10:56:00','50754.0','50760.0','50746.0','50747.25'),(557,'bank_nifty_fut','35165','2024-07-26 10:57:00','50747.25','50754.9','50747.25','50747.25'),(558,'bank_nifty_fut','35165','2024-07-26 10:58:00','50746.0','50746.95','50737.5','50740.0'),(559,'bank_nifty_fut','35165','2024-07-26 10:59:00','50740.0','50764.0','50735.0','50761.2'),(560,'bank_nifty_fut','35165','2024-07-26 11:00:00','50757.5','50795.0','50755.0','50795.0'),(561,'bank_nifty_fut','35165','2024-07-26 11:01:00','50795.0','50799.0','50780.35','50795.0'),(562,'bank_nifty_fut','35165','2024-07-26 11:02:00','50795.0','50811.7','50793.0','50802.25'),(563,'bank_nifty_fut','35165','2024-07-26 11:03:00','50802.25','50838.8','50802.25','50829.55'),(564,'bank_nifty_fut','35165','2024-07-26 11:04:00','50829.85','50850.0','50823.0','50849.0'),(565,'bank_nifty_fut','35165','2024-07-26 11:05:00','50843.75','50855.8','50830.45','50840.0'),(566,'bank_nifty_fut','35165','2024-07-26 11:06:00','50840.0','50840.45','50825.0','50831.5'),(567,'bank_nifty_fut','35165','2024-07-26 11:07:00','50828.6','50839.0','50828.6','50830.0'),(568,'bank_nifty_fut','35165','2024-07-26 11:08:00','50830.0','50865.0','50823.85','50865.0'),(569,'bank_nifty_fut','35165','2024-07-26 11:09:00','50865.0','50934.7','50855.85','50934.7'),(570,'bank_nifty_fut','35165','2024-07-26 11:10:00','50935.0','50955.25','50914.35','50950.0'),(571,'bank_nifty_fut','35165','2024-07-26 11:11:00','50950.0','50973.85','50931.45','50973.85'),(572,'bank_nifty_fut','35165','2024-07-26 11:12:00','50973.85','50978.0','50953.4','50967.7'),(573,'bank_nifty_fut','35165','2024-07-26 11:13:00','50967.7','50985.85','50957.4','50971.15'),(574,'bank_nifty_fut','35165','2024-07-26 11:14:00','50982.55','50982.65','50942.1','50942.1'),(575,'bank_nifty_fut','35165','2024-07-26 11:15:00','50940.0','50951.55','50939.0','50949.15'),(576,'bank_nifty_fut','35165','2024-07-26 11:16:00','50949.15','50950.25','50925.7','50930.0'),(577,'bank_nifty_fut','35165','2024-07-26 11:17:00','50930.0','50933.4','50915.15','50926.0'),(578,'bank_nifty_fut','35165','2024-07-26 11:18:00','50926.0','50939.0','50925.0','50932.8'),(579,'bank_nifty_fut','35165','2024-07-26 11:19:00','50937.35','50937.35','50914.65','50926.55'),(580,'bank_nifty_fut','35165','2024-07-26 11:20:00','50917.6','50930.0','50905.0','50924.7'),(581,'bank_nifty_fut','35165','2024-07-26 11:21:00','50916.95','50929.55','50905.0','50905.0'),(582,'bank_nifty_fut','35165','2024-07-26 11:22:00','50905.0','50930.0','50903.05','50922.3'),(583,'bank_nifty_fut','35165','2024-07-26 11:23:00','50922.3','50924.05','50907.5','50918.65'),(584,'bank_nifty_fut','35165','2024-07-26 11:24:00','50918.65','50920.0','50905.4','50920.0'),(585,'bank_nifty_fut','35165','2024-07-26 11:25:00','50917.8','50937.95','50917.65','50917.65'),(586,'bank_nifty_fut','35165','2024-07-26 11:26:00','50917.65','50922.0','50906.8','50914.0'),(587,'bank_nifty_fut','35165','2024-07-26 11:27:00','50914.0','50930.0','50905.3','50930.0'),(588,'bank_nifty_fut','35165','2024-07-26 11:28:00','50929.7','50938.9','50925.5','50935.95'),(589,'bank_nifty_fut','35165','2024-07-26 11:29:00','50935.95','50935.95','50913.85','50929.95'),(590,'bank_nifty_fut','35165','2024-07-26 11:30:00','50922.75','50934.5','50915.0','50922.95'),(591,'bank_nifty_fut','35165','2024-07-26 11:31:00','50923.0','50923.0','50887.9','50893.1'),(592,'bank_nifty_fut','35165','2024-07-26 11:32:00','50893.1','50913.15','50884.1','50910.4'),(593,'bank_nifty_fut','35165','2024-07-26 11:33:00','50910.25','50910.25','50890.2','50900.0'),(594,'bank_nifty_fut','35165','2024-07-26 11:34:00','50900.0','50910.4','50875.0','50875.0'),(595,'bank_nifty_fut','35165','2024-07-26 11:35:00','50875.0','50910.0','50875.0','50908.5'),(596,'bank_nifty_fut','35165','2024-07-26 11:36:00','50908.5','50915.4','50900.35','50914.15'),(597,'bank_nifty_fut','35165','2024-07-26 11:37:00','50914.15','50924.0','50903.95','50920.25'),(598,'bank_nifty_fut','35165','2024-07-26 11:38:00','50920.25','50927.4','50910.2','50916.85'),(599,'bank_nifty_fut','35165','2024-07-26 11:39:00','50914.9','50917.1','50903.05','50917.1'),(600,'bank_nifty_fut','35165','2024-07-26 11:40:00','50917.1','50936.25','50915.7','50936.25'),(601,'bank_nifty_fut','35165','2024-07-26 11:41:00','50936.25','50936.25','50913.55','50920.15'),(602,'bank_nifty_fut','35165','2024-07-26 11:42:00','50920.15','50940.85','50920.15','50935.2'),(603,'bank_nifty_fut','35165','2024-07-26 11:43:00','50935.2','50948.95','50934.75','50947.05'),(604,'bank_nifty_fut','35165','2024-07-26 11:44:00','50947.05','50960.25','50945.0','50957.25'),(605,'bank_nifty_fut','35165','2024-07-26 11:45:00','50957.25','50960.0','50950.25','50955.95'),(606,'bank_nifty_fut','35165','2024-07-26 11:46:00','50955.95','50965.0','50945.05','50960.5'),(607,'bank_nifty_fut','35165','2024-07-26 11:47:00','50960.5','50976.0','50954.0','50954.0'),(608,'bank_nifty_fut','35165','2024-07-26 11:48:00','50954.0','50959.4','50948.95','50952.05'),(609,'bank_nifty_fut','35165','2024-07-26 11:49:00','50952.05','50959.55','50940.0','50950.2'),(610,'bank_nifty_fut','35165','2024-07-26 11:50:00','50950.2','50956.8','50944.05','50944.05'),(611,'bank_nifty_fut','35165','2024-07-26 11:51:00','50944.05','50945.45','50932.0','50933.3'),(612,'bank_nifty_fut','35165','2024-07-26 11:52:00','50933.3','50950.0','50933.3','50949.95'),(613,'bank_nifty_fut','35165','2024-07-26 11:53:00','50949.95','50954.95','50945.0','50953.85'),(614,'bank_nifty_fut','35165','2024-07-26 11:54:00','50955.25','50955.25','50945.05','50945.4'),(615,'bank_nifty_fut','35165','2024-07-26 11:55:00','50953.7','50955.0','50940.0','50947.35'),(616,'bank_nifty_fut','35165','2024-07-26 12:48:00','51100.7','51109.4','51100.7','51101.65'),(617,'bank_nifty_fut','35165','2024-07-26 12:49:00','51099.6','51099.6','51072.0','51077.05'),(618,'bank_nifty_fut','35165','2024-07-26 12:50:00','51077.05','51089.05','51066.35','51084.0'),(619,'bank_nifty_fut','35165','2024-07-26 12:51:00','51084.0','51103.1','51078.0','51088.65'),(620,'bank_nifty_fut','35165','2024-07-26 12:57:00','51088.2','51098.8','51083.6','51095.45'),(621,'bank_nifty_fut','35165','2024-07-26 12:59:00','51102.5','51107.15','51092.0','51107.15'),(622,'bank_nifty_fut','35165','2024-07-26 13:00:00','51106.1','51120.0','51101.55','51114.0'),(623,'bank_nifty_fut','35165','2024-07-26 13:02:00','51125.0','51142.0','51111.8','51127.5'),(624,'bank_nifty_fut','35165','2024-07-26 13:03:00','51127.5','51144.0','51125.0','51133.8'),(625,'bank_nifty_fut','35165','2024-07-26 13:04:00','51113.95','51113.95','51113.95','51113.95'),(626,'bank_nifty_fut','35165','2024-07-26 13:05:00','51113.95','51119.95','51104.7','51115.0'),(627,'bank_nifty_fut','35165','2024-07-26 13:15:00','51237.65','51258.0','51237.65','51248.1'),(628,'bank_nifty_fut','35165','2024-07-26 13:18:00','51208.0','51208.0','51196.1','51196.1'),(629,'bank_nifty_fut','35165','2024-07-26 13:19:00','51196.1','51223.35','51195.0','51219.0'),(630,'bank_nifty_fut','35165','2024-07-26 13:20:00','51219.0','51236.05','51209.85','51221.5'),(631,'bank_nifty_fut','35165','2024-07-26 13:21:00','51219.1','51230.2','51219.1','51230.0'),(632,'bank_nifty_fut','35165','2024-07-26 13:22:00','51230.0','51230.85','51205.85','51207.65'),(633,'bank_nifty_fut','35165','2024-07-26 13:23:00','51207.65','51238.5','51207.65','51238.5'),(634,'bank_nifty_fut','35165','2024-07-26 13:24:00','51235.3','51237.15','51216.15','51237.15'),(635,'bank_nifty_fut','35165','2024-07-26 13:25:00','51230.2','51236.8','51212.85','51229.5'),(636,'bank_nifty_fut','35165','2024-07-26 13:26:00','51229.5','51252.0','51229.5','51241.85'),(637,'bank_nifty_fut','35165','2024-07-26 13:27:00','51241.85','51250.0','51213.6','51224.9'),(638,'bank_nifty_fut','35165','2024-07-26 13:28:00','51225.0','51231.95','51214.05','51231.1'),(639,'bank_nifty_fut','35165','2024-07-26 13:29:00','51233.7','51237.15','51217.0','51217.0'),(640,'bank_nifty_fut','35165','2024-07-26 13:30:00','51217.0','51236.25','51216.85','51232.9'),(641,'bank_nifty_fut','35165','2024-07-26 13:31:00','51232.9','51232.9','51190.1','51194.95'),(642,'bank_nifty_fut','35165','2024-07-26 13:32:00','51194.95','51229.75','51192.55','51229.75'),(643,'bank_nifty_fut','35165','2024-07-26 13:33:00','51224.0','51230.2','51215.35','51224.95'),(644,'bank_nifty_fut','35165','2024-07-26 13:34:00','51216.7','51223.55','51206.0','51211.0'),(645,'bank_nifty_fut','35165','2024-07-26 13:35:00','51211.0','51239.7','51211.0','51235.25'),(646,'bank_nifty_fut','35165','2024-07-26 13:36:00','51235.25','51249.4','51235.0','51245.3'),(647,'bank_nifty_fut','35165','2024-07-26 13:37:00','51250.0','51290.0','51245.6','51290.0'),(648,'bank_nifty_fut','35165','2024-07-26 13:38:00','51290.0','51311.45','51284.9','51306.55'),(649,'bank_nifty_fut','35165','2024-07-26 13:39:00','51306.55','51324.05','51300.5','51305.8'),(650,'bank_nifty_fut','35165','2024-07-26 13:40:00','51305.8','51311.0','51282.0','51282.0'),(651,'bank_nifty_fut','35165','2024-07-26 13:41:00','51282.0','51291.8','51267.4','51268.85'),(652,'bank_nifty_fut','35165','2024-07-26 13:42:00','51268.85','51286.15','51268.85','51284.55'),(653,'bank_nifty_fut','35165','2024-07-26 13:43:00','51284.55','51285.0','51268.0','51280.0'),(654,'bank_nifty_fut','35165','2024-07-26 13:44:00','51280.0','51280.0','51268.85','51275.05'),(655,'bank_nifty_fut','35165','2024-07-26 13:45:00','51275.05','51300.15','51271.35','51300.0'),(656,'bank_nifty_fut','35165','2024-07-26 13:46:00','51299.35','51318.0','51298.0','51301.2'),(657,'bank_nifty_fut','35165','2024-07-26 13:47:00','51301.2','51314.55','51295.0','51307.6'),(658,'bank_nifty_fut','35165','2024-07-26 13:48:00','51310.0','51345.0','51300.6','51338.0'),(659,'bank_nifty_fut','35165','2024-07-26 13:49:00','51338.0','51380.0','51338.0','51377.4'),(660,'bank_nifty_fut','35165','2024-07-26 13:50:00','51361.95','51365.5','51361.95','51365.0'),(661,'bank_nifty_fut','35165','2024-07-26 13:51:00','51364.65','51388.5','51360.05','51385.55'),(662,'bank_nifty_fut','35165','2024-07-26 13:52:00','51385.55','51389.0','51350.05','51353.35'),(663,'bank_nifty_fut','35165','2024-07-26 13:53:00','51360.0','51363.0','51344.2','51361.4'),(664,'bank_nifty_fut','35165','2024-07-26 13:54:00','51359.25','51364.15','51340.05','51361.0'),(665,'bank_nifty_fut','35165','2024-07-26 13:55:00','51361.0','51364.95','51335.7','51352.25'),(666,'bank_nifty_fut','35165','2024-07-26 13:56:00','51359.4','51359.4','51319.45','51324.0'),(667,'bank_nifty_fut','35165','2024-07-26 13:57:00','51318.0','51318.0','51271.3','51284.35'),(668,'bank_nifty_fut','35165','2024-07-26 13:58:00','51281.05','51291.85','51210.1','51236.85'),(669,'bank_nifty_fut','35165','2024-07-26 13:59:00','51245.6','51275.0','51231.45','51265.6'),(670,'bank_nifty_fut','35165','2024-07-26 14:00:00','51271.85','51275.0','51217.45','51226.2'),(671,'bank_nifty_fut','35165','2024-07-26 14:01:00','51228.0','51240.0','51218.5','51240.0'),(672,'bank_nifty_fut','35165','2024-07-26 14:05:00','51235.0','51259.9','51235.0','51252.6'),(673,'bank_nifty_fut','35165','2024-07-26 14:06:00','51252.6','51275.0','51252.6','51267.95'),(674,'bank_nifty_fut','35165','2024-07-26 14:07:00','51267.95','51267.95','51240.0','51242.25'),(675,'bank_nifty_fut','35165','2024-07-26 14:17:00','51230.0','51239.05','51220.0','51220.0'),(676,'bank_nifty_fut','35165','2024-07-26 14:18:00','51219.5','51231.1','51205.65','51213.2'),(677,'bank_nifty_fut','35165','2024-07-26 14:19:00','51213.2','51230.0','51213.2','51224.8'),(678,'bank_nifty_fut','35165','2024-07-26 14:20:00','51223.0','51238.95','51223.0','51237.8'),(679,'bank_nifty_fut','35165','2024-07-26 14:21:00','51237.8','51244.8','51204.6','51219.15'),(680,'bank_nifty_fut','35165','2024-07-26 14:22:00','51217.35','51217.4','51172.2','51193.8'),(681,'bank_nifty_fut','35165','2024-07-26 14:23:00','51193.8','51193.8','51150.05','51164.1'),(682,'bank_nifty_fut','35165','2024-07-26 14:24:00','51164.1','51171.2','51141.15','51149.75'),(683,'bank_nifty_fut','35165','2024-07-26 14:25:00','51149.75','51187.95','51144.9','51187.95'),(684,'bank_nifty_fut','35165','2024-07-26 14:26:00','51187.95','51199.65','51161.75','51198.0'),(685,'bank_nifty_fut','35165','2024-07-26 14:27:00','51198.0','51230.0','51195.0','51211.05'),(686,'bank_nifty_fut','35165','2024-07-26 14:28:00','51211.05','51224.75','51201.15','51216.15'),(687,'bank_nifty_fut','35165','2024-07-26 14:29:00','51216.15','51218.0','51192.8','51204.95'),(688,'bank_nifty_fut','35165','2024-07-26 14:30:00','51202.0','51212.4','51193.5','51209.7'),(689,'bank_nifty_fut','35165','2024-07-26 14:31:00','51209.7','51232.3','51208.1','51231.2'),(690,'bank_nifty_fut','35165','2024-07-26 14:32:00','51228.1','51228.8','51214.15','51224.9'),(691,'bank_nifty_fut','35165','2024-07-26 14:33:00','51224.9','51228.95','51207.25','51218.85'),(692,'bank_nifty_fut','35165','2024-07-26 14:34:00','51218.85','51230.95','51212.9','51227.65'),(693,'bank_nifty_fut','35165','2024-07-26 14:39:00','51239.75','51249.55','51236.6','51247.45'),(694,'bank_nifty_fut','35165','2024-07-26 14:43:00','51244.2','51244.2','51244.2','51244.2'),(695,'bank_nifty_fut','35165','2024-07-26 14:44:00','51244.2','51254.3','51232.0','51246.0'),(696,'bank_nifty_fut','35165','2024-07-26 14:45:00','51246.0','51262.0','51240.15','51262.0');
/*!40000 ALTER TABLE `plutusAI_candledata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plutusAI_configuration`
--

DROP TABLE IF EXISTS `plutusAI_configuration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plutusAI_configuration` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `index_name` varchar(50) NOT NULL,
  `initial_sl` varchar(10) NOT NULL,
  `is_place_sl_required` tinyint(1) NOT NULL,
  `safe_sl` varchar(10) NOT NULL,
  `target_for_safe_sl` varchar(10) NOT NULL,
  `trailing_points` varchar(10) NOT NULL,
  `trend_check_points` varchar(10) NOT NULL,
  `levels` varchar(5000) NOT NULL,
  `user_id` varchar(500) NOT NULL,
  `start_scheduler` tinyint(1) NOT NULL,
  `stage` varchar(250) NOT NULL,
  `strike` varchar(5) NOT NULL,
  `lots` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_configuration`
--

LOCK TABLES `plutusAI_configuration` WRITE;
/*!40000 ALTER TABLE `plutusAI_configuration` DISABLE KEYS */;
INSERT INTO `plutusAI_configuration` VALUES (1,'nifty','10',1,'3','10','10','20','24500,24600,24700,24800,24900,24400,24300,24200,24100','antonyrajan.d@gmail.com',0,'stopped','100','1'),(2,'bank_nifty','30',1,'10','30','20','50','51500,51300,52000,51000','antonyrajan.d@gmail.com',0,'stopped','10','10'),(3,'fin_nifty','10',1,'10','10','10','15','23300,23500,23000','antonyrajan.d@gmail.com',0,'stopped','10','10');
/*!40000 ALTER TABLE `plutusAI_configuration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plutusAI_indexdetails`
--

DROP TABLE IF EXISTS `plutusAI_indexdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plutusAI_indexdetails` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `index_name` varchar(50) NOT NULL,
  `index_group` varchar(50) NOT NULL,
  `ltp` varchar(50) NOT NULL,
  `index_token` varchar(50) NOT NULL,
  `last_updated_time` varchar(250) NOT NULL,
  `qty` varchar(5) NOT NULL,
  `current_expiry` varchar(50) NOT NULL,
  `next_expiry` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_indexdetails`
--

LOCK TABLES `plutusAI_indexdetails` WRITE;
/*!40000 ALTER TABLE `plutusAI_indexdetails` DISABLE KEYS */;
INSERT INTO `plutusAI_indexdetails` VALUES (1,'nifty','indian_index','24805.95','99926000','2024-07-26 14:46:05','25','01-AUG-2024','08-AUG-2024'),(2,'bank_nifty','indian_index','51254.6','99926009','2024-07-26 14:46:01','15','31-JUL-2024','07-AUG-2024'),(3,'fin_nifty','indian_index','23316.3','99926037','2024-07-26 14:46:03','40','30-JUL-2024','06-AUG-2024'),(4,'bank_nifty_fut','indian_index','51252.0','35165','2024-07-26 14:46:10','15','16-JUL-2024','16-JUL-2024');
/*!40000 ALTER TABLE `plutusAI_indexdetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plutusAI_jobdetails`
--

DROP TABLE IF EXISTS `plutusAI_jobdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plutusAI_jobdetails` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` varchar(500) NOT NULL,
  `index_name` varchar(50) NOT NULL,
  `job_id` varchar(300) NOT NULL,
  `strategy` varchar(300) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=562 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_jobdetails`
--

LOCK TABLES `plutusAI_jobdetails` WRITE;
/*!40000 ALTER TABLE `plutusAI_jobdetails` DISABLE KEYS */;
/*!40000 ALTER TABLE `plutusAI_jobdetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plutusAI_orderbook`
--

DROP TABLE IF EXISTS `plutusAI_orderbook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plutusAI_orderbook` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` varchar(500) NOT NULL,
  `entry_time` bigint NOT NULL,
  `script_name` varchar(250) NOT NULL,
  `qty` varchar(250) NOT NULL,
  `entry_price` varchar(250) NOT NULL,
  `exit_price` varchar(250) DEFAULT NULL,
  `status` varchar(250) NOT NULL,
  `exit_time` bigint DEFAULT NULL,
  `total` varchar(250) DEFAULT NULL,
  `strategy` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=132 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_orderbook`
--

LOCK TABLES `plutusAI_orderbook` WRITE;
/*!40000 ALTER TABLE `plutusAI_orderbook` DISABLE KEYS */;
INSERT INTO `plutusAI_orderbook` VALUES (104,'antonyrajan.d@gmail.com',1721620083,'BANKNIFTY24JUL2452100PE','15','610.0','630.25','order_exited',1721620115,'303.75','scalper'),(105,'antonyrajan.d@gmail.com',1721965624,'BANKNIFTY31JUL2450700PE','15','378.25','337.6','order_exited',1721965744,'-609.7499999999997','scalper'),(106,'antonyrajan.d@gmail.com',1721965745,'BANKNIFTY31JUL2450700CE','15','444.7','413.45','order_exited',1721966104,'-468.75','scalper'),(107,'antonyrajan.d@gmail.com',1721966106,'BANKNIFTY31JUL2450900PE','15','459.3','433.0','order_exited',1721966162,'-394.50000000000017','scalper'),(108,'antonyrajan.d@gmail.com',1721966163,'BANKNIFTY31JUL2450700CE','15','436.3','397.2','order_exited',1721966404,'-586.5000000000003','scalper'),(109,'antonyrajan.d@gmail.com',1721966406,'BANKNIFTY31JUL2450800PE','15','404.45','395.0','order_exited',1721966523,'-141.74999999999983','scalper'),(110,'antonyrajan.d@gmail.com',1721966524,'BANKNIFTY31JUL2450600CE','15','471.15','457.75','order_exited',1721966583,'-200.99999999999966','scalper'),(111,'antonyrajan.d@gmail.com',1721966585,'BANKNIFTY31JUL2450800PE','15','408.25','366.95','order_exited',1721966821,'-619.5000000000002','scalper'),(112,'antonyrajan.d@gmail.com',1721966825,'BANKNIFTY31JUL2450700CE','15','432.05','397.2','order_exited',1721967242,'-522.7500000000003','scalper'),(113,'antonyrajan.d@gmail.com',1721967244,'BANKNIFTY31JUL2450800PE','15','400.55','373.9','order_exited',1721967301,'-399.7500000000005','scalper'),(114,'antonyrajan.d@gmail.com',1721967304,'BANKNIFTY31JUL2450700CE','15','414.6','400.6','order_exited',1721967604,'-210.0','scalper'),(115,'antonyrajan.d@gmail.com',1721967606,'BANKNIFTY31JUL2450800PE','15','390.0','439.15','order_exited',1721967739,'737.2499999999997','scalper'),(116,'antonyrajan.d@gmail.com',1721968683,'BANKNIFTY31JUL2450700CE','15','394.2','379.15','order_exited',1721968741,'-225.75000000000017','scalper'),(117,'antonyrajan.d@gmail.com',1721968744,'BANKNIFTY31JUL2450800PE','15','399.15','395.15','order_exited',1721968980,'-60.0','scalper'),(118,'antonyrajan.d@gmail.com',1721968982,'BANKNIFTY31JUL2450600CE','15','434.0','422.95','order_exited',1721969042,'-165.75000000000017','scalper'),(119,'antonyrajan.d@gmail.com',1721969044,'BANKNIFTY31JUL2450800PE','15','408.95','393.05','order_exited',1721969220,'-238.49999999999966','scalper'),(120,'antonyrajan.d@gmail.com',1721969222,'BANKNIFTY31JUL2450600CE','15','436.0','419.1','order_exited',1721970961,'-253.49999999999966','scalper'),(121,'antonyrajan.d@gmail.com',1721970963,'BANKNIFTY31JUL2450800PE','15','395.7','391.95','order_exited',1721971021,'-56.25','scalper'),(122,'antonyrajan.d@gmail.com',1721971022,'BANKNIFTY31JUL2450600CE','15','428.0','421.35','order_exited',1721971140,'-99.74999999999966','scalper'),(123,'antonyrajan.d@gmail.com',1721971141,'BANKNIFTY31JUL2450800PE','15','401.9','391.7','order_exited',1721971440,'-152.99999999999983','scalper'),(124,'antonyrajan.d@gmail.com',1721971441,'BANKNIFTY31JUL2450600CE','15','430.15','545.4','order_exited',1721972358,'1728.75','scalper'),(125,'antonyrajan.d@gmail.com',1721978322,'BANKNIFTY31JUL2451000CE','15','405.25',NULL,'order_placed',NULL,NULL,'scalper'),(126,'antonyrajan.d@gmail.com',1721982429,'NIFTY01AUG2424850PE','25','161.6','150.2','order_exited',1721982576,'-285.0000000000001','hunter'),(127,'antonyrajan.d@gmail.com',1721983801,'BANKNIFTY31JUL2451100CE','15','413.9','390.4','order_exited',1721983981,'-352.5','scalper'),(128,'antonyrajan.d@gmail.com',1721983983,'BANKNIFTY31JUL2451300PE','15','414.7','388.05','order_exited',1721984341,'-399.74999999999966','scalper'),(129,'antonyrajan.d@gmail.com',1721984341,'BANKNIFTY31JUL2451100CE','15','401.5','396.2','order_exited',1721984402,'-79.50000000000017','scalper'),(130,'antonyrajan.d@gmail.com',1721984402,'BANKNIFTY31JUL2451300PE','15','394.3','386.55','order_exited',1721984522,'-116.25','scalper'),(131,'antonyrajan.d@gmail.com',1721984522,'BANKNIFTY31JUL2451100CE','15','403.5',NULL,'order_placed',NULL,NULL,'scalper');
/*!40000 ALTER TABLE `plutusAI_orderbook` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plutusAI_paymentdetails`
--

DROP TABLE IF EXISTS `plutusAI_paymentdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plutusAI_paymentdetails` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` varchar(500) NOT NULL,
  `registed_date` varchar(200) NOT NULL,
  `renew_date` varchar(200) NOT NULL,
  `opted_index` varchar(500) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_paymentdetails`
--

LOCK TABLES `plutusAI_paymentdetails` WRITE;
/*!40000 ALTER TABLE `plutusAI_paymentdetails` DISABLE KEYS */;
/*!40000 ALTER TABLE `plutusAI_paymentdetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plutusAI_scalperdetails`
--

DROP TABLE IF EXISTS `plutusAI_scalperdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plutusAI_scalperdetails` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` varchar(500) NOT NULL,
  `index_name` varchar(50) NOT NULL,
  `strike` varchar(10) NOT NULL,
  `is_demo_trading_enabled` tinyint(1) NOT NULL,
  `use_full_capital` tinyint(1) NOT NULL,
  `target` varchar(100) NOT NULL,
  `lots` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_scalperdetails`
--

LOCK TABLES `plutusAI_scalperdetails` WRITE;
/*!40000 ALTER TABLE `plutusAI_scalperdetails` DISABLE KEYS */;
INSERT INTO `plutusAI_scalperdetails` VALUES (1,'antonyrajan.d@gmail.com','bank_nifty','100',1,0,'20','1');
/*!40000 ALTER TABLE `plutusAI_scalperdetails` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-26 21:05:31
