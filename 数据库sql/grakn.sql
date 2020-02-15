/*
Navicat MySQL Data Transfer

Source Server         : MYSQL
Source Server Version : 50528
Source Host           : localhost:3306
Source Database       : grakn

Target Server Type    : MYSQL
Target Server Version : 50528
File Encoding         : 65001

Date: 2020-02-15 16:15:14
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `checkitems`
-- ----------------------------
DROP TABLE IF EXISTS `checkitems`;
CREATE TABLE `checkitems` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ck_name` varchar(255) DEFAULT NULL,
  `n_prpt` int(11) DEFAULT NULL,
  `items` text CHARACTER SET utf8,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of checkitems
-- ----------------------------
INSERT INTO `checkitems` VALUES ('1', '左室检查', '1', '左室');
INSERT INTO `checkitems` VALUES ('2', '肌小梁等检查1', '5', '肌小梁,非致密心肌,致密心肌,NC/C,CDFI');
INSERT INTO `checkitems` VALUES ('3', '肌小梁增生运动检查', '1', '肌小梁增生的左室壁心肌运动');
INSERT INTO `checkitems` VALUES ('4', '右室检查', '1', '右室');
INSERT INTO `checkitems` VALUES ('5', '肌小梁等检查2', '2', '肌小梁,致密心肌');
INSERT INTO `checkitems` VALUES ('6', '心内膜检查', '2', '心内膜,回声');
INSERT INTO `checkitems` VALUES ('7', '左室壁检查', '2', '厚度,心肌运动');
INSERT INTO `checkitems` VALUES ('8', '宫内感染史检查', '1', '宫内感染史');
INSERT INTO `checkitems` VALUES ('9', '母体抗SSA抗体检查', '1', '母体抗SSA抗体');
INSERT INTO `checkitems` VALUES ('10', '感染因素检查', '1', '感染因素');

-- ----------------------------
-- Table structure for `edge1`
-- ----------------------------
DROP TABLE IF EXISTS `edge1`;
CREATE TABLE `edge1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start_id` int(11) NOT NULL,
  `end_id` int(11) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `label` varchar(255) CHARACTER SET utf8 NOT NULL,
  `next_check` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Edge1_end` (`end_id`),
  KEY `Edge1_start` (`start_id`),
  KEY `Edge1_parent` (`parent_id`),
  CONSTRAINT `Edge1_end` FOREIGN KEY (`end_id`) REFERENCES `node1` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Edge1_parent` FOREIGN KEY (`parent_id`) REFERENCES `edge1` (`id`) ON DELETE SET NULL ON UPDATE SET NULL,
  CONSTRAINT `Edge1_start` FOREIGN KEY (`start_id`) REFERENCES `node1` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of edge1
-- ----------------------------
INSERT INTO `edge1` VALUES ('1', '1', '2', null, 'NEXT', '左室检查');
INSERT INTO `edge1` VALUES ('2', '1', '3', null, 'NEXT', '右室检查');
INSERT INTO `edge1` VALUES ('3', '2', '4', '1', 'NEXT', '肌小梁等检查1');
INSERT INTO `edge1` VALUES ('4', '2', '5', '1', 'NEXT', '肌小梁等检查2');
INSERT INTO `edge1` VALUES ('5', '4', '6', '3', 'NEXT', '肌小梁增生运动检查');
INSERT INTO `edge1` VALUES ('6', '5', '7', '4', 'NEXT', '心内膜检查');
INSERT INTO `edge1` VALUES ('7', '5', '8', '4', 'NEXT', '心内膜检查');
INSERT INTO `edge1` VALUES ('8', '6', '1', '5', 'DESE', null);
INSERT INTO `edge1` VALUES ('10', '7', '9', '6', 'NEXT', '左室壁检查');
INSERT INTO `edge1` VALUES ('11', '8', '10', '7', 'NEXT', '左室壁检查');
INSERT INTO `edge1` VALUES ('12', '9', '3', '10', 'DESE', null);
INSERT INTO `edge1` VALUES ('13', '10', '11', '11', 'NEXT', '宫内感染史检查');
INSERT INTO `edge1` VALUES ('14', '10', '12', '11', 'NEXT', '母体抗SSA抗体检查');
INSERT INTO `edge1` VALUES ('15', '10', '13', '11', 'NEXT', '感染因素检查');
INSERT INTO `edge1` VALUES ('16', '11', '4', '13', 'DESE', null);
INSERT INTO `edge1` VALUES ('17', '12', '5', '14', 'DESE', null);
INSERT INTO `edge1` VALUES ('18', '13', '6', '15', 'DESE', null);

-- ----------------------------
-- Table structure for `edge2`
-- ----------------------------
DROP TABLE IF EXISTS `edge2`;
CREATE TABLE `edge2` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start_id` int(11) NOT NULL,
  `end_id` int(11) NOT NULL,
  `label` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT 'PRPT',
  `prpt_name` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Edge2_end` (`end_id`),
  KEY `Edge2_start` (`start_id`),
  CONSTRAINT `Edge2_end` FOREIGN KEY (`end_id`) REFERENCES `node2` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `Edge2_start` FOREIGN KEY (`start_id`) REFERENCES `node1` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of edge2
-- ----------------------------
INSERT INTO `edge2` VALUES ('1', '4', '1', 'PRPT', null);
INSERT INTO `edge2` VALUES ('2', '4', '2', 'PRPT', null);
INSERT INTO `edge2` VALUES ('3', '4', '3', 'PRPT', null);
INSERT INTO `edge2` VALUES ('4', '4', '4', 'PRPT', null);
INSERT INTO `edge2` VALUES ('5', '4', '5', 'PRPT', null);
INSERT INTO `edge2` VALUES ('6', '7', '6', 'PRPT', null);
INSERT INTO `edge2` VALUES ('7', '7', '7', 'PRPT', null);
INSERT INTO `edge2` VALUES ('8', '8', '8', 'PRPT', null);
INSERT INTO `edge2` VALUES ('9', '8', '9', 'PRPT', null);
INSERT INTO `edge2` VALUES ('10', '9', '10', 'PRPT', null);
INSERT INTO `edge2` VALUES ('11', '9', '11', 'PRPT', null);
INSERT INTO `edge2` VALUES ('12', '10', '12', 'PRPT', null);
INSERT INTO `edge2` VALUES ('13', '10', '13', 'PRPT', null);

-- ----------------------------
-- Table structure for `node1`
-- ----------------------------
DROP TABLE IF EXISTS `node1`;
CREATE TABLE `node1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) DEFAULT NULL,
  `check` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `n_prpt` int(11) DEFAULT NULL,
  `key` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `value` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `prpt_relation` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Node1_prt` (`parent_id`),
  CONSTRAINT `Node1_prt` FOREIGN KEY (`parent_id`) REFERENCES `node1` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of node1
-- ----------------------------
INSERT INTO `node1` VALUES ('1', null, null, null, null, '', null, '四腔心', null);
INSERT INTO `node1` VALUES ('2', '1', '左室检查', '1', '左室', '扩张', null, '左室扩张', null);
INSERT INTO `node1` VALUES ('3', '1', '右室检查', '1', '右室', '扩张', null, '右室扩张', null);
INSERT INTO `node1` VALUES ('4', '2', '肌小梁等检查1', '5', null, null, null, '肌小梁明显增多，非致密心肌增厚，致密心肌变薄，NC/C>2,CDFI:隐窝内可见血流信号。\r', null);
INSERT INTO `node1` VALUES ('5', '2', '肌小梁等检查2', '2', null, null, null, '肌小梁无明显增生，致密心肌无变薄\r', null);
INSERT INTO `node1` VALUES ('6', '4', '肌小梁增生运动检查', '1', '肌小梁增生的左室壁心肌运动', '减低', null, '肌小梁增生的左室壁心肌运动减低\r', null);
INSERT INTO `node1` VALUES ('7', '5', '心内膜检查', '2', null, null, null, '心内膜增厚，回声增强\r', null);
INSERT INTO `node1` VALUES ('8', '5', '心内膜检查', '2', null, null, null, '心内膜无增厚，回声正常\r', null);
INSERT INTO `node1` VALUES ('9', '7', '左室壁检查', '2', null, null, null, '厚度正常或变薄，心肌运动减低', null);
INSERT INTO `node1` VALUES ('10', '8', '左室壁检查', '2', null, null, null, '厚度正常或变薄，心肌运动减低', null);
INSERT INTO `node1` VALUES ('11', '10', '宫内感染检查', '1', '宫内感染史', '有', null, '有宫内感染史', null);
INSERT INTO `node1` VALUES ('12', '10', '母体抗SSA抗体检查', '1', '母体抗SSA抗体', '阳性', null, '母体抗SSA抗体阳性\r', null);
INSERT INTO `node1` VALUES ('13', '10', '感染因素检查', '1', '感染因素', '无', null, '无感染因素', null);

-- ----------------------------
-- Table structure for `node2`
-- ----------------------------
DROP TABLE IF EXISTS `node2`;
CREATE TABLE `node2` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL,
  `key` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `value` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  `type` varchar(255) DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Node2_pa` (`parent_id`),
  CONSTRAINT `Node2_pa` FOREIGN KEY (`parent_id`) REFERENCES `node1` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of node2
-- ----------------------------
INSERT INTO `node2` VALUES ('1', '4', '肌小梁', '增多', null, '肌小梁增多');
INSERT INTO `node2` VALUES ('2', '4', '非致密心肌', '增厚', null, '非致密心肌增厚');
INSERT INTO `node2` VALUES ('3', '4', '致密心肌', '变薄', null, '致密心肌变薄');
INSERT INTO `node2` VALUES ('4', '4', 'NC/C', '2', 'gt', 'NC/C>2');
INSERT INTO `node2` VALUES ('5', '4', 'CDFI', '可见', null, '隐窝内可见血流信号');
INSERT INTO `node2` VALUES ('6', '7', '心内膜厚度', '增厚', null, '心内膜增厚');
INSERT INTO `node2` VALUES ('7', '7', '心内膜回声', '增强', null, '回声增强');
INSERT INTO `node2` VALUES ('8', '8', '心内膜厚度', '无增厚', null, '心内膜无增厚');
INSERT INTO `node2` VALUES ('9', '8', '心内膜回声', '正常', null, '心内膜回声正常');
INSERT INTO `node2` VALUES ('10', '9', '左室壁厚度', '正常|变薄', 'or', '左室壁厚度正常或变薄');
INSERT INTO `node2` VALUES ('11', '9', '左室壁心肌运动', '减低', null, '心肌运动减低');
INSERT INTO `node2` VALUES ('12', '10', '左室壁厚度', '正常|变薄', 'or', '厚度正常或变薄');
INSERT INTO `node2` VALUES ('13', '10', '左室壁心肌运动', '减低', null, '心肌运动减低');

-- ----------------------------
-- Table structure for `node3`
-- ----------------------------
DROP TABLE IF EXISTS `node3`;
CREATE TABLE `node3` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) NOT NULL,
  `label` varchar(255) DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`id`),
  KEY `Node3_prt` (`parent_id`),
  CONSTRAINT `Node3_prt` FOREIGN KEY (`parent_id`) REFERENCES `node1` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of node3
-- ----------------------------
INSERT INTO `node3` VALUES ('1', '6', 'DESE', '左室受累型心肌致密化不全\r');
INSERT INTO `node3` VALUES ('2', '6', 'PROG', '1、胎儿期表现为肥厚型心肌病，预后通常不良。\r2、心血管整体评分≤5分，预后更差，存在宫内丢失风险。\r3、建议对患儿及其一级亲属进行遗传学检测（心肌病panel更佳），寻找遗传学异常。\r4、对该患病家庭进行专业预后咨询，如发现致病基因，可指导下一胎生育（进行第三代试管婴儿）。\r\r');
INSERT INTO `node3` VALUES ('3', '9', 'DESE', '左室受累型心内膜弹力纤维增生症\r');
INSERT INTO `node3` VALUES ('4', '11', 'DESE', '左室受累型心肌炎可能\r');
INSERT INTO `node3` VALUES ('5', '12', 'DESE', '母体自身免疫性疾病导致继发左心室扩大\r');
INSERT INTO `node3` VALUES ('6', '13', 'DESE', '左室受累型扩张型心肌病\r');

-- ----------------------------
-- Table structure for `valueset`
-- ----------------------------
DROP TABLE IF EXISTS `valueset`;
CREATE TABLE `valueset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `key1` varchar(255) DEFAULT NULL,
  `valueSet` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of valueset
-- ----------------------------
INSERT INTO `valueset` VALUES ('1', '左室', '扩张,正常,收缩');
INSERT INTO `valueset` VALUES ('2', '右室', '扩张,正常,收缩');
INSERT INTO `valueset` VALUES ('3', '肌小梁', '增多,减少,正常');
INSERT INTO `valueset` VALUES ('4', '非致密心肌', '增厚,正常,变薄');
INSERT INTO `valueset` VALUES ('5', '致密心肌', '增厚,正常,变薄');
INSERT INTO `valueset` VALUES ('6', 'NC/C', 'NUMBER');
INSERT INTO `valueset` VALUES ('7', 'CDFI', '可见,不可见');
INSERT INTO `valueset` VALUES ('8', '肌小梁增生的左室壁心肌运动', '加快,减低,正常');
INSERT INTO `valueset` VALUES ('9', '心内膜厚度', '增厚,正常,变薄');
INSERT INTO `valueset` VALUES ('10', '心内膜回声', '正常,增强,减弱');
INSERT INTO `valueset` VALUES ('11', '左室壁厚度', '增厚,变薄,正常');
INSERT INTO `valueset` VALUES ('12', '左室壁心肌运动', '正常,减低,加快');
INSERT INTO `valueset` VALUES ('13', '宫内感染史', '有,无');
INSERT INTO `valueset` VALUES ('14', '母体抗SSA抗体', '阳性,阴性');
INSERT INTO `valueset` VALUES ('15', '感染因素', '有,无');
