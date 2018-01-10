/*
Navicat MySQL Data Transfer

Source Server         : Local
Source Server Version : 50714
Source Host           : localhost:3306
Source Database       : transfermarkt

Target Server Type    : MYSQL
Target Server Version : 50714
File Encoding         : 65001

Date: 2017-08-26 22:40:55
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for country
-- ----------------------------
DROP TABLE IF EXISTS `country`;
CREATE TABLE `country` (
  `id` int(5) NOT NULL,
  `code` varchar(3) DEFAULT NULL,
  `name` varchar(20) DEFAULT NULL,
  `cname` varchar(15) DEFAULT NULL,
  `flag_id` int(4) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `index_code` (`code`) USING BTREE
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of country
-- ----------------------------
INSERT INTO `country` VALUES ('3437', 'ARG', 'Argentina', '阿根廷', '9');
INSERT INTO `country` VALUES ('3433', 'AUS', 'Australia', '澳大利亞', '12');
INSERT INTO `country` VALUES ('3382', 'BEL', 'Belgium', '比利時', '19');
INSERT INTO `country` VALUES ('3394', 'BGR', 'Bulgaria', '保加利亞', '28');
INSERT INTO `country` VALUES ('3446', 'BIH', 'Bosnia-Herzegovina', '波士尼亞', '24');
INSERT INTO `country` VALUES ('3439', 'BRA', 'Brazil', '巴西', '26');
INSERT INTO `country` VALUES ('3510', 'CAN', 'Canada', '加拿大', '80');
INSERT INTO `country` VALUES ('3700', 'CHI', 'Chile', '智利', '33');
INSERT INTO `country` VALUES ('5598', 'CHN', 'China', '中國', '34');
INSERT INTO `country` VALUES ('3591', 'CIV', 'Ivory Coast', '象牙海岸', '38');
INSERT INTO `country` VALUES ('3434', 'CMR', 'Cameroon', '喀麥隆', '31');
INSERT INTO `country` VALUES ('3816', 'COL', 'Colombia', '哥倫比亞', '83');
INSERT INTO `country` VALUES ('3854', 'COD', 'DR Congo', '剛果民主共和國', '193');
INSERT INTO `country` VALUES ('3556', 'CRO', 'Croatia', '克羅埃西亞', '37');
INSERT INTO `country` VALUES ('3445', 'CZE', 'Czech', '捷克', '172');
INSERT INTO `country` VALUES ('3436', 'DEN', 'Denmark', '丹麥', '39');
INSERT INTO `country` VALUES ('3614', 'DZA', 'Algeria', '阿爾及利亞', '4');
INSERT INTO `country` VALUES ('5750', 'ECU', 'Ecuador', '厄瓜多', '44');
INSERT INTO `country` VALUES ('3672', 'EGY', 'Egypt', '埃及', '2');
INSERT INTO `country` VALUES ('3299', 'ENG', 'England', '英格蘭', '189');
INSERT INTO `country` VALUES ('3443', 'FIN', 'Finland', '芬蘭', '49');
INSERT INTO `country` VALUES ('3377', 'FRA', 'France', '法國', '50');
INSERT INTO `country` VALUES ('3262', 'GER', 'Germany', '德國', '40');
INSERT INTO `country` VALUES ('3441', 'GHA', 'Ghana', '迦納', '54');
INSERT INTO `country` VALUES ('3378', 'GRE', 'Greece', '希臘', '56');
INSERT INTO `country` VALUES ('3590', 'HND', 'Honduras', '宏都拉斯', '66');
INSERT INTO `country` VALUES ('3509', 'IRL', 'Ireland', '愛爾蘭', '72');
INSERT INTO `country` VALUES ('3574', 'ISL', 'Iceland', '冰島', '73');
INSERT INTO `country` VALUES ('5547', 'ISR', 'Israel', '以色列', '74');
INSERT INTO `country` VALUES ('3376', 'ITA', 'Italy', '義大利', '75');
INSERT INTO `country` VALUES ('3435', 'JPN', 'Japan', '日本', '77');
INSERT INTO `country` VALUES ('3589', 'KOR', 'South Korea', '南韓', '87');
INSERT INTO `country` VALUES ('3851', 'LTU', 'Lithuania', '立陶宛', '98');
INSERT INTO `country` VALUES ('6303', 'MEX', 'Mexico', '墨西哥', '110');
INSERT INTO `country` VALUES ('5148', 'MKD', 'Macedonia', '馬其頓', '100');
INSERT INTO `country` VALUES ('3674', 'MLI', 'Mali', '馬里', '105');
INSERT INTO `country` VALUES ('11953', 'MNE', 'Montenegro', '蒙特內哥羅', '216');
INSERT INTO `country` VALUES ('3575', 'MOR', 'Morocco', '摩洛哥', '107');
INSERT INTO `country` VALUES ('3444', 'NGA', 'Nigeria', '奈及利亞', '124');
INSERT INTO `country` VALUES ('5674', 'NIR', 'Northern Ireland', '北愛爾蘭', '192');
INSERT INTO `country` VALUES ('3379', 'NED', 'Netherlands', '荷蘭', '122');
INSERT INTO `country` VALUES ('3440', 'NOR', 'Norway', '挪威', '125');
INSERT INTO `country` VALUES ('9171', 'NZL', 'New Zealand', '紐西蘭', '120');
INSERT INTO `country` VALUES ('3442', 'POL', 'Poland', '波蘭', '135');
INSERT INTO `country` VALUES ('3300', 'POR', 'Portugal', '葡萄牙', '136');
INSERT INTO `country` VALUES ('3447', 'ROU', 'Romania', '羅馬尼亞', '140');
INSERT INTO `country` VALUES ('3448', 'RUS', 'Russia', '俄羅斯', '141');
INSERT INTO `country` VALUES ('3380', 'SCO', 'Scottland', '蘇格蘭', '190');
INSERT INTO `country` VALUES ('3499', 'SEN', 'Senegal', '塞內加爾', '149');
INSERT INTO `country` VALUES ('3375', 'ESP', 'Spain', '西班牙', '157');
INSERT INTO `country` VALUES ('3438', 'SRB', 'Serbia', '塞爾維亞', '215');
INSERT INTO `country` VALUES ('3503', 'SVK', 'Slovakia', '斯洛伐克', '154');
INSERT INTO `country` VALUES ('3588', 'SVN', 'Slovenia', '斯洛維尼亞', '155');
INSERT INTO `country` VALUES ('3557', 'SWE', 'Sweden', '瑞典', '147');
INSERT INTO `country` VALUES ('3384', 'SUI', 'Switzerland', '瑞士', '148');
INSERT INTO `country` VALUES ('3815', 'TGO', 'Togo', '多哥', '168');
INSERT INTO `country` VALUES ('3381', 'TUR', 'Turkey', '土耳其', '174');
INSERT INTO `country` VALUES ('3699', 'UKR', 'Ukraine', '烏克蘭', '177');
INSERT INTO `country` VALUES ('3449', 'URU', 'Uruguay', '烏拉圭', '179');
INSERT INTO `country` VALUES ('3505', 'USA', 'USA', '美國', '184');
INSERT INTO `country` VALUES ('3504', 'VEN', 'Venezuela', '委內瑞拉', '182');
INSERT INTO `country` VALUES ('3864', 'WAL', 'Wales', '威爾士', '191');
INSERT INTO `country` VALUES ('3806', 'ZAF', 'South Africa', '南非', '159');
INSERT INTO `country` VALUES ('3584', 'PER', 'Peru', '祕魯', '133');
INSERT INTO `country` VALUES ('8497', 'CRI', 'Costa Rica', '哥斯大黎加', '36');
INSERT INTO `country` VALUES ('3383', 'AUT', 'Austria', '奧地利', '127');
INSERT INTO `country` VALUES ('3581', 'PRY', 'Paraguay', '巴拉圭', '132');
INSERT INTO `country` VALUES ('3582', 'IRN', 'Iran', '伊朗', '71');
INSERT INTO `country` VALUES ('3670', 'TUN', 'Tunisia', '突尼西亞', '173');
INSERT INTO `country` VALUES ('5872', 'BFA', 'Burkina Faso', '布吉納法索', '29');
INSERT INTO `country` VALUES ('14161', 'HAI', 'Haiti', '海地', '62');
INSERT INTO `country` VALUES ('3468', 'HUN', 'Hungary', '匈牙利', '178');
INSERT INTO `country` VALUES ('3671', 'JAM', 'Jamaica', '牙買加', '76');
INSERT INTO `country` VALUES ('3807', 'KSA', 'Saudi Arabia', '沙烏地阿拉伯', '146');
INSERT INTO `country` VALUES ('3577', 'PAN', 'Panama', '巴拿馬', '130');
INSERT INTO `country` VALUES ('3561', 'ALB', 'Albania', '阿爾巴尼亞', '3');
INSERT INTO `country` VALUES ('3563', 'UZB', 'Uzbekistan', '烏茲別克', '180');
INSERT INTO `country` VALUES ('3856', 'GUI', 'Guinea', '幾內亞', '59');
INSERT INTO `country` VALUES ('5233', 'BOL', 'Bolivia', '玻利維亞', '23');
INSERT INTO `country` VALUES ('3450', 'BLR', 'Belarus', '白俄羅斯', '18');
INSERT INTO `country` VALUES ('6219', 'ARM', 'Armenia', '亞美尼亞', '10');
INSERT INTO `country` VALUES ('13497', 'UGA', 'Uganda', '烏干達', '176');
INSERT INTO `country` VALUES ('5147', 'UAE', 'United Arab Emirates', '阿拉伯聯合大公國', '183');
INSERT INTO `country` VALUES ('8987', 'KEN', 'Kenya', '肯亞', '82');
INSERT INTO `country` VALUES ('6133', 'EST', 'Estonia', '愛沙尼亞', '47');
