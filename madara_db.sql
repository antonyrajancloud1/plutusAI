-- MySQL dump 10.13  Distrib 8.0.39, for Linux (x86_64)
--
-- Host: localhost    Database: madara_db
-- ------------------------------------------------------
-- Server version	8.0.39-0ubuntu0.22.04.1

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
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add configuration',7,'add_configuration'),(26,'Can change configuration',7,'change_configuration'),(27,'Can delete configuration',7,'delete_configuration'),(28,'Can view configuration',7,'view_configuration'),(29,'Can add broker details',8,'add_brokerdetails'),(30,'Can change broker details',8,'change_brokerdetails'),(31,'Can delete broker details',8,'delete_brokerdetails'),(32,'Can view broker details',8,'view_brokerdetails'),(33,'Can add order book',9,'add_orderbook'),(34,'Can change order book',9,'change_orderbook'),(35,'Can delete order book',9,'delete_orderbook'),(36,'Can view order book',9,'view_orderbook'),(37,'Can add index details',10,'add_indexdetails'),(38,'Can change index details',10,'change_indexdetails'),(39,'Can delete index details',10,'delete_indexdetails'),(40,'Can view index details',10,'view_indexdetails'),(41,'Can add job details',11,'add_jobdetails'),(42,'Can change job details',11,'change_jobdetails'),(43,'Can delete job details',11,'delete_jobdetails'),(44,'Can view job details',11,'view_jobdetails'),(45,'Can add payment details',12,'add_paymentdetails'),(46,'Can change payment details',12,'change_paymentdetails'),(47,'Can delete payment details',12,'delete_paymentdetails'),(48,'Can view payment details',12,'view_paymentdetails'),(49,'Can add configuration',13,'add_configuration'),(50,'Can change configuration',13,'change_configuration'),(51,'Can delete configuration',13,'delete_configuration'),(52,'Can view configuration',13,'view_configuration'),(53,'Can add broker details',14,'add_brokerdetails'),(54,'Can change broker details',14,'change_brokerdetails'),(55,'Can delete broker details',14,'delete_brokerdetails'),(56,'Can view broker details',14,'view_brokerdetails'),(57,'Can add order book',15,'add_orderbook'),(58,'Can change order book',15,'change_orderbook'),(59,'Can delete order book',15,'delete_orderbook'),(60,'Can view order book',15,'view_orderbook'),(61,'Can add index details',16,'add_indexdetails'),(62,'Can change index details',16,'change_indexdetails'),(63,'Can delete index details',16,'delete_indexdetails'),(64,'Can view index details',16,'view_indexdetails'),(65,'Can add job details',17,'add_jobdetails'),(66,'Can change job details',17,'change_jobdetails'),(67,'Can delete job details',17,'delete_jobdetails'),(68,'Can view job details',17,'view_jobdetails'),(69,'Can add payment details',18,'add_paymentdetails'),(70,'Can change payment details',18,'change_paymentdetails'),(71,'Can delete payment details',18,'delete_paymentdetails'),(72,'Can view payment details',18,'view_paymentdetails'),(73,'Can add scalper details',19,'add_scalperdetails'),(74,'Can change scalper details',19,'change_scalperdetails'),(75,'Can delete scalper details',19,'delete_scalperdetails'),(76,'Can view scalper details',19,'view_scalperdetails'),(77,'Can add candle data',20,'add_candledata'),(78,'Can change candle data',20,'change_candledata'),(79,'Can delete candle data',20,'delete_candledata'),(80,'Can view candle data',20,'view_candledata'),(81,'Can add user auth tokens',21,'add_userauthtokens'),(82,'Can change user auth tokens',21,'change_userauthtokens'),(83,'Can delete user auth tokens',21,'delete_userauthtokens'),(84,'Can view user auth tokens',21,'view_userauthtokens'),(85,'Can add manual orders',22,'add_manualorders'),(86,'Can change manual orders',22,'change_manualorders'),(87,'Can delete manual orders',22,'delete_manualorders'),(88,'Can view manual orders',22,'view_manualorders'),(89,'Can add webhook details',23,'add_webhookdetails'),(90,'Can change webhook details',23,'change_webhookdetails'),(91,'Can delete webhook details',23,'delete_webhookdetails'),(92,'Can view webhook details',23,'view_webhookdetails');
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$720000$TrRCp4ZEcCaTlJwjDlgH4n$bXk1dvyXOBkHUCj4N2oz2av/RSJgPbv2aSX+u6Z+Daw=','2024-08-26 03:33:07.093469',1,'admin','','','madara@plutus.com',1,1,'2024-06-15 12:09:57.133766'),(2,'pbkdf2_sha256$720000$su9jHjriTejd7pUVflaCpW$zYqJtpAqxjfNEVZEVupo4bhWZI2XlrAvdVoIugS7MM4=','2024-08-30 04:19:41.825588',0,'antonyrajan.d','antonyrajan.d','','antonyrajan.d@gmail.com',0,1,'2024-06-15 12:19:09.052744'),(3,'pbkdf2_sha256$720000$BYD9wX9N3J8WILz9MjGC6z$DfCzh7MD1ZGakOEJomrM5moIZ/SRUCK9InnXmnpOqbc=','2024-09-06 03:29:06.563018',0,'kamezwaran.r','kamezwaran.r','','kamezwaran.r@gmail.com',0,1,'2024-07-28 07:20:41.773660');
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
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(8,'madaraApp','brokerdetails'),(7,'madaraApp','configuration'),(10,'madaraApp','indexdetails'),(11,'madaraApp','jobdetails'),(9,'madaraApp','orderbook'),(12,'madaraApp','paymentdetails'),(14,'plutusAI','brokerdetails'),(20,'plutusAI','candledata'),(13,'plutusAI','configuration'),(16,'plutusAI','indexdetails'),(17,'plutusAI','jobdetails'),(22,'plutusAI','manualorders'),(15,'plutusAI','orderbook'),(18,'plutusAI','paymentdetails'),(19,'plutusAI','scalperdetails'),(21,'plutusAI','userauthtokens'),(23,'plutusAI','webhookdetails'),(6,'sessions','session');
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
) ENGINE=InnoDB AUTO_INCREMENT=109 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-06-15 12:02:20.084320'),(2,'auth','0001_initial','2024-06-15 12:03:05.244407'),(3,'admin','0001_initial','2024-06-15 12:03:15.119429'),(4,'admin','0002_logentry_remove_auto_add','2024-06-15 12:03:15.325262'),(5,'admin','0003_logentry_add_action_flag_choices','2024-06-15 12:03:15.637149'),(6,'contenttypes','0002_remove_content_type_name','2024-06-15 12:03:21.877062'),(7,'auth','0002_alter_permission_name_max_length','2024-06-15 12:03:27.939462'),(8,'auth','0003_alter_user_email_max_length','2024-06-15 12:03:28.471649'),(9,'auth','0004_alter_user_username_opts','2024-06-15 12:03:28.800176'),(10,'auth','0005_alter_user_last_login_null','2024-06-15 12:03:33.421193'),(11,'auth','0006_require_contenttypes_0002','2024-06-15 12:03:33.985967'),(12,'auth','0007_alter_validators_add_error_messages','2024-06-15 12:03:34.747565'),(13,'auth','0008_alter_user_username_max_length','2024-06-15 12:03:40.350750'),(14,'auth','0009_alter_user_last_name_max_length','2024-06-15 12:03:46.485267'),(15,'auth','0010_alter_group_name_max_length','2024-06-15 12:03:47.223014'),(16,'auth','0011_update_proxy_permissions','2024-06-15 12:03:48.089320'),(17,'auth','0012_alter_user_first_name_max_length','2024-06-15 12:03:53.620107'),(18,'madaraApp','0001_initial','2024-06-15 12:03:55.626302'),(19,'madaraApp','0002_levels_remove_configuration_target_and_more','2024-06-15 12:04:26.236798'),(20,'madaraApp','0003_configuration_trailing_points_and_more','2024-06-15 12:04:31.008526'),(21,'madaraApp','0004_remove_configuration_levels_configuration_levels','2024-06-15 12:04:33.870250'),(22,'madaraApp','0005_delete_levels_configuration_user_id','2024-06-15 12:04:38.192991'),(23,'madaraApp','0006_configuration_start_scheduler','2024-06-15 12:04:40.835549'),(24,'madaraApp','0007_configuration_stage_configuration_strike','2024-06-15 12:04:46.791665'),(25,'madaraApp','0008_brokerdetails_orderbook','2024-06-15 12:04:51.436069'),(26,'madaraApp','0009_brokerdetails_is_demo_trading_enabled','2024-06-15 12:04:53.774299'),(27,'madaraApp','0010_alter_brokerdetails_user_id_and_more','2024-06-15 12:04:54.081200'),(28,'madaraApp','0011_brokerdetails_broker_api_token_and_more','2024-06-15 12:04:59.023843'),(29,'madaraApp','0012_indexdetails_jobdetails_and_more','2024-06-15 12:05:04.731802'),(30,'madaraApp','0013_brokerdetails_index_group','2024-06-15 12:05:07.228864'),(31,'madaraApp','0014_paymentdetails','2024-06-15 12:05:09.833452'),(32,'madaraApp','0015_jobdetails_terminate_job','2024-06-15 12:05:11.464829'),(33,'madaraApp','0016_alter_jobdetails_terminate_job','2024-06-15 12:05:17.943298'),(34,'madaraApp','0017_remove_jobdetails_terminate_job','2024-06-15 12:05:19.954183'),(35,'madaraApp','0018_indexdetails_index_ltp_indexdetails_index_token','2024-06-15 12:05:23.404805'),(36,'madaraApp','0019_rename_index_ltp_indexdetails_ltp_and_more','2024-06-15 12:05:26.593994'),(37,'madaraApp','0020_configuration_lots','2024-06-15 12:05:29.311089'),(38,'madaraApp','0021_indexdetails_qty','2024-06-15 12:05:31.329100'),(39,'madaraApp','0022_alter_configuration_lots','2024-06-15 12:05:31.549297'),(40,'madaraApp','0023_indexdetails_current_expiry_indexdetails_next_expiry','2024-06-15 12:05:34.506065'),(41,'madaraApp','0024_rename_time_orderbook_entry_time_orderbook_exit_time_and_more','2024-06-15 12:05:39.447613'),(42,'madaraApp','0025_supportedbrokers','2024-06-15 12:05:42.216629'),(43,'madaraApp','0026_alter_supportedbrokers_instruments','2024-06-15 12:05:42.543369'),(44,'madaraApp','0027_alter_supportedbrokers_instruments','2024-06-15 12:05:42.772467'),(45,'madaraApp','0028_alter_supportedbrokers_instruments','2024-06-15 12:05:42.948876'),(46,'madaraApp','0029_delete_supportedbrokers','2024-06-15 12:05:45.208042'),(47,'madaraApp','0030_alter_orderbook_exit_price_alter_orderbook_exit_time','2024-06-15 12:05:53.532372'),(48,'madaraApp','0031_orderbook_cumulative_p_l','2024-06-15 12:05:56.106308'),(49,'madaraApp','0032_rename_cumulative_p_l_orderbook_total','2024-06-15 12:05:57.373743'),(50,'madaraApp','0033_alter_orderbook_entry_time_alter_orderbook_exit_time','2024-06-15 12:06:07.645784'),(51,'madaraApp','0034_alter_orderbook_entry_time','2024-06-15 12:06:07.814832'),(52,'madaraApp','0035_alter_orderbook_entry_time_alter_orderbook_exit_time','2024-06-15 12:06:18.955808'),(53,'sessions','0001_initial','2024-06-15 12:06:22.209235'),(54,'plutusAI','0001_initial','2024-06-28 11:25:32.152488'),(55,'plutusAI','0002_levels_remove_configuration_target_and_more','2024-06-28 11:25:40.327923'),(56,'plutusAI','0003_configuration_trailing_points_and_more','2024-06-28 11:25:41.546149'),(57,'plutusAI','0004_remove_configuration_levels_configuration_levels','2024-06-28 11:25:42.421099'),(58,'plutusAI','0005_delete_levels_configuration_user_id','2024-06-28 11:25:43.398115'),(59,'plutusAI','0006_configuration_start_scheduler','2024-06-28 11:25:43.997191'),(60,'plutusAI','0007_configuration_stage_configuration_strike','2024-06-28 11:25:45.804286'),(61,'plutusAI','0008_brokerdetails_orderbook','2024-06-28 11:25:47.088906'),(62,'plutusAI','0009_brokerdetails_is_demo_trading_enabled','2024-06-28 11:25:47.744083'),(63,'plutusAI','0010_alter_brokerdetails_user_id_and_more','2024-06-28 11:25:47.833230'),(64,'plutusAI','0011_brokerdetails_broker_api_token_and_more','2024-06-28 11:25:49.122124'),(65,'plutusAI','0012_indexdetails_jobdetails_and_more','2024-06-28 11:25:51.448043'),(66,'plutusAI','0013_brokerdetails_index_group','2024-06-28 11:25:51.889756'),(67,'plutusAI','0014_paymentdetails','2024-06-28 11:25:52.521700'),(68,'plutusAI','0015_jobdetails_terminate_job','2024-06-28 11:25:53.110337'),(69,'plutusAI','0016_alter_jobdetails_terminate_job','2024-06-28 11:25:54.962080'),(70,'plutusAI','0017_remove_jobdetails_terminate_job','2024-06-28 11:25:55.802918'),(71,'plutusAI','0018_indexdetails_index_ltp_indexdetails_index_token','2024-06-28 11:25:57.420723'),(72,'plutusAI','0019_rename_index_ltp_indexdetails_ltp_and_more','2024-06-28 11:25:58.849286'),(73,'plutusAI','0020_configuration_lots','2024-06-28 11:25:59.539261'),(74,'plutusAI','0021_indexdetails_qty','2024-06-28 11:26:00.002390'),(75,'plutusAI','0022_alter_configuration_lots','2024-06-28 11:26:00.127633'),(76,'plutusAI','0023_indexdetails_current_expiry_indexdetails_next_expiry','2024-06-28 11:26:01.151605'),(77,'plutusAI','0024_rename_time_orderbook_entry_time_orderbook_exit_time_and_more','2024-06-28 11:26:01.970431'),(78,'plutusAI','0025_supportedbrokers','2024-06-28 11:26:02.951083'),(79,'plutusAI','0026_alter_supportedbrokers_instruments','2024-06-28 11:26:03.037508'),(80,'plutusAI','0027_alter_supportedbrokers_instruments','2024-06-28 11:26:03.136228'),(81,'plutusAI','0028_alter_supportedbrokers_instruments','2024-06-28 11:26:03.236543'),(82,'plutusAI','0029_delete_supportedbrokers','2024-06-28 11:26:03.716101'),(83,'plutusAI','0030_alter_orderbook_exit_price_alter_orderbook_exit_time','2024-06-28 11:26:05.800617'),(84,'plutusAI','0031_orderbook_cumulative_p_l','2024-06-28 11:26:06.335256'),(85,'plutusAI','0032_rename_cumulative_p_l_orderbook_total','2024-06-28 11:26:07.082821'),(86,'plutusAI','0033_alter_orderbook_entry_time_alter_orderbook_exit_time','2024-06-28 11:26:12.186488'),(87,'plutusAI','0034_alter_orderbook_entry_time','2024-06-28 11:26:12.265476'),(88,'plutusAI','0035_alter_orderbook_entry_time_alter_orderbook_exit_time','2024-06-28 11:26:15.701922'),(89,'plutusAI','0036_orderbook_strategy','2024-06-28 11:26:16.840524'),(90,'plutusAI','0037_jobdetails_strategy','2024-06-28 11:57:45.886402'),(91,'plutusAI','0038_scalperdetails','2024-06-29 15:47:23.836694'),(92,'plutusAI','0039_scalperdetails_is_demo_trading_enabled_and_more','2024-06-29 15:50:41.640121'),(93,'plutusAI','0040_scalperdetails_target','2024-06-29 16:00:13.207342'),(94,'plutusAI','0041_scalperdetails_lots','2024-07-04 05:26:34.514852'),(95,'plutusAI','0042_candledata_remove_scalperdetails_capital','2024-07-13 16:16:23.086358'),(96,'plutusAI','0043_alter_orderbook_entry_time_alter_orderbook_exit_time','2024-08-03 14:06:16.328674'),(97,'plutusAI','0044_userauthtokens','2024-08-09 04:02:29.425077'),(98,'plutusAI','0045_userauthtokens_lat_updated_time','2024-08-09 06:21:10.101914'),(99,'plutusAI','0046_remove_userauthtokens_jwt_token_and_more','2024-08-09 06:22:23.049446'),(100,'plutusAI','0047_rename_lat_updated_time_userauthtokens_last_updated_time','2024-08-09 07:32:12.604819'),(101,'plutusAI','0048_manualorders_webhookdetails','2024-08-09 12:40:45.249122'),(102,'plutusAI','0049_manualorders_is_demo_trading_enabled_and_more','2024-08-09 13:05:00.261759'),(103,'plutusAI','0050_orderbook_index_name','2024-08-09 14:01:41.742511'),(104,'plutusAI','0051_manualorders_strike','2024-08-10 05:39:44.861040'),(105,'plutusAI','0052_manualorders_lots','2024-08-10 05:41:47.423162'),(106,'plutusAI','0053_scalperdetails_on_candle_close','2024-08-13 16:33:16.614749'),(107,'plutusAI','0054_scalperdetails_status','2024-08-16 03:54:12.557391'),(108,'plutusAI','0055_rename_stage_configuration_status','2024-08-16 04:21:52.311014');
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
INSERT INTO `django_session` VALUES ('0s9rpf73rxz14csbt16p2j8mf5ebc4dv','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sXyQH:YZSbJcXnvPSM_k7HMEUDxqLA7glufY-3gllwmr0wl88','2024-08-11 07:34:29.248553'),('0tgkghfhwjufjpeca6zcnevhm4vs13mv','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sbAxG:WAZMRbWz_Rqp_HqFFJiUZdobAkBnHtQ3V1aYy6G4HP4','2024-08-20 03:33:46.715323'),('1tjnngoqgc6icwy4glvmw6201gqa5hlj','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sgyZz:HGm7aUfTDBke8ohiKxGRuKskkTI5Ob4AHG8oK1xMQ18','2024-09-05 03:33:43.022242'),('1w3rjocdrkbirb4emasru3uik7qbvyyx','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1serjM:fsm-zLDReKYxTbKVPkL_oZPI-dncMB4p0J3vCOVkWgU','2024-08-30 07:50:40.417272'),('22meergtgfz93dlpty8n7c776kl43e4a','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sYdYq:jWjfp6baoLCqvIUYSqVzzrdMXpKFHeYFj6nBZ4J772c','2024-08-13 03:30:04.744637'),('2cq14lo936z9aztyyumrp7uwron7xboc','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1safiv:KPN9Q-7hSCVelshneeFTNEAsjewpexbxOcj6oaZfIps','2024-08-18 18:12:53.886832'),('2y3j1qgxtrfo7qt8u9o9xy6gmozfj5jb','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sOqZg:L7UpklxZ8coWp1fxwexKp_k4U9iwVlO8G7f-an7RK1E','2024-07-17 03:22:28.848509'),('353vqnehg81n7gakbvg4rwp8dt5u4ntw','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1smPek:1pBKRTdk0-1BC27eQ4bZLZVbnqz_Kgr_h0M0YebP0LM','2024-09-20 03:29:06.795998'),('3k16xuy9ibvmbs1ocl5ya51n6uesedqd','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sadWd:WPu4aGq-eAhaKt-0k42SbJIBACo4CXkCOpWy0y0eOvU','2024-08-18 15:52:03.172785'),('48r0sv36sseibe36g69dgt3sq8c01do8','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sgcYH:lXbBs4gODEZ-rMRxbj_A8ef2Jdezfto07GG-sO7UsfU','2024-09-04 04:02:29.581558'),('4i7k3evdhzkw2bjbhzn67a5wvd11ni1k','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sISNf:rz6C4so4auNahvUBVexX7mUnT8Uh7NF_VZphUnIyTe0','2024-06-29 12:19:39.087860'),('4m1j6fdrk6vmqnaggkpn88oozfqfe16g','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sbXEP:wrQvxUMBW6OfKW0BDGly8VHPGBFY8mJgRx2FjWUPWE4','2024-08-21 03:20:57.984341'),('4yof7wloo7biyzeugedqgq2flun8r8u6','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1seqFE:gfXqVJCnJUlmzGHmgqmcz28xx_3HHiw-bstUAaE_FIw','2024-08-30 06:15:28.719113'),('5tx2le56gntim4afiheddepgrydlk7ej','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sin0j:GX0cgUg2DcJH-rigEB60e1vV59OrQgR_sfXsq5GdtXE','2024-09-10 03:36:49.624239'),('5vqusqh8csab0gpd2ogpqew18ao6uuyv','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sXyTS:mZrCnpnct7Ctz3A88irumkRoNOuVdT3nR5AeRZIsSfw','2024-08-11 07:37:46.565746'),('6i37486jv28xlabgk1yi3hcpkgyjkf13','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sZMiy:nzLg2BISf-1YBn6EkbFaHAHc57cyxMxJ7qMBx-5YUbo','2024-08-15 03:43:32.696338'),('6nngtz4wagaqxu1oa3jv4j9ylvbsr63x','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sYGo4:I_yxjI7i9pNKqGLApPskiWFh6tme3ZlcWHABg0ALUVE','2024-08-12 03:12:16.679433'),('6rdjyy2cbjo65gihe3ui3ro0wy19atyn','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sYdnV:EhjoRVtlYSBUHfckMIszTYtakhw6SywuRVlrq0aatlU','2024-08-13 03:45:13.490252'),('7jq13qgo8p8qxem1191eono1twx10q9h','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1siQmB:tIGVGcZCY4sNu7rFLS_CyG3JmKLiLzKd_dMZXEdH4rE','2024-09-09 03:52:19.938775'),('7uc7j4si2miicm21c9uvlz9sp14pj9ry','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sbY0M:wZQK-_dQs2FkbfcqaNVFtO55hBscbs-MYZ2EjD7UKL0','2024-08-21 04:10:30.544311'),('7yydcfa3looup8mn7kfc0ol0304vb1r3','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sj9gU:I3BtxjfD6KeHe3R-TUb0V1YsGeFcQeQF-uCLkdW5H80','2024-09-11 03:49:26.231881'),('7zjm0vy7mj3exlkix2774xjgrypm11xg','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1siQOa:XpDP96kPx1v1SxZcq0eoLCGNmDn9kbwtFqsmXMgA23Y','2024-09-09 03:27:56.982703'),('9bjt2xnb749z8n4wouomuwivxmlwq0lu','.eJxVjMsOwiAQRf-FtSEMjwIu3fcbyAyMUjU0Ke3K-O_apAvd3nPOfYmE21rT1nlJUxFnAeL0uxHmB7cdlDu22yzz3NZlIrkr8qBdjnPh5-Vw_w4q9vqtjQUqSpkcQUfGQNYYnSEzqODY2-KjxoEhKBc8KWs9XS37HHkghxTE-wPFnTdt:1siQTZ:4IGGr0uYgjM9QRiM5rMGuGcg6HpL9a1sIGnQbhq1cCo','2024-09-09 03:33:05.988210'),('9e71hcespj289zd07nkccivp4u9qn6f1','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sentO:o5GdteD_dTpN4fgMdSU3_Qkx9PIpCq6QkyEzFb6l2Ww','2024-08-30 03:44:46.725293'),('af182jkuc7thf5b1jpc1svx89mrwvae3','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sXhY7:8iuuAX_gHBW1nfiz8mHDCw8hfypJt0824jX2wq1Drlk','2024-08-10 13:33:27.166639'),('b7a9ll21yf3b9603vsq2kcsuhhh74v2l','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sbXSy:Q14LtQcp7ttr_5s-s4bUs9ZGVXEKeOfpks6eBFhM4F8','2024-08-21 03:36:00.908955'),('bdjy3no66rzpty31tuu9xnxh05z1x9cu','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sOqUz:OG5lpOn-rrIauTNOkGy_xFaOM7VbpreV11eo20DDUSQ','2024-07-17 03:17:37.045572'),('bmohkgrykvve8wy3xl90n6ws69ahohm6','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sYHWW:deS1LMeNLSF3_1m68ySOx4XVrGRLMBecqJ-AWJIwUJ8','2024-08-12 03:58:12.432809'),('br0qoe60vrg06x9f6xc3d6deo9ou89bt','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sdLuV:bfprFSaTlVlHWPo1e32wFSm4DVvfwFyc_15mMIhzT_s','2024-08-26 03:39:55.779148'),('c3rdv3rgah7wep5nb6mkhgzr390bu28q','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sZMgG:rTK-Va03VNTriv4DC38UVS82BfA85fsbTvJWeMOWDdk','2024-08-15 03:40:44.965916'),('c8pkgeiqed4lqtzdj653d5uwpoxy4w4c','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sbu2w:HHTqDJI6VHOQtGu0ie3X8ZfoxBR6Q6uAFkSk0UUsk4s','2024-08-22 03:42:38.201884'),('cheb4ei6u6q3e8syxl91z4jqi23ocyjo','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1se4nL:Sz6h4cQb02ZcuMtFFIGWwgHRUZqBek4kHHE1mSlkiws','2024-08-28 03:35:31.938597'),('clbko78uvh0hc30xbr0b2jihcluz900b','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sYJmR:g4I1iriY6EzXWO89vXo7BV4TaCznJkLlhCYSIcZNiMk','2024-08-12 06:22:47.940480'),('d86htw1tdqxj8f9149qydeuxstpnuqxj','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sZMpQ:NC8BpoCvG7BMSch6GTUtEtZUu4552mlr3TMvJ116QRE','2024-08-15 03:50:12.213207'),('dgp9cya2c4x2ymg5xejjf1lfqamjf6zl','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1serOH:YeSZKaDu_VAB1VEcHGbBkobO3jMhdtPSI1ye4x4P7E4','2024-08-30 07:28:53.296276'),('dte1a3alrd152yp95ey24yaaqdoq6k61','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sZj3z:YQ32lzVvr69hQNG749Cjdnz1ZP98Yei9sPMnXrrdobo','2024-08-16 03:34:43.736623'),('e7xtiz2ut1w0yucfu03vgrsbz4z05hc8','.eJxVjMsOwiAQRf-FtSEMjwIu3fcbyAyMUjU0Ke3K-O_apAvd3nPOfYmE21rT1nlJUxFnAeL0uxHmB7cdlDu22yzz3NZlIrkr8qBdjnPh5-Vw_w4q9vqtjQUqSpkcQUfGQNYYnSEzqODY2-KjxoEhKBc8KWs9XS37HHkghxTE-wPFnTdt:1sISEn:5nqopMDP56toJY3cYxaLEnijZ6ZUnr7qjgQaloiEvj4','2024-06-29 12:10:29.755173'),('einw0als4czb470uy10na8m0l83qnw6t','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sbXEQ:pvcMNK7qUwoZoG1hmTWBBHM4dyRUgOONi3HIF_jg8rg','2024-08-21 03:20:58.782112'),('erzt5xhhv8q2xtn39y916jqf7udng727','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sN9hB:D1vdKi-9csGFODYjMBpLOLH8_xC7Y0OLVoc96Fgwtxo','2024-07-12 11:23:13.012241'),('eswr59y1w2wlpgxq1q2izz3uerxit1ex','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sZ2Am:WUfSosAr2eKTmUpgzAjB7rveHt7NKgU_OoeftJHOu6I','2024-08-14 05:46:52.692186'),('f8un0g1st15m3suhx7ymkoz0irdgdmi7','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1siR2o:dOUX1Tt12Un08Y3KTdIRK1SbTDOvx_vrB7SJxM6WWW4','2024-09-09 04:09:30.333175'),('fyhu303r5suhfw984otd6okqgwm7bpul','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1slgsF:2hP3HObfWDubjcfG736E7Vr_aVU2DVWP5z7i_fUN-rk','2024-09-18 03:40:03.659045'),('g4hqeomvk4do4i9gg5fh3y50fqb91cv9','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sdiZi:XKCpGTIcuNb3baoyQYhLznxlKPZJJC1hWjN3oL4C_6w','2024-08-27 03:51:58.893558'),('g6q1ls3n4s7psbe7inwf4lsz6ji54j20','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sXyTT:qAEnandNUoaBbWxDDzrzhmbP4peqhoHndRQsgXwOSKI','2024-08-11 07:37:47.719855'),('h696djzr0147s9s5t6dbmfyyfs3qoghx','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1shKxz:QCfUdbvp-65---zOcBLi8AezBTaZgDE90Xkyy1D1WMs','2024-09-06 03:27:59.693786'),('hd9165ylvl8bwgdhr4tiq9e4yx41vdub','.eJxVjMsOwiAQRf-FtSEMjwIu3fcbyAyMUjU0Ke3K-O_apAvd3nPOfYmE21rT1nlJUxFnAeL0uxHmB7cdlDu22yzz3NZlIrkr8qBdjnPh5-Vw_w4q9vqtjQUqSpkcQUfGQNYYnSEzqODY2-KjxoEhKBc8KWs9XS37HHkghxTE-wPFnTdt:1siQTb:HR7Ph_D-iQMEBe6sHv-xU47wyO7z6pM5hfqhZJz2Te0','2024-09-09 03:33:07.171451'),('hdfidrp28dg7njd7etk7o1r47rdvk53b','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sgyXy:lA7fUiSzGazhwTN8hj0Tuw02v45otPklvPcSw8gUuGU','2024-09-05 03:31:38.192605'),('hm6j77v8buwthal25sp5aca2g0qky4fs','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sSXV2:WSf9sq2KX8edcN1vRh4FVbUsLGzy0KpG53bYjl5wbpo','2024-07-27 07:48:56.531386'),('hp0rrgmiszw6v9x4s6feyz3qgbxy9b5w','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1slL6v:jUBSZ57WWhmZbSZaDkeyMlqEjKdpb7EGFG8xwvOlJfU','2024-09-17 04:25:45.284901'),('i3tqnzk8ozeaiieudd07j3og5pwy6uhd','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sOqZi:0_WbPAA4NT6xUUyRQyU8s4r3C169iInAGVNWnT8NSJ8','2024-07-17 03:22:30.107491'),('jfvqfa1uzi6zb7t6dofqmo8ghjirtehk','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sdiOR:dMD7v0DCZGhmV1GIO3BJaovnCr70xqrfcEnzFB8Ea-E','2024-08-27 03:40:19.824174'),('jitu9suzvax750ht855s812gk0ftu0zk','.eJxVjMsOwiAQRf-FtSEMjwIu3fcbyAyMUjU0Ke3K-O_apAvd3nPOfYmE21rT1nlJUxFnAeL0uxHmB7cdlDu22yzz3NZlIrkr8qBdjnPh5-Vw_w4q9vqtjQUqSpkcQUfGQNYYnSEzqODY2-KjxoEhKBc8KWs9XS37HHkghxTE-wPFnTdt:1sSXVw:6KwTYkQVEq0Sfk5pgJG4EjgOqR_Tjr-mip1dWHkYN5w','2024-07-27 07:49:52.089921'),('jle62xcuhfbke3a7iipwc1iqzyn3nrad','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sbu2v:TA_YSAowTjfJr4gNgVI6f9U34Mm3UpgV0DG2ptSL3q4','2024-08-22 03:42:37.001108'),('jpbfs59taf97kvpvoaqqmjj7yfuorb8v','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sgc4m:dsRqOGEtD8kFuGmCKuS9nO0chMUmeQLX0K4QnWV2Uz4','2024-09-04 03:32:00.882216'),('jy4j7xsqtmgibf54axtnu9pta1bv3t29','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sgyZ4:PDetC3VD1CNxZ8OyEDYwK8-XjxQBkuz8tRBP2NGb4H4','2024-09-05 03:32:46.806647'),('kyhmnhkv0fdvv07yhcx54piocuqnc6qc','.eJxVjMsOwiAQRf-FtSEMjwIu3fcbyAyMUjU0Ke3K-O_apAvd3nPOfYmE21rT1nlJUxFnAeL0uxHmB7cdlDu22yzz3NZlIrkr8qBdjnPh5-Vw_w4q9vqtjQUqSpkcQUfGQNYYnSEzqODY2-KjxoEhKBc8KWs9XS37HHkghxTE-wPFnTdt:1sISQz:tPKj-ClanmA-Dk7Aww1zqQ-VKfssykyIPVFAvv-Dmhw','2024-06-29 12:23:05.675170'),('lf7xmrg6ckb3lv6j0i5ax8hls6sq0z05','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sYHG9:pIboJJJ1ZEETstq44YTPro_tbxcXaL_vC-tEu_0JbPA','2024-08-12 03:41:17.873088'),('lh83mfwuinulynz3wqjywqft347zdowc','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sjW6i:WImRAq9Trm1024if9XlT6sYGsbwjREnoSskUmo2eiCk','2024-09-12 03:46:00.374849'),('lmzf23fd3i15khsb4x2gqvfvqkudea01','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1senow:gLx8pWZ2nP56OFjMpgFBXgbVQBsfJmVYLL1bzVv34cY','2024-08-30 03:40:10.941765'),('lttzzng07lzuy9c28r9pivy1jwj3ypj7','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sgJR9:TdD8KQqs7b2JZNsK3MLMWZlkeFWDFuo1Nge7WGiIK5E','2024-09-03 07:37:51.926639'),('m66spp8fags77ejmtedyh1dziyypf7xm','.eJxVjMsOwiAQRf-FtSEMjwIu3fcbyAyMUjU0Ke3K-O_apAvd3nPOfYmE21rT1nlJUxFnAeL0uxHmB7cdlDu22yzz3NZlIrkr8qBdjnPh5-Vw_w4q9vqtjQUqSpkcQUfGQNYYnSEzqODY2-KjxoEhKBc8KWs9XS37HHkghxTE-wPFnTdt:1sXyC4:4yjkBjzUjZ3kApepTNk0V97vH1zQA7KFW1GcaIPJmYk','2024-08-11 07:19:48.177399'),('mcm9p3e9pdacuobatwbavr271vg0us36','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1se533:jeqpZsAotGLfVol_D_c0q6jRup45DQLIu3KRbaG2p4s','2024-08-28 03:51:45.045210'),('mkcz6bwyrof3i5gpyqocz5m7ke2ozg2u','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1saoo9:nPKek14sxmik8LKrq2OfsjEk8YH_l84AuaVu3cRj6gI','2024-08-19 03:54:53.360242'),('mydzcjky3kxexenutgo48618gi72s0km','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1skxqx:O6NMuysGp0WfowxuBvMSOg7faHw1D4YqSBVPKSuTMHQ','2024-09-16 03:35:43.922609'),('n3pubvbjtr4dyowjom46bjqzydn5k9hl','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sgyx4:m0Tbv-X1cCmO4IlwtEWttkQrvVKqVNcWJEXsDbh_rag','2024-09-05 03:57:34.174026'),('n7gip9o4sl61bxka6znuiw2o4v1qvhjb','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1siQKU:OJ2yYeGyGJ60WqDSFohLMfK56g4hud2S8tIBUKyfnT0','2024-09-09 03:23:42.744424'),('nkkh4m28m8mmnn16hluk9b4wf9yr4fz1','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sXyDL:LMVBCE2ZYrbqWv3XhP6LyIW940W5PsB1_yt93-tFpAM','2024-08-11 07:21:07.399821'),('nxpeki7kgyt9y9s8wc007k44dtpsfdb6','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sZMgD:hoU16Vy6UzqPH1aOfzJI0OZWnTTw6jMq6SR3EuUIet0','2024-08-15 03:40:41.515028'),('o7aq6tdcomo0dft883judg36w9o12y06','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sjYf9:k_KgEzvTBcqcLT7r3HF1e3qtoOaEJmj0xt8q7lYw5pA','2024-09-12 06:29:43.389200'),('olja5axf757w9t6zqawuv2z2kb862jui','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sbY0O:mtst74bBbGq_ifhZSEPwRHFDVvz6AH7dDeTP5BU8A8o','2024-08-21 04:10:32.515537'),('oqjfai52eov94chv6jmeoozgcx9247ht','.eJxVjMsOwiAQRf-FtSEMjwIu3fcbyAyMUjU0Ke3K-O_apAvd3nPOfYmE21rT1nlJUxFnAeL0uxHmB7cdlDu22yzz3NZlIrkr8qBdjnPh5-Vw_w4q9vqtjQUqSpkcQUfGQNYYnSEzqODY2-KjxoEhKBc8KWs9XS37HHkghxTE-wPFnTdt:1sdLC1:I9xhoUVveX1xIMdk1RcW8nkTJIbw2DQhw5pgS-yVxPY','2024-08-26 02:53:57.416425'),('pcuc27134fp4t15hjw32zpsyf8tde3pn','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sYIy9:mKqeQM0f6yP4d4mNPwXXzySKOOUxU9r_RA2hG0_GTMk','2024-08-12 05:30:49.039777'),('plett7u78di15n1jpw8rraivexlp0qbf','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1serju:-eC4crmxQjX0vGucPvdug71m_9VfhWAcnC2aW-ENm8g','2024-08-30 07:51:14.511936'),('pri82v6cbnqk4f7pmw20s8ixrvhtctvb','.eJxVjMsOwiAQRf-FtSEMjwIu3fcbyAyMUjU0Ke3K-O_apAvd3nPOfYmE21rT1nlJUxFnAeL0uxHmB7cdlDu22yzz3NZlIrkr8qBdjnPh5-Vw_w4q9vqtjQUqSpkcQUfGQNYYnSEzqODY2-KjxoEhKBc8KWs9XS37HHkghxTE-wPFnTdt:1sQej6:NIuFBRq1gRdkCB5zOuZE2omH0TWQ2HM33LMSMjUn2mA','2024-07-22 03:07:40.182675'),('qp5f4933s4c9k7g03kbdhesea0c44nze','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1shkBD:5Lyh5YaFvgk5uhJUhdtxbvgeNz8-9qFC4XdfuS9D_E8','2024-09-07 06:23:19.332390'),('scy45vrbkojqr1or0cxhqly6bqw3cfq7','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1si6sY:ZOIqLeEG5tc8074vbKFq7WAPpBirVQOnMWWnzffOi0g','2024-09-08 06:37:34.094647'),('shsvq0ofy2ge7wgs7fh7fr43gpl3pnch','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sgyaO:etmFJls_lfyy5i5fFOXxDSxJ0CSQuIFAc86nS0d8t4A','2024-09-05 03:34:08.082780'),('sm3jy6ndi9e3t5wpxdu0hqi75qspnkt5','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sXyPv:iqj5iY7cE-vk_en0sGxge4Y9X7No1kqBPjrs-MZ_ikk','2024-08-11 07:34:07.730903'),('stpufp01x22nu13vnoutivrtg8w865fu','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sXyJi:hrtHKakbnoexRVxSXXCabRkHViGdhecrA016cEEwsBI','2024-08-11 07:27:42.523672'),('sufbgk64vc5rpstfy0fe2q2q1emtz1oz','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1shLCS:YEcx4PKFzQh6i_8Y8k8lB8mv4uz7NP2BODn6WM4rvD4','2024-09-06 03:42:56.229538'),('t4jf4e0169nktmzyid1bsiu3ph7mjcgy','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sOqUx:rooxrBXoGRwZEolrVt-InZ1MTHaZREBRK370suc8WHU','2024-07-17 03:17:35.795418'),('t98dumrkmky68f01exwkw1mypit9glqj','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sgc4l:jXl6qHe0iOArvGZxRhuLSfgTwT7l7ZvpelZkEpyxftk','2024-09-04 03:31:59.808486'),('tdvaqo8abtd2zoiz9rltiizjy1tcyoo2','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sYdmx:Y1taYOlaVaoO18XCnrMe0oMW0K0XcOXKLTBsK2RsmAw','2024-08-13 03:44:39.911458'),('tvjil8cnzs0ei0ionvcl3szlkpyop6d8','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sjW4N:HtjW7b508ZZWeVby2TsOalG207QQlMMZ_B2G7pNunF8','2024-09-12 03:43:35.839448'),('tyil8duo5kku5utumjo9yhjx6t61837o','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sOqZf:a6Bt-5mMNluq-kMmH2IQyEL5aLzA1jJhHpj4c7o4nSQ','2024-07-17 03:22:27.495393'),('uhgpppuf3ets20xefd4wr3qunspbf9b5','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sgz20:oDa39gaakDl5mw6w3twTyyFlK2mCEXh_yc3KtbZMYqY','2024-09-05 04:02:40.730609'),('ujet1r0vjdatuc3403yqf9yuusuon45j','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sm3MJ:BomwhO7oV68Vr7q8Otj5Lxf2LNdMKFizcddlQgDI4_s','2024-09-19 03:40:35.923212'),('vhao97j773azajvhq0plcvxxuku2g9i5','.eJxVjMsOwiAQRf-FtSEMjwIu3fcbyAyMUjU0Ke3K-O_apAvd3nPOfYmE21rT1nlJUxFnAeL0uxHmB7cdlDu22yzz3NZlIrkr8qBdjnPh5-Vw_w4q9vqtjQUqSpkcQUfGQNYYnSEzqODY2-KjxoEhKBc8KWs9XS37HHkghxTE-wPFnTdt:1sRkp0:4Od5ily03gLhP-JcethZxcrcDt-Yyhu8B0CrNgSbYGI','2024-07-25 03:50:18.311605'),('w3pfcpn9y4vp93atdglum94ycqm7xrz4','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1scn8T:-n2d6vuSzndQHJiucWFsauEb6u5xAxnAvNCNw_JD-aA','2024-08-24 14:32:01.424498'),('w7psubfsgtwsvnkhdrayw0ugbonss510','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sftCJ:Vb_ugw7ICE04BdsADGbenHCtDA4jc1WadBliw79qaNQ','2024-09-02 03:36:47.404528'),('wvsv5fjx9jr7kdhwkojer4x4hzgl5n00','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sYfMK:eUXigXHMoHwlzR6eIJkhBrJ3e7UiKDuk7TVeFTFZcxE','2024-08-13 05:25:16.002599'),('xnexpf16ds7utiyqfr60dwvj8bruage3','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sXi3h:swd-ENeAaMMvm-LDGPWLAVlJU0jiu5aa5rgrL_AxhOQ','2024-08-10 14:06:05.218239'),('xpirp5576mvw1b7337tkw7fa04kh8t52','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sjt7h:Bqr5IwgBy5dftIj9BTiNTZftaByZnZ7G5-FlsL32gPM','2024-09-13 04:20:33.125672'),('xzmg7qvnpp02hk8p6ux488f5nif32m80','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1skL5N:fAv4dpagvBYpeS1Y3RNB3Q9sEWnGdakEhwvRKY9cjZU','2024-09-14 10:12:01.216059'),('y0nphqusd8omi2r3g5y2lt7r9qa3ukj6','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sXxim:PACrxxWuOARygwmwXsDjwaMGAABaJU3z2XsaPAjH3Lg','2024-08-11 06:49:32.799492'),('y3wxtnfp0di0gm2xuzs6x5lyijagswb8','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sYfMX:68ZPa6dhi_iqWc7gfMH3FD9Uo-kptv5knnCUA1OZ0tg','2024-08-13 05:25:29.318457'),('ys6f5suc5tmy7jvo5m99q0ez6nalwsu2','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sgFhV:HpSdF13MDAMZHIyusl0iGmNztaSIiOdPo7zFepR7bbQ','2024-09-03 03:38:29.199597'),('z105u2x9kors85wbnw67qnx40aquhtcq','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1shBGA:-9wcNluj_1_pQU0drNeX_Iuo2ExLSd7pqHlvBYaYTa8','2024-09-05 17:06:06.810137'),('zp5fhiuk02lql608351ohzwjdzmdhaij','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sbXSz:QDiDBLoNfONBivRjEju5U3TsuZw0KTMsP2HBpq65D8U','2024-08-21 03:36:01.185963');
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_brokerdetails`
--

LOCK TABLES `plutusAI_brokerdetails` WRITE;
/*!40000 ALTER TABLE `plutusAI_brokerdetails` DISABLE KEYS */;
INSERT INTO `plutusAI_brokerdetails` VALUES (1,'antonyrajan.d@gmail.com','A58033497','ANTONY RAJAN DANIEL','angel_one','generated',0,'pOruxLYZ','1005','RQFCDA2ZX2DMFZ5GR6HXXPFITY','indian_index'),(2,'madara@plutus.com','S50761409','SAHAYARAJ  SAHAYARAJ','angel_one','generated',0,'Q12feFjR','1005','5TXNGVJEVZYMHCLF6HHOQHHTZ4','indian_index'),(3,'kamezwaran.r@gmail.com','K60814687','KAMESWARAN R','angel_one','generated',0,'fSe5lcvn','2011','2K42JL4YOHKINI2RO7EEIXALG4','indian_index');
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
) ENGINE=InnoDB AUTO_INCREMENT=6006 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_candledata`
--

