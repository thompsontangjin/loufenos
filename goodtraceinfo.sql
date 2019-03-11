-- phpMyAdmin SQL Dump
-- version 3.3.8.1
-- http://www.phpmyadmin.net
--
-- Host: w.rdc.sae.sina.com.cn:3307
-- Generation Time: Apr 13, 2016 at 08:24 PM
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
-- Table structure for table `goodtraceinfo`
--

CREATE TABLE IF NOT EXISTS `goodtraceinfo` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `goodnumber` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `trucknumber` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=23 ;

--
-- Dumping data for table `goodtraceinfo`
--

INSERT INTO `goodtraceinfo` (`id`, `goodnumber`, `trucknumber`, `date`) VALUES
(18, '6901028169998', '13779961531', '2015-07-14 22:11:59'),
(17, '123', '13779961531', '2015-05-08 11:31:26'),
(16, '980035894378', '13779961531', '2015-05-07 10:33:50'),
(15, '6901028142564', '13779961531', '2015-05-06 23:50:47'),
(5, '5698232', '13779961531', '2015-05-06 23:50:47'),
(7, '22501', '13779961531', '2015-05-06 23:50:47'),
(8, '13779961531', '13779961531', '2015-05-06 23:50:47'),
(9, '18659291718', '13779961531', '2015-05-06 23:50:47'),
(14, '12345', '13779961531', '2015-05-06 23:50:47'),
(19, '6918717162017', '13779961531', '2015-07-28 14:32:44'),
(20, '8711173002037', '13779961531', '2015-09-11 23:31:37'),
(21, '4893055810054', '13779961531', '2015-10-19 10:26:18'),
(22, '6920283120339', '13779961531', '2015-10-27 19:30:00');
