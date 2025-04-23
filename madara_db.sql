-- MySQL dump 10.13  Distrib 8.0.41, for Linux (x86_64)
--
-- Host: localhost    Database: madara_db
-- ------------------------------------------------------
-- Server version	8.0.41-0ubuntu0.24.04.1

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
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add configuration',7,'add_configuration'),(26,'Can change configuration',7,'change_configuration'),(27,'Can delete configuration',7,'delete_configuration'),(28,'Can view configuration',7,'view_configuration'),(29,'Can add order book',8,'add_orderbook'),(30,'Can change order book',8,'change_orderbook'),(31,'Can delete order book',8,'delete_orderbook'),(32,'Can view order book',8,'view_orderbook'),(33,'Can add broker details',9,'add_brokerdetails'),(34,'Can change broker details',9,'change_brokerdetails'),(35,'Can delete broker details',9,'delete_brokerdetails'),(36,'Can view broker details',9,'view_brokerdetails'),(37,'Can add index details',10,'add_indexdetails'),(38,'Can change index details',10,'change_indexdetails'),(39,'Can delete index details',10,'delete_indexdetails'),(40,'Can view index details',10,'view_indexdetails'),(41,'Can add job details',11,'add_jobdetails'),(42,'Can change job details',11,'change_jobdetails'),(43,'Can delete job details',11,'delete_jobdetails'),(44,'Can view job details',11,'view_jobdetails'),(45,'Can add payment details',12,'add_paymentdetails'),(46,'Can change payment details',12,'change_paymentdetails'),(47,'Can delete payment details',12,'delete_paymentdetails'),(48,'Can view payment details',12,'view_paymentdetails'),(49,'Can add scalper details',13,'add_scalperdetails'),(50,'Can change scalper details',13,'change_scalperdetails'),(51,'Can delete scalper details',13,'delete_scalperdetails'),(52,'Can view scalper details',13,'view_scalperdetails'),(53,'Can add candle data',14,'add_candledata'),(54,'Can change candle data',14,'change_candledata'),(55,'Can delete candle data',14,'delete_candledata'),(56,'Can view candle data',14,'view_candledata'),(57,'Can add user auth tokens',15,'add_userauthtokens'),(58,'Can change user auth tokens',15,'change_userauthtokens'),(59,'Can delete user auth tokens',15,'delete_userauthtokens'),(60,'Can view user auth tokens',15,'view_userauthtokens'),(61,'Can add manual orders',16,'add_manualorders'),(62,'Can change manual orders',16,'change_manualorders'),(63,'Can delete manual orders',16,'delete_manualorders'),(64,'Can view manual orders',16,'view_manualorders'),(65,'Can add webhook details',17,'add_webhookdetails'),(66,'Can change webhook details',17,'change_webhookdetails'),(67,'Can delete webhook details',17,'delete_webhookdetails'),(68,'Can view webhook details',17,'view_webhookdetails'),(69,'Can add flash details',18,'add_flashdetails'),(70,'Can change flash details',18,'change_flashdetails'),(71,'Can delete flash details',18,'delete_flashdetails'),(72,'Can view flash details',18,'view_flashdetails'),(73,'Can add Token',19,'add_token'),(74,'Can change Token',19,'change_token'),(75,'Can delete Token',19,'delete_token'),(76,'Can view Token',19,'view_token'),(77,'Can add Token',20,'add_tokenproxy'),(78,'Can change Token',20,'change_tokenproxy'),(79,'Can delete Token',20,'delete_tokenproxy'),(80,'Can view Token',20,'view_tokenproxy');
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
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$870000$20wEZAECaaKdsTfRSjQY1U$WMEis13ONpVR/p5mRRPv8nn38WyoCuZR+Ly7Ou1GshY=','2025-04-22 05:02:08.583536',1,'admin','','','madara@plutus.com',1,1,'2025-04-11 17:28:54.818042'),(2,'pbkdf2_sha256$870000$uqtJeLIJQiAzm0TNoXjB33$FpyzR5rOZ1e4fnYYkyfsclggAtDgLhP67c6hnJ8dGSw=','2025-04-11 17:37:37.724729',0,'antonyrajan.d','antonyrajan.d','','antonyrajan.d@gmail.com',0,1,'2025-04-11 17:34:17.116396'),(3,'pbkdf2_sha256$870000$cqhfslLrNo4k8l6eSYWrNT$QvTigNiplq8LqgflPptT4h/quu84U4F8XUhInXp8sfA=','2025-04-23 16:11:55.960903',0,'user1','user1','','user1@gmail.com',0,1,'2025-04-23 16:09:17.156046');
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
-- Table structure for table `authtoken_token`
--

