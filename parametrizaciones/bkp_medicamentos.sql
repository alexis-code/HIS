-- MySQL dump 10.13  Distrib 8.0.25, for Win64 (x86_64)
--
-- Host: localhost    Database: db_hospitaljapones_test
-- ------------------------------------------------------
-- Server version	8.0.25

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tb_medicamento`
--

DROP TABLE IF EXISTS `tb_medicamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tb_medicamento` (
  `id_medicamentoPK` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(500) NOT NULL,
  `medida` varchar(100) NOT NULL,
  `estado` varchar(20) NOT NULL,
  PRIMARY KEY (`id_medicamentoPK`)
) ENGINE=InnoDB AUTO_INCREMENT=231 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_medicamento`
--

LOCK TABLES `tb_medicamento` WRITE;
/*!40000 ALTER TABLE `tb_medicamento` DISABLE KEYS */;
INSERT INTO `tb_medicamento` VALUES (116,'Acido Ascorbico 1 gr  ampolla','-','activo'),(117,'Acetilcisteina 600 mg  sobre','-','activo'),(118,'Acido Ascorbico 1 gr  comprimido','-','activo'),(119,'Acido Ascorbico 500 mg  ampolla','-','activo'),(120,'Adenosina 6mg/2ml , ampolla','-','activo'),(121,'Adrenalina 1mg ; ampolla','-','activo'),(122,'Agua Destilada 5 cc                        ','-','activo'),(123,'Albumina humana 20% 50ml ; fco/vial','-','activo'),(124,'Amikacina 100mg  fco/vial; ','-','activo'),(125,'Amikacina 500mg  fco/vial; ','-','activo'),(126,'Aminoácidos 10% 500ml ; fco','-','activo'),(127,'Aminoácidos 20% 500ml ; fco','-','activo'),(128,'Amiodarona 150 mg ; ampolla','-','activo'),(129,'Atracurio besilato 25 mg ; ampolla','-','activo'),(130,'Atracurio besilato 50 mg ; ampolla','-','activo'),(131,'Atropina 1mg ; ampolla','-','activo'),(132,'Betametasona fosfato 4mg/1ml ; ampolla','-','activo'),(133,'Bicarbonato de sodio 8% ; fco 500ml ','-','activo'),(134,'Bicarbonato de sodio 8% 20 ml ; ampolla ','-','activo'),(135,'Bolsa colectora ','-','activo'),(136,'Bolsa colectora 2000 ml','-','activo'),(137,'Branula N 20','-','activo'),(138,'Cateter de  via central  doble lumen ','-','activo'),(139,'Cateter de  via central  triple lumen ','-','activo'),(140,'Cateter intravenoso 14Gx2','-','activo'),(141,'Cateter intravenoso 16Gx1','-','activo'),(142,'Cateter intravenoso 18Gx1 1/4','-','activo'),(143,'Cateter intravenoso 20Gx1  1/4','-','activo'),(144,'Cefotaxima 1gramo ; fco/vial','-','activo'),(145,'Ceftriaxona 1g   ; fco/vial ','-','activo'),(146,'Ciprofloxacina 200mg ; Sachet','-','activo'),(147,'Circuito cerrado de aspiracion  ','-','activo'),(148,'Clorfenamina Maleato 20 mg ; fco/ampolla','-','activo'),(149,'Cloruro de potasio 20% 27 mEq ; ampolla     ','-','activo'),(150,'Cloruro de sodio 20% 70 mEq ; ampolla','-','activo'),(151,'Colistina  100mg ; ampolla','-','activo'),(152,'Dexametazona 4mg; ampolla','-','activo'),(153,'Dexametazona 8 mg; ampolla','-','activo'),(154,'Dexmedetomidina 200 Ug ; fco/ampolla','-','activo'),(155,'Diazepan 10mg ; ampolla','-','activo'),(156,'Digoxina 0.25mg ; ampolla','-','activo'),(157,'Dobutamina 250mg ; ampolla','-','activo'),(158,'Dopamina 200 mg ; ampolla','-','activo'),(159,'Electrodos ','-','activo'),(160,'Equipo de precisión','-','activo'),(161,'Equipo de suero           ','-','activo'),(162,'Equipo microgotero           ','-','activo'),(163,'Fenitoina 100 mg; ampolla','-','activo'),(164,'Fenitoina 250mg ; ampolla','-','activo'),(165,'Fenobarbital 100 mg ; ampolla','-','activo'),(166,'Fenobarbital 250 mg ; ampolla','-','activo'),(167,'Fentanyl 100ug ; fco/vial','-','activo'),(168,'Fentanyl 500ug ; Fco/vial','-','activo'),(169,'filtro  humidificador  y antibacteriano ','-','activo'),(170,'Levofloxacino 500 mg ; infusor/sachet','-','activo'),(171,'Fluconazol 200 mg  fco/vial; ','-','activo'),(172,'Furosemida 10mg ; ampolla','-','activo'),(173,'Furosemida 20 mg ; ampolla','-','activo'),(174,'Gluconato de Calcio 4.6mEq 10%; ampolla                        ','-','activo'),(175,'Heparina de bajo peso molecular 40 UI  jeringa precargada','-','activo'),(176,'Heparina de bajo peso molecular 60 UI  jeringa precargada','-','activo'),(177,'Heparina de bajo peso molecular 80 UI  jeringa precargada','-','activo'),(178,'Heparina Sodica 2500 UI ; fco/vial ','-','activo'),(179,'Hidrocortisona 100mg ; fco','-','activo'),(180,'Hidrocortisona 500mg; fco','-','activo'),(181,'Hilo Mononylon 1-0 ','-','activo'),(182,'Hilo Mononylon 2-0 ','-','activo'),(183,'Hilo Mononylon 3-0 ','-','activo'),(184,'Imipenem 500mg   fco/vial  ','-','activo'),(185,'Insulina cristalina 100 UI/ml ; fco/vial','-','activo'),(186,'Insulina NPH 100 UI/ml ; fco/vial','-','activo'),(187,'Ketamina clorhidrato 500 mg ; fco/vial','-','activo'),(188,'Lidocaina 2% 20ml ; fco ','-','activo'),(189,'Lidramina 20 mg ; fco/ampolla','-','activo'),(190,'Llave de tres vías                                  ','-','activo'),(191,'Manitol 20% 500 ml ; fco/infusor','-','activo'),(192,'Metamizol 1 gr ; ampolla','-','activo'),(193,'Metilprednisolona 1000 mg ; fco/vial','-','activo'),(194,'Metilprednisolona 500 mg ; fco/vial','-','activo'),(195,'Metoclopramida 10mg ; ampolla','-','activo'),(196,'Metronidazol 500mg ; fco/vial','-','activo'),(197,'Midazolam 15mg ; ampolla','-','activo'),(198,'Morfina 10 mg ; ampolla','-','activo'),(199,'Nitroglicerina 25 mg ; ampolla','-','activo'),(200,'Nitroglicerina 50mg ; ampolla','-','activo'),(201,'Norepinefrina 4 mg ampolla','-','activo'),(202,'Omeprazol 40mg ; fco ampolla','-','activo'),(203,'Ondansetron 8 mg ; ampolla','-','activo'),(204,'Ranitidina 50mg ; ampolla ','-','activo'),(205,'Solución Ringer Lactato 1000 ml ; fco  infusor','-','activo'),(206,'Solución Ringer Normal 1000 ml ; fco  infusor','-','activo'),(207,'Solución Dextrosa 50% 500ml ; fco infusor','-','activo'),(208,'Solución Dextrosa al 10 % 1000 ml; fco Infusor','-','activo'),(209,'Solución Dextrosa al 5% 1000 ; fco infusor','-','activo'),(210,'Solución Fisiológica 0,9% 1000 ml; fco infusor                ','-','activo'),(211,'Solucion Hipertrose 33.3% ; ampolla','-','activo'),(212,'Sonda FOLEY   N14     ','-','activo'),(213,'Sonda FOLEY   N16     ','-','activo'),(214,'Sonda FOLEY   N18','-','activo'),(215,'Succinil Colina 500 mg ; fco/vial','-','activo'),(216,'Sulfato de magnesio10% 8 meq ; ampolla','-','activo'),(217,'Terapidol Magnesico 2 gr ; ampolla','-','activo'),(218,'Tiopental Sodico 1000 mg  ; fco/ampolla','-','activo'),(219,'Tiopental Sodico 500 mg ; fco/ampolla','-','activo'),(220,'Tubo orotraqueal con cuff','-','activo'),(221,'Vancomicina  100mg ; fco/vial','-','activo'),(222,'Vancomicina  500mg ; fco/vial','-','activo'),(223,'Vitamina K 10mg ; ampolla','-','activo'),(224,'Meropenem 500mg   fco/vial  ','-','activo'),(225,'Acido Tranexamico 500 mg ; ampolla','-','activo'),(226,'Gentamicina 80mg/2ml ; ampolla','-','activo'),(227,'Alprazolam 2mg ; comprimido','-','activo'),(228,'Tramadol 100 mg/2ml ; ampolla','-','activo'),(229,'Ketoprofeno 100mg/2ml ; ampolla','-','activo'),(230,'Butil bromuro de Hioscina 20mg /1ml ; ampolla','-','Anulado');
/*!40000 ALTER TABLE `tb_medicamento` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-12-01 14:07:02
