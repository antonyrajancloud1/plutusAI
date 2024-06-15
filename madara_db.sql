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
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add configuration',7,'add_configuration'),(26,'Can change configuration',7,'change_configuration'),(27,'Can delete configuration',7,'delete_configuration'),(28,'Can view configuration',7,'view_configuration'),(29,'Can add broker details',8,'add_brokerdetails'),(30,'Can change broker details',8,'change_brokerdetails'),(31,'Can delete broker details',8,'delete_brokerdetails'),(32,'Can view broker details',8,'view_brokerdetails'),(33,'Can add order book',9,'add_orderbook'),(34,'Can change order book',9,'change_orderbook'),(35,'Can delete order book',9,'delete_orderbook'),(36,'Can view order book',9,'view_orderbook'),(37,'Can add index details',10,'add_indexdetails'),(38,'Can change index details',10,'change_indexdetails'),(39,'Can delete index details',10,'delete_indexdetails'),(40,'Can view index details',10,'view_indexdetails'),(41,'Can add job details',11,'add_jobdetails'),(42,'Can change job details',11,'change_jobdetails'),(43,'Can delete job details',11,'delete_jobdetails'),(44,'Can view job details',11,'view_jobdetails'),(45,'Can add payment details',12,'add_paymentdetails'),(46,'Can change payment details',12,'change_paymentdetails'),(47,'Can delete payment details',12,'delete_paymentdetails'),(48,'Can view payment details',12,'view_paymentdetails');
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
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$720000$TrRCp4ZEcCaTlJwjDlgH4n$bXk1dvyXOBkHUCj4N2oz2av/RSJgPbv2aSX+u6Z+Daw=','2024-06-15 12:23:05.491808',1,'admin','','','madara@plutus.com',1,1,'2024-06-15 12:09:57.133766'),(2,'pbkdf2_sha256$720000$su9jHjriTejd7pUVflaCpW$zYqJtpAqxjfNEVZEVupo4bhWZI2XlrAvdVoIugS7MM4=','2024-06-15 12:19:38.880639',0,'antonyrajan.d','antonyrajan.d','','antonyrajan.d@gmail.com',0,1,'2024-06-15 12:19:09.052744');
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
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(8,'madaraApp','brokerdetails'),(7,'madaraApp','configuration'),(10,'madaraApp','indexdetails'),(11,'madaraApp','jobdetails'),(9,'madaraApp','orderbook'),(12,'madaraApp','paymentdetails'),(6,'sessions','session');
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
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-06-15 12:02:20.084320'),(2,'auth','0001_initial','2024-06-15 12:03:05.244407'),(3,'admin','0001_initial','2024-06-15 12:03:15.119429'),(4,'admin','0002_logentry_remove_auto_add','2024-06-15 12:03:15.325262'),(5,'admin','0003_logentry_add_action_flag_choices','2024-06-15 12:03:15.637149'),(6,'contenttypes','0002_remove_content_type_name','2024-06-15 12:03:21.877062'),(7,'auth','0002_alter_permission_name_max_length','2024-06-15 12:03:27.939462'),(8,'auth','0003_alter_user_email_max_length','2024-06-15 12:03:28.471649'),(9,'auth','0004_alter_user_username_opts','2024-06-15 12:03:28.800176'),(10,'auth','0005_alter_user_last_login_null','2024-06-15 12:03:33.421193'),(11,'auth','0006_require_contenttypes_0002','2024-06-15 12:03:33.985967'),(12,'auth','0007_alter_validators_add_error_messages','2024-06-15 12:03:34.747565'),(13,'auth','0008_alter_user_username_max_length','2024-06-15 12:03:40.350750'),(14,'auth','0009_alter_user_last_name_max_length','2024-06-15 12:03:46.485267'),(15,'auth','0010_alter_group_name_max_length','2024-06-15 12:03:47.223014'),(16,'auth','0011_update_proxy_permissions','2024-06-15 12:03:48.089320'),(17,'auth','0012_alter_user_first_name_max_length','2024-06-15 12:03:53.620107'),(18,'madaraApp','0001_initial','2024-06-15 12:03:55.626302'),(19,'madaraApp','0002_levels_remove_configuration_target_and_more','2024-06-15 12:04:26.236798'),(20,'madaraApp','0003_configuration_trailing_points_and_more','2024-06-15 12:04:31.008526'),(21,'madaraApp','0004_remove_configuration_levels_configuration_levels','2024-06-15 12:04:33.870250'),(22,'madaraApp','0005_delete_levels_configuration_user_id','2024-06-15 12:04:38.192991'),(23,'madaraApp','0006_configuration_start_scheduler','2024-06-15 12:04:40.835549'),(24,'madaraApp','0007_configuration_stage_configuration_strike','2024-06-15 12:04:46.791665'),(25,'madaraApp','0008_brokerdetails_orderbook','2024-06-15 12:04:51.436069'),(26,'madaraApp','0009_brokerdetails_is_demo_trading_enabled','2024-06-15 12:04:53.774299'),(27,'madaraApp','0010_alter_brokerdetails_user_id_and_more','2024-06-15 12:04:54.081200'),(28,'madaraApp','0011_brokerdetails_broker_api_token_and_more','2024-06-15 12:04:59.023843'),(29,'madaraApp','0012_indexdetails_jobdetails_and_more','2024-06-15 12:05:04.731802'),(30,'madaraApp','0013_brokerdetails_index_group','2024-06-15 12:05:07.228864'),(31,'madaraApp','0014_paymentdetails','2024-06-15 12:05:09.833452'),(32,'madaraApp','0015_jobdetails_terminate_job','2024-06-15 12:05:11.464829'),(33,'madaraApp','0016_alter_jobdetails_terminate_job','2024-06-15 12:05:17.943298'),(34,'madaraApp','0017_remove_jobdetails_terminate_job','2024-06-15 12:05:19.954183'),(35,'madaraApp','0018_indexdetails_index_ltp_indexdetails_index_token','2024-06-15 12:05:23.404805'),(36,'madaraApp','0019_rename_index_ltp_indexdetails_ltp_and_more','2024-06-15 12:05:26.593994'),(37,'madaraApp','0020_configuration_lots','2024-06-15 12:05:29.311089'),(38,'madaraApp','0021_indexdetails_qty','2024-06-15 12:05:31.329100'),(39,'madaraApp','0022_alter_configuration_lots','2024-06-15 12:05:31.549297'),(40,'madaraApp','0023_indexdetails_current_expiry_indexdetails_next_expiry','2024-06-15 12:05:34.506065'),(41,'madaraApp','0024_rename_time_orderbook_entry_time_orderbook_exit_time_and_more','2024-06-15 12:05:39.447613'),(42,'madaraApp','0025_supportedbrokers','2024-06-15 12:05:42.216629'),(43,'madaraApp','0026_alter_supportedbrokers_instruments','2024-06-15 12:05:42.543369'),(44,'madaraApp','0027_alter_supportedbrokers_instruments','2024-06-15 12:05:42.772467'),(45,'madaraApp','0028_alter_supportedbrokers_instruments','2024-06-15 12:05:42.948876'),(46,'madaraApp','0029_delete_supportedbrokers','2024-06-15 12:05:45.208042'),(47,'madaraApp','0030_alter_orderbook_exit_price_alter_orderbook_exit_time','2024-06-15 12:05:53.532372'),(48,'madaraApp','0031_orderbook_cumulative_p_l','2024-06-15 12:05:56.106308'),(49,'madaraApp','0032_rename_cumulative_p_l_orderbook_total','2024-06-15 12:05:57.373743'),(50,'madaraApp','0033_alter_orderbook_entry_time_alter_orderbook_exit_time','2024-06-15 12:06:07.645784'),(51,'madaraApp','0034_alter_orderbook_entry_time','2024-06-15 12:06:07.814832'),(52,'madaraApp','0035_alter_orderbook_entry_time_alter_orderbook_exit_time','2024-06-15 12:06:18.955808'),(53,'sessions','0001_initial','2024-06-15 12:06:22.209235');
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
INSERT INTO `django_session` VALUES ('4i7k3evdhzkw2bjbhzn67a5wvd11ni1k','.eJxVjMsOwiAQRf-FtSGVYQZw6b7fQIaBStXQpI-V8d-1SRe6veec-1KRt7XGbSlzHLO6KKNOv1tieZS2g3zndpu0TG2dx6R3RR900f2Uy_N6uH8HlZf6rbvsLDvhJEIIoQgNHAwYEuc7S-eBiAUsY8jkATqPFhFQDJPBZEC9P-GONxE:1sISNf:rz6C4so4auNahvUBVexX7mUnT8Uh7NF_VZphUnIyTe0','2024-06-29 12:19:39.087860'),('e7xtiz2ut1w0yucfu03vgrsbz4z05hc8','.eJxVjMsOwiAQRf-FtSEMjwIu3fcbyAyMUjU0Ke3K-O_apAvd3nPOfYmE21rT1nlJUxFnAeL0uxHmB7cdlDu22yzz3NZlIrkr8qBdjnPh5-Vw_w4q9vqtjQUqSpkcQUfGQNYYnSEzqODY2-KjxoEhKBc8KWs9XS37HHkghxTE-wPFnTdt:1sISEn:5nqopMDP56toJY3cYxaLEnijZ6ZUnr7qjgQaloiEvj4','2024-06-29 12:10:29.755173'),('kyhmnhkv0fdvv07yhcx54piocuqnc6qc','.eJxVjMsOwiAQRf-FtSEMjwIu3fcbyAyMUjU0Ke3K-O_apAvd3nPOfYmE21rT1nlJUxFnAeL0uxHmB7cdlDu22yzz3NZlIrkr8qBdjnPh5-Vw_w4q9vqtjQUqSpkcQUfGQNYYnSEzqODY2-KjxoEhKBc8KWs9XS37HHkghxTE-wPFnTdt:1sISQz:tPKj-ClanmA-Dk7Aww1zqQ-VKfssykyIPVFAvv-Dmhw','2024-06-29 12:23:05.675170');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `madaraApp_brokerdetails`
--

