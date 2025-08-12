-- phpMyAdmin SQL Dump
-- version 5.2.1deb1+deb12u1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Erstellungszeit: 12. Aug 2025 um 19:34
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

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `TodoRememberme`
--

CREATE TABLE `TodoRememberme` (
  `RemembermeID` int(11) NOT NULL,
  `RememberDateTime` datetime NOT NULL,
  `IsNotified` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `TodoState`
--

CREATE TABLE `TodoState` (
  `StateID` int(11) NOT NULL,
  `PercentID` int(11) NOT NULL,
  `StateDescription` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  MODIFY `EnddateID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `TodoPercent`
--
ALTER TABLE `TodoPercent`
  MODIFY `PercentID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT für Tabelle `TodoRememberHistory`
--
ALTER TABLE `TodoRememberHistory`
  MODIFY `HistoryID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `TodoRememberme`
--
ALTER TABLE `TodoRememberme`
  MODIFY `RemembermeID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `TodoState`
--
ALTER TABLE `TodoState`
  MODIFY `StateID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `TodoStateHistory`
--
ALTER TABLE `TodoStateHistory`
  MODIFY `HistoryID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `TodoTodolist`
--
ALTER TABLE `TodoTodolist`
  MODIFY `TodoID` int(11) NOT NULL AUTO_INCREMENT;

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
