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
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$720000$TrRCp4ZEcCaTlJwjDlgH4n$bXk1dvyXOBkHUCj4N2oz2av/RSJgPbv2aSX+u6Z+Daw=','2024-08-12 02:53:57.227711',1,'admin','','','madara@plutus.com',1,1,'2024-06-15 12:09:57.133766'),(2,'pbkdf2_sha256$720000$su9jHjriTejd7pUVflaCpW$zYqJtpAqxjfNEVZEVupo4bhWZI2XlrAvdVoIugS7MM4=','2024-08-13 03:51:58.428175',0,'antonyrajan.d','antonyrajan.d','','antonyrajan.d@gmail.com',0,1,'2024-06-15 12:19:09.052744'),(3,'pbkdf2_sha256$720000$BYD9wX9N3J8WILz9MjGC6z$DfCzh7MD1ZGakOEJomrM5moIZ/SRUCK9InnXmnpOqbc=','2024-08-16 07:51:14.374919',0,'kamezwaran.r','kamezwaran.r','','kamezwaran.r@gmail.com',0,1,'2024-07-28 07:20:41.773660');
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
INSERT INTO `django_session` VALUES ('0s9rpf73rxz14csbt16p2j8mf5ebc4dv','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sXyQH:YZSbJcXnvPSM_k7HMEUDxqLA7glufY-3gllwmr0wl88','2024-08-11 07:34:29.248553'),('0tgkghfhwjufjpeca6zcnevhm4vs13mv','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sbAxG:WAZMRbWz_Rqp_HqFFJiUZdobAkBnHtQ3V1aYy6G4HP4','2024-08-20 03:33:46.715323'),('1w3rjocdrkbirb4emasru3uik7qbvyyx','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1serjM:fsm-zLDReKYxTbKVPkL_oZPI-dncMB4p0J3vCOVkWgU','2024-08-30 07:50:40.417272'),('22meergtgfz93dlpty8n7c776kl43e4a','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sYdYq:jWjfp6baoLCqvIUYSqVzzrdMXpKFHeYFj6nBZ4J772c','2024-08-13 03:30:04.744637'),('2cq14lo936z9aztyyumrp7uwron7xboc','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1safiv:KPN9Q-7hSCVelshneeFTNEAsjewpexbxOcj6oaZfIps','2024-08-18 18:12:53.886832'),('2y3j1qgxtrfo7qt8u9o9xy6gmozfj5jb','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sOqZg:L7UpklxZ8coWp1fxwexKp_k4U9iwVlO8G7f-an7RK1E','2024-07-17 03:22:28.848509'),('3k16xuy9ibvmbs1ocl5ya51n6uesedqd','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sadWd:WPu4aGq-eAhaKt-0k42SbJIBACo4CXkCOpWy0y0eOvU','2024-08-18 15:52:03.172785'),('4i7k3evdhzkw2bjbhzn67a5wvd11ni1k','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sISNf:rz6C4so4auNahvUBVexX7mUnT8Uh7NF_VZphUnIyTe0','2024-06-29 12:19:39.087860'),('4m1j6fdrk6vmqnaggkpn88oozfqfe16g','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sbXEP:wrQvxUMBW6OfKW0BDGly8VHPGBFY8mJgRx2FjWUPWE4','2024-08-21 03:20:57.984341'),('4yof7wloo7biyzeugedqgq2flun8r8u6','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1seqFE:gfXqVJCnJUlmzGHmgqmcz28xx_3HHiw-bstUAaE_FIw','2024-08-30 06:15:28.719113'),('5vqusqh8csab0gpd2ogpqew18ao6uuyv','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sXyTS:mZrCnpnct7Ctz3A88irumkRoNOuVdT3nR5AeRZIsSfw','2024-08-11 07:37:46.565746'),('6i37486jv28xlabgk1yi3hcpkgyjkf13','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sZMiy:nzLg2BISf-1YBn6EkbFaHAHc57cyxMxJ7qMBx-5YUbo','2024-08-15 03:43:32.696338'),('6nngtz4wagaqxu1oa3jv4j9ylvbsr63x','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sYGo4:I_yxjI7i9pNKqGLApPskiWFh6tme3ZlcWHABg0ALUVE','2024-08-12 03:12:16.679433'),('6rdjyy2cbjo65gihe3ui3ro0wy19atyn','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sYdnV:EhjoRVtlYSBUHfckMIszTYtakhw6SywuRVlrq0aatlU','2024-08-13 03:45:13.490252'),('7uc7j4si2miicm21c9uvlz9sp14pj9ry','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sbY0M:wZQK-_dQs2FkbfcqaNVFtO55hBscbs-MYZ2EjD7UKL0','2024-08-21 04:10:30.544311'),('9e71hcespj289zd07nkccivp4u9qn6f1','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sentO:o5GdteD_dTpN4fgMdSU3_Qkx9PIpCq6QkyEzFb6l2Ww','2024-08-30 03:44:46.725293'),('af182jkuc7thf5b1jpc1svx89mrwvae3','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sXhY7:8iuuAX_gHBW1nfiz8mHDCw8hfypJt0824jX2wq1Drlk','2024-08-10 13:33:27.166639'),('b7a9ll21yf3b9603vsq2kcsuhhh74v2l','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sbXSy:Q14LtQcp7ttr_5s-s4bUs9ZGVXEKeOfpks6eBFhM4F8','2024-08-21 03:36:00.908955'),('bdjy3no66rzpty31tuu9xnxh05z1x9cu','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sOqUz:OG5lpOn-rrIauTNOkGy_xFaOM7VbpreV11eo20DDUSQ','2024-07-17 03:17:37.045572'),('bmohkgrykvve8wy3xl90n6ws69ahohm6','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sYHWW:deS1LMeNLSF3_1m68ySOx4XVrGRLMBecqJ-AWJIwUJ8','2024-08-12 03:58:12.432809'),('br0qoe60vrg06x9f6xc3d6deo9ou89bt','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sdLuV:bfprFSaTlVlHWPo1e32wFSm4DVvfwFyc_15mMIhzT_s','2024-08-26 03:39:55.779148'),('c3rdv3rgah7wep5nb6mkhgzr390bu28q','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sZMgG:rTK-Va03VNTriv4DC38UVS82BfA85fsbTvJWeMOWDdk','2024-08-15 03:40:44.965916'),('c8pkgeiqed4lqtzdj653d5uwpoxy4w4c','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sbu2w:HHTqDJI6VHOQtGu0ie3X8ZfoxBR6Q6uAFkSk0UUsk4s','2024-08-22 03:42:38.201884'),('cheb4ei6u6q3e8syxl91z4jqi23ocyjo','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1se4nL:Sz6h4cQb02ZcuMtFFIGWwgHRUZqBek4kHHE1mSlkiws','2024-08-28 03:35:31.938597'),('clbko78uvh0hc30xbr0b2jihcluz900b','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sYJmR:g4I1iriY6EzXWO89vXo7BV4TaCznJkLlhCYSIcZNiMk','2024-08-12 06:22:47.940480'),('d86htw1tdqxj8f9149qydeuxstpnuqxj','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sZMpQ:NC8BpoCvG7BMSch6GTUtEtZUu4552mlr3TMvJ116QRE','2024-08-15 03:50:12.213207'),('dgp9cya2c4x2ymg5xejjf1lfqamjf6zl','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1serOH:YeSZKaDu_VAB1VEcHGbBkobO3jMhdtPSI1ye4x4P7E4','2024-08-30 07:28:53.296276'),('dte1a3alrd152yp95ey24yaaqdoq6k61','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sZj3z:YQ32lzVvr69hQNG749Cjdnz1ZP98Yei9sPMnXrrdobo','2024-08-16 03:34:43.736623'),('e7xtiz2ut1w0yucfu03vgrsbz4z05hc8','.eJxVjMsOwiAQRf-FtSEMjwIu3fcbyAyMUjU0Ke3K-O_apAvd3nPOfYmE21rT1nlJUxFnAeL0uxHmB7cdlDu22yzz3NZlIrkr8qBdjnPh5-Vw_w4q9vqtjQUqSpkcQUfGQNYYnSEzqODY2-KjxoEhKBc8KWs9XS37HHkghxTE-wPFnTdt:1sISEn:5nqopMDP56toJY3cYxaLEnijZ6ZUnr7qjgQaloiEvj4','2024-06-29 12:10:29.755173'),('einw0als4czb470uy10na8m0l83qnw6t','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sbXEQ:pvcMNK7qUwoZoG1hmTWBBHM4dyRUgOONi3HIF_jg8rg','2024-08-21 03:20:58.782112'),('erzt5xhhv8q2xtn39y916jqf7udng727','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sN9hB:D1vdKi-9csGFODYjMBpLOLH8_xC7Y0OLVoc96Fgwtxo','2024-07-12 11:23:13.012241'),('eswr59y1w2wlpgxq1q2izz3uerxit1ex','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sZ2Am:WUfSosAr2eKTmUpgzAjB7rveHt7NKgU_OoeftJHOu6I','2024-08-14 05:46:52.692186'),('g4hqeomvk4do4i9gg5fh3y50fqb91cv9','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sdiZi:XKCpGTIcuNb3baoyQYhLznxlKPZJJC1hWjN3oL4C_6w','2024-08-27 03:51:58.893558'),('g6q1ls3n4s7psbe7inwf4lsz6ji54j20','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sXyTT:qAEnandNUoaBbWxDDzrzhmbP4peqhoHndRQsgXwOSKI','2024-08-11 07:37:47.719855'),('hm6j77v8buwthal25sp5aca2g0qky4fs','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sSXV2:WSf9sq2KX8edcN1vRh4FVbUsLGzy0KpG53bYjl5wbpo','2024-07-27 07:48:56.531386'),('i3tqnzk8ozeaiieudd07j3og5pwy6uhd','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sOqZi:0_WbPAA4NT6xUUyRQyU8s4r3C169iInAGVNWnT8NSJ8','2024-07-17 03:22:30.107491'),('jfvqfa1uzi6zb7t6dofqmo8ghjirtehk','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sdiOR:dMD7v0DCZGhmV1GIO3BJaovnCr70xqrfcEnzFB8Ea-E','2024-08-27 03:40:19.824174'),('jitu9suzvax750ht855s812gk0ftu0zk','.eJxVjMsOwiAQRf-FtSEMjwIu3fcbyAyMUjU0Ke3K-O_apAvd3nPOfYmE21rT1nlJUxFnAeL0uxHmB7cdlDu22yzz3NZlIrkr8qBdjnPh5-Vw_w4q9vqtjQUqSpkcQUfGQNYYnSEzqODY2-KjxoEhKBc8KWs9XS37HHkghxTE-wPFnTdt:1sSXVw:6KwTYkQVEq0Sfk5pgJG4EjgOqR_Tjr-mip1dWHkYN5w','2024-07-27 07:49:52.089921'),('jle62xcuhfbke3a7iipwc1iqzyn3nrad','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sbu2v:TA_YSAowTjfJr4gNgVI6f9U34Mm3UpgV0DG2ptSL3q4','2024-08-22 03:42:37.001108'),('kyhmnhkv0fdvv07yhcx54piocuqnc6qc','.eJxVjMsOwiAQRf-FtSEMjwIu3fcbyAyMUjU0Ke3K-O_apAvd3nPOfYmE21rT1nlJUxFnAeL0uxHmB7cdlDu22yzz3NZlIrkr8qBdjnPh5-Vw_w4q9vqtjQUqSpkcQUfGQNYYnSEzqODY2-KjxoEhKBc8KWs9XS37HHkghxTE-wPFnTdt:1sISQz:tPKj-ClanmA-Dk7Aww1zqQ-VKfssykyIPVFAvv-Dmhw','2024-06-29 12:23:05.675170'),('lf7xmrg6ckb3lv6j0i5ax8hls6sq0z05','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sYHG9:pIboJJJ1ZEETstq44YTPro_tbxcXaL_vC-tEu_0JbPA','2024-08-12 03:41:17.873088'),('lmzf23fd3i15khsb4x2gqvfvqkudea01','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1senow:gLx8pWZ2nP56OFjMpgFBXgbVQBsfJmVYLL1bzVv34cY','2024-08-30 03:40:10.941765'),('m66spp8fags77ejmtedyh1dziyypf7xm','.eJxVjMsOwiAQRf-FtSEMjwIu3fcbyAyMUjU0Ke3K-O_apAvd3nPOfYmE21rT1nlJUxFnAeL0uxHmB7cdlDu22yzz3NZlIrkr8qBdjnPh5-Vw_w4q9vqtjQUqSpkcQUfGQNYYnSEzqODY2-KjxoEhKBc8KWs9XS37HHkghxTE-wPFnTdt:1sXyC4:4yjkBjzUjZ3kApepTNk0V97vH1zQA7KFW1GcaIPJmYk','2024-08-11 07:19:48.177399'),('mcm9p3e9pdacuobatwbavr271vg0us36','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1se533:jeqpZsAotGLfVol_D_c0q6jRup45DQLIu3KRbaG2p4s','2024-08-28 03:51:45.045210'),('mkcz6bwyrof3i5gpyqocz5m7ke2ozg2u','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1saoo9:nPKek14sxmik8LKrq2OfsjEk8YH_l84AuaVu3cRj6gI','2024-08-19 03:54:53.360242'),('nkkh4m28m8mmnn16hluk9b4wf9yr4fz1','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sXyDL:LMVBCE2ZYrbqWv3XhP6LyIW940W5PsB1_yt93-tFpAM','2024-08-11 07:21:07.399821'),('nxpeki7kgyt9y9s8wc007k44dtpsfdb6','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sZMgD:hoU16Vy6UzqPH1aOfzJI0OZWnTTw6jMq6SR3EuUIet0','2024-08-15 03:40:41.515028'),('olja5axf757w9t6zqawuv2z2kb862jui','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sbY0O:mtst74bBbGq_ifhZSEPwRHFDVvz6AH7dDeTP5BU8A8o','2024-08-21 04:10:32.515537'),('oqjfai52eov94chv6jmeoozgcx9247ht','.eJxVjMsOwiAQRf-FtSEMjwIu3fcbyAyMUjU0Ke3K-O_apAvd3nPOfYmE21rT1nlJUxFnAeL0uxHmB7cdlDu22yzz3NZlIrkr8qBdjnPh5-Vw_w4q9vqtjQUqSpkcQUfGQNYYnSEzqODY2-KjxoEhKBc8KWs9XS37HHkghxTE-wPFnTdt:1sdLC1:I9xhoUVveX1xIMdk1RcW8nkTJIbw2DQhw5pgS-yVxPY','2024-08-26 02:53:57.416425'),('pcuc27134fp4t15hjw32zpsyf8tde3pn','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sYIy9:mKqeQM0f6yP4d4mNPwXXzySKOOUxU9r_RA2hG0_GTMk','2024-08-12 05:30:49.039777'),('plett7u78di15n1jpw8rraivexlp0qbf','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1serju:-eC4crmxQjX0vGucPvdug71m_9VfhWAcnC2aW-ENm8g','2024-08-30 07:51:14.511936'),('pri82v6cbnqk4f7pmw20s8ixrvhtctvb','.eJxVjMsOwiAQRf-FtSEMjwIu3fcbyAyMUjU0Ke3K-O_apAvd3nPOfYmE21rT1nlJUxFnAeL0uxHmB7cdlDu22yzz3NZlIrkr8qBdjnPh5-Vw_w4q9vqtjQUqSpkcQUfGQNYYnSEzqODY2-KjxoEhKBc8KWs9XS37HHkghxTE-wPFnTdt:1sQej6:NIuFBRq1gRdkCB5zOuZE2omH0TWQ2HM33LMSMjUn2mA','2024-07-22 03:07:40.182675'),('sm3jy6ndi9e3t5wpxdu0hqi75qspnkt5','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sXyPv:iqj5iY7cE-vk_en0sGxge4Y9X7No1kqBPjrs-MZ_ikk','2024-08-11 07:34:07.730903'),('stpufp01x22nu13vnoutivrtg8w865fu','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sXyJi:hrtHKakbnoexRVxSXXCabRkHViGdhecrA016cEEwsBI','2024-08-11 07:27:42.523672'),('t4jf4e0169nktmzyid1bsiu3ph7mjcgy','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sOqUx:rooxrBXoGRwZEolrVt-InZ1MTHaZREBRK370suc8WHU','2024-07-17 03:17:35.795418'),('tdvaqo8abtd2zoiz9rltiizjy1tcyoo2','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sYdmx:Y1taYOlaVaoO18XCnrMe0oMW0K0XcOXKLTBsK2RsmAw','2024-08-13 03:44:39.911458'),('tyil8duo5kku5utumjo9yhjx6t61837o','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sOqZf:a6Bt-5mMNluq-kMmH2IQyEL5aLzA1jJhHpj4c7o4nSQ','2024-07-17 03:22:27.495393'),('vhao97j773azajvhq0plcvxxuku2g9i5','.eJxVjMsOwiAQRf-FtSEMjwIu3fcbyAyMUjU0Ke3K-O_apAvd3nPOfYmE21rT1nlJUxFnAeL0uxHmB7cdlDu22yzz3NZlIrkr8qBdjnPh5-Vw_w4q9vqtjQUqSpkcQUfGQNYYnSEzqODY2-KjxoEhKBc8KWs9XS37HHkghxTE-wPFnTdt:1sRkp0:4Od5ily03gLhP-JcethZxcrcDt-Yyhu8B0CrNgSbYGI','2024-07-25 03:50:18.311605'),('w3pfcpn9y4vp93atdglum94ycqm7xrz4','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1scn8T:-n2d6vuSzndQHJiucWFsauEb6u5xAxnAvNCNw_JD-aA','2024-08-24 14:32:01.424498'),('wvsv5fjx9jr7kdhwkojer4x4hzgl5n00','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sYfMK:eUXigXHMoHwlzR6eIJkhBrJ3e7UiKDuk7TVeFTFZcxE','2024-08-13 05:25:16.002599'),('xnexpf16ds7utiyqfr60dwvj8bruage3','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sXi3h:swd-ENeAaMMvm-LDGPWLAVlJU0jiu5aa5rgrL_AxhOQ','2024-08-10 14:06:05.218239'),('y0nphqusd8omi2r3g5y2lt7r9qa3ukj6','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sXxim:PACrxxWuOARygwmwXsDjwaMGAABaJU3z2XsaPAjH3Lg','2024-08-11 06:49:32.799492'),('y3wxtnfp0di0gm2xuzs6x5lyijagswb8','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sYfMX:68ZPa6dhi_iqWc7gfMH3FD9Uo-kptv5knnCUA1OZ0tg','2024-08-13 05:25:29.318457'),('zp5fhiuk02lql608351ohzwjdzmdhaij','.eJxVjMsOwiAQRf-FtSG8MoBL934DGZipVA0kpV0Z_12bdKHbe865L5FwW2vaBi9pJnEWVpx-t4zlwW0HdMd267L0ti5zlrsiDzrktRM_L4f7d1Bx1G8NwSMp8IqzcmBBg8qBfDFRFWLPcdIQNU7GkWYXCxSynpSJOiJlDOL9AdNfN9k:1sbXSz:QDiDBLoNfONBivRjEju5U3TsuZw0KTMsP2HBpq65D8U','2024-08-21 03:36:01.185963');
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
INSERT INTO `plutusAI_brokerdetails` VALUES (1,'antonyrajan.d@gmail.com','A58033497','ANTONY RAJAN DANIEL','angel_one','generated',1,'pOruxLYZ','1005','RQFCDA2ZX2DMFZ5GR6HXXPFITY','indian_index'),(2,'madara@plutus.com','S50761409','SAHAYARAJ  SAHAYARAJ','angel_one','generated',0,'Q12feFjR','1005','5TXNGVJEVZYMHCLF6HHOQHHTZ4','indian_index'),(3,'kamezwaran.r@gmail.com','K60814687','KAMESWARAN R','angel_one','generated',1,'fSe5lcvn','2011','2K42JL4YOHKINI2RO7EEIXALG4','indian_index');
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
) ENGINE=InnoDB AUTO_INCREMENT=3572 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_candledata`
--

LOCK TABLES `plutusAI_candledata` WRITE;
/*!40000 ALTER TABLE `plutusAI_candledata` DISABLE KEYS */;
INSERT INTO `plutusAI_candledata` VALUES (3513,'bank_nifty_fut','35089','2024-08-16 11:38:00','50269.85','50280.0','50259.75','50276.7'),(3514,'bank_nifty_fut','35089','2024-08-16 11:40:00','50271.05','50277.05','50271.0','50277.05'),(3515,'bank_nifty_fut','35089','2024-08-16 11:41:00','50277.05','50280.0','50260.0','50260.0'),(3516,'bank_nifty_fut','35089','2024-08-16 11:42:00','50261.15','50267.1','50250.0','50260.0'),(3517,'bank_nifty_fut','35089','2024-08-16 11:43:00','50257.25','50284.1','50257.2','50283.0'),(3518,'bank_nifty_fut','35089','2024-08-16 11:49:00','50335.0','50339.45','50322.0','50335.95'),(3519,'bank_nifty_fut','35089','2024-08-16 11:50:00','50335.95','50355.0','50323.0','50350.0'),(3520,'bank_nifty_fut','35089','2024-08-16 11:51:00','50350.0','50360.0','50328.25','50331.05'),(3521,'bank_nifty_fut','35089','2024-08-16 11:52:00','50331.05','50331.05','50302.15','50306.4'),(3522,'bank_nifty_fut','35089','2024-08-16 11:53:00','50306.4','50327.9','50306.4','50321.45'),(3523,'bank_nifty_fut','35089','2024-08-16 11:54:00','50320.5','50339.7','50317.55','50331.1'),(3524,'bank_nifty_fut','35089','2024-08-16 11:55:00','50331.1','50334.8','50314.05','50315.2'),(3525,'bank_nifty_fut','35089','2024-08-16 11:56:00','50314.2','50324.35','50305.25','50318.2'),(3526,'bank_nifty_fut','35089','2024-08-16 11:57:00','50318.2','50330.65','50308.9','50318.0'),(3527,'bank_nifty_fut','35089','2024-08-16 11:58:00','50317.5','50348.5','50317.5','50347.45'),(3528,'bank_nifty_fut','35089','2024-08-16 11:59:00','50349.95','50384.8','50336.95','50365.05'),(3529,'bank_nifty_fut','35089','2024-08-16 12:00:00','50372.15','50389.9','50356.95','50371.85'),(3530,'bank_nifty_fut','35089','2024-08-16 12:01:00','50375.45','50383.0','50363.1','50375.0'),(3531,'bank_nifty_fut','35089','2024-08-16 12:02:00','50375.0','50375.0','50359.0','50371.35'),(3532,'bank_nifty_fut','35089','2024-08-16 12:03:00','50371.35','50432.45','50364.1','50416.9'),(3533,'bank_nifty_fut','35089','2024-08-16 12:59:00','50463.8','50475.95','50460.35','50475.0'),(3534,'bank_nifty_fut','35089','2024-08-16 13:00:00','50467.6','50510.0','50465.55','50494.75'),(3535,'bank_nifty_fut','35089','2024-08-16 13:01:00','50494.75','50534.3','50494.75','50526.15'),(3536,'bank_nifty_fut','35089','2024-08-16 13:02:00','50526.05','50550.0','50519.0','50547.2'),(3537,'bank_nifty_fut','35089','2024-08-16 13:03:00','50547.2','50550.0','50530.65','50538.0'),(3538,'bank_nifty_fut','35089','2024-08-16 13:04:00','50538.0','50550.5','50538.0','50549.0'),(3539,'bank_nifty_fut','35089','2024-08-16 13:05:00','50549.0','50555.35','50533.05','50536.5'),(3540,'bank_nifty_fut','35089','2024-08-16 13:06:00','50536.5','50545.0','50525.05','50529.8'),(3541,'bank_nifty_fut','35089','2024-08-16 13:07:00','50529.8','50534.55','50510.05','50512.0'),(3542,'bank_nifty_fut','35089','2024-08-16 13:08:00','50512.0','50520.0','50494.0','50507.4'),(3543,'bank_nifty_fut','35089','2024-08-16 13:09:00','50507.4','50516.65','50500.0','50512.45'),(3544,'bank_nifty_fut','35089','2024-08-16 13:10:00','50512.45','50533.95','50511.05','50526.0'),(3545,'bank_nifty_fut','35089','2024-08-16 13:11:00','50526.0','50532.2','50511.25','50514.1'),(3546,'bank_nifty_fut','35089','2024-08-16 13:12:00','50514.1','50514.1','50502.25','50502.25'),(3547,'bank_nifty_fut','35089','2024-08-16 13:13:00','50502.25','50509.0','50500.0','50509.0'),(3548,'bank_nifty_fut','35089','2024-08-16 13:14:00','50510.45','50515.0','50502.25','50515.0'),(3549,'bank_nifty_fut','35089','2024-08-16 13:15:00','50515.0','50518.0','50509.0','50518.0'),(3550,'bank_nifty_fut','35089','2024-08-16 13:16:00','50518.0','50518.0','50500.1','50515.05'),(3551,'bank_nifty_fut','35089','2024-08-16 13:17:00','50515.05','50515.05','50501.25','50509.9'),(3552,'bank_nifty_fut','35089','2024-08-16 13:18:00','50509.9','50530.0','50509.9','50525.0'),(3553,'bank_nifty_fut','35089','2024-08-16 13:19:00','50525.0','50538.9','50520.05','50521.15'),(3554,'bank_nifty_fut','35089','2024-08-16 13:20:00','50521.15','50533.0','50507.1','50518.15'),(3555,'bank_nifty_fut','35089','2024-08-16 13:21:00','50518.15','50525.0','50502.45','50517.8'),(3556,'bank_nifty_fut','35089','2024-08-16 13:22:00','50516.0','50522.3','50513.65','50516.0'),(3557,'bank_nifty_fut','35089','2024-08-16 13:23:00','50516.0','50526.0','50515.3','50518.85'),(3558,'bank_nifty_fut','35089','2024-08-16 13:24:00','50518.85','50525.0','50515.0','50524.2'),(3559,'bank_nifty_fut','35089','2024-08-16 13:25:00','50524.2','50539.5','50523.9','50538.0'),(3560,'bank_nifty_fut','35089','2024-08-16 13:26:00','50540.0','50543.35','50526.8','50543.35'),(3561,'bank_nifty_fut','35089','2024-08-16 13:27:00','50544.0','50545.55','50528.05','50532.05'),(3562,'bank_nifty_fut','35089','2024-08-16 13:28:00','50532.05','50532.05','50505.55','50512.65'),(3563,'bank_nifty_fut','35089','2024-08-16 13:29:00','50512.65','50519.5','50490.2','50519.5'),(3564,'bank_nifty_fut','35089','2024-08-16 13:30:00','50517.7','50526.45','50502.2','50516.65'),(3565,'bank_nifty_fut','35089','2024-08-16 13:31:00','50516.65','50532.2','50500.0','50514.6'),(3566,'bank_nifty_fut','35089','2024-08-16 13:32:00','50514.8','50529.0','50507.15','50520.0'),(3567,'bank_nifty_fut','35089','2024-08-16 13:33:00','50520.0','50534.35','50512.25','50534.35'),(3568,'bank_nifty_fut','35089','2024-08-16 13:34:00','50529.0','50545.25','50521.5','50545.0'),(3569,'bank_nifty_fut','35089','2024-08-16 13:35:00','50545.0','50565.0','50545.0','50554.45'),(3570,'bank_nifty_fut','35089','2024-08-16 13:36:00','50555.0','50586.05','50550.0','50580.0'),(3571,'bank_nifty_fut','35089','2024-08-16 13:37:00','50580.0','50589.0','50565.1','50585.0');
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
INSERT INTO `plutusAI_configuration` VALUES (1,'nifty','10',1,'3','10','10','15','25200,25500,24774,24500,25000,24300,24100,24000,23800,23500,23000','antonyrajan.d@gmail.com',0,'started','50','1'),(2,'bank_nifty','50',1,'10','30','5','20','50500,50400,50300,50200,50100,50000,49900,49800,49700,49600,49500,49400,49300,49200,49100,49000,50600,50700,50800,50900,51000,51100,51200,51300,51400,51500,51600,51700,51800,51900,52000,52500,53000,49000,48500,48000','antonyrajan.d@gmail.com',0,'started','100','1'),(3,'fin_nifty','10',1,'10','10','10','15','23300,23400,23500,23600,23200,23200,23100,23000','antonyrajan.d@gmail.com',0,'started','50','10'),(4,'nifty','10',1,'10','10','10','15','24298,24398,24222','kamezwaran.r@gmail.com',0,'stopped','100','6'),(5,'bank_nifty','30',1,'10','30','20','50','update levels','kamezwaran.r@gmail.com',0,'stopped','10','10'),(6,'fin_nifty','10',1,'10','10','10','15','update levels','kamezwaran.r@gmail.com',0,'stopped','10','10');
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
INSERT INTO `plutusAI_indexdetails` VALUES (1,'nifty','indian_index','24139.0','99926000','2024-08-14 08:33:13','25','22-AUG-2024','29-AUG-2024'),(2,'bank_nifty','indian_index','49831.85','99926009','2024-08-14 08:33:14','15','21-AUG-2024','28-AUG-2024'),(3,'fin_nifty','indian_index','22596.8','99926037','2024-08-14 08:33:16','40','20-AUG-2024','27-AUG-2024'),(4,'bank_nifty_fut','indian_index','50588.65','35089','2024-08-16 13:38:41','15','16-JUL-2024','16-JUL-2024');
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
) ENGINE=InnoDB AUTO_INCREMENT=811 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_jobdetails`
--