DROP TABLE IF EXISTS `madaraApp_brokerdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `madaraApp_brokerdetails` (
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
-- Dumping data for table `madaraApp_brokerdetails`
--

LOCK TABLES `madaraApp_brokerdetails` WRITE;
/*!40000 ALTER TABLE `madaraApp_brokerdetails` DISABLE KEYS */;
INSERT INTO `madaraApp_brokerdetails` VALUES (1,'antonyrajan.d@gmail.com','S50761409','SAHAYA RAJ','angel_one','added',1,'Q12feFjR','1005','5TXNGVJEVZYMHCLF6HHOQHHTZ4','indian_index'),(2,'madara@plutus.com','S50761409','SAHAYARAJ  SAHAYARAJ','angel_one','generated',0,'Q12feFjR','1005','5TXNGVJEVZYMHCLF6HHOQHHTZ4','indian_index');
/*!40000 ALTER TABLE `madaraApp_brokerdetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `madaraApp_configuration`
--

DROP TABLE IF EXISTS `madaraApp_configuration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `madaraApp_configuration` (
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
-- Dumping data for table `madaraApp_configuration`
--

LOCK TABLES `madaraApp_configuration` WRITE;
/*!40000 ALTER TABLE `madaraApp_configuration` DISABLE KEYS */;
INSERT INTO `madaraApp_configuration` VALUES (1,'nifty','10',1,'3','10','10','20','22500','antonyrajan.d@gmail.com',0,'stopped','100','1'),(2,'bank_nifty','30',1,'10','30','20','50','update levels','antonyrajan.d@gmail.com',0,'stopped','10','10'),(3,'fin_nifty','10',1,'10','10','10','15','update levels','antonyrajan.d@gmail.com',0,'stopped','10','10');
/*!40000 ALTER TABLE `madaraApp_configuration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `madaraApp_indexdetails`
--