DROP TABLE IF EXISTS `authtoken_token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authtoken_token` (
  `key` varchar(40) NOT NULL,
  `created` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `authtoken_token_user_id_35299eff_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authtoken_token`
--

LOCK TABLES `authtoken_token` WRITE;
/*!40000 ALTER TABLE `authtoken_token` DISABLE KEYS */;
INSERT INTO `authtoken_token` VALUES ('43101e56d3cbb7e01b10f0b9dfca0adb74303ff3','2025-04-12 06:53:24.289496',2),('a51709c4d3b8c632663fce4102af80ca7f0b8b6d','2025-04-23 16:12:02.796535',3);
/*!40000 ALTER TABLE `authtoken_token` ENABLE KEYS */;
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
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(19,'authtoken','token'),(20,'authtoken','tokenproxy'),(5,'contenttypes','contenttype'),(9,'plutusAI','brokerdetails'),(14,'plutusAI','candledata'),(7,'plutusAI','configuration'),(18,'plutusAI','flashdetails'),(10,'plutusAI','indexdetails'),(11,'plutusAI','jobdetails'),(16,'plutusAI','manualorders'),(8,'plutusAI','orderbook'),(12,'plutusAI','paymentdetails'),(13,'plutusAI','scalperdetails'),(15,'plutusAI','userauthtokens'),(17,'plutusAI','webhookdetails'),(6,'sessions','session');
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
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-04-11 16:46:43.866805'),(2,'auth','0001_initial','2025-04-11 16:47:08.693881'),(3,'admin','0001_initial','2025-04-11 16:47:14.869031'),(4,'admin','0002_logentry_remove_auto_add','2025-04-11 16:47:15.001681'),(5,'admin','0003_logentry_add_action_flag_choices','2025-04-11 16:47:15.170190'),(6,'contenttypes','0002_remove_content_type_name','2025-04-11 16:47:18.231127'),(7,'auth','0002_alter_permission_name_max_length','2025-04-11 16:47:21.023681'),(8,'auth','0003_alter_user_email_max_length','2025-04-11 16:47:21.455347'),(9,'auth','0004_alter_user_username_opts','2025-04-11 16:47:21.672399'),(10,'auth','0005_alter_user_last_login_null','2025-04-11 16:47:23.408081'),(11,'auth','0006_require_contenttypes_0002','2025-04-11 16:47:23.537635'),(12,'auth','0007_alter_validators_add_error_messages','2025-04-11 16:47:23.779205'),(13,'auth','0008_alter_user_username_max_length','2025-04-11 16:47:26.678161'),(14,'auth','0009_alter_user_last_name_max_length','2025-04-11 16:47:29.602675'),(15,'auth','0010_alter_group_name_max_length','2025-04-11 16:47:29.866928'),(16,'auth','0011_update_proxy_permissions','2025-04-11 16:47:30.049275'),(17,'auth','0012_alter_user_first_name_max_length','2025-04-11 16:47:33.272035'),(18,'authtoken','0001_initial','2025-04-11 16:47:36.650449'),(19,'authtoken','0002_auto_20160226_1747','2025-04-11 16:47:37.184203'),(20,'authtoken','0003_tokenproxy','2025-04-11 16:47:37.414902'),(21,'authtoken','0004_alter_tokenproxy_options','2025-04-11 16:47:37.632386'),(22,'sessions','0001_initial','2025-04-11 16:47:38.888157'),(23,'plutusAI','0001_initial','2025-04-11 16:58:04.413500'),(24,'plutusAI','0002_alter_manualorders_current_premium_and_more','2025-04-12 06:52:16.630749');
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
INSERT INTO `django_session` VALUES ('012sh8kvhcuf0otiadp75h263qa28qk5','.eJxVjEEOwiAQRe_C2hDo0KG4dO8ZCAMzUjVtUtqV8e7apAvd_vfef6mYtrXGrfESx6LOyqrT70YpP3jaQbmn6TbrPE_rMpLeFX3Qpq9z4eflcP8Oamr1WxOj4JAcGNujD8aTc1l8BhDwoS9WMHgg6QDRoR0osHAxmW0HQmTU-wPPNDex:1u3IBZ:_JRW9jPPhpUPDGwNv-IQp33IfclJl1hfpoUtxvPONmM','2025-04-25 17:29:01.293997'),('4uex0gqcwfskxthvnf9sppvv6agwxhb8','.eJxVjEEOwiAQRe_C2hDo0KG4dO8ZCAMzUjVtUtqV8e7apAvd_vfef6mYtrXGrfESx6LOyqrT70YpP3jaQbmn6TbrPE_rMpLeFX3Qpq9z4eflcP8Oamr1WxOj4JAcGNujD8aTc1l8BhDwoS9WMHgg6QDRoR0osHAxmW0HQmTU-wPPNDex:1u75lo:zAVQEER9AFPWd3riBbPyRDA5eeJmil7maefRhYScElM','2025-05-06 05:02:08.145681'),('7zudw2twmb1lbvunfgus0ox9znns0fjc','.eJxVjEEOwiAQRe_C2hDo0KG4dO8ZCAMzUjVtUtqV8e7apAvd_vfef6mYtrXGrfESx6LOyqrT70YpP3jaQbmn6TbrPE_rMpLeFX3Qpq9z4eflcP8Oamr1WxOj4JAcGNujD8aTc1l8BhDwoS9WMHgg6QDRoR0osHAxmW0HQmTU-wPPNDex:1u75lo:zAVQEER9AFPWd3riBbPyRDA5eeJmil7maefRhYScElM','2025-05-06 05:02:08.915017'),('ivq0461pec5wm4g2hd7jyerk788cnghf','.eJxVjDsOwjAQBe_iGlm2N_5R0nMGy-tdkwCKpTipEHeHSCmgfTPzXiLlbR3T1nlJE4mzAHH63TCXB887oHueb02WNq_LhHJX5EG7vDbi5-Vw_w7G3MdvbUsIVUdviiEHg4qeyGTMpL2PaFQoDgEsD1iBGMBhNNoqy0ZV1pHF-wPZKDek:1u7chY:yZb43mqjKZer6mnaTELvLHHKfSRybH16pTVD_WCRhAQ','2025-05-07 16:11:56.148224'),('lkqqw6t1oab2yhpaohxqaygp40uzlwa5','.eJxVjDsOwjAQBe_iGlm2N_5R0nMGy-tdkwCKpTipEHeHSCmgfTPzXiLlbR3T1nlJE4mzAHH63TCXB887oHueb02WNq_LhHJX5EG7vDbi5-Vw_w7G3MdvbUsIVUdviiEHg4qeyGTMpL2PaFQoDgEsD1iBGMBhNNoqy0ZV1pHF-wPZKDek:1u7cfh:cWXSAK3abz77GHYPSeptGG3GAjgRWtoddxhfxlr9ZNo','2025-05-07 16:10:01.275476'),('y0qrckfrhz98sfxjxf7m1s2tqeqtw4yq','.eJxVjEEOwiAQRe_C2hBkbJm6dN8zkBkYpGogKe3KeHfbpAvd_vfefytP65L92mT2U1RXZdXpd2MKTyk7iA8q96pDLcs8sd4VfdCmxxrldTvcv4NMLW91kL4HiWAJI4UBDZERN3SQEECkI2cTMwte0LAzDEOP58QJ2KLZKvX5AgIVOF8:1u3IJt:bqvh273XTGn0Ad1yWLBQD_rfwcYEbxmZb5dTtpcaDHQ','2025-04-25 17:37:37.869750');
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
  `broker_name` varchar(250) NOT NULL,
  `broker_user_id` varchar(250) NOT NULL,
  `broker_user_name` varchar(250) NOT NULL,
  `broker_mpin` varchar(250) NOT NULL,
  `broker_api_token` varchar(250) NOT NULL,
  `broker_qr` varchar(250) NOT NULL,
  `token_status` varchar(250) NOT NULL,
  `is_demo_trading_enabled` tinyint(1) NOT NULL,
  `index_group` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_brokerdetails`
--

LOCK TABLES `plutusAI_brokerdetails` WRITE;
/*!40000 ALTER TABLE `plutusAI_brokerdetails` DISABLE KEYS */;
INSERT INTO `plutusAI_brokerdetails` VALUES (1,'antonyrajan.d@gmail.com','angel_one','A58033497','Antony Rajan D','5948','pOruxLYZ','RQFCDA2ZX2DMFZ5GR6HXXPFITY','generated',1,'indian_index'),(2,'madara@plutus.com','angel_one','S50761409','SAHAYARAJ  SAHAYARAJ','1005','Q12feFjR','5TXNGVJEVZYMHCLF6HHOQHHTZ4','generated',1,'indian_index'),(3,'user1@gmail.com','angel_one','B12345678','JOHN DOE','1234','aBc123XyZ','QR123ABCXYZ987TOKEN456','generated',1,'indian_index');
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_candledata`
--

LOCK TABLES `plutusAI_candledata` WRITE;
/*!40000 ALTER TABLE `plutusAI_candledata` DISABLE KEYS */;
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
  `user_id` varchar(500) NOT NULL,
  `levels` varchar(5000) NOT NULL,
  `index_name` varchar(50) NOT NULL,
  `start_scheduler` tinyint(1) NOT NULL,
  `strike` varchar(5) NOT NULL,
  `is_place_sl_required` tinyint(1) NOT NULL,
  `trend_check_points` varchar(10) NOT NULL,
  `trailing_points` varchar(10) NOT NULL,
  `initial_sl` varchar(10) NOT NULL,
  `safe_sl` varchar(10) NOT NULL,
  `target_for_safe_sl` varchar(10) NOT NULL,
  `status` varchar(250) NOT NULL,
  `lots` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_configuration`
--

LOCK TABLES `plutusAI_configuration` WRITE;
/*!40000 ALTER TABLE `plutusAI_configuration` DISABLE KEYS */;
INSERT INTO `plutusAI_configuration` VALUES (1,'antonyrajan.d@gmail.com','24230,24300,24400,24500,24600,24100,24000,23900,23800','nifty',0,'100',1,'15','10','25','5','10','stopped','3'),(2,'antonyrajan.d@gmail.com','update levels','bank_nifty',0,'10',1,'50','20','30','10','30','stopped','10'),(3,'antonyrajan.d@gmail.com','update levels','fin_nifty',0,'10',1,'15','10','10','10','10','stopped','10'),(4,'user1@gmail.com','update levels','nifty',0,'10',1,'15','10','10','10','10','stopped','10'),(5,'user1@gmail.com','update levels','bank_nifty',0,'10',1,'50','20','30','10','30','stopped','10'),(6,'user1@gmail.com','update levels','fin_nifty',0,'10',1,'15','10','10','10','10','stopped','10');
/*!40000 ALTER TABLE `plutusAI_configuration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `plutusAI_flashdetails`
--

DROP TABLE IF EXISTS `plutusAI_flashdetails`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `plutusAI_flashdetails` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` varchar(100) NOT NULL,
  `index_name` varchar(20) NOT NULL,
  `strike` varchar(10) NOT NULL,
  `max_profit` varchar(20) NOT NULL,
  `max_loss` varchar(20) NOT NULL,
  `trend_check_points` varchar(10) NOT NULL,
  `trailing_points` varchar(10) NOT NULL,
  `is_demo_trading_enabled` tinyint(1) NOT NULL,
  `lots` varchar(10) NOT NULL,
  `status` varchar(20) NOT NULL,
  `average_points` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_flashdetails`
--

LOCK TABLES `plutusAI_flashdetails` WRITE;
/*!40000 ALTER TABLE `plutusAI_flashdetails` DISABLE KEYS */;
INSERT INTO `plutusAI_flashdetails` VALUES (1,'antonyrajan.d@gmail.com','nifty','100','5000','2000','10','30',1,'2','started','5'),(2,'user1@gmail.com','nifty','100','5000','2000','50','30',1,'2','active','25');
/*!40000 ALTER TABLE `plutusAI_flashdetails` ENABLE KEYS */;
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
  `index_token` varchar(50) NOT NULL,
  `ltp` varchar(50) NOT NULL,
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
INSERT INTO `plutusAI_indexdetails` VALUES (1,'nifty','indian_index','99926000','Internet connection issue','2025-04-22 11:47:15','75','24-APR-2025','30-APR-2025'),(2,'bank_nifty','indian_index','99926009','Internet connection issue','2025-04-22 11:46:33','15','24-APR-2025','29-MAY-2025'),(3,'fin_nifty','indian_index','99926037','Internet connection issue','2025-04-22 11:46:54','25','24-APR-2025','29-MAY-2025'),(4,'bank_nifty_fut','indian_index','35075','54090.0','2024-09-25 14:10:17','15','16-JUL-2024','16-JUL-2024');
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
) ENGINE=InnoDB AUTO_INCREMENT=81 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
  `strike` varchar(100) NOT NULL,
  `lots` varchar(100) NOT NULL,
  `trigger` varchar(100) NOT NULL,
  `time` varchar(100) DEFAULT NULL,
  `order_id` varchar(100) DEFAULT NULL,
  `unique_order_id` varchar(100) DEFAULT NULL,
  `current_premium` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_manualorders`
--

LOCK TABLES `plutusAI_manualorders` WRITE;
/*!40000 ALTER TABLE `plutusAI_manualorders` DISABLE KEYS */;
INSERT INTO `plutusAI_manualorders` VALUES (1,'antonyrajan.d@gmail.com','nifty','10','5','order_placed','100','1','3','123',NULL,'2799ebd7-6633-4429-b97e-f12333c470c4','NIFTY17APR2522750CE'),(2,'antonyrajan.d@gmail.com','bank_nifty','15','7','order_placed','100','2','5','123',NULL,'ad2110e4-a923-4dfe-84f2-e0d2e64a97ce','BANKNIFTY24APR2550900CE'),(3,'antonyrajan.d@gmail.com','fin_nifty','8','4','order_placed','100','1','2','123',NULL,NULL,NULL),(4,'user1@gmail.com','nifty','10','5','order_placed','100','1','3','123',NULL,NULL,NULL),(5,'user1@gmail.com','bank_nifty','15','7','order_placed','100','2','5','123',NULL,NULL,NULL),(6,'user1@gmail.com','fin_nifty','8','4','order_placed','100','1','2','123',NULL,NULL,NULL);
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
  `exit_time` varchar(500) DEFAULT NULL,
  `script_name` varchar(250) NOT NULL,
  `qty` varchar(250) NOT NULL,
  `entry_price` varchar(250) NOT NULL,
  `exit_price` varchar(250) DEFAULT NULL,
  `status` varchar(250) NOT NULL,
  `total` varchar(250) DEFAULT NULL,
  `strategy` varchar(250) DEFAULT NULL,
  `index_name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_orderbook`
--

LOCK TABLES `plutusAI_orderbook` WRITE;
/*!40000 ALTER TABLE `plutusAI_orderbook` DISABLE KEYS */;
INSERT INTO `plutusAI_orderbook` VALUES (1,'antonyrajan.d@gmail.com','1744434451.174892',NULL,'NIFTY17APR2522860PE','75','Internet connection issue',NULL,'order_placed',NULL,'hunter','nifty'),(2,'antonyrajan.d@gmail.com','1744434608.444632',NULL,'NIFTY17APR2522840CE','75','Internet connection issue',NULL,'order_placed',NULL,'hunter','nifty'),(3,'antonyrajan.d@gmail.com','1744434718.890894',NULL,'NIFTY17APR2522840CE','75','Internet connection issue',NULL,'order_placed',NULL,'hunter','nifty'),(4,'antonyrajan.d@gmail.com','1744434787.637859','1744434801.821981','NIFTY17APR2522750CE','75','312.25','312.25','order_exited','0.0','hunter','nifty'),(5,'antonyrajan.d@gmail.com','1744434802.806942','1744434818.559204','NIFTY17APR2522950PE','75','291.55','291.55','order_exited','0.0','hunter','nifty'),(6,'antonyrajan.d@gmail.com','1745301280.684852','1745301473.652157','NIFTY24APR2524300PE','75','156.35','161.35','order_exited','375.0','hunter','nifty');
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
  `target` varchar(100) NOT NULL,
  `is_demo_trading_enabled` tinyint(1) NOT NULL,
  `use_full_capital` tinyint(1) NOT NULL,
  `lots` varchar(10) NOT NULL,
  `on_candle_close` tinyint(1) NOT NULL,
  `status` varchar(250) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_scalperdetails`
