-- phpMyAdmin SQL Dump
-- version 5.2.1deb1+deb12u1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Erstellungszeit: 12. Aug 2025 um 17:08
-- Server-Version: 10.11.11-MariaDB-0+deb12u1
-- PHP-Version: 8.2.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `Modularbeit`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `TodoEnddate`
--

CREATE TABLE `TodoEnddate` (
  `EnddateID` int(11) NOT NULL,
  `Enddate` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `TodoEnddate`
--

INSERT INTO `TodoEnddate` (`EnddateID`, `Enddate`) VALUES
(1, '2025-04-13'),
(2, '2025-04-13'),
(3, '2025-04-13'),
(4, '2025-04-13'),
(5, '2026-11-02'),
(6, '2025-07-02'),
(7, '2025-08-13'),
(8, '2025-08-12');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `TodoPercent`
--

CREATE TABLE `TodoPercent` (
  `PercentID` int(11) NOT NULL,
  `Percent` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `TodoPercent`
--

INSERT INTO `TodoPercent` (`PercentID`, `Percent`) VALUES
(1, 0),
(2, 10),
(3, 20),
(4, 30),
(5, 40),
(6, 50),
(7, 60),
(8, 70),
(9, 80),
(10, 90),
(11, 100);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `TodoRememberHistory`
--

CREATE TABLE `TodoRememberHistory` (
  `HistoryID` int(11) NOT NULL,
  `TodoID` int(11) NOT NULL,
  `RemembermeID` int(11) NOT NULL,
  `ChangedAt` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `TodoRememberHistory`
--

INSERT INTO `TodoRememberHistory` (`HistoryID`, `TodoID`, `RemembermeID`, `ChangedAt`) VALUES
(1, 4, 3, '2025-06-11 21:10:36'),
(2, 4, 4, '2025-06-11 21:11:32'),
(3, 2, 5, '2025-06-11 21:29:07'),
(4, 5, 6, '2025-06-11 21:40:14'),
(5, 5, 7, '2025-06-11 21:49:21'),
(6, 5, 8, '2025-06-11 21:59:24'),
(7, 6, 9, '2025-07-02 20:44:58'),
(8, 7, 10, '2025-08-12 17:56:02'),
(9, 8, 11, '2025-08-12 17:57:00'),
(10, 6, 12, '2025-08-12 18:07:00');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `TodoRememberme`
--

CREATE TABLE `TodoRememberme` (
  `RemembermeID` int(11) NOT NULL,
  `RememberDateTime` datetime NOT NULL,
  `IsNotified` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `TodoRememberme`
--

INSERT INTO `TodoRememberme` (`RemembermeID`, `RememberDateTime`, `IsNotified`) VALUES
(1, '2025-04-13 22:13:00', 1),
(2, '2025-04-11 12:00:00', 1),
(3, '2024-04-25 13:00:00', 1),
(4, '2025-02-15 12:00:00', 1),
(5, '2022-12-01 12:00:00', 1),
(6, '2025-06-11 21:45:00', 1),
(7, '2025-06-11 21:55:00', 1),
(8, '2025-06-11 22:00:00', 1),
(9, '2025-07-02 21:44:59', 1),
(10, '2025-08-12 18:55:46', 0),
(11, '2025-08-12 18:56:57', 0),
(12, '2025-08-12 20:06:00', 0);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `TodoState`
--

CREATE TABLE `TodoState` (
  `StateID` int(11) NOT NULL,
  `PercentID` int(11) NOT NULL,
  `StateDescription` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `TodoState`
--

INSERT INTO `TodoState` (`StateID`, `PercentID`, `StateDescription`) VALUES
(1, 1, ''),
(2, 1, 'start'),
(3, 11, 'fertig'),
(4, 1, 'nö'),
(5, 1, 'shit'),
(6, 1, 'test'),
(7, 5, 'fast fertig'),
(8, 11, 'fertig'),
(9, 11, 'nö'),
(10, 11, 'fertig'),
(11, 2, 'Angefangen'),
(12, 1, 'nö'),
(13, 1, 'asdf'),
(14, 1, 'test'),
(15, 1, 'Neu'),
(16, 1, 'Neu'),
(17, 2, 'angefangen'),
(18, 1, 'Neu');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `TodoStateHistory`
--

CREATE TABLE `TodoStateHistory` (
  `HistoryID` int(11) NOT NULL,
  `TodoID` int(11) NOT NULL,
  `StateID` int(11) NOT NULL,
  `ChangedAt` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `TodoStateHistory`
--

INSERT INTO `TodoStateHistory` (`HistoryID`, `TodoID`, `StateID`, `ChangedAt`) VALUES
(1, 1, 1, '2025-06-11 20:24:34'),
(2, 2, 2, '2025-06-11 20:47:35'),
(3, 1, 3, '2025-06-11 20:47:50'),
(4, 3, 4, '2025-06-11 20:59:03'),
(5, 3, 5, '2025-06-11 20:59:35'),
(6, 4, 6, '2025-06-11 21:10:36'),
(7, 4, 7, '2025-06-11 21:11:15'),
(8, 2, 8, '2025-06-11 21:13:22'),
(9, 2, 9, '2025-06-11 21:13:54'),
(10, 4, 10, '2025-06-11 21:17:16'),
(11, 2, 11, '2025-06-11 21:27:44'),
(12, 5, 12, '2025-06-11 21:40:14'),
(13, 5, 13, '2025-06-11 21:49:01'),
(14, 5, 14, '2025-06-11 21:58:59'),
(15, 6, 15, '2025-07-02 20:44:58'),
(16, 7, 16, '2025-08-12 17:56:02'),
(17, 7, 17, '2025-08-12 17:56:27'),
(18, 8, 18, '2025-08-12 17:57:00');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `TodoTodolist`
--

CREATE TABLE `TodoTodolist` (
  `TodoID` int(11) NOT NULL,
  `TodoName` varchar(255) NOT NULL,
  `TodoDescription` text NOT NULL,
  `StateID` int(11) NOT NULL,
  `EnddateID` int(11) NOT NULL,
  `RemembermeID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `TodoTodolist`
--

INSERT INTO `TodoTodolist` (`TodoID`, `TodoName`, `TodoDescription`, `StateID`, `EnddateID`, `RemembermeID`) VALUES
(1, 'todo', 'bescheibung', 3, 1, NULL),
(2, 'test', 'todo', 11, 2, 5),
(3, 'todo', 'rembmer', 5, 3, 2),
(4, 'Schlafen gehen', 'Ich bin müde', 10, 4, 4),
(5, 'warnung', 'warnung', 14, 5, 8),
(6, 'g', 'g', 15, 6, 12),
(7, 'test', 'dies ist ein test', 17, 7, 10),
(8, 'a', 'test', 18, 8, 11);

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `TodoEnddate`
--
ALTER TABLE `TodoEnddate`
  ADD PRIMARY KEY (`EnddateID`);

--
-- Indizes für die Tabelle `TodoPercent`
--
ALTER TABLE `TodoPercent`
  ADD PRIMARY KEY (`PercentID`);

--
-- Indizes für die Tabelle `TodoRememberHistory`
--
ALTER TABLE `TodoRememberHistory`
  ADD PRIMARY KEY (`HistoryID`);

--
-- Indizes für die Tabelle `TodoRememberme`
--
ALTER TABLE `TodoRememberme`
  ADD PRIMARY KEY (`RemembermeID`);

--
-- Indizes für die Tabelle `TodoState`
--
ALTER TABLE `TodoState`
  ADD PRIMARY KEY (`StateID`),
  ADD KEY `PercentID` (`PercentID`);

--
-- Indizes für die Tabelle `TodoStateHistory`
--
ALTER TABLE `TodoStateHistory`
  ADD PRIMARY KEY (`HistoryID`),
  ADD KEY `TodoID` (`TodoID`),
  ADD KEY `StateID` (`StateID`);

--
-- Indizes für die Tabelle `TodoTodolist`
--
ALTER TABLE `TodoTodolist`
  ADD PRIMARY KEY (`TodoID`),
  ADD KEY `StateID` (`StateID`),
  ADD KEY `EnddateID` (`EnddateID`),
  ADD KEY `RemembermeID` (`RemembermeID`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `TodoEnddate`
--
ALTER TABLE `TodoEnddate`
  MODIFY `EnddateID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT für Tabelle `TodoPercent`
--
ALTER TABLE `TodoPercent`
  MODIFY `PercentID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT für Tabelle `TodoRememberHistory`
--
ALTER TABLE `TodoRememberHistory`
  MODIFY `HistoryID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT für Tabelle `TodoRememberme`
--
ALTER TABLE `TodoRememberme`
  MODIFY `RemembermeID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT für Tabelle `TodoState`
--
ALTER TABLE `TodoState`
  MODIFY `StateID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT für Tabelle `TodoStateHistory`
--
ALTER TABLE `TodoStateHistory`
  MODIFY `HistoryID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT für Tabelle `TodoTodolist`
--
ALTER TABLE `TodoTodolist`
  MODIFY `TodoID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `TodoState`
--
ALTER TABLE `TodoState`
  ADD CONSTRAINT `TodoState_ibfk_1` FOREIGN KEY (`PercentID`) REFERENCES `TodoPercent` (`PercentID`) ON UPDATE CASCADE;

--
-- Constraints der Tabelle `TodoStateHistory`
--
ALTER TABLE `TodoStateHistory`
  ADD CONSTRAINT `TodoStateHistory_ibfk_1` FOREIGN KEY (`TodoID`) REFERENCES `TodoTodolist` (`TodoID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `TodoStateHistory_ibfk_2` FOREIGN KEY (`StateID`) REFERENCES `TodoState` (`StateID`) ON UPDATE CASCADE;

--
-- Constraints der Tabelle `TodoTodolist`
--
ALTER TABLE `TodoTodolist`
  ADD CONSTRAINT `TodoTodolist_ibfk_1` FOREIGN KEY (`StateID`) REFERENCES `TodoState` (`StateID`) ON UPDATE CASCADE,
  ADD CONSTRAINT `TodoTodolist_ibfk_2` FOREIGN KEY (`EnddateID`) REFERENCES `TodoEnddate` (`EnddateID`) ON UPDATE CASCADE,
  ADD CONSTRAINT `TodoTodolist_ibfk_3` FOREIGN KEY (`RemembermeID`) REFERENCES `TodoRememberme` (`RemembermeID`) ON DELETE SET NULL ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