LOCK TABLES `plutusAI_candledata` WRITE;
/*!40000 ALTER TABLE `plutusAI_candledata` DISABLE KEYS */;
INSERT INTO `plutusAI_candledata` VALUES (5755,'bank_nifty_fut','35075','2024-09-04 11:51:00','51645.9','51656.95','51640.05','51650.0'),(5756,'bank_nifty_fut','35075','2024-09-04 11:52:00','51650.0','51655.1','51642.5','51652.0'),(5757,'bank_nifty_fut','35075','2024-09-04 11:53:00','51652.0','51660.0','51648.85','51655.0'),(5758,'bank_nifty_fut','35075','2024-09-04 11:54:00','51655.0','51655.3','51645.05','51646.3'),(5759,'bank_nifty_fut','35075','2024-09-04 11:55:00','51650.0','51652.75','51643.0','51644.15'),(5760,'bank_nifty_fut','35075','2024-09-04 11:56:00','51644.15','51651.0','51641.35','51650.85'),(5761,'bank_nifty_fut','35075','2024-09-04 11:57:00','51650.9','51656.95','51643.55','51646.8'),(5762,'bank_nifty_fut','35075','2024-09-04 11:58:00','51645.55','51659.45','51645.55','51659.45'),(5763,'bank_nifty_fut','35075','2024-09-04 11:59:00','51653.3','51659.7','51650.0','51650.25'),(5764,'bank_nifty_fut','35075','2024-09-04 12:00:00','51658.4','51659.7','51650.0','51652.1'),(5765,'bank_nifty_fut','35075','2024-09-04 12:01:00','51658.0','51662.9','51652.45','51662.9'),(5766,'bank_nifty_fut','35075','2024-09-04 12:02:00','51660.0','51669.4','51652.0','51658.5'),(5767,'bank_nifty_fut','35075','2024-09-04 12:03:00','51659.35','51662.2','51652.0','51659.75'),(5768,'bank_nifty_fut','35075','2024-09-04 12:04:00','51653.35','51659.45','51651.05','51651.05'),(5769,'bank_nifty_fut','35075','2024-09-04 12:05:00','51651.0','51665.1','51651.0','51655.5'),(5770,'bank_nifty_fut','35075','2024-09-04 12:06:00','51663.85','51675.25','51658.1','51669.5'),(5771,'bank_nifty_fut','35075','2024-09-04 12:07:00','51670.65','51675.1','51660.75','51663.3'),(5772,'bank_nifty_fut','35075','2024-09-04 12:08:00','51672.1','51679.95','51665.05','51672.1'),(5773,'bank_nifty_fut','35075','2024-09-04 12:09:00','51679.75','51680.7','51667.1','51679.0'),(5774,'bank_nifty_fut','35075','2024-09-04 12:10:00','51679.0','51682.7','51671.8','51673.05'),(5775,'bank_nifty_fut','35075','2024-09-04 12:11:00','51679.0','51684.95','51673.5','51683.65'),(5776,'bank_nifty_fut','35075','2024-09-04 12:12:00','51676.85','51683.65','51667.7','51679.05'),(5777,'bank_nifty_fut','35075','2024-09-04 12:14:00','51662.85','51674.9','51662.25','51674.9'),(5778,'bank_nifty_fut','35075','2024-09-04 12:15:00','51665.0','51675.0','51663.05','51668.3'),(5779,'bank_nifty_fut','35075','2024-09-04 12:16:00','51668.25','51675.7','51664.85','51665.0'),(5780,'bank_nifty_fut','35075','2024-09-04 12:17:00','51665.0','51674.0','51658.15','51673.95'),(5781,'bank_nifty_fut','35075','2024-09-04 12:18:00','51665.2','51678.0','51665.2','51668.0'),(5782,'bank_nifty_fut','35075','2024-09-04 12:19:00','51668.0','51678.0','51666.4','51677.05'),(5783,'bank_nifty_fut','35075','2024-09-04 12:20:00','51677.95','51690.0','51670.0','51676.25'),(5784,'bank_nifty_fut','35075','2024-09-04 12:21:00','51676.1','51685.7','51672.95','51680.0'),(5785,'bank_nifty_fut','35075','2024-09-04 12:23:00','51672.0','51680.0','51672.0','51679.0'),(5786,'bank_nifty_fut','35075','2024-09-04 12:24:00','51675.0','51680.0','51672.0','51679.0'),(5787,'bank_nifty_fut','35075','2024-09-04 12:25:00','51679.0','51679.0','51671.0','51671.0'),(5788,'bank_nifty_fut','35075','2024-09-04 12:26:00','51674.0','51680.0','51671.0','51680.0'),(5789,'bank_nifty_fut','35075','2024-09-04 12:27:00','51680.0','51680.0','51666.65','51668.0'),(5790,'bank_nifty_fut','35075','2024-09-04 12:28:00','51668.0','51675.05','51667.0','51673.55'),(5791,'bank_nifty_fut','35075','2024-09-04 12:29:00','51674.95','51675.0','51667.0','51673.8'),(5792,'bank_nifty_fut','35075','2024-09-04 12:30:00','51673.75','51675.0','51667.0','51667.0'),(5793,'bank_nifty_fut','35075','2024-09-04 12:31:00','51667.0','51674.05','51650.0','51660.75'),(5794,'bank_nifty_fut','35075','2024-09-04 12:32:00','51661.0','51669.6','51652.5','51658.1'),(5795,'bank_nifty_fut','35075','2024-09-04 12:33:00','51667.1','51669.25','51658.95','51659.35'),(5796,'bank_nifty_fut','35075','2024-09-04 12:34:00','51665.0','51672.0','51660.85','51665.0'),(5797,'bank_nifty_fut','35075','2024-09-04 12:35:00','51667.35','51670.0','51665.0','51667.55'),(5798,'bank_nifty_fut','35075','2024-09-04 12:36:00','51666.0','51669.2','51665.0','51669.2'),(5799,'bank_nifty_fut','35075','2024-09-04 12:37:00','51669.2','51672.0','51657.05','51672.0'),(5800,'bank_nifty_fut','35075','2024-09-04 12:45:00','51654.05','51669.4','51653.95','51666.9'),(5801,'bank_nifty_fut','35075','2024-09-04 12:46:00','51660.0','51667.0','51657.25','51661.0'),(5802,'bank_nifty_fut','35075','2024-09-04 12:55:00','51645.05','51656.4','51645.05','51655.0'),(5803,'bank_nifty_fut','35075','2024-09-04 12:56:00','51646.05','51655.0','51646.05','51650.0'),(5804,'bank_nifty_fut','35075','2024-09-04 12:57:00','51646.0','51650.0','51638.45','51641.15'),(5805,'bank_nifty_fut','35075','2024-09-04 12:58:00','51641.05','51649.95','51635.25','51636.4'),(5806,'bank_nifty_fut','35075','2024-09-04 12:59:00','51635.4','51647.7','51635.0','51635.25'),(5807,'bank_nifty_fut','35075','2024-09-04 13:00:00','51635.05','51641.65','51626.1','51630.0'),(5808,'bank_nifty_fut','35075','2024-09-04 13:01:00','51628.5','51640.55','51625.55','51635.0'),(5809,'bank_nifty_fut','35075','2024-09-04 13:02:00','51630.1','51640.0','51630.0','51632.7'),(5810,'bank_nifty_fut','35075','2024-09-04 13:03:00','51633.75','51644.0','51630.3','51642.35'),(5811,'bank_nifty_fut','35075','2024-09-04 13:05:00','51643.95','51644.0','51639.1','51644.0'),(5812,'bank_nifty_fut','35075','2024-09-04 13:06:00','51644.0','51654.95','51640.0','51654.95'),(5813,'bank_nifty_fut','35075','2024-09-04 13:07:00','51655.0','51663.75','51645.65','51655.9'),(5814,'bank_nifty_fut','35075','2024-09-04 13:08:00','51655.6','51655.6','51640.4','51650.8'),(5815,'bank_nifty_fut','35075','2024-09-04 13:09:00','51650.0','51653.25','51642.05','51653.25'),(5816,'bank_nifty_fut','35075','2024-09-04 13:13:00','51654.05','51664.95','51646.0','51659.85'),(5817,'bank_nifty_fut','35075','2024-09-04 13:14:00','51653.0','51663.0','51646.25','51651.3'),(5818,'bank_nifty_fut','35075','2024-09-04 13:15:00','51650.65','51670.0','51650.3','51670.0'),(5819,'bank_nifty_fut','35075','2024-09-04 13:16:00','51662.7','51685.0','51662.7','51677.7'),(5820,'bank_nifty_fut','35075','2024-09-04 13:17:00','51677.65','51686.85','51669.25','51675.0'),(5821,'bank_nifty_fut','35075','2024-09-04 13:19:00','51680.05','51689.0','51676.45','51685.0'),(5822,'bank_nifty_fut','35075','2024-09-04 13:20:00','51685.0','51685.0','51679.0','51685.0'),(5823,'bank_nifty_fut','35075','2024-09-04 13:21:00','51688.65','51689.0','51680.0','51680.0'),(5824,'bank_nifty_fut','35075','2024-09-04 13:22:00','51685.35','51686.2','51673.25','51679.95'),(5825,'bank_nifty_fut','35075','2024-09-04 13:23:00','51678.0','51678.0','51663.95','51665.0'),(5826,'bank_nifty_fut','35075','2024-09-04 13:24:00','51665.0','51675.0','51664.05','51673.85'),(5827,'bank_nifty_fut','35075','2024-09-04 13:25:00','51673.9','51675.0','51666.2','51671.0'),(5828,'bank_nifty_fut','35075','2024-09-04 13:26:00','51675.0','51680.0','51670.0','51677.95'),(5829,'bank_nifty_fut','35075','2024-09-04 13:27:00','51670.0','51677.95','51666.0','51670.0'),(5830,'bank_nifty_fut','35075','2024-09-04 13:28:00','51669.95','51675.0','51663.1','51674.55'),(5831,'bank_nifty_fut','35075','2024-09-04 13:29:00','51673.7','51674.85','51660.0','51670.0'),(5832,'bank_nifty_fut','35075','2024-09-04 13:30:00','51669.95','51676.7','51664.0','51666.35'),(5833,'bank_nifty_fut','35075','2024-09-04 13:31:00','51665.0','51685.0','51664.05','51673.8'),(5834,'bank_nifty_fut','35075','2024-09-04 13:32:00','51680.0','51685.0','51673.05','51684.75'),(5835,'bank_nifty_fut','35075','2024-09-04 13:33:00','51684.05','51685.0','51673.85','51673.85'),(5836,'bank_nifty_fut','35075','2024-09-04 13:34:00','51673.85','51682.8','51668.05','51679.25'),(5837,'bank_nifty_fut','35075','2024-09-04 13:35:00','51673.0','51683.55','51672.0','51681.0'),(5838,'bank_nifty_fut','35075','2024-09-04 13:36:00','51673.05','51676.9','51665.0','51667.0'),(5839,'bank_nifty_fut','35075','2024-09-04 13:37:00','51666.0','51667.0','51659.0','51659.0'),(5840,'bank_nifty_fut','35075','2024-09-04 13:38:00','51658.9','51667.5','51654.75','51656.25'),(5841,'bank_nifty_fut','35075','2024-09-04 13:39:00','51664.4','51666.65','51654.65','51658.3'),(5842,'bank_nifty_fut','35075','2024-09-04 13:40:00','51665.0','51667.25','51655.0','51663.7'),(5843,'bank_nifty_fut','35075','2024-09-04 13:41:00','51655.0','51662.9','51655.0','51662.0'),(5844,'bank_nifty_fut','35075','2024-09-04 13:42:00','51662.0','51663.25','51655.0','51662.9'),(5845,'bank_nifty_fut','35075','2024-09-04 13:43:00','51655.25','51662.25','51646.0','51649.95'),(5846,'bank_nifty_fut','35075','2024-09-04 13:44:00','51654.9','51655.0','51646.05','51655.0'),(5847,'bank_nifty_fut','35075','2024-09-04 13:45:00','51648.25','51655.0','51647.1','51654.95'),(5848,'bank_nifty_fut','35075','2024-09-04 13:46:00','51654.95','51655.0','51650.0','51653.0'),(5849,'bank_nifty_fut','35075','2024-09-04 13:47:00','51650.0','51655.0','51647.0','51650.0'),(5850,'bank_nifty_fut','35075','2024-09-04 13:48:00','51650.0','51654.0','51647.95','51654.0'),(5851,'bank_nifty_fut','35075','2024-09-04 13:49:00','51654.0','51668.0','51649.0','51667.0'),(5852,'bank_nifty_fut','35075','2024-09-04 13:50:00','51666.35','51668.0','51660.0','51661.0'),(5853,'bank_nifty_fut','35075','2024-09-04 13:51:00','51667.5','51672.7','51660.0','51668.9'),(5854,'bank_nifty_fut','35075','2024-09-04 13:52:00','51664.35','51675.0','51661.0','51661.0'),(5855,'bank_nifty_fut','35075','2024-09-04 13:53:00','51661.0','51668.25','51652.25','51656.35'),(5856,'bank_nifty_fut','35075','2024-09-04 13:54:00','51662.8','51665.0','51653.75','51664.0'),(5857,'bank_nifty_fut','35075','2024-09-04 13:55:00','51665.0','51665.0','51652.55','51652.55'),(5858,'bank_nifty_fut','35075','2024-09-04 13:56:00','51652.4','51666.3','51652.0','51657.4'),(5859,'bank_nifty_fut','35075','2024-09-04 13:57:00','51665.4','51667.75','51652.25','51662.25'),(5860,'bank_nifty_fut','35075','2024-09-04 13:58:00','51661.0','51667.65','51653.0','51658.35'),(5861,'bank_nifty_fut','35075','2024-09-04 13:59:00','51659.0','51667.1','51653.75','51658.15'),(5862,'bank_nifty_fut','35075','2024-09-04 14:00:00','51658.7','51677.0','51658.7','51667.95'),(5863,'bank_nifty_fut','35075','2024-09-04 14:01:00','51676.6','51678.95','51666.1','51666.1'),(5864,'bank_nifty_fut','35075','2024-09-04 14:02:00','51668.2','51678.15','51666.4','51667.4'),(5865,'bank_nifty_fut','35075','2024-09-04 14:03:00','51667.4','51679.0','51663.25','51669.7'),(5866,'bank_nifty_fut','35075','2024-09-04 14:04:00','51670.0','51677.35','51667.3','51669.05'),(5867,'bank_nifty_fut','35075','2024-09-04 14:05:00','51670.65','51678.0','51665.45','51674.4'),(5868,'bank_nifty_fut','35075','2024-09-04 14:06:00','51676.0','51676.6','51667.15','51675.45'),(5869,'bank_nifty_fut','35075','2024-09-04 14:07:00','51667.1','51674.7','51644.6','51644.6'),(5870,'bank_nifty_fut','35075','2024-09-04 14:08:00','51654.9','51667.05','51648.45','51660.0'),(5871,'bank_nifty_fut','35075','2024-09-04 14:09:00','51665.65','51666.0','51654.85','51660.0'),(5872,'bank_nifty_fut','35075','2024-09-04 14:10:00','51664.3','51673.75','51663.4','51671.75'),(5873,'bank_nifty_fut','35075','2024-09-04 14:11:00','51668.3','51668.65','51660.35','51663.3'),(5874,'bank_nifty_fut','35075','2024-09-04 14:12:00','51663.45','51663.45','51660.0','51660.9'),(5875,'bank_nifty_fut','35075','2024-09-04 14:13:00','51664.7','51664.85','51652.65','51661.85'),(5876,'bank_nifty_fut','35075','2024-09-04 14:14:00','51657.6','51659.95','51646.85','51657.1'),(5877,'bank_nifty_fut','35075','2024-09-04 14:15:00','51647.7','51660.95','51647.7','51653.25'),(5878,'bank_nifty_fut','35075','2024-09-04 14:16:00','51659.3','51663.25','51647.0','51649.8'),(5879,'bank_nifty_fut','35075','2024-09-04 14:17:00','51659.65','51659.65','51645.75','51658.65'),(5880,'bank_nifty_fut','35075','2024-09-04 14:18:00','51658.0','51659.05','51646.85','51659.05'),(5881,'bank_nifty_fut','35075','2024-09-04 14:19:00','51658.25','51658.25','51620.35','51623.7'),(5882,'bank_nifty_fut','35075','2024-09-04 14:20:00','51621.25','51638.1','51620.5','51635.4'),(5883,'bank_nifty_fut','35075','2024-09-04 14:21:00','51630.0','51636.6','51623.35','51635.0'),(5884,'bank_nifty_fut','35075','2024-09-04 14:22:00','51628.05','51649.0','51628.05','51638.0'),(5885,'bank_nifty_fut','35075','2024-09-04 14:23:00','51647.55','51657.7','51637.85','51641.0'),(5886,'bank_nifty_fut','35075','2024-09-04 14:24:00','51640.95','51651.15','51637.2','51644.0'),(5887,'bank_nifty_fut','35075','2024-09-04 14:25:00','51640.0','51650.0','51637.5','51640.3'),(5888,'bank_nifty_fut','35075','2024-09-04 14:26:00','51640.0','51651.1','51639.35','51649.8'),(5889,'bank_nifty_fut','35075','2024-09-04 14:27:00','51641.05','51651.0','51640.45','51648.0'),(5890,'bank_nifty_fut','35075','2024-09-04 14:28:00','51642.7','51650.0','51642.35','51650.0'),(5891,'bank_nifty_fut','35075','2024-09-04 14:29:00','51649.5','51651.35','51639.0','51639.05'),(5892,'bank_nifty_fut','35075','2024-09-04 14:30:00','51639.05','51646.4','51639.0','51640.0'),(5893,'bank_nifty_fut','35075','2024-09-04 14:31:00','51641.0','51641.5','51628.05','51638.0'),(5894,'bank_nifty_fut','35075','2024-09-04 14:32:00','51633.0','51647.95','51630.2','51647.95'),(5895,'bank_nifty_fut','35075','2024-09-04 14:33:00','51648.0','51649.2','51637.0','51637.0'),(5896,'bank_nifty_fut','35075','2024-09-04 14:34:00','51640.0','51644.9','51631.0','51631.0'),(5897,'bank_nifty_fut','35075','2024-09-04 14:35:00','51633.05','51646.95','51631.4','51646.05'),(5898,'bank_nifty_fut','35075','2024-09-04 14:36:00','51646.2','51655.0','51640.05','51655.0'),(5899,'bank_nifty_fut','35075','2024-09-04 14:37:00','51655.0','51666.25','51645.0','51663.9'),(5900,'bank_nifty_fut','35075','2024-09-04 14:38:00','51653.6','51664.6','51648.85','51657.3'),(5901,'bank_nifty_fut','35075','2024-09-04 14:39:00','51646.4','51657.55','51644.65','51654.4'),(5902,'bank_nifty_fut','35075','2024-09-04 14:40:00','51654.9','51664.0','51646.05','51654.5'),(5903,'bank_nifty_fut','35075','2024-09-04 14:41:00','51660.15','51668.65','51652.25','51668.65'),(5904,'bank_nifty_fut','35075','2024-09-04 14:42:00','51668.8','51677.4','51657.1','51660.2'),(5905,'bank_nifty_fut','35075','2024-09-05 14:44:00','51705.1','51712.0','51701.0','51703.65'),(5906,'bank_nifty_fut','35075','2024-09-05 14:44:00','51705.1','51712.0','51701.0','51703.65'),(5907,'bank_nifty_fut','35075','2024-09-06 09:18:00','51561.3','51565.95','51544.9','51551.2'),(5908,'bank_nifty_fut','35075','2024-09-06 09:19:00','51549.1','51549.8','51521.2','51525.2'),(5909,'bank_nifty_fut','35075','2024-09-06 09:20:00','51529.95','51533.05','51505.5','51525.5'),(5910,'bank_nifty_fut','35075','2024-09-06 09:21:00','51522.55','51548.35','51516.0','51542.9'),(5911,'bank_nifty_fut','35075','2024-09-06 09:22:00','51545.0','51549.0','51530.55','51548.0'),(5912,'bank_nifty_fut','35075','2024-09-06 09:23:00','51548.0','51550.0','51514.0','51522.3'),(5913,'bank_nifty_fut','35075','2024-09-06 09:24:00','51522.85','51523.0','51511.0','51516.05'),(5914,'bank_nifty_fut','35075','2024-09-06 09:25:00','51516.05','51530.35','51510.0','51524.0'),(5915,'bank_nifty_fut','35075','2024-09-06 09:26:00','51520.2','51537.3','51520.2','51534.0'),(5916,'bank_nifty_fut','35075','2024-09-06 09:27:00','51537.7','51540.0','51512.0','51519.9'),(5917,'bank_nifty_fut','35075','2024-09-06 09:28:00','51519.9','51570.0','51516.9','51564.25'),(5918,'bank_nifty_fut','35075','2024-09-06 09:29:00','51565.2','51585.15','51551.0','51560.5'),(5919,'bank_nifty_fut','35075','2024-09-06 09:30:00','51564.1','51576.0','51550.0','51562.75'),(5920,'bank_nifty_fut','35075','2024-09-06 09:31:00','51566.85','51581.0','51561.2','51581.0'),(5921,'bank_nifty_fut','35075','2024-09-06 09:32:00','51578.0','51582.9','51570.0','51575.0'),(5922,'bank_nifty_fut','35075','2024-09-06 09:33:00','51573.8','51576.45','51550.0','51555.0'),(5923,'bank_nifty_fut','35075','2024-09-06 09:15:00','51530.0','51670.0','51530.0','51590.0'),(5924,'bank_nifty_fut','35075','2024-09-06 10:25:00','51222.0','51222.0','51222.0','51222.0'),(5925,'bank_nifty_fut','35075','2024-09-06 10:28:00','51200.0','51200.0','51200.0','51200.0'),(5926,'bank_nifty_fut','35075','2024-09-06 10:29:00','51224.8','51224.8','51224.8','51224.8'),(5927,'bank_nifty_fut','35075','2024-09-06 10:30:00','51249.8','51249.8','51248.0','51248.0'),(5928,'bank_nifty_fut','35075','2024-09-06 10:31:00','51236.0','51236.0','51236.0','51236.0'),(5929,'bank_nifty_fut','35075','2024-09-06 10:32:00','51217.5','51217.5','51217.5','51217.5'),(5930,'bank_nifty_fut','35075','2024-09-06 10:33:00','51236.15','51236.15','51236.15','51236.15'),(5931,'bank_nifty_fut','35075','2024-09-06 10:39:00','51150.0','51150.0','51150.0','51150.0'),(5932,'bank_nifty_fut','35075','2024-09-06 10:41:00','51170.8','51175.3','51153.45','51160.95'),(5933,'bank_nifty_fut','35075','2024-09-06 10:42:00','51156.0','51167.6','51150.0','51156.5'),(5934,'bank_nifty_fut','35075','2024-09-06 10:43:00','51156.5','51176.55','51148.0','51166.85'),(5935,'bank_nifty_fut','35075','2024-09-06 10:44:00','51166.4','51183.15','51148.95','51152.45'),(5936,'bank_nifty_fut','35075','2024-09-06 10:45:00','51160.55','51165.4','51133.1','51133.1'),(5937,'bank_nifty_fut','35075','2024-09-06 10:46:00','51136.05','51136.1','51110.0','51110.0'),(5938,'bank_nifty_fut','35075','2024-09-06 10:47:00','51115.0','51144.1','51110.0','51138.75'),(5939,'bank_nifty_fut','35075','2024-09-06 10:48:00','51138.0','51147.6','51133.4','51140.0'),(5940,'bank_nifty_fut','35075','2024-09-06 10:49:00','51146.5','51159.6','51143.4','51151.35'),(5941,'bank_nifty_fut','35075','2024-09-06 10:50:00','51159.0','51162.65','51140.7','51150.0'),(5942,'bank_nifty_fut','35075','2024-09-06 10:51:00','51150.0','51175.0','51145.0','51175.0'),(5943,'bank_nifty_fut','35075','2024-09-06 10:52:00','51170.0','51187.95','51167.4','51185.0'),(5944,'bank_nifty_fut','35075','2024-09-06 10:53:00','51177.0','51199.0','51170.75','51185.25'),(5945,'bank_nifty_fut','35075','2024-09-06 10:54:00','51186.45','51194.3','51176.0','51180.0'),(5946,'bank_nifty_fut','35075','2024-09-06 10:55:00','51179.4','51184.85','51155.35','51158.65'),(5947,'bank_nifty_fut','35075','2024-09-06 10:56:00','51160.0','51173.55','51160.0','51165.65'),(5948,'bank_nifty_fut','35075','2024-09-06 10:57:00','51168.1','51188.95','51165.45','51182.0'),(5949,'bank_nifty_fut','35075','2024-09-06 10:58:00','51189.95','51199.0','51182.0','51199.0'),(5950,'bank_nifty_fut','35075','2024-09-06 10:59:00','51196.0','51205.9','51151.0','51151.75'),(5951,'bank_nifty_fut','35075','2024-09-06 11:00:00','51151.0','51161.8','51145.0','51146.95'),(5952,'bank_nifty_fut','35075','2024-09-06 11:01:00','51146.1','51155.7','51142.9','51145.1'),(5953,'bank_nifty_fut','35075','2024-09-06 11:02:00','51145.3','51150.0','51120.0','51124.3'),(5954,'bank_nifty_fut','35075','2024-09-06 11:03:00','51120.0','51138.1','51113.3','51124.7'),(5955,'bank_nifty_fut','35075','2024-09-06 11:04:00','51124.7','51150.0','51120.45','51139.7'),(5956,'bank_nifty_fut','35075','2024-09-06 11:05:00','51139.85','51140.55','51125.0','51131.95'),(5957,'bank_nifty_fut','35075','2024-09-06 11:06:00','51136.15','51147.4','51126.0','51137.9'),(5958,'bank_nifty_fut','35075','2024-09-06 11:07:00','51130.6','51148.95','51126.05','51147.1'),(5959,'bank_nifty_fut','35075','2024-09-06 11:08:00','51145.25','51150.0','51126.0','51126.0'),(5960,'bank_nifty_fut','35075','2024-09-06 11:09:00','51133.1','51137.4','51106.0','51107.0'),(5961,'bank_nifty_fut','35075','2024-09-06 11:10:00','51106.05','51111.0','51075.0','51085.0'),(5962,'bank_nifty_fut','35075','2024-09-06 11:11:00','51084.8','51130.75','51084.8','51119.7'),(5963,'bank_nifty_fut','35075','2024-09-06 11:12:00','51119.75','51123.9','51085.0','51098.45'),(5964,'bank_nifty_fut','35075','2024-09-06 11:13:00','51091.6','51121.1','51091.55','51120.9'),(5965,'bank_nifty_fut','35075','2024-09-06 11:14:00','51123.55','51125.2','51097.0','51100.0'),(5966,'bank_nifty_fut','35075','2024-09-06 11:15:00','51097.0','51116.65','51091.0','51115.85'),(5967,'bank_nifty_fut','35075','2024-09-06 11:16:00','51107.2','51131.9','51104.7','51130.0'),(5968,'bank_nifty_fut','35075','2024-09-06 11:17:00','51130.0','51130.0','51110.8','51125.0'),(5969,'bank_nifty_fut','35075','2024-09-06 11:18:00','51125.0','51130.0','51115.55','51121.75'),(5970,'bank_nifty_fut','35075','2024-09-06 11:19:00','51121.0','51140.0','51120.0','51125.15'),(5971,'bank_nifty_fut','35075','2024-09-06 11:20:00','51125.2','51134.45','51115.6','51131.0'),(5972,'bank_nifty_fut','35075','2024-09-06 11:21:00','51130.0','51134.95','51121.0','51131.25'),(5973,'bank_nifty_fut','35075','2024-09-06 11:22:00','51131.25','51142.0','51120.05','51122.3'),(5974,'bank_nifty_fut','35075','2024-09-06 11:23:00','51131.9','51136.0','51118.7','51118.7'),(5975,'bank_nifty_fut','35075','2024-09-06 11:24:00','51120.0','51135.85','51115.6','51115.6'),(5976,'bank_nifty_fut','35075','2024-09-06 11:25:00','51113.05','51128.25','51088.0','51088.6'),(5977,'bank_nifty_fut','35075','2024-09-06 11:26:00','51094.5','51096.15','51077.9','51088.5'),(5978,'bank_nifty_fut','35075','2024-09-06 11:27:00','51089.3','51091.95','51070.0','51070.0'),(5979,'bank_nifty_fut','35075','2024-09-06 11:28:00','51070.0','51075.0','51040.0','51049.0'),(5980,'bank_nifty_fut','35075','2024-09-06 11:29:00','51046.0','51085.0','51040.6','51085.0'),(5981,'bank_nifty_fut','35075','2024-09-06 11:30:00','51083.15','51097.15','51076.15','51085.35'),(5982,'bank_nifty_fut','35075','2024-09-06 11:31:00','51082.75','51096.45','51061.0','51061.0'),(5983,'bank_nifty_fut','35075','2024-09-06 11:32:00','51060.2','51078.25','51057.5','51058.65'),(5984,'bank_nifty_fut','35075','2024-09-06 11:33:00','51060.05','51076.0','51057.15','51066.25'),(5985,'bank_nifty_fut','35075','2024-09-06 11:34:00','51069.95','51099.0','51065.9','51097.4'),(5986,'bank_nifty_fut','35075','2024-09-06 11:35:00','51093.05','51117.35','51088.7','51106.15'),(5987,'bank_nifty_fut','35075','2024-09-06 11:36:00','51107.3','51108.7','51091.65','51099.7'),(5988,'bank_nifty_fut','35075','2024-09-06 11:37:00','51100.95','51112.0','51087.2','51112.0'),(5989,'bank_nifty_fut','35075','2024-09-06 11:38:00','51117.05','51139.0','51101.65','51135.95'),(5990,'bank_nifty_fut','35075','2024-09-06 11:39:00','51127.2','51136.8','51113.3','51116.7'),(5991,'bank_nifty_fut','35075','2024-09-06 11:40:00','51124.75','51137.05','51117.4','51122.2'),(5992,'bank_nifty_fut','35075','2024-09-06 11:41:00','51122.2','51127.75','51100.05','51106.0'),(5993,'bank_nifty_fut','35075','2024-09-06 11:42:00','51115.1','51115.1','51099.0','51104.0'),(5994,'bank_nifty_fut','35075','2024-09-06 11:43:00','51104.0','51122.55','51104.0','51115.7'),(5995,'bank_nifty_fut','35075','2024-09-06 11:44:00','51110.0','51122.2','51100.75','51115.0'),(5996,'bank_nifty_fut','35075','2024-09-06 11:45:00','51115.0','51132.95','51110.0','51130.0'),(5997,'bank_nifty_fut','35075','2024-09-06 11:46:00','51130.0','51140.35','51121.15','51125.0'),(5998,'bank_nifty_fut','35075','2024-09-06 11:47:00','51130.0','51133.15','51110.0','51116.85'),(5999,'bank_nifty_fut','35075','2024-09-06 11:48:00','51105.65','51116.2','51103.0','51116.2'),(6000,'bank_nifty_fut','35075','2024-09-06 11:49:00','51109.55','51132.3','51109.55','51129.6'),(6001,'bank_nifty_fut','35075','2024-09-06 11:50:00','51131.9','51131.9','51120.35','51130.75'),(6002,'bank_nifty_fut','35075','2024-09-06 11:51:00','51131.95','51141.55','51122.0','51134.6'),(6003,'bank_nifty_fut','35075','2024-09-06 11:52:00','51134.6','51146.1','51123.45','51142.05'),(6004,'bank_nifty_fut','35075','2024-09-06 13:43:00','50996.55','50997.25','50986.0','50989.7'),(6005,'bank_nifty_fut','35075','2024-09-06 13:44:00','50988.05','51006.2','50985.0','51003.1');
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
  `status` varchar(250) NOT NULL,
  `strike` varchar(5) NOT NULL,
  `lots` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_configuration`
--

LOCK TABLES `plutusAI_configuration` WRITE;
/*!40000 ALTER TABLE `plutusAI_configuration` DISABLE KEYS */;
INSERT INTO `plutusAI_configuration` VALUES (1,'nifty','10',1,'3','10','10','15','25200,25500,24774,24500,25000,24300,24100,24000,23800,23500,23000','antonyrajan.d@gmail.com',0,'stopped','50','1'),(2,'bank_nifty','50',1,'10','30','5','20','50500,50400,50300,50200,50100,50000,49900,49800,49700,49600,49500,49400,49300,49200,49100,49000,50600,50700,50800,50900,51000,51100,51200,51300,51400,51500,51600,51700,51800,51900,52000,52500,53000,49000,48500,48000','antonyrajan.d@gmail.com',0,'stopped','100','1'),(3,'fin_nifty','10',1,'10','10','10','15','23300,23400,23500,23600,23200,23200,23100,23000','antonyrajan.d@gmail.com',0,'stopped','50','10'),(4,'nifty','10',1,'10','10','10','15','25120,25075,25133,24884,25015,24760,24806,25180,2540','kamezwaran.r@gmail.com',0,'stopped','100','6'),(5,'bank_nifty','30',1,'10','30','20','50','51268,51391,51143,51484,51034,50886,50750','kamezwaran.r@gmail.com',0,'stopped','10','10'),(6,'fin_nifty','10',1,'10','10','10','15','23400,23306,23478,23215,23139','kamezwaran.r@gmail.com',0,'stopped','10','10');
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_indexdetails`
--

