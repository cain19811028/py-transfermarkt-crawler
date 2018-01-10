/*
Navicat MySQL Data Transfer

Source Server         : Local
Source Server Version : 50714
Source Host           : localhost:3306
Source Database       : transfermarkt

Target Server Type    : MYSQL
Target Server Version : 50714
File Encoding         : 65001

Date: 2017-08-26 22:38:58
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for position
-- ----------------------------
DROP TABLE IF EXISTS `position`;
CREATE TABLE `position` (
  `id` tinyint(2) NOT NULL,
  `type` varchar(10) DEFAULT NULL,
  `position` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of position
-- ----------------------------
INSERT INTO `position` VALUES ('1', 'Goalkeeper', 'Keeper');
INSERT INTO `position` VALUES ('4', 'Defence', 'Sweeper');
INSERT INTO `position` VALUES ('5', 'Defence', 'Centre-Back');
INSERT INTO `position` VALUES ('2', 'Defence', 'Left-Back');
INSERT INTO `position` VALUES ('3', 'Defence', 'Right-Back');
INSERT INTO `position` VALUES ('6', 'Midfield', 'Defensive Midfield');
INSERT INTO `position` VALUES ('7', 'Midfield', 'Left Midfield');
INSERT INTO `position` VALUES ('8', 'Midfield', 'Right Midfield');
INSERT INTO `position` VALUES ('9', 'Midfield', 'Central Midfield');
INSERT INTO `position` VALUES ('10', 'Midfield', 'Attacking Midfield');
INSERT INTO `position` VALUES ('11', 'Striker', 'Left Wing');
INSERT INTO `position` VALUES ('12', 'Striker', 'Right Wing');
INSERT INTO `position` VALUES ('13', 'Striker', 'Secondary Striker');
INSERT INTO `position` VALUES ('14', 'Striker', 'Centre-Forward');
