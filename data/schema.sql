-- MySQL dump 10.16  Distrib 10.1.34-MariaDB, for Win32 (AMD64)
--
-- Host: localhost    Database: ab_slack
-- ------------------------------------------------------
-- Server version	10.1.34-MariaDB

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
-- Temporary table structure for view `post_view`
--

DROP TABLE IF EXISTS `post_view`;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
CREATE TABLE `post_view` (
  `post_time` tinyint NOT NULL,
  `post_subject` tinyint NOT NULL,
  `post_text` tinyint NOT NULL,
  `username` tinyint NOT NULL,
  `user_id` tinyint NOT NULL,
  `type` tinyint NOT NULL
) ENGINE=MyISAM;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `t_channel`
--

DROP TABLE IF EXISTS `t_channel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_channel` (
  `id` varchar(512) NOT NULL,
  `name` varchar(1024) DEFAULT NULL,
  `created` INTEGER,
  `creator` varchar(1024) DEFAULT NULL,
  `is_archived` BOOLEAN DEFAULT False,
  `is_general` BOOLEAN DEFAULT False,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `t_channel_members`
--

DROP TABLE IF EXISTS `t_channel_members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_channel_members` (
  `id` varchar(512) NOT NULL,
  `member` varchar(512), /*'id' in t_user*/
  `parent_id` varchar(512), /*'id' of t_channel*/
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `t_channel_pins`
--

DROP TABLE IF EXISTS `t_channel_pins`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_channel_pins` (
  `id` varchar(512) NOT NULL,
  `type` varchar(1024) DEFAULT NULL,
  `created` INTEGER,
  `user` varchar(1024) DEFAULT NULL, /*'id' in t_user*/
  `owner` varchar(1024) DEFAULT NULL, /*'id' in t_user*/
  `parent_id` varchar(512), /*'id' of t_channel*/
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=93 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `t_channel_topic`
--

DROP TABLE IF EXISTS `t_channel_topic`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_channel_topic` (
  `value` varchar(1024) DEFAULT NULL,
  `creator` varchar(1024) DEFAULT NULL,
  `last_set` INTEGER,
  `parent_id` varchar(512), /*'id' in t_channel*/
  PRIMARY KEY (`parent_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `t_channel_purpose`
--

DROP TABLE IF EXISTS `t_channel_purpose`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_channel_purpose` (
  `value` varchar(1024) DEFAULT NULL,
  `creator` varchar(1024) DEFAULT NULL,
  `last_set` INTEGER,
  `parent_id` varchar(512), /*'id' in t_channel*/
  PRIMARY KEY (`parent_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `t_message`
--

DROP TABLE IF EXISTS `t_message`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_message` (
  `id_str` varchar(512) NOT NULL,
  `dirname` varchar(1024) DEFAULT NULL,
  `filename` varchar(1024) DEFAULT NULL,
  `client_msg_id` varchar(1024) DEFAULT NULL,
  `type` varchar(1024) DEFAULT NULL,
  `subtype` varchar(1024) DEFAULT NULL,
  `text` text,
  `purpose` varchar(1024) DEFAULT NULL,
  `topic` varchar(1024) DEFAULT NULL,
  `user` varchar(512),
  `ts` varchar(1024) DEFAULT NULL,
  `team` varchar(1024) DEFAULT NULL,
  `user_team` varchar(1024) DEFAULT NULL,
  `source_team` varchar(1024) DEFAULT NULL,
  `thread_ts` varchar(1024) DEFAULT NULL,
  `parent_user_id` varchar(512), /*'id' of t_user*/
  `reply_count` INTEGER DEFAULT 0,
  `reply_users_count` INTEGER DEFAULT 0,
  `latest_reply` varchar(1024) DEFAULT NULL,
  `last_read` varchar(1024) DEFAULT NULL,
  `subscribed` BOOLEAN DEFAULT FALSE,
  `upload` BOOLEAN DEFAULT FALSE,
  `display_as_bot` BOOLEAN DEFAULT FALSE,
  `inviter` varchar(1024) DEFAULT NULL,
  `bot_id` varchar(1024) DEFAULT NULL,
  PRIMARY KEY (`id_str`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `t_message_root`
--

DROP TABLE IF EXISTS `t_message_root`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_message_root` (
  `client_msg_id` varchar(512) DEFAULT NULL,
  `type` varchar(512) DEFAULT NULL,
  `text` text,
  `user` varchar(512),
  `ts` varchar(1024) DEFAULT NULL,
  `team` varchar(1024) DEFAULT NULL,
  `thread_ts` varchar(1024) DEFAULT NULL,
  `reply_count` INTEGER DEFAULT 0,
  `reply_users_count` INTEGER DEFAULT 0,
  `latest_reply` varchar(1024) DEFAULT NULL,
  `subscribed` BOOLEAN DEFAULT FALSE,
  `parent_id` varchar(512), /*'id_str' of t_message*/
  PRIMARY KEY (`parent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `t_message_root_reply_users`
--

DROP TABLE IF EXISTS `t_message_root_reply_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_message_root_reply_users` (
  `id` varchar(512) NOT NULL,
  `user` varchar(512),
  `parent_id` varchar(512), /*'parent_id' in t_message_root*/
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `t_message_edited`
--

DROP TABLE IF EXISTS `t_message_edited`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_message_edited` (
  `user` varchar(512),
  `ts` varchar(1024),
  `parent_id` varchar(512), /*'id' in t_message*/
  PRIMARY KEY (`parent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `t_message_reactions`
--

DROP TABLE IF EXISTS `t_message_reactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_message_reactions` (
  `id` varchar(512) NOT NULL,
  `name` varchar(1024) DEFAULT NULL,
  `count` INTEGER,
  `parent_id` varchar(512), /*'id' in t_message*/
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `t_message_reactions_users`
--

DROP TABLE IF EXISTS `t_message_reactions_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_message_reactions_users` (
  `id` varchar(512),
  `user` varchar(512), /*'id' in t_user*/
  `parent_id` varchar(512), /*'id' in t_message_reactions*/
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `t_message_replies`
--

DROP TABLE IF EXISTS `t_message_replies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_message_replies` (
  `id` varchar(512) NOT NULL,
  `user` varchar(512), /*'id' in t_user*/
  `ts` varchar(1024),
  `parent_id` varchar(512), /*'id' in t_message*/
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `t_message_reply_users`
--

DROP TABLE IF EXISTS `t_message_reply_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_message_reply_users` (
  `id` varchar(512),
  `user` varchar(512), /*'id' in t_user*/
  `parent_id` varchar(512), /*'id' of t_message*/
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `t_message_files`
--

DROP TABLE IF EXISTS `t_message_files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_message_files` (
  `id` varchar(512) NOT NULL,
  `user` varchar(1024) DEFAULT NULL,
  `ts` varchar(1024) DEFAULT NULL,
  `created` int(11) DEFAULT NULL,
  `timestamp` int(11) DEFAULT NULL,
  `name` varchar(1024) DEFAULT NULL,
  `title` varchar(1024) DEFAULT NULL,
  `mimetype` varchar(1024) DEFAULT NULL,
  `filetype` varchar(1024) DEFAULT NULL,
  `pretty_type` varchar(1024) DEFAULT NULL,
  `editable` BOOLEAN DEFAULT FALSE,
  `size` int(11) DEFAULT NULL,
  `mode` varchar(1024) DEFAULT NULL,
  `is_external` BOOLEAN DEFAULT FALSE,
  `external_type` varchar(1024) DEFAULT NULL,
  `is_public` BOOLEAN DEFAULT FALSE,
  `public_url_shared` BOOLEAN DEFAULT FALSE,
  `display_as_bot` BOOLEAN DEFAULT FALSE,
  `username` varchar(1024) DEFAULT NULL,
  `url_private` varchar(1024) DEFAULT NULL,
  `url_private_download` varchar(1024) DEFAULT NULL,
  `permalink` varchar(1024) DEFAULT NULL,
  `permalink_public` varchar(1024) DEFAULT NULL,
  `preview` text DEFAULT NULL,
  `updated` int(11) DEFAULT NULL,
  `editor` varchar(1024) DEFAULT NULL,
  `last_editor` varchar(1024) DEFAULT NULL,
  `state` varchar(1024) DEFAULT NULL,
  `thumb_64` varchar(1024) DEFAULT NULL,
  `thumb_80` varchar(1024) DEFAULT NULL,
  `thumb_360` varchar(1024) DEFAULT NULL,
  `thumb_360_w` int(11) DEFAULT NULL,
  `thumb_360_h` int(11) DEFAULT NULL,
  `thumb_160` varchar(1024) DEFAULT NULL,
  `image_exif_rotation` int(11) DEFAULT NULL,
  `original_w` int(11) DEFAULT NULL,
  `original_h` int(11) DEFAULT NULL,
  `thumb_480` varchar(1024) DEFAULT NULL,
  `thumb_480_w` int(11) DEFAULT NULL,
  `thumb_480_h` int(11) DEFAULT NULL,
  `thumb_720` varchar(1024) DEFAULT NULL,
  `thumb_720_w` int(11) DEFAULT NULL,
  `thumb_720_h` int(11) DEFAULT NULL,
  `thumb_800` varchar(1024) DEFAULT NULL,
  `thumb_800_w` int(11) DEFAULT NULL,
  `thumb_800_h` int(11) DEFAULT NULL,
  `thumb_960` varchar(1024) DEFAULT NULL,
  `thumb_960_w` int(11) DEFAULT NULL,
  `thumb_960_h` int(11) DEFAULT NULL,
  `thumb_1024` varchar(1024) DEFAULT NULL,
  `thumb_1024_w` int(11) DEFAULT NULL,
  `thumb_1024_h` int(11) DEFAULT NULL,
  `thumb_tiny` varchar(1024) DEFAULT NULL,
  `is_starred` BOOLEAN DEFAULT FALSE,
  `has_rich_preview` BOOLEAN DEFAULT FALSE,
  `parent_id` varchar(512), /*'id_str' of t_message*/
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `t_message_blocks`
--

-- DROP TABLE IF EXISTS `t_message_blocks`;
-- /*!40101 SET @saved_cs_client     = @@character_set_client */;
-- /*!40101 SET character_set_client = utf8 */;
-- CREATE TABLE `t_message_blocks` (
--   `block_id` varchar(512) NOT NULL,
--   `type` varchar(1024) DEFAULT NULL,
--   `parent_id` varchar(512), /*'id_str' of t_message*/
--   PRIMARY KEY (`block_id`)
-- ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
-- /*!40101 SET character_set_client = @saved_cs_client */;

-- --
-- -- Table structure for table `t_message_blocks_elements`
-- --

-- DROP TABLE IF EXISTS `t_message_blocks_elements`;
-- /*!40101 SET @saved_cs_client     = @@character_set_client */;
-- /*!40101 SET character_set_client = utf8 */;
-- CREATE TABLE `t_message_blocks_elements` (
--   `id` int(11) NOT NULL AUTO_INCREMENT,
--   `type` varchar(1024) DEFAULT NULL,
--   `parent_id` varchar(512), /*'block_id' in t_message_blocks*/
--   PRIMARY KEY (`id`)
-- ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
-- /*!40101 SET character_set_client = @saved_cs_client */;

-- --
-- -- Table structure for table `t_message_blocks_elements_elements`
-- --

-- DROP TABLE IF EXISTS `t_message_blocks_elements_elements`;
-- /*!40101 SET @saved_cs_client     = @@character_set_client */;
-- /*!40101 SET character_set_client = utf8 */;
-- CREATE TABLE `t_message_blocks_elements_elements` (
--   `id` int(11) NOT NULL AUTO_INCREMENT,
--   `type` varchar(1024) DEFAULT NULL, /*[user, text, emoji]*/
--   `user_id` varchar(1024) DEFAULT NULL, /*user being tagged*/
--   `text` text,
--   `name` varchar(1024) DEFAULT NULL, /*name of emoji*/
--   `channel_id` varchar(512) DEFAULT NULL,
--   `parent_id` int(11), /*'id' in t_message_blocks_elements*/
--   PRIMARY KEY (`id`)
-- ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
-- /*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `t_user`
--

DROP TABLE IF EXISTS `t_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_user` (
  `id` varchar(512) NOT NULL,
  `team_id` varchar(1024) DEFAULT NULL,
  `name` varchar(1024) DEFAULT NULL,
  `deleted` BOOLEAN DEFAULT False,
  `color` varchar(1024) DEFAULT NULL,
  `real_name` varchar(1024) DEFAULT NULL,
  `tz` varchar(1024) DEFAULT NULL,
  `tz_label` varchar(1024) DEFAULT NULL,
  `tz_offset` INTEGER,
  `is_admin` BOOLEAN DEFAULT False,
  `is_owner` BOOLEAN DEFAULT False,
  `is_primary_owner` BOOLEAN DEFAULT False,
  `is_restricted` BOOLEAN DEFAULT False,
  `is_ultra_restricted` BOOLEAN DEFAULT False,
  `is_bot` BOOLEAN DEFAULT False,
  `is_app_user` BOOLEAN DEFAULT False,
  `updated` INTEGER,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `t_user_profile`
--

DROP TABLE IF EXISTS `t_user_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_user_profile` (
  `email` varchar(255) DEFAULT NULL,
  `title` varchar(1024) DEFAULT NULL,
  `phone` varchar(1024) DEFAULT NULL,
  `skype` varchar(1024) DEFAULT NULL,
  `real_name` varchar(1024) DEFAULT NULL,
  `real_name_normalized` varchar(1024) DEFAULT NULL,
  `display_name` varchar(1024) DEFAULT NULL,
  `display_name_normalized` varchar(1024) DEFAULT NULL,
  `fields` varchar(1024) DEFAULT NULL,
  `status_text` varchar(1024) DEFAULT NULL,
  `status_emoji` varchar(1024) DEFAULT NULL,
  `status_expiration` INTEGER,
  `avatar_hash` varchar(1024) DEFAULT NULL,
  `image_original` varchar(1024) DEFAULT NULL,
  `is_custom_image` tinyint(1) DEFAULT NULL,
  `first_name` varchar(1024) DEFAULT NULL,
  `last_name` varchar(1024) DEFAULT NULL,
  `image_24` varchar(1024) DEFAULT NULL,
  `image_32` varchar(1024) DEFAULT NULL,
  `image_48` varchar(1024) DEFAULT NULL,
  `image_72` varchar(1024) DEFAULT NULL,
  `image_192` varchar(1024) DEFAULT NULL,
  `image_512` varchar(1024) DEFAULT NULL,
  `image_1024` varchar(1024) DEFAULT NULL,
  `status_text_canonical` varchar(1024) DEFAULT NULL,
  `team` varchar(1024) DEFAULT NULL,
  `bot_id` varchar(1024) DEFAULT NULL,
  `api_app_id` varchar(1024) DEFAULT NULL,
  `always_active` BOOLEAN DEFAULT FALSE,
  `parent_id` varchar(512), /*'id' of t_user*/
  PRIMARY KEY (`parent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Temporary table structure for view `user_view`
--

DROP TABLE IF EXISTS `user_view`;
/*!50001 DROP VIEW IF EXISTS `user_view`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `user_view` (
  `id` tinyint NOT NULL,
  `email` tinyint NOT NULL,
  `real_name` tinyint NOT NULL,
  `username` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `post_view`
--

/*!50001 DROP TABLE IF EXISTS `post_view`*/;
/*!50001 DROP VIEW IF EXISTS `post_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `post_view` AS select from_unixtime(`p`.`ts`) AS `post_time`,`p`.`dirname` AS `post_subject`,`p`.`text` AS `post_text`,`u`.`username` AS `username`,`u`.`id` AS `user_id`,(case when (`p`.`subtype` > '') then `p`.`subtype` else `p`.`type` end) AS `type` from (`t_message` `p` join `user_view` `u` on((`p`.`user` = `u`.`id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `user_view`
--

/*!50001 DROP TABLE IF EXISTS `user_view`*/;
/*!50001 DROP VIEW IF EXISTS `user_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `user_view` AS select `u`.`id` AS `id`,`p`.`email` AS `email`,`p`.`real_name` AS `real_name`,(case when (`p`.`display_name` > '') then `p`.`display_name` else `u`.`name` end) AS `username` from (`t_user` `u` join `t_user_profile` `p` on((`u`.`id` = `p`.`parent_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-06-04 18:38:45
