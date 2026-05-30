-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.1.38-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for cyber_saler
CREATE DATABASE IF NOT EXISTS `cyber_saler` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `cyber_saler`;

-- Dumping structure for table cyber_saler.tbl_achat
CREATE TABLE IF NOT EXISTS `tbl_achat` (
  `achat_id` int(11) NOT NULL AUTO_INCREMENT,
  `entreprise_id` int(11) NOT NULL,
  `categorie_id` int(11) NOT NULL,
  `article_id` int(11) NOT NULL,
  `quantite` decimal(10,2) NOT NULL,
  `prix_unitaire` decimal(10,2) NOT NULL,
  `transport_sur_achat` decimal(10,2) DEFAULT '0.00',
  `rendu_rabais_sur_achat` decimal(10,2) DEFAULT '0.00',
  `cout_total` decimal(10,2) DEFAULT '0.00',
  `cree_par` int(11) DEFAULT NULL,
  `cree_le` datetime DEFAULT NULL,
  `modifie_par` int(11) DEFAULT NULL,
  `modifie_le` datetime DEFAULT NULL,
  PRIMARY KEY (`achat_id`) USING BTREE,
  KEY `fk_entreprise_2` (`entreprise_id`) USING BTREE,
  KEY `fk_categorie` (`categorie_id`) USING BTREE,
  KEY `fk_article` (`article_id`) USING BTREE,
  CONSTRAINT `fk_article` FOREIGN KEY (`article_id`) REFERENCES `tbl_article` (`article_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_categorie` FOREIGN KEY (`categorie_id`) REFERENCES `tbl_categorie` (`categorie_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_entreprise_2` FOREIGN KEY (`entreprise_id`) REFERENCES `tbl_entreprise` (`entreprise_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.

-- Dumping structure for table cyber_saler.tbl_article
CREATE TABLE IF NOT EXISTS `tbl_article` (
  `article_id` int(11) NOT NULL AUTO_INCREMENT,
  `article_code` varchar(45) NOT NULL,
  `article_desc` varchar(60) NOT NULL,
  `categorie_id` int(11) NOT NULL,
  `cree_par` int(11) DEFAULT NULL,
  `cree_le` datetime DEFAULT NULL,
  `modifie_par` int(11) DEFAULT NULL,
  `modifie_le` datetime DEFAULT NULL,
  PRIMARY KEY (`article_id`),
  UNIQUE KEY `article_code_UNIQUE` (`article_code`),
  UNIQUE KEY `article_desc_UNIQUE` (`article_desc`),
  KEY `fk_categorie_1` (`categorie_id`),
  CONSTRAINT `fk_categorie_1` FOREIGN KEY (`categorie_id`) REFERENCES `tbl_categorie` (`categorie_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table cyber_saler.tbl_categorie
CREATE TABLE IF NOT EXISTS `tbl_categorie` (
  `categorie_id` int(11) NOT NULL AUTO_INCREMENT,
  `categorie_code` varchar(45) NOT NULL,
  `categorie_desc` varchar(60) NOT NULL,
  `val_unit_cigle` varchar(2) NOT NULL,
  `val_unit_nom` varchar(20) NOT NULL,
  `cree_par` int(11) DEFAULT NULL,
  `cree_le` datetime DEFAULT NULL,
  `modifie_par` int(11) DEFAULT NULL,
  `modifie_le` datetime DEFAULT NULL,
  PRIMARY KEY (`categorie_id`),
  UNIQUE KEY `categorie_code` (`categorie_code`),
  UNIQUE KEY `categorie_desc` (`categorie_desc`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table cyber_saler.tbl_distribution
CREATE TABLE IF NOT EXISTS `tbl_distribution` (
  `distribution_id` int(11) NOT NULL AUTO_INCREMENT,
  `entreprise_id` int(11) NOT NULL,
  `adresse` varchar(120) DEFAULT NULL,
  `tel1` varchar(11) DEFAULT NULL,
  `tel2` varchar(11) DEFAULT NULL,
  `cree_par` int(11) DEFAULT NULL,
  `cree_le` datetime DEFAULT NULL,
  `modifie_par` int(11) DEFAULT NULL,
  `modifie_le` datetime DEFAULT NULL,
  PRIMARY KEY (`distribution_id`),
  KEY `fk_entreprise` (`entreprise_id`),
  CONSTRAINT `fk_entreprise` FOREIGN KEY (`entreprise_id`) REFERENCES `tbl_entreprise` (`entreprise_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table cyber_saler.tbl_entreprise
CREATE TABLE IF NOT EXISTS `tbl_entreprise` (
  `entreprise_id` int(11) NOT NULL AUTO_INCREMENT,
  `nom_commercial` varchar(45) NOT NULL,
  `contact` varchar(120) NOT NULL,
  `adresse` varchar(125) NOT NULL,
  `tel1` varchar(12) NOT NULL,
  `tel2` varchar(12) DEFAULT NULL,
  `email` varchar(125) DEFAULT NULL,
  `site` varchar(45) DEFAULT NULL,
  `cree_par` int(11) DEFAULT NULL,
  `cree_le` datetime DEFAULT NULL,
  `modifie_par` int(11) DEFAULT NULL,
  `modifie_le` datetime DEFAULT NULL,
  PRIMARY KEY (`entreprise_id`),
  UNIQUE KEY `nom_commercial_UNIQUE` (`nom_commercial`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table cyber_saler.tbl_level
CREATE TABLE IF NOT EXISTS `tbl_level` (
  `level_id` int(11) NOT NULL,
  `level_name` varchar(45) NOT NULL,
  PRIMARY KEY (`level_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.

-- Dumping structure for table cyber_saler.tbl_ligne_vente
CREATE TABLE IF NOT EXISTS `tbl_ligne_vente` (
  `ligne_id` int(11) NOT NULL AUTO_INCREMENT,
  `vente_id` int(11) NOT NULL,
  `entreprise_id` int(11) NOT NULL,
  `distribution_id` int(11) NOT NULL,
  `categorie_id` int(11) NOT NULL,
  `article_id` int(11) NOT NULL,
  `prix_vente_id` int(11) DEFAULT NULL,
  `prix_vente` decimal(10,2) DEFAULT NULL,
  `quantite` decimal(10,2) DEFAULT NULL,
  `unite` varchar(2) DEFAULT NULL,
  `cout_vente_total` decimal(10,2) DEFAULT NULL,
  `cree_par` int(11) DEFAULT NULL,
  `cree_le` datetime DEFAULT NULL,
  PRIMARY KEY (`ligne_id`),
  KEY `fk_distribution_1` (`distribution_id`),
  KEY `fk_categorie_2` (`categorie_id`),
  KEY `fk_article_2` (`article_id`),
  KEY `ind_ent_dist_cat_art` (`entreprise_id`,`distribution_id`,`categorie_id`,`article_id`),
  KEY `fk_prix_vente` (`prix_vente_id`),
  KEY `fk_vente_1_idx` (`vente_id`),
  CONSTRAINT `fk_article_2` FOREIGN KEY (`article_id`) REFERENCES `tbl_article` (`article_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_categorie_2` FOREIGN KEY (`categorie_id`) REFERENCES `tbl_categorie` (`categorie_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_distribution_1` FOREIGN KEY (`distribution_id`) REFERENCES `tbl_distribution` (`distribution_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_entreprise_1` FOREIGN KEY (`entreprise_id`) REFERENCES `tbl_entreprise` (`entreprise_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_prix_vente` FOREIGN KEY (`prix_vente_id`) REFERENCES `tbl_prix_vente` (`prix_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_vente_1` FOREIGN KEY (`vente_id`) REFERENCES `tbl_vente` (`vente_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.

-- Dumping structure for table cyber_saler.tbl_prix_vente
CREATE TABLE IF NOT EXISTS `tbl_prix_vente` (
  `prix_id` int(11) NOT NULL AUTO_INCREMENT,
  `entreprise_id` int(11) NOT NULL,
  `distribution_id` int(11) NOT NULL,
  `categorie_id` int(11) NOT NULL,
  `article_id` int(11) NOT NULL,
  `prix_vente` decimal(10,2) NOT NULL,
  `cree_par` int(11) DEFAULT NULL,
  `cree_le` datetime DEFAULT NULL,
  `modifie_par` int(11) DEFAULT NULL,
  `modifie_le` datetime DEFAULT NULL,
  PRIMARY KEY (`prix_id`),
  UNIQUE KEY `prix_unique` (`entreprise_id`,`distribution_id`,`categorie_id`,`article_id`),
  KEY `fk_categorie2` (`categorie_id`),
  KEY `fk_article_1` (`article_id`),
  KEY `fk_entreprise_3` (`distribution_id`),
  CONSTRAINT `fk_article_1` FOREIGN KEY (`article_id`) REFERENCES `tbl_article` (`article_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_categorie2` FOREIGN KEY (`categorie_id`) REFERENCES `tbl_categorie` (`categorie_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_distribution` FOREIGN KEY (`distribution_id`) REFERENCES `tbl_distribution` (`distribution_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_entreprise_3` FOREIGN KEY (`distribution_id`) REFERENCES `tbl_distribution` (`distribution_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.

-- Dumping structure for table cyber_saler.tbl_prix_vente_histo
CREATE TABLE IF NOT EXISTS `tbl_prix_vente_histo` (
  `prix_histo_id` int(11) NOT NULL AUTO_INCREMENT,
  `prix_id` int(11) NOT NULL,
  `entreprise_id` int(11) NOT NULL,
  `distribution_id` int(11) NOT NULL,
  `categorie_id` int(11) NOT NULL,
  `article_id` int(11) NOT NULL,
  `prix_vente` decimal(10,2) NOT NULL,
  `cree_par` int(11) DEFAULT NULL,
  `cree_le` datetime DEFAULT NULL,
  `modifie_par` int(11) DEFAULT NULL,
  `modifie_le` datetime DEFAULT NULL,
  PRIMARY KEY (`prix_histo_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Data exporting was unselected.

-- Dumping structure for table cyber_saler.tbl_users
CREATE TABLE IF NOT EXISTS `tbl_users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `nom_prenom` varchar(120) DEFAULT NULL,
  `username` varchar(45) NOT NULL,
  `password` varchar(255) NOT NULL,
  `entreprise_id` int(11) DEFAULT NULL,
  `distribution_id` int(11) DEFAULT NULL,
  `level_id` int(11) NOT NULL,
  `statut_user` tinyint(1) DEFAULT '0',
  `cree_par` int(11) DEFAULT NULL,
  `cree_le` datetime DEFAULT NULL,
  `modifie_par` int(11) DEFAULT NULL,
  `modifie_Le` datetime DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  KEY `fk_level` (`level_id`),
  CONSTRAINT `fk_level` FOREIGN KEY (`level_id`) REFERENCES `tbl_level` (`level_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

-- Data exporting was unselected.

-- Dumping structure for table cyber_saler.tbl_vente
CREATE TABLE IF NOT EXISTS `tbl_vente` (
  `vente_id` int(11) NOT NULL AUTO_INCREMENT,
  `entreprise_id` int(11) NOT NULL,
  `distribution_id` int(11) NOT NULL,
  `cree_par` int(11) DEFAULT NULL,
  `cree_le` datetime DEFAULT NULL,
  PRIMARY KEY (`vente_id`),
  KEY `fk_ent` (`entreprise_id`),
  KEY `fk_dist` (`distribution_id`),
  CONSTRAINT `fk_dist` FOREIGN KEY (`distribution_id`) REFERENCES `tbl_distribution` (`distribution_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_ent` FOREIGN KEY (`entreprise_id`) REFERENCES `tbl_entreprise` (`entreprise_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=latin1;

-- Data exporting was unselected.

-- Dumping structure for trigger cyber_saler.tbl_article_BEFORE_INSERT
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `cyber_saler`.`tbl_article_BEFORE_INSERT` BEFORE INSERT ON `tbl_article` FOR EACH ROW
BEGIN
	set new.cree_le = now();
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Dumping structure for trigger cyber_saler.tbl_article_BEFORE_UPDATE
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `cyber_saler`.`tbl_article_BEFORE_UPDATE` BEFORE UPDATE ON `tbl_article` FOR EACH ROW
BEGIN
	set new.modifie_le = now();
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Dumping structure for trigger cyber_saler.tbl_ligne_vente_BEFORE_INSERT
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `cyber_saler`.`tbl_ligne_vente_BEFORE_INSERT` BEFORE INSERT ON `tbl_ligne_vente` FOR EACH ROW
BEGIN
	-- get unite from categorie
    SET NEW.unite = (
		SELECT val_unit_cigle
        FROM tbl_categorie
        WHERE categorie_id = NEW.categorie_id
    );
    
	-- get id prix vente
	SET NEW.prix_vente_id = (
		SELECT prix_id
        FROM tbl_prix_vente
        WHERE entreprise_id = NEW.entreprise_id
        AND distribution_id = NEW.distribution_id
        AND categorie_id = NEW.categorie_id
        AND article_id = NEW.article_id
    );
    
    -- get id prix vente value
    SET NEW.prix_vente = (
		SELECT prix_vente
		FROM tbl_prix_vente
		WHERE prix_id = NEW.prix_vente_id
	);
    
    SET NEW.cout_vente_total = NEW.quantite * NEW.prix_vente;
    SET NEW.cree_le = now();
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Dumping structure for trigger cyber_saler.tbl_prix_vente_BEFORE_UPDATE
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `cyber_saler`.`tbl_prix_vente_BEFORE_UPDATE` BEFORE UPDATE ON `tbl_prix_vente` FOR EACH ROW
BEGIN
	IF NEW.prix_vente <> OLD.prix_vente then
		INSERT INTO `tbl_prix_vente_histo`
			(`prix_id`,
			`entreprise_id`,
			`distribution_id`,
			`categorie_id`,
			`article_id`,
			`prix_vente`,
			`cree_par`,
			`cree_le`,
			`modifie_par`,
			`modifie_le`)
		VALUES( 
			OLD.prix_id,
			OLD.entreprise_id,
			OLD.distribution_id,
			OLD.categorie_id,
			OLD.article_id,
			OLD.prix_vente,
			OLD.cree_par,
			OLD.cree_le,
			OLD.modifie_par,
			OLD.modifie_le);
	END IF;

END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

-- Dumping structure for trigger cyber_saler.tbl_vente_BEFORE_INSERT
SET @OLDTMP_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
DELIMITER //
CREATE TRIGGER `cyber_saler`.`tbl_vente_BEFORE_INSERT` BEFORE INSERT ON `tbl_vente` FOR EACH ROW
BEGIN
	SET NEW.cree_le = now();
END//
DELIMITER ;
SET SQL_MODE=@OLDTMP_SQL_MODE;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