--

LOCK TABLES `plutusAI_scalperdetails` WRITE;
/*!40000 ALTER TABLE `plutusAI_scalperdetails` DISABLE KEYS */;
INSERT INTO `plutusAI_scalperdetails` VALUES (1,'antonyrajan.d@gmail.com','nifty','100','10',1,0,'2',1,'stopped'),(2,'user1@gmail.com','nifty','100','10',1,0,'2',1,'running');
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
  `jwtToken` varchar(2000) NOT NULL,
  `feedToken` varchar(2000) NOT NULL,
  `last_updated_time` varchar(500) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `plutusAI_userauthtokens`
--

LOCK TABLES `plutusAI_userauthtokens` WRITE;
/*!40000 ALTER TABLE `plutusAI_userauthtokens` DISABLE KEYS */;
INSERT INTO `plutusAI_userauthtokens` VALUES (1,'antonyrajan.d@gmail.com','eyJhbGciOiJIUzUxMiJ9.eyJ0b2tlbiI6IlJFRlJFU0gtVE9LRU4iLCJSRUZSRVNILVRPS0VOIjoiZXlKaGJHY2lPaUpTVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5WDNSNWNHVWlPaUpqYkdsbGJuUWlMQ0owYjJ0bGJsOTBlWEJsSWpvaWRISmhaR1ZmY21WbWNtVnphRjkwYjJ0bGJpSXNJbWR0WDJsa0lqb3dMQ0p6YjNWeVkyVWlPaUl6SWl3aVpHVjJhV05sWDJsa0lqb2lPRGs0TWpaak1USXRZakE0WkMwek5qRTFMVGt6T1dJdFlqTTFaVGN5WVRkbE56QmpJaXdpYTJsa0lqb2lkSEpoWkdWZmEyVjVYM1l5SWl3aWIyMXVaVzFoYm1GblpYSnBaQ0k2TUN3aWFYTnpJam9pYkc5bmFXNWZjMlZ5ZG1salpTSXNJbk4xWWlJNklrRTFPREF6TXpRNU55SXNJbVY0Y0NJNk1UYzBOVE00TlRFNU5Td2libUptSWpveE56UTFNams0TmpFMUxDSnBZWFFpT2pFM05EVXlPVGcyTVRVc0ltcDBhU0k2SW1VMVlUVTRPR1F6TFdJNE9EZ3ROR1kwWXkwNU1tVmxMVGczWkRObVpETTNNRGc0TVNJc0lsUnZhMlZ1SWpvaUluMC5BSW11eG5iS19IdmJ5dGxWYUFGLVZ0aHJsdzZXQU00ZjFNUkYzT2FybUpZd3V0Vm03YjJ0NEhKX0tDaTdzaDBYaWp3VVlMeUVRdVZyWGdQWVZnS000anJRWk8xelNFcTR2T0VvNlI4bDVaYnFZTVVJUVRUZjU2MkFrOFQxeWN4ZWJoX2F0LTlRRjF6dmpORWU2aEZyNDV0a2F3WGxxVHpFQnhTWU9odE1sbWMiLCJpYXQiOjE3NDUyOTg3OTV9.h0HrbKlgXjWyIdsD8nLfhpnN9m1M1r1wNRd-eQiEyM05kx1sBeY6EuXpHlxX-deOXXPCCVIF0jhyl0gUvriH1g','eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6IkE1ODAzMzQ5NyIsInJvbGVzIjowLCJ1c2VydHlwZSI6IlVTRVIiLCJ0b2tlbiI6ImV5SmhiR2NpT2lKU1V6STFOaUlzSW5SNWNDSTZJa3BYVkNKOS5leUoxYzJWeVgzUjVjR1VpT2lKamJHbGxiblFpTENKMGIydGxibDkwZVhCbElqb2lkSEpoWkdWZllXTmpaWE56WDNSdmEyVnVJaXdpWjIxZmFXUWlPallzSW5OdmRYSmpaU0k2SWpNaUxDSmtaWFpwWTJWZmFXUWlPaUk0T1RneU5tTXhNaTFpTURoa0xUTTJNVFV0T1RNNVlpMWlNelZsTnpKaE4yVTNNR01pTENKcmFXUWlPaUowY21Ga1pWOXJaWGxmZGpJaUxDSnZiVzVsYldGdVlXZGxjbWxrSWpvMkxDSndjbTlrZFdOMGN5STZleUprWlcxaGRDSTZleUp6ZEdGMGRYTWlPaUpoWTNScGRtVWlmU3dpYldZaU9uc2ljM1JoZEhWeklqb2lZV04wYVhabEluMHNJbTVpZFY5c1pXNWthVzVuSWpwN0luTjBZWFIxY3lJNkltRmpkR2wyWlNKOWZTd2lhWE56SWpvaWRISmhaR1ZmYkc5bmFXNWZjMlZ5ZG1salpTSXNJbk4xWWlJNklrRTFPREF6TXpRNU55SXNJbVY0Y0NJNk1UYzBOVE00TlRFNU5Td2libUptSWpveE56UTFNams0TmpFMUxDSnBZWFFpT2pFM05EVXlPVGcyTVRVc0ltcDBhU0k2SWpkbU9HSTBPR00xTFROa1ltVXRORFkwTVMxaE1qRmtMVGd4TVRoalpqQmlNR1EwWXlJc0lsUnZhMlZ1SWpvaUluMC53NlhOeEFwWlhjX0huTEVxcmRSeDNIcGhVSjlkemdSc2lpREk5NHhFaFo0SldqSlRTZTFRWFptdnZycUZCNDBPRFU2S0FaMzZxQURCcTd2bzJ2bGFIb0FjbGlRQUtSY1J1QlJMTVRXM0FybGg5SjBDeWtmMEVGdENlaUI4ZUhmUVhaVU91eDNsVWtlVUpZXzY0cmllbzdOUEtrcjBuQUMyMmJrejBnWXM2Z0EiLCJBUEktS0VZIjoicE9ydXhMWVoiLCJpYXQiOjE3NDUyOTg3OTUsImV4cCI6MTc0NTM4NTE5NX0.NeEDiEX14E_laM1_55f5q-o7Tu4bWh3mFuqg5tg2BZ9O37nfiUfT-f9JSRd5uW_jLLYqTAVkRcHQpzGEvt2zdA','eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6IkE1ODAzMzQ5NyIsImlhdCI6MTc0NTI5ODc5NSwiZXhwIjoxNzQ1Mzg1MTk1fQ.VFapRvNjX-4ldIoPPVIS3TsARh5vWiNwGmmjon0I1z6AMvAgb0clY9rbqU9_mrFXqBt_X8_KzZU8l_h2P2m9TA','1745298795.556541'),(2,'madara@plutus.com','eyJhbGciOiJIUzUxMiJ9.eyJ0b2tlbiI6IlJFRlJFU0gtVE9LRU4iLCJSRUZSRVNILVRPS0VOIjoiZXlKaGJHY2lPaUpTVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5WDNSNWNHVWlPaUpqYkdsbGJuUWlMQ0owYjJ0bGJsOTBlWEJsSWpvaWRISmhaR1ZmY21WbWNtVnphRjkwYjJ0bGJpSXNJbWR0WDJsa0lqb3dMQ0p6YjNWeVkyVWlPaUl6SWl3aVpHVjJhV05sWDJsa0lqb2lORGd4T0dFME5Ea3RZamc1WVMwek5HSXhMVGc1TVRVdE4yRmlPVGRpTlRSa09EVTFJaXdpYTJsa0lqb2lkSEpoWkdWZmEyVjVYM1l5SWl3aWIyMXVaVzFoYm1GblpYSnBaQ0k2TUN3aWFYTnpJam9pYkc5bmFXNWZjMlZ5ZG1salpTSXNJbk4xWWlJNklsTTFNRGMyTVRRd09TSXNJbVY0Y0NJNk1UYzBOVE00TlRFd01Dd2libUptSWpveE56UTFNams0TlRJd0xDSnBZWFFpT2pFM05EVXlPVGcxTWpBc0ltcDBhU0k2SW1VMU5ESm1ZVFU0TFRZMk5EVXRORGN5TlMwNVpqTXpMVFk1T0dZeFltRTFPRFZtWVNJc0lsUnZhMlZ1SWpvaUluMC5NTHJYRXQ5SFg2UGhQZDl2VkI0UDhIQ09MdGJvdjJQclFrNTV4ZmNqTDNhZXMxczgtQy1KWVhJcnBkVXlLajJpY3hjVjYxcFNGZ0k3b0xmQUlRbGZQVmFfRms2WWNUN3QtRWk0c05xckxrM0kxLUNDT1dYYzYxSFU2bXJXOVM4THhQLTdrc1ZWakdvNWYzeHUzZGEwcGJOQWFYRUJVMVRkRF9lTmdQQno4VWciLCJpYXQiOjE3NDUyOTg3MDB9.quO7mACZoYcBr26kLo3HL7CzKS6rV53bex7x2P9lYubMmKy-ekxKZDQIc4x4G8Qb8z11mkiGbFU0PnqjkyUGag','eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6IlM1MDc2MTQwOSIsInJvbGVzIjowLCJ1c2VydHlwZSI6IlVTRVIiLCJ0b2tlbiI6ImV5SmhiR2NpT2lKU1V6STFOaUlzSW5SNWNDSTZJa3BYVkNKOS5leUoxYzJWeVgzUjVjR1VpT2lKamJHbGxiblFpTENKMGIydGxibDkwZVhCbElqb2lkSEpoWkdWZllXTmpaWE56WDNSdmEyVnVJaXdpWjIxZmFXUWlPakV4TENKemIzVnlZMlVpT2lJeklpd2laR1YyYVdObFgybGtJam9pTkRneE9HRTBORGt0WWpnNVlTMHpOR0l4TFRnNU1UVXROMkZpT1RkaU5UUmtPRFUxSWl3aWEybGtJam9pZEhKaFpHVmZhMlY1WDNZeUlpd2liMjF1WlcxaGJtRm5aWEpwWkNJNk1URXNJbkJ5YjJSMVkzUnpJanA3SW1SbGJXRjBJanA3SW5OMFlYUjFjeUk2SW1GamRHbDJaU0o5TENKdFppSTZleUp6ZEdGMGRYTWlPaUpoWTNScGRtVWlmWDBzSW1semN5STZJblJ5WVdSbFgyeHZaMmx1WDNObGNuWnBZMlVpTENKemRXSWlPaUpUTlRBM05qRTBNRGtpTENKbGVIQWlPakUzTkRVek9EVXhNREFzSW01aVppSTZNVGMwTlRJNU9EVXlNQ3dpYVdGMElqb3hOelExTWprNE5USXdMQ0pxZEdraU9pSmlNV1ZpWW1RMVpTMWxNV000TFRSaVpUVXRPRE5qTmkwM05XRTJPR1prWTJNNVlXSWlMQ0pVYjJ0bGJpSTZJaUo5LmRCM0VKYTJiUTMtUjN2Q1pUZlYtb3ZLaWRWdWtyUnJuYU5RS1JORW5SQ21LbTJ4YTFDZjgzU01QMHN3ZDNXM3cyWlh0MTdRY1NySDZkRVpGSUZyVkZvdTRiMnpLUW91MnVXdVM0VVVEU1BCbDN1clQ1YS1BaUxZTXY1bXRJUldvZG5RT2FnS0ZaQXBxLUZEUldyUDBqenlhU05Ra01saVFDZXI0WUJfcDlMNCIsIkFQSS1LRVkiOiJRMTJmZUZqUiIsImlhdCI6MTc0NTI5ODcwMCwiZXhwIjoxNzQ1Mzg1MTAwfQ.V3a2IpwDJxaVUdRLDx_Tqe0hrQZkZvpK2bUYWmIZNnlbq7lWvWDGt_o0wWPMctV9zfydpw41I6iyoOioDOVvEA','eyJhbGciOiJIUzUxMiJ9.eyJ1c2VybmFtZSI6IlM1MDc2MTQwOSIsImlhdCI6MTc0NTI5ODcwMCwiZXhwIjoxNzQ1Mzg1MTAwfQ.l3Y7rkM0ID8xXsy9lza5DAmEk5TrsSTu-60aWZKsCiCjMIvIFx5Hnc6cEiF1unxZKoKhCeAd1NVr7yQjq11MNQ','1745298700.204404');
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
  `target` varchar(100) DEFAULT NULL,
  `order_status` varchar(100) NOT NULL,
  `time` varchar(100) NOT NULL,
  `is_demo_trading_enabled` tinyint(1) NOT NULL,
  `strategy` varchar(100) NOT NULL,
  `order_id` varchar(100) NOT NULL,
  `unique_order_id` varchar(100) NOT NULL,
  `current_premium` varchar(100) NOT NULL,
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

-- Dump completed on 2025-04-23 21:50:45