LOCK TABLES `plutusAI_indexdetails` WRITE;
/*!40000 ALTER TABLE `plutusAI_indexdetails` DISABLE KEYS */;
INSERT INTO `plutusAI_indexdetails` VALUES (1,'nifty','indian_index','25235.9','99926000','2024-08-31 09:02:25','25','12-SEP-2024','19-SEP-2024'),(2,'bank_nifty','indian_index','51351.0','99926009','2024-08-31 09:02:23','15','11-SEP-2024','18-SEP-2024'),(3,'fin_nifty','indian_index','23637.9','99926037','2024-08-31 09:02:24','40','10-SEP-2024','17-SEP-2024'),(5,'bank_nifty_fut','indian_index','51000.05','35075','2024-09-06 13:45:52','15','16-JUL-2024','16-JUL-2024');
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
) ENGINE=InnoDB AUTO_INCREMENT=1065 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_jobdetails`
--

LOCK TABLES `plutusAI_jobdetails` WRITE;
/*!40000 ALTER TABLE `plutusAI_jobdetails` DISABLE KEYS */;
/*!40000 ALTER TABLE `plutusAI_jobdetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plutusAI_manualorders`
--

DROP TABLE IF EXISTS `plutusAI_manualorders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plutusAI_manualorders` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` varchar(100) NOT NULL,
  `index_name` varchar(100) NOT NULL,
  `target` varchar(100) NOT NULL,
  `stop_loss` varchar(100) NOT NULL,
  `order_status` varchar(100) NOT NULL,
  `time` varchar(100) NOT NULL,
  `is_demo_trading_enabled` tinyint(1) NOT NULL,
  `strike` varchar(100) NOT NULL,
  `lots` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_manualorders`
--

LOCK TABLES `plutusAI_manualorders` WRITE;
/*!40000 ALTER TABLE `plutusAI_manualorders` DISABLE KEYS */;
INSERT INTO `plutusAI_manualorders` VALUES (1,'antonyrajan.d@gmail.com','nifty','10','10','order_placed','123',1,'100','1'),(2,'antonyrajan.d@gmail.com','bank_nifty','10','10','order_placed','123',1,'200','1');
/*!40000 ALTER TABLE `plutusAI_manualorders` ENABLE KEYS */;
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
  `entry_time` varchar(500) NOT NULL,
  `script_name` varchar(250) NOT NULL,
  `qty` varchar(250) NOT NULL,
  `entry_price` varchar(250) NOT NULL,
  `exit_price` varchar(250) DEFAULT NULL,
  `status` varchar(250) NOT NULL,
  `exit_time` varchar(500) DEFAULT NULL,
  `total` varchar(250) DEFAULT NULL,
  `strategy` varchar(250) DEFAULT NULL,
  `index_name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=916 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_orderbook`
--

LOCK TABLES `plutusAI_orderbook` WRITE;
/*!40000 ALTER TABLE `plutusAI_orderbook` DISABLE KEYS */;
INSERT INTO `plutusAI_orderbook` VALUES (908,'antonyrajan.d@gmail.com','1725439981.805565','BANKNIFTY04SEP2451200CE','15','210.0','224.0','order_exited','1725440014.645099','210.0','scalper','bank_nifty'),(909,'antonyrajan.d@gmail.com','1725594601.714614','BANKNIFTY11SEP2451500PE','15','374.85','345.45','order_exited','1725595109.633988','-441.0000000000005','hunter','bank_nifty'),(910,'antonyrajan.d@gmail.com','1725595110.627988','BANKNIFTY11SEP2451100CE','15','433.25','426.4','order_exited','1725595192.428107','-102.75000000000034','hunter','bank_nifty'),(911,'antonyrajan.d@gmail.com','1725595193.378733','BANKNIFTY11SEP2451500PE','15','345.0','339.45','order_exited','1725595197.4008','-83.25000000000017','hunter','bank_nifty'),(912,'antonyrajan.d@gmail.com','1725595198.339857','BANKNIFTY11SEP2451100CE','15','434.8','427.85','order_exited','1725595234.776761','-104.24999999999983','hunter','bank_nifty'),(913,'antonyrajan.d@gmail.com','1725595235.799671','BANKNIFTY11SEP2451500PE','15','345.65','344.4','order_exited','1725595239.740364','-18.75','hunter','bank_nifty'),(914,'antonyrajan.d@gmail.com','1725595240.739912','BANKNIFTY11SEP2451100CE','15','428.45',NULL,'order_placed',NULL,NULL,'hunter','bank_nifty'),(915,'antonyrajan.d@gmail.com','1725610501.407059','BANKNIFTY11SEP2450600CE','15','433.65',NULL,'order_placed',NULL,NULL,'scalper','bank_nifty');
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
  `on_candle_close` tinyint(1) NOT NULL,
  `status` varchar(250) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_scalperdetails`
