-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 18, 2021 at 11:35 AM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 8.0.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `project`
--

-- --------------------------------------------------------

--
-- Table structure for table `bike`
--

CREATE TABLE `bike` (
  `bikeID` int(11) NOT NULL,
  `bikeStatus` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `locationID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `bike`
--

INSERT INTO `bike` (`bikeID`, `bikeStatus`, `locationID`) VALUES
(1, 'good', 1),
(2, 'good', 2),
(3, 'good', 3),
(4, 'good', 4),
(5, 'good', 5),
(6, 'good', 6);

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `customerID` int(11) NOT NULL,
  `totalPaid` double DEFAULT NULL,
  `email` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `password` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `account_total` int(11) DEFAULT NULL,
  `rental_status` tinyint(1) DEFAULT NULL,
  `card_details` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`customerID`, `totalPaid`, `email`, `password`, `account_total`, `rental_status`, `card_details`) VALUES
(1, 23, 'lkasdalj@gmail.uk', 'khsdancna', 10, 0, '4002205152120'),
(2, 2, 'asdsgd@gmail.uk', 'aytwbjd', 20, 0, '665221541210'),
(3, 20, 'qhgwqh@gmail.uk', 'lajdhdhs', 16, 0, '45451215544');

-- --------------------------------------------------------

--
-- Table structure for table `customeractivity`
--

CREATE TABLE `customeractivity` (
  `ActID` int(11) NOT NULL,
  `customerID` int(11) DEFAULT NULL,
  `bikeID` int(11) DEFAULT NULL,
  `startTime` datetime DEFAULT NULL,
  `endTime` datetime DEFAULT NULL,
  `startLocation` int(11) DEFAULT NULL,
  `endLocation` int(11) DEFAULT NULL,
  `charged` float DEFAULT NULL,
  `paid` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `customeractivity`
--

INSERT INTO `customeractivity` (`ActID`, `customerID`, `bikeID`, `startTime`, `endTime`, `startLocation`, `endLocation`, `charged`, `paid`) VALUES
(1, 2, 1, '2021-01-19 13:14:07', '2021-01-19 14:19:27', 1, 2, 3.14, 1),
(2, 1, 2, '2021-08-09 03:04:07', '2021-08-09 03:19:27', 2, 1, 5, 1);

-- --------------------------------------------------------

--
-- Table structure for table `location`
--

CREATE TABLE `location` (
  `locationID` int(11) NOT NULL,
  `postCode` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `location`
--

INSERT INTO `location` (`locationID`, `postCode`) VALUES
(1, 'postcode1'),
(2, 'postcode2'),
(3, 'postcode3'),
(4, 'postcode4'),
(5, 'postcode5'),
(6, 'postcode6');

-- --------------------------------------------------------

--
-- Table structure for table `operatoractivity`
--

CREATE TABLE `operatoractivity` (
  `ActID` int(11) NOT NULL,
  `bikeID` int(11) DEFAULT NULL,
  `actionName` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `operatoractivity`
--

INSERT INTO `operatoractivity` (`ActID`, `bikeID`, `actionName`) VALUES
(1, 2, 'action 1'),
(2, 1, 'action 2'),
(3, 3, 'action 3');

-- --------------------------------------------------------

--
-- Table structure for table `reviews`
--

CREATE TABLE `reviews` (
  `reviewID` int(11) NOT NULL,
  `customerID` int(11) NOT NULL,
  `bikeID` int(11) NOT NULL,
  `starRating` int(11) DEFAULT NULL,
  `comments` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `reviewTime` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `reviews`
--

INSERT INTO `reviews` (`reviewID`, `customerID`, `bikeID`, `starRating`, `comments`, `reviewTime`) VALUES
(1, 3, 4, 5, 'Great ride', '2021-10-16 22:46:53'),
(2, 3, 4, 3, 'decent ride', '2021-10-17 09:49:32');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bike`
--
ALTER TABLE `bike`
  ADD PRIMARY KEY (`bikeID`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`customerID`);

--
-- Indexes for table `customeractivity`
--
ALTER TABLE `customeractivity`
  ADD PRIMARY KEY (`ActID`);

--
-- Indexes for table `location`
--
ALTER TABLE `location`
  ADD PRIMARY KEY (`locationID`);

--
-- Indexes for table `operatoractivity`
--
ALTER TABLE `operatoractivity`
  ADD PRIMARY KEY (`ActID`);

--
-- Indexes for table `reviews`
--
ALTER TABLE `reviews`
  ADD PRIMARY KEY (`reviewID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bike`
--
ALTER TABLE `bike`
  MODIFY `bikeID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `customerID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `customeractivity`
--
ALTER TABLE `customeractivity`
  MODIFY `ActID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `location`
--
ALTER TABLE `location`
  MODIFY `locationID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `operatoractivity`
--
ALTER TABLE `operatoractivity`
  MODIFY `ActID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `reviews`
--
ALTER TABLE `reviews`
  MODIFY `reviewID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