DROP TABLE IF EXISTS `madaraApp_indexdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `madaraApp_indexdetails` (
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `madaraApp_indexdetails`
--

LOCK TABLES `madaraApp_indexdetails` WRITE;
/*!40000 ALTER TABLE `madaraApp_indexdetails` DISABLE KEYS */;
INSERT INTO `madaraApp_indexdetails` VALUES (1,'nifty','indian_index','23465.6','99926000','24-06-15 18:16:21','25','20-JUN-2024','27-JUN-2024'),(2,'bank_nifty','indian_index','50002.0','99926009','24-06-15 18:16:24','15','19-JUN-2024','26-JUN-2024'),(3,'fin_nifty','indian_index','22411.95','99926037','24-06-15 18:16:20','40','18-JUN-2024','25-JUN-2024');
/*!40000 ALTER TABLE `madaraApp_indexdetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `madaraApp_jobdetails`
--

DROP TABLE IF EXISTS `madaraApp_jobdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `madaraApp_jobdetails` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` varchar(500) NOT NULL,
  `index_name` varchar(50) NOT NULL,
  `job_id` varchar(300) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `madaraApp_jobdetails`
--

LOCK TABLES `madaraApp_jobdetails` WRITE;
/*!40000 ALTER TABLE `madaraApp_jobdetails` DISABLE KEYS */;
INSERT INTO `madaraApp_jobdetails` VALUES (1,'madara@plutus.com','socket_job','4e7f46e7-95a8-4e5b-b53b-742cdbd99c22');
/*!40000 ALTER TABLE `madaraApp_jobdetails` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `madaraApp_orderbook`
--

DROP TABLE IF EXISTS `madaraApp_orderbook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `madaraApp_orderbook` (
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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `madaraApp_orderbook`
--

LOCK TABLES `madaraApp_orderbook` WRITE;
/*!40000 ALTER TABLE `madaraApp_orderbook` DISABLE KEYS */;
/*!40000 ALTER TABLE `madaraApp_orderbook` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `madaraApp_paymentdetails`
--

DROP TABLE IF EXISTS `madaraApp_paymentdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `madaraApp_paymentdetails` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` varchar(500) NOT NULL,
  `registed_date` varchar(200) NOT NULL,
  `renew_date` varchar(200) NOT NULL,
  `opted_index` varchar(500) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `madaraApp_paymentdetails`
--

LOCK TABLES `madaraApp_paymentdetails` WRITE;
/*!40000 ALTER TABLE `madaraApp_paymentdetails` DISABLE KEYS */;
/*!40000 ALTER TABLE `madaraApp_paymentdetails` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-15 12:46:25