--

LOCK TABLES `plutusAI_scalperdetails` WRITE;
/*!40000 ALTER TABLE `plutusAI_scalperdetails` DISABLE KEYS */;
INSERT INTO `plutusAI_scalperdetails` VALUES (3,'kamezwaran.r@gmail.com','bank_nifty','200',0,0,'15','1',0,'stopped'),(4,'antonyrajan.d@gmail.com','bank_nifty','200',1,0,'15','1',0,'stopped');
/*!40000 ALTER TABLE `plutusAI_scalperdetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plutusAI_userauthtokens`
--

DROP TABLE IF EXISTS `plutusAI_userauthtokens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plutusAI_userauthtokens` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` varchar(500) NOT NULL,
  `refreshToken` varchar(2000) NOT NULL,
  `feedToken` varchar(2000) NOT NULL,
  `last_updated_time` varchar(500) NOT NULL,
  `jwtToken` varchar(2000) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_userauthtokens`
--

LOCK TABLES `plutusAI_userauthtokens` WRITE;
/*!40000 ALTER TABLE `plutusAI_userauthtokens` DISABLE KEYS */;
INSERT INTO `plutusAI_userauthtokens` VALUES (9,'antonyrajan.d@gmail.com','eyJhbGciOiJIUzUxMiJ9.eyJ0b2tlbiI6IlJFRlJFU0gtVE9LRU4iLCJSRUZSRVNILVRPS0VOIjoiZXlKaGJHY2lPaUpTVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5WDNSNWNHVWlPaUpqYkdsbGJuUWlMQ0owYjJ0bGJsOTBlWEJsSWpvaWRISmhaR1ZmY21WbWNtVnphRjkwYjJ0bGJpSXNJbWR0WDJsa0lqb3dMQ0prWlhacFkyVmZhV1FpT2lJNE9UZ3lObU14TWkxaU1EaGtMVE0yTVRVdE9UTTVZaTFpTXpWbE56SmhOMlUzTUdNaUxDSnJhV1FpT2lKMGNtRmtaVjlyWlhsZmRqRWlMQ0p2Ylc1bGJXRnVZV2RsY21sa0lqb3dMQ0pwYzNNaU9pSnNiMmRwYmw5elpYSjJhV05sSWl3aWMzVmlJam9pUVRVNE1ETXpORGszSWl3aVpYaHdJam94TnpJMU56Z3pNVGsxTENKdVltWWlPakUzTWpVMk1UQXpNelVzSW1saGRDSTZNVGN5TlRZeE1ETXpOU3dpYW5ScElqb2lORE0wTlROaVlqa3RPREExTUMwME9ETmpMV0V3WVRjdE56Wm1NR001WmpZd1l6VXhJbjAuWFBaa2dCZ21FaUVJMzNKcEtycndKQjU5X0RiOW42R1YydHJ1WGlOXzRRWVZnakgyck9uWFpROTNEa1B0ZXk0VnVnSlNjMTJjUlJqcF90cWtJNmhIYUU2eG9rNDl5REw4ZmpHRHdrRHowc18ta1ZDcVp5STFmN0ZESXBEMDFnY21iU19ha3E5cVZCSWpmVXBQTjUtUkVYeEd6N294bjQ4ekZ4S3lxNGpTVmdRIiwiaWF0IjoxNzI1NjEwMzk1fQ.iQrc7OPdF62h6Dv1AabAn348BhnYIrxYrcpyZtUowwB3Kf4k2zRVRFIjpDFojM1KU2QHYvCJfq3Qyk0mm8ckcA','eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6IkE1ODAzMzQ5NyIsImlhdCI6MTcyNTYxMDM5NSwiZXhwIjoxNzI1Njk2Nzk1fQ.9xVlZ548kC85B93sZNo7m90ihWN1mHqE8BGuqy1cc9AzUYnBDTcwKJFSO-3xVYBGlp0z6ytuMqIGBbQWEAzp1Q','1725610396.051771','eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6IkE1ODAzMzQ5NyIsInJvbGVzIjowLCJ1c2VydHlwZSI6IlVTRVIiLCJ0b2tlbiI6ImV5SmhiR2NpT2lKU1V6STFOaUlzSW5SNWNDSTZJa3BYVkNKOS5leUoxYzJWeVgzUjVjR1VpT2lKamJHbGxiblFpTENKMGIydGxibDkwZVhCbElqb2lkSEpoWkdWZllXTmpaWE56WDNSdmEyVnVJaXdpWjIxZmFXUWlPallzSW5OdmRYSmpaU0k2SWpNaUxDSmtaWFpwWTJWZmFXUWlPaUk0T1RneU5tTXhNaTFpTURoa0xUTTJNVFV0T1RNNVlpMWlNelZsTnpKaE4yVTNNR01pTENKcmFXUWlPaUowY21Ga1pWOXJaWGxmZGpFaUxDSnZiVzVsYldGdVlXZGxjbWxrSWpvMkxDSndjbTlrZFdOMGN5STZleUprWlcxaGRDSTZleUp6ZEdGMGRYTWlPaUpoWTNScGRtVWlmWDBzSW1semN5STZJblJ5WVdSbFgyeHZaMmx1WDNObGNuWnBZMlVpTENKemRXSWlPaUpCTlRnd016TTBPVGNpTENKbGVIQWlPakUzTWpVM01EUTJNRElzSW01aVppSTZNVGN5TlRZeE1ETXpOU3dpYVdGMElqb3hOekkxTmpFd016TTFMQ0pxZEdraU9pSTBOV1UyWW1Ga01TMDNaVGc1TFRRNE16WXRZbUV3TkMwd01tRm1ZMlpqTnpBMk1Ea2lmUS5GSTYxME1oNklMb2ZPZndlc1Njc0R1VF9KTGF6dlRqNHh2RXJ0Tm5LaTRpMnJIS2tBcWo2TG8yT3dxU1JvMWp1LVpCZF9CekpjTE1oRWk0Z0JSQjh3QzRWTDAxSGYwVnRSMVpWUklFSnVLSi1sWVFIdmk0QmREOFg2bXBsUHJlcUx4eUNRaTU1OF8zN1g5T2xuLUdXZUd0WWhqNE4xcEMwcE1pNGl4dlBWWTQiLCJBUEktS0VZIjoicE9ydXhMWVoiLCJpYXQiOjE3MjU2MTAzOTUsImV4cCI6MTcyNTcwNDYwMn0.1fyC6XGa4Z1NVXUF1YLjRXWuIZmVoxfgyln3YlGzVtsxXPuZWFfcLG1sfo_Cyl1EjFsNHv0eTM81xnI7cmOldw'),(10,'madara@plutus.com','eyJhbGciOiJIUzUxMiJ9.eyJ0b2tlbiI6IlJFRlJFU0gtVE9LRU4iLCJSRUZSRVNILVRPS0VOIjoiZXlKaGJHY2lPaUpTVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5WDNSNWNHVWlPaUpqYkdsbGJuUWlMQ0owYjJ0bGJsOTBlWEJsSWpvaWRISmhaR1ZmY21WbWNtVnphRjkwYjJ0bGJpSXNJbWR0WDJsa0lqb3dMQ0prWlhacFkyVmZhV1FpT2lJME9ERTRZVFEwT1MxaU9EbGhMVE0wWWpFdE9Ea3hOUzAzWVdJNU4ySTFOR1E0TlRVaUxDSnJhV1FpT2lKMGNtRmtaVjlyWlhsZmRqRWlMQ0p2Ylc1bGJXRnVZV2RsY21sa0lqb3dMQ0pwYzNNaU9pSnNiMmRwYmw5elpYSjJhV05sSWl3aWMzVmlJam9pVXpVd056WXhOREE1SWl3aVpYaHdJam94TnpJMU56WTJNVGsxTENKdVltWWlPakUzTWpVMU9UTXpNelVzSW1saGRDSTZNVGN5TlRVNU16TXpOU3dpYW5ScElqb2lNalJrWkRBNU1qSXRNakJsTnkwME0yUTVMV0ZpTldJdFpEZzFNemxtT1dJM1lqSmxJbjAubHplNHJpOFJnU3lYVlRNeTlqRUpXaFotU2taRldkS2J0UUd5TXpfOG5IbWFwVk1OU2hMSnFsY2tZUEc1cHRxNFA5TGJscm9XV2NpcGY0RXBKNk42OWZmLXFfbEZkMnVkTjVUVnJDWXY1SU9vUE1POExkdnZCUHdmY01PY3hLOXJlZFRReE9mc25BWTRRcUNnNXZ5dHA2Tmt1UGpSVk1Ibm5vLV80VVJVei1vIiwiaWF0IjoxNzI1NTkzMzk1fQ.RD4tZ5yQSnrT2XeE4EeoyTgyANwOimAEI40O0VZeUuRC0MssYjDrpJCAcMy0Mv2XCcK_rt7cELOBFISOoKJZIg','eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6IlM1MDc2MTQwOSIsImlhdCI6MTcyNTU5MzM5NSwiZXhwIjoxNzI1Njc5Nzk1fQ.mp180FbFeYBmhdQsJGNRzHZEfhBHmSuqWOkiclHTjnS3O76nC04XglvjUE5bYcNVpd7O3x6JUtX4SHiz-4SEHA','1725593394.400224','eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6IlM1MDc2MTQwOSIsInJvbGVzIjowLCJ1c2VydHlwZSI6IlVTRVIiLCJ0b2tlbiI6ImV5SmhiR2NpT2lKU1V6STFOaUlzSW5SNWNDSTZJa3BYVkNKOS5leUoxYzJWeVgzUjVjR1VpT2lKamJHbGxiblFpTENKMGIydGxibDkwZVhCbElqb2lkSEpoWkdWZllXTmpaWE56WDNSdmEyVnVJaXdpWjIxZmFXUWlPakV4TENKemIzVnlZMlVpT2lJeklpd2laR1YyYVdObFgybGtJam9pTkRneE9HRTBORGt0WWpnNVlTMHpOR0l4TFRnNU1UVXROMkZpT1RkaU5UUmtPRFUxSWl3aWEybGtJam9pZEhKaFpHVmZhMlY1WDNZeElpd2liMjF1WlcxaGJtRm5aWEpwWkNJNk1URXNJbkJ5YjJSMVkzUnpJanA3SW1SbGJXRjBJanA3SW5OMFlYUjFjeUk2SW1GamRHbDJaU0o5ZlN3aWFYTnpJam9pZEhKaFpHVmZiRzluYVc1ZmMyVnlkbWxqWlNJc0luTjFZaUk2SWxNMU1EYzJNVFF3T1NJc0ltVjRjQ0k2TVRjeU5UWTRPRGswTUN3aWJtSm1Jam94TnpJMU5Ua3pNek0xTENKcFlYUWlPakUzTWpVMU9UTXpNelVzSW1wMGFTSTZJbVl6TnpjME1tSXhMVGxtTlRndE5HVTFNUzA0WW1VM0xURXpOMll3TXpjelltUXlZU0o5LmJMa0MyVzJ1dFNLckppZFVzblJzZ2dyYzdWcXhKLTZZUUJjbDk3ZHd2WWlHSWhicU9wcmJxLXlDMFo0eE1taWJWcDUxZ0lvUWRBMjRkY2FzaEZtMUZUajBDWXpfcUR4TWZya2p2SlViOVRxdE56bFVLRkFXRlBRYjFRc0kyZnFGYjNBZ1N5RzhXOWRyanJlOWM3bUcySWlmclF2cmI1Z0lESlZYWnJwTUNWVSIsIkFQSS1LRVkiOiJRMTJmZUZqUiIsImlhdCI6MTcyNTU5MzM5NSwiZXhwIjoxNzI1Njg4OTQwfQ.wiR157xvvzeS4UitRnSJOA7hV1Xwy6g9g3umBdKyqQDWWoWRZdklww3ZwsbH0VilyPvEKTcM1Hez2-wcctRqaw'),(11,'kamezwaran.r@gmail.com','eyJhbGciOiJIUzUxMiJ9.eyJ0b2tlbiI6IlJFRlJFU0gtVE9LRU4iLCJSRUZSRVNILVRPS0VOIjoiZXlKaGJHY2lPaUpTVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5WDNSNWNHVWlPaUpqYkdsbGJuUWlMQ0owYjJ0bGJsOTBlWEJsSWpvaWRISmhaR1ZmY21WbWNtVnphRjkwYjJ0bGJpSXNJbWR0WDJsa0lqb3dMQ0prWlhacFkyVmZhV1FpT2lJNU9EVTBPR05tTkMweVpHVTVMVE15WVRZdE9UVXdaQzAwTlRnNFlURmtabVprWW1NaUxDSnJhV1FpT2lKMGNtRmtaVjlyWlhsZmRqRWlMQ0p2Ylc1bGJXRnVZV2RsY21sa0lqb3dMQ0pwYzNNaU9pSnNiMmRwYmw5elpYSjJhV05sSWl3aWMzVmlJam9pU3pZd09ERTBOamczSWl3aVpYaHdJam94TnpJMU5qZ3dOakEwTENKdVltWWlPakUzTWpVMU1EYzNORFFzSW1saGRDSTZNVGN5TlRVd056YzBOQ3dpYW5ScElqb2lOakF6TUdOaU1qUXRNVE14TWkwMFltUXdMV0ZtWm1JdE9EWXlNVFZrTlRZNE16bGhJbjAubFMwYXNjd1RlclM2YnZuT3JPYjFZTl9NbF9IOEJDX09hMnl5MndCTFh3VHQzMkJBbW9MMFJtc2ZGc3J3d1F3MlB2OFAtc2FzSi1yZm44RnBEaFZDbHhRU3pacWJWeEgtYUpKcmg3YkxEOE4ybW1LZS03SkVUS0lOTFZzNDBGNmFkTVhUVlkyVGdSU1V3aHc2dm9Wb3AtRncwNXNldDdWRFRPNkFSa05IM2NBIiwiaWF0IjoxNzI1NTA3ODA0fQ._qU6Z20TD1GgGgvsUIaIKF7JRdtz5QRMmP1_7qE_o2R4KyIi4z4zuNDxbSKitySdkiLjcySSOL9_lMcu-cw_Vw','eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6Iks2MDgxNDY4NyIsImlhdCI6MTcyNTUwNzgwNCwiZXhwIjoxNzI1NTk0MjA0fQ.dD4CpwZzPNAZA8LtkpRoDE469Gbe-TLcHsfgpko2mcrvJjdtUg-Aqkpl2TReAeLf91dZ6wCemmmiBZ5B2TCE0Q','1725507804.628934','eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6Iks2MDgxNDY4NyIsInJvbGVzIjowLCJ1c2VydHlwZSI6IlVTRVIiLCJ0b2tlbiI6ImV5SmhiR2NpT2lKU1V6STFOaUlzSW5SNWNDSTZJa3BYVkNKOS5leUoxYzJWeVgzUjVjR1VpT2lKamJHbGxiblFpTENKMGIydGxibDkwZVhCbElqb2lkSEpoWkdWZllXTmpaWE56WDNSdmEyVnVJaXdpWjIxZmFXUWlPamtzSW5OdmRYSmpaU0k2SWpNaUxDSmtaWFpwWTJWZmFXUWlPaUk1T0RVME9HTm1OQzB5WkdVNUxUTXlZVFl0T1RVd1pDMDBOVGc0WVRGa1ptWmtZbU1pTENKcmFXUWlPaUowY21Ga1pWOXJaWGxmZGpFaUxDSnZiVzVsYldGdVlXZGxjbWxrSWpvNUxDSndjbTlrZFdOMGN5STZleUprWlcxaGRDSTZleUp6ZEdGMGRYTWlPaUpoWTNScGRtVWlmWDBzSW1semN5STZJblJ5WVdSbFgyeHZaMmx1WDNObGNuWnBZMlVpTENKemRXSWlPaUpMTmpBNE1UUTJPRGNpTENKbGVIQWlPakUzTWpVMU9UVXlNellzSW01aVppSTZNVGN5TlRVd056YzBOQ3dpYVdGMElqb3hOekkxTlRBM056UTBMQ0pxZEdraU9pSTVZVEF3WWpVNVlTMDJPV016TFRSaE5XRXRZVEF6TVMwM1lUZzVNVE0yWWpVMU4ySWlmUS5tMlIyR01Xd3hzVjRkejNxSHB5M1k0bmYtZVo1YlllUDdaU3JCSnpZMGZfdlpSLVB3UlloVmxzWWZydjc4UUVHRThDM3ZFSEpVemZYbmdCbUJJRGVSWDdDMVVLdUM0NFdMaHdNVFRZY0t2YXd2R1dsUWRQc2tONU5jQXktSl85ME9YMlVFWlJ5c3NEQVd5b0oxRVhRRHlLcGZHSEN6ejhoc3ZabzZ1bUZnREEiLCJBUEktS0VZIjoiZlNlNWxjdm4iLCJpYXQiOjE3MjU1MDc4MDQsImV4cCI6MTcyNTU5NTIzNn0.eBbDmnglapkpbZFD7FVJJPJt5cm8HGlzpVtUdn-RecgLBzWe4BITRYn_ZfkmUanRIeJWxHvAHq-SwLYFw6T3Aw');
/*!40000 ALTER TABLE `plutusAI_userauthtokens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plutusAI_webhookdetails`
--

DROP TABLE IF EXISTS `plutusAI_webhookdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plutusAI_webhookdetails` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` varchar(100) NOT NULL,
  `index_name` varchar(100) NOT NULL,
  `target` varchar(100) NOT NULL,
  `order_status` varchar(100) NOT NULL,
  `time` varchar(100) NOT NULL,
  `is_demo_trading_enabled` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_webhookdetails`
--

LOCK TABLES `plutusAI_webhookdetails` WRITE;
/*!40000 ALTER TABLE `plutusAI_webhookdetails` DISABLE KEYS */;
/*!40000 ALTER TABLE `plutusAI_webhookdetails` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-06 22:28:16