LOCK TABLES `plutusAI_jobdetails` WRITE;
/*!40000 ALTER TABLE `plutusAI_jobdetails` DISABLE KEYS */;
INSERT INTO `plutusAI_jobdetails` VALUES (798,'antonyrajan.d@gmail.com','bank_nifty','86033aa2-3339-4381-a415-2af0397301f0','hunter'),(800,'antonyrajan.d@gmail.com','nifty','0c621c0e-44a1-4847-b478-be00e5bc3fee','hunter'),(806,'madara@plutus.com','socket_job','9c4929f1-5c92-49c3-8e67-1246fabdf9aa','socket_job');
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
) ENGINE=InnoDB AUTO_INCREMENT=658 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_orderbook`
--

LOCK TABLES `plutusAI_orderbook` WRITE;
/*!40000 ALTER TABLE `plutusAI_orderbook` DISABLE KEYS */;
INSERT INTO `plutusAI_orderbook` VALUES (654,'kamezwaran.r@gmail.com','1723793460.863606','BANKNIFTY21AUG2450200CE','15','464.4','468.65','order_exited','1723793485.978413','63.75','scalper','bank_nifty'),(655,'kamezwaran.r@gmail.com','1723794001.194326','BANKNIFTY21AUG2450200CE','15','470.35','462.0','order_exited','1723794182.398615','-125.25000000000034','scalper','bank_nifty'),(656,'kamezwaran.r@gmail.com','1723794182.960125','BANKNIFTY21AUG2450600PE','15','426.3','419.85','order_exited','1723794241.414861','-96.74999999999983','scalper','bank_nifty'),(657,'kamezwaran.r@gmail.com','1723794242.105905','BANKNIFTY21AUG2450200CE','15','465.15','503.85','order_exited','1723795530.585287','580.5000000000007','scalper','bank_nifty');
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
INSERT INTO `plutusAI_scalperdetails` VALUES (3,'kamezwaran.r@gmail.com','bank_nifty','200',1,0,'20','1',1,'stopped'),(4,'antonyrajan.d@gmail.com','bank_nifty','200',1,0,'20','1',0,'stopped');
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
INSERT INTO `plutusAI_userauthtokens` VALUES (9,'antonyrajan.d@gmail.com','eyJhbGciOiJIUzUxMiJ9.eyJ0b2tlbiI6IlJFRlJFU0gtVE9LRU4iLCJSRUZSRVNILVRPS0VOIjoiZXlKaGJHY2lPaUpTVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5WDNSNWNHVWlPaUpqYkdsbGJuUWlMQ0owYjJ0bGJsOTBlWEJsSWpvaWRISmhaR1ZmY21WbWNtVnphRjkwYjJ0bGJpSXNJbWR0WDJsa0lqb3dMQ0prWlhacFkyVmZhV1FpT2lJNE9UZ3lObU14TWkxaU1EaGtMVE0yTVRVdE9UTTVZaTFpTXpWbE56SmhOMlUzTUdNaUxDSnJhV1FpT2lKMGNtRmtaVjlyWlhsZmRqRWlMQ0p2Ylc1bGJXRnVZV2RsY21sa0lqb3dMQ0pwYzNNaU9pSnNiMmRwYmw5elpYSjJhV05sSWl3aWMzVmlJam9pUVRVNE1ETXpORGszSWl3aVpYaHdJam94TnpJek9UVXlOekF6TENKdVltWWlPakUzTWpNM056azRORE1zSW1saGRDSTZNVGN5TXpjM09UZzBNeXdpYW5ScElqb2lOakUyT1Rjek4yVXROR0UyT0MwME1HVXpMVGc1Tm1JdE5EaGtZamhsT0dVek5EUTNJbjAuRy1wMVduUnBiSkRkbEg3cE80cmxuY2FxaVVZNjNpUWo5aXZ4ZUhvRjBBdkFkdnJXdVdHQzBGaDJnUXpORVpkQm9vMkFxVHdlQ0dvT2lBZHYwZEtBODQyNmY5NkVmVjVteXFsTFJFenRNeW1KbmZHLWhvdVozaWtGTEVNQU0xSmNXSU1kRHdxc3ZuRFJ2MXA0OFF3VVVBVWxSTzlieWNUN0tpZjV4YUhWS1ZnIiwiaWF0IjoxNzIzNzc5OTAzfQ.DxYPY1Sscx94TjAVggGJw_urZJNOPs1ggvlTY2Wpr5-ZQXTZqVbbNgIpsnlfMD_Beh8-Q2avZf60XR9WYhCYgg','eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6IkE1ODAzMzQ5NyIsImlhdCI6MTcyMzc3OTkwMywiZXhwIjoxNzIzODY2MzAzfQ.QFK64ICyzVy9Leo2JyHANyxZ-h8cwHGynS_xiSrygi6fvScvRouzdUmJQhZNakIHZTCk49YDG1hg6-zaMXqBFQ','1723779903.959384','eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6IkE1ODAzMzQ5NyIsInJvbGVzIjowLCJ1c2VydHlwZSI6IlVTRVIiLCJ0b2tlbiI6ImV5SmhiR2NpT2lKU1V6STFOaUlzSW5SNWNDSTZJa3BYVkNKOS5leUoxYzJWeVgzUjVjR1VpT2lKamJHbGxiblFpTENKMGIydGxibDkwZVhCbElqb2lkSEpoWkdWZllXTmpaWE56WDNSdmEyVnVJaXdpWjIxZmFXUWlPakVzSW5OdmRYSmpaU0k2SWpNaUxDSmtaWFpwWTJWZmFXUWlPaUk0T1RneU5tTXhNaTFpTURoa0xUTTJNVFV0T1RNNVlpMWlNelZsTnpKaE4yVTNNR01pTENKcmFXUWlPaUowY21Ga1pWOXJaWGxmZGpFaUxDSnZiVzVsYldGdVlXZGxjbWxrSWpveExDSndjbTlrZFdOMGN5STZleUprWlcxaGRDSTZleUp6ZEdGMGRYTWlPaUpoWTNScGRtVWlmWDBzSW1semN5STZJblJ5WVdSbFgyeHZaMmx1WDNObGNuWnBZMlVpTENKemRXSWlPaUpCTlRnd016TTBPVGNpTENKbGVIQWlPakUzTWpNNE56WXdOemNzSW01aVppSTZNVGN5TXpjM09UZzBNeXdpYVdGMElqb3hOekl6TnpjNU9EUXpMQ0pxZEdraU9pSm1Nak0wTldRME55MWtPVEV6TFRRNE1HSXRZalk0WkMxbVltUTROR0U1T0dKa1lUVWlmUS5QQmdFSTE3R0pSaG5vWUtGQ1BIQXk5Qjg4WC1JYVlLT2RkemRpSWdJNlZ5cmgwNm1oN211M0tLVmhkZXlOcjF4LXJWTHI3MnFXT1dBVDhidGZrOUpxZF9UWWJLV3dYSGYybVhrR1FIS2Y3UWJmY2xKSXJrdE5LS3hjUk4zbWx6RzZGengtblUtNzUtVWV3Ujg1UnhFN2I3aDk5NWhXWUlPUnkzejhTMmxENFEiLCJBUEktS0VZIjoicE9ydXhMWVoiLCJpYXQiOjE3MjM3Nzk5MDMsImV4cCI6MTcyMzg3NjA3N30.vfpCYx2FCBoiJTIKfKlonEgm1Svg6yXpeET_eYav3WMhW5E4gYo07HGBG0TZ6O5Dl2Wtm4HY0Ukbmui0ZgkbaA'),(10,'madara@plutus.com','eyJhbGciOiJIUzUxMiJ9.eyJ0b2tlbiI6IlJFRlJFU0gtVE9LRU4iLCJSRUZSRVNILVRPS0VOIjoiZXlKaGJHY2lPaUpTVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5WDNSNWNHVWlPaUpqYkdsbGJuUWlMQ0owYjJ0bGJsOTBlWEJsSWpvaWRISmhaR1ZmY21WbWNtVnphRjkwYjJ0bGJpSXNJbWR0WDJsa0lqb3dMQ0prWlhacFkyVmZhV1FpT2lJME9ERTRZVFEwT1MxaU9EbGhMVE0wWWpFdE9Ea3hOUzAzWVdJNU4ySTFOR1E0TlRVaUxDSnJhV1FpT2lKMGNtRmtaVjlyWlhsZmRqRWlMQ0p2Ylc1bGJXRnVZV2RsY21sa0lqb3dMQ0pwYzNNaU9pSnNiMmRwYmw5elpYSjJhV05sSWl3aWMzVmlJam9pVXpVd056WXhOREE1SWl3aVpYaHdJam94TnpJek9UVXlOalV5TENKdVltWWlPakUzTWpNM056azNPVElzSW1saGRDSTZNVGN5TXpjM09UYzVNaXdpYW5ScElqb2lZbUk0TURRek5UTXROemd3TnkwMFlqSTVMVGszWTJJdE4ySTVNekEzWTJFNE5XWTBJbjAuV210bzVlQ2I2YkhBZ3NIYWtPdk03U08xLWdGTmRmN3VMb0FmQTJ1dEpBUE1lWTNBckhiSmNWT3o3UVFpc18yYlE0cUZaMjJodTJnckpUUDJ1eGxGNGFobDR5U00yd2RtLXJRQzhPWjdpVGdJNGszZE5QUS1hRTljWHVYckM3TUVuT3RBZGdhd0xvbWt2YXBaZi1YRzcyWXBIZ0lwYUxBRHplRzQ3RmNhOFJFIiwiaWF0IjoxNzIzNzc5ODUyfQ.yU1iL883KHIRY1nP3YY4VMoPP3GtW579GbmS_gFwy_mQiMijp8zO0pkvEAVJ5TWbfppPZplFU9ciCL3Wk3T82g','eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6IlM1MDc2MTQwOSIsImlhdCI6MTcyMzc3OTg1MiwiZXhwIjoxNzIzODY2MjUyfQ.0v50Y9tGsRHDjdTBitGiN_44vWHRtFEOzfds7jhTqc0o89NRfaNO6WhhESlqqS6Qr1-Rz-svrhG4693X6BSyWA','1723779852.2982','eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6IlM1MDc2MTQwOSIsInJvbGVzIjowLCJ1c2VydHlwZSI6IlVTRVIiLCJ0b2tlbiI6ImV5SmhiR2NpT2lKU1V6STFOaUlzSW5SNWNDSTZJa3BYVkNKOS5leUoxYzJWeVgzUjVjR1VpT2lKamJHbGxiblFpTENKMGIydGxibDkwZVhCbElqb2lkSEpoWkdWZllXTmpaWE56WDNSdmEyVnVJaXdpWjIxZmFXUWlPakV4TENKemIzVnlZMlVpT2lJeklpd2laR1YyYVdObFgybGtJam9pTkRneE9HRTBORGt0WWpnNVlTMHpOR0l4TFRnNU1UVXROMkZpT1RkaU5UUmtPRFUxSWl3aWEybGtJam9pZEhKaFpHVmZhMlY1WDNZeElpd2liMjF1WlcxaGJtRm5aWEpwWkNJNk1URXNJbkJ5YjJSMVkzUnpJanA3SW1SbGJXRjBJanA3SW5OMFlYUjFjeUk2SW1GamRHbDJaU0o5ZlN3aWFYTnpJam9pZEhKaFpHVmZiRzluYVc1ZmMyVnlkbWxqWlNJc0luTjFZaUk2SWxNMU1EYzJNVFF3T1NJc0ltVjRjQ0k2TVRjeU16ZzNPREl5TVN3aWJtSm1Jam94TnpJek56YzVOemt5TENKcFlYUWlPakUzTWpNM056azNPVElzSW1wMGFTSTZJakV6TmpOaU5EQTVMV0ptTldVdE5EWXhPUzFoT0RsaUxUZzBOMkpoTnpRMU1UWTFZU0o5LlNWUENyRUhLaEdFa1Jrd3FvX3QzTEtDcVo5aTdoRFdwaXV6UFI2UnhIdUxIMlhKT0I2UE45U1FteG9YYjNnUTluOWZReFZqRkZoVzBrX3JUeGczTXo3cHpZdm5VMmJhUkJkRmZlM0wtZEVpNkxGSWtJaGNYMWs4MGF1WmRreHotUEV4aFY2R21fVlNINmlZVGRPS2t2WnNQUmxSTU1FNmROMkpOUl9kc3JzOCIsIkFQSS1LRVkiOiJRMTJmZUZqUiIsImlhdCI6MTcyMzc3OTg1MiwiZXhwIjoxNzIzODc4MjIxfQ.QhYcwN0Bn_XWZsjGHpMRsAD4Qe3t2XUxwjCprAAMzBcGYgqAfqDHrOl-HO_maBslxb-vwWq1aIXG9S8M9ZsK2g'),(11,'kamezwaran.r@gmail.com','eyJhbGciOiJIUzUxMiJ9.eyJ0b2tlbiI6IlJFRlJFU0gtVE9LRU4iLCJSRUZSRVNILVRPS0VOIjoiZXlKaGJHY2lPaUpTVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5WDNSNWNHVWlPaUpqYkdsbGJuUWlMQ0owYjJ0bGJsOTBlWEJsSWpvaWRISmhaR1ZmY21WbWNtVnphRjkwYjJ0bGJpSXNJbWR0WDJsa0lqb3dMQ0prWlhacFkyVmZhV1FpT2lJNU9EVTBPR05tTkMweVpHVTVMVE15WVRZdE9UVXdaQzAwTlRnNFlURmtabVprWW1NaUxDSnJhV1FpT2lKMGNtRmtaVjlyWlhsZmRqRWlMQ0p2Ylc1bGJXRnVZV2RsY21sa0lqb3dMQ0pwYzNNaU9pSnNiMmRwYmw5elpYSjJhV05sSWl3aWMzVmlJam9pU3pZd09ERTBOamczSWl3aVpYaHdJam94TnpJek9UVXlOekEzTENKdVltWWlPakUzTWpNM056azRORGNzSW1saGRDSTZNVGN5TXpjM09UZzBOeXdpYW5ScElqb2lOV1JsTkdSbE9EVXRaREprWkMwMFlqQTJMV0kwTXprdE1EaGxNemN5T1RZd00yUm1JbjAuYS10dkUxa2kzeE01MVBMUzJwNjJkZGpmekE2aDlvZ001Z1hmaDZTNHZBWThEQmhVa1JmTnZaQ2pnbV83M2JqMFZzNV9BdmVqdDZBd3RxQmFzTHR2UVAxc2RUYUd1QmpTcnpuLTY4bmNNVkR1TmVSZnZVZ09rSWtCN3lScWZIZEhqS0RzMFJyeU5Nem1JX3FwZlBlY1pTaGhnWHdTZXJSWldLdWJnVUprQjNZIiwiaWF0IjoxNzIzNzc5OTA3fQ.lnaUnnlrH96C5sXshIdSsIlbnJ4A6whm0P4Pm0P7LTzo0bagum5xK53qIhZpyOCAc9ebtcp6bjd3BazFluvb3Q','eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6Iks2MDgxNDY4NyIsImlhdCI6MTcyMzc3OTkwNywiZXhwIjoxNzIzODY2MzA3fQ.S4hZjuAnqxsl7AU6u2-NqD0n9yxRQW9odmMOb74CylGh0zXDUYjsWK0ne9HonJKeKjz97FPwcTdEQWciJRTtHQ','1723779907.86679','eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6Iks2MDgxNDY4NyIsInJvbGVzIjowLCJ1c2VydHlwZSI6IlVTRVIiLCJ0b2tlbiI6ImV5SmhiR2NpT2lKU1V6STFOaUlzSW5SNWNDSTZJa3BYVkNKOS5leUoxYzJWeVgzUjVjR1VpT2lKamJHbGxiblFpTENKMGIydGxibDkwZVhCbElqb2lkSEpoWkdWZllXTmpaWE56WDNSdmEyVnVJaXdpWjIxZmFXUWlPamtzSW5OdmRYSmpaU0k2SWpNaUxDSmtaWFpwWTJWZmFXUWlPaUk1T0RVME9HTm1OQzB5WkdVNUxUTXlZVFl0T1RVd1pDMDBOVGc0WVRGa1ptWmtZbU1pTENKcmFXUWlPaUowY21Ga1pWOXJaWGxmZGpFaUxDSnZiVzVsYldGdVlXZGxjbWxrSWpvNUxDSndjbTlrZFdOMGN5STZleUprWlcxaGRDSTZleUp6ZEdGMGRYTWlPaUpoWTNScGRtVWlmWDBzSW1semN5STZJblJ5WVdSbFgyeHZaMmx1WDNObGNuWnBZMlVpTENKemRXSWlPaUpMTmpBNE1UUTJPRGNpTENKbGVIQWlPakUzTWpNNE56STNNemdzSW01aVppSTZNVGN5TXpjM09UZzBOeXdpYVdGMElqb3hOekl6TnpjNU9EUTNMQ0pxZEdraU9pSTBORGxsWkdFMU5DMHlNemczTFRRNE4ySXRZbU0yWWkwMVpETXlOVE0yWXpZMVkyTWlmUS5aRkRlUFRzd3dyZnozZDVGY2N2azVUVDNDMXBEM0RtdGV6NHZ0bGlnVGxtVWliR3Z6a1FrS2tWaHZ4UTdqS3NScU1OMnh5UGROY1A3TzNTWFRCc0Q0QTNvVVRuRzBZTVdLOThkeUY4VHphdkZxN3RqUXBvLUdyZ2txa2JBdC1yN3dMb1B6WDRTeE8xS3BVMlVRNnB2S2o1VnUyMDJRYnFKSGNhNzJ5QnBZRTAiLCJBUEktS0VZIjoiZlNlNWxjdm4iLCJpYXQiOjE3MjM3Nzk5MDcsImV4cCI6MTcyMzg3MjczOH0.GDnOYvbekv7HjSFk1omKWlaKXoyyZ2nFyVxohiAKhIn88ej-z-LC4eFajkxtth8U8T-MJW4Njq0UNK6qtOI5BQ');
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

-- Dump completed on 2024-08-16 17:58:47
