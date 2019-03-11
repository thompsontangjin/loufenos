-- phpMyAdmin SQL Dump
-- version 3.3.8.1
-- http://www.phpmyadmin.net
--
-- Host: w.rdc.sae.sina.com.cn:3307
-- Generation Time: Apr 13, 2016 at 08:25 PM
-- Server version: 5.6.23
-- PHP Version: 5.3.3

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `app_newlogistics`
--

-- --------------------------------------------------------

--
-- Table structure for table `traceinfo`
--

CREATE TABLE IF NOT EXISTS `traceinfo` (
  `id` int(20) unsigned NOT NULL AUTO_INCREMENT,
  `phonenumber` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `latlong` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=25 ;

--
-- Dumping data for table `traceinfo`
--

INSERT INTO `traceinfo` (`id`, `phonenumber`, `latlong`, `date`) VALUES
(23, '18659291718', '24.5142098429,118.121441078', '2015-04-22 17:18:26'),
(24, '13779961531', '24.47385653,118.158875975', '2015-10-27 19:30:33');
