-- MySQL dump 10.13  Distrib 9.2.0, for macos14.7 (x86_64)
--
-- Host: localhost    Database: concesionaria_Autos
-- ------------------------------------------------------
-- Server version	9.1.0

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
-- Table structure for table `Aseguradora`
--

DROP TABLE IF EXISTS `Aseguradora`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Aseguradora` (
  `idAseguradora` int NOT NULL AUTO_INCREMENT,
  `nombreAseguradora` varchar(20) NOT NULL,
  `contactoAseguradora` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`idAseguradora`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Aseguradora`
--

LOCK TABLES `Aseguradora` WRITE;
/*!40000 ALTER TABLE `Aseguradora` DISABLE KEYS */;
INSERT INTO `Aseguradora` VALUES (1,'Allianz','allianz@contacto.com'),(2,'Mapfre','mapfre@contacto.com'),(3,'AXA','axa@contacto.com'),(4,'Liberty Seguros','liberty@contacto.com'),(5,'Zurich','zurich@contacto.com');
/*!40000 ALTER TABLE `Aseguradora` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `CLIENTE`
--

DROP TABLE IF EXISTS `CLIENTE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `CLIENTE` (
  `idCliente` int NOT NULL AUTO_INCREMENT,
  `idPersona` int NOT NULL,
  `fecha_registro` date NOT NULL,
  PRIMARY KEY (`idCliente`),
  KEY `idPersona` (`idPersona`),
  CONSTRAINT `cliente_ibfk_1` FOREIGN KEY (`idPersona`) REFERENCES `PERSONA` (`idPersona`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=159 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CLIENTE`
--

LOCK TABLES `CLIENTE` WRITE;
/*!40000 ALTER TABLE `CLIENTE` DISABLE KEYS */;
INSERT INTO `CLIENTE` VALUES (118,1088,'2021-09-15'),(139,1145,'2021-08-17'),(142,1129,'2019-07-10'),(147,1112,'2020-02-05'),(155,1075,'2023-07-14');
/*!40000 ALTER TABLE `CLIENTE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `EMPLEADO`
--

DROP TABLE IF EXISTS `EMPLEADO`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `EMPLEADO` (
  `idEmpleado` int NOT NULL AUTO_INCREMENT,
  `idPersona` int NOT NULL,
  `email` varchar(64) DEFAULT NULL,
  `ci` varchar(10) DEFAULT NULL,
  `comisionES` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`idEmpleado`),
  KEY `idPersona` (`idPersona`),
  CONSTRAINT `empleado_ibfk_1` FOREIGN KEY (`idPersona`) REFERENCES `PERSONA` (`idPersona`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=226 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `EMPLEADO`
--

LOCK TABLES `EMPLEADO` WRITE;
/*!40000 ALTER TABLE `EMPLEADO` DISABLE KEYS */;
INSERT INTO `EMPLEADO` VALUES (205,1056,'andrea.empresa@example.com','87654321','10%'),(210,1023,'luis.empresa@example.com','12345678','5%'),(211,1203,'ana.empresa@example.com','44556677','7%'),(212,1004,'maria.empresa@example.com','22334455','8%'),(213,1039,'oscar.empresa@example.com','77889900','6%');
/*!40000 ALTER TABLE `EMPLEADO` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ESTADO_VEHICULO`
--

DROP TABLE IF EXISTS `ESTADO_VEHICULO`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ESTADO_VEHICULO` (
  `idEstadoVehiculo` int NOT NULL AUTO_INCREMENT,
  `nombre_estado` varchar(20) NOT NULL,
  `descripcion` varchar(100) NOT NULL,
  PRIMARY KEY (`idEstadoVehiculo`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ESTADO_VEHICULO`
--

LOCK TABLES `ESTADO_VEHICULO` WRITE;
/*!40000 ALTER TABLE `ESTADO_VEHICULO` DISABLE KEYS */;
INSERT INTO `ESTADO_VEHICULO` VALUES (1,'Disponible','Vehículo disponible para reserva o venta'),(2,'En Mantenimiento','Vehículo en revisión o reparación'),(3,'Alquilado','Vehículo actualmente alquilado'),(4,'Vendido','Vehículo vendido, no disponible'),(5,'Reservado','Vehículo reservado por un cliente');
/*!40000 ALTER TABLE `ESTADO_VEHICULO` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `FIDELIZACION`
--

DROP TABLE IF EXISTS `FIDELIZACION`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `FIDELIZACION` (
  `idFidelizacion` int NOT NULL AUTO_INCREMENT,
  `idCliente` int NOT NULL,
  `puntos` int NOT NULL,
  `nivel` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`idFidelizacion`),
  KEY `fk_fidelizacion_idCliente` (`idCliente`),
  CONSTRAINT `fk_fidelizacion_idCliente` FOREIGN KEY (`idCliente`) REFERENCES `CLIENTE` (`idCliente`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=511 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `FIDELIZACION`
--

LOCK TABLES `FIDELIZACION` WRITE;
/*!40000 ALTER TABLE `FIDELIZACION` DISABLE KEYS */;
INSERT INTO `FIDELIZACION` VALUES (503,142,350,'Oro'),(505,118,200,'Plata'),(507,139,180,'Bronce'),(508,147,280,'Plata'),(510,155,220,'Plata');
/*!40000 ALTER TABLE `FIDELIZACION` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MANTENIMIENTO`
--

DROP TABLE IF EXISTS `MANTENIMIENTO`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MANTENIMIENTO` (
  `idMantenimiento` int NOT NULL AUTO_INCREMENT,
  `idVehiculo` int NOT NULL,
  `descripcion` varchar(100) DEFAULT NULL,
  `estado` varchar(20) DEFAULT NULL,
  `fechaMantenimiento` date NOT NULL,
  PRIMARY KEY (`idMantenimiento`),
  KEY `idVehiculo` (`idVehiculo`),
  CONSTRAINT `mantenimiento_ibfk_1` FOREIGN KEY (`idVehiculo`) REFERENCES `VEHICULO` (`idVehiculo`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MANTENIMIENTO`
--

LOCK TABLES `MANTENIMIENTO` WRITE;
/*!40000 ALTER TABLE `MANTENIMIENTO` DISABLE KEYS */;
INSERT INTO `MANTENIMIENTO` VALUES (1,1,'Cambio de aceite y filtros','Completado','2024-10-10'),(2,2,'Reparación del sistema de frenos','Pendiente','2024-10-12'),(3,3,'Mantenimiento de transmisión','En progreso','2024-10-14'),(4,4,'Alineación de ruedas','Completado','2024-10-15'),(5,5,'Revisión general','En espera','2024-10-16'),(6,6,'Reparación de suspensión','En progreso','2024-10-17'),(7,7,'Cambio de bujías','Completado','2024-10-18'),(8,8,'Revisión del sistema de escape','Pendiente','2024-10-19'),(9,9,'Inspección de carrocería','En espera','2024-10-20'),(10,10,'Revisión eléctrica','Completado','2024-10-21');
/*!40000 ALTER TABLE `MANTENIMIENTO` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MANTENIMIENTO_REPUESTOS`
--

DROP TABLE IF EXISTS `MANTENIMIENTO_REPUESTOS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MANTENIMIENTO_REPUESTOS` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idMantenimiento` int NOT NULL,
  `idRepuestos` int NOT NULL,
  `cantidad` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idMantenimiento` (`idMantenimiento`),
  KEY `idRepuestos` (`idRepuestos`),
  CONSTRAINT `mantenimiento_repuestos_ibfk_1` FOREIGN KEY (`idMantenimiento`) REFERENCES `MANTENIMIENTO` (`idMantenimiento`),
  CONSTRAINT `mantenimiento_repuestos_ibfk_2` FOREIGN KEY (`idRepuestos`) REFERENCES `REPUESTOS` (`idRepuestos`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MANTENIMIENTO_REPUESTOS`
--

LOCK TABLES `MANTENIMIENTO_REPUESTOS` WRITE;
/*!40000 ALTER TABLE `MANTENIMIENTO_REPUESTOS` DISABLE KEYS */;
INSERT INTO `MANTENIMIENTO_REPUESTOS` VALUES (1,1,1,1),(2,2,2,1),(3,3,3,4),(4,4,4,3),(5,5,5,2),(6,6,6,1),(7,7,7,1),(8,8,8,1),(9,9,9,4),(10,10,10,1);
/*!40000 ALTER TABLE `MANTENIMIENTO_REPUESTOS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `MARCA`
--

DROP TABLE IF EXISTS `MARCA`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `MARCA` (
  `idMarca` int NOT NULL AUTO_INCREMENT,
  `nombreMarca` varchar(10) NOT NULL,
  `descripcion` varchar(100) DEFAULT NULL,
  `paisMarca` varchar(15) NOT NULL,
  PRIMARY KEY (`idMarca`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `MARCA`
--

LOCK TABLES `MARCA` WRITE;
/*!40000 ALTER TABLE `MARCA` DISABLE KEYS */;
INSERT INTO `MARCA` VALUES (1,'Toyota','Marca japonesa de vehículos confiable y popular','Japón'),(2,'Ford','Pionera en la industria automotriz','Estados Unidos'),(3,'BMW','Fabricante alemán de autos de lujo','Alemania'),(4,'Chevrolet','Marca estadounidense de autos y camionetas','Estados Unidos'),(5,'Hyundai','Marca de vehículos coreana','Corea del Sur'),(6,'Honda','Marca japonesa con una gran variedad de vehículos','Japón'),(7,'Kia','Fabricante surcoreano de vehículos','Corea del Sur'),(8,'Audi','Marca alemana de autos de lujo','Alemania'),(9,'Nissan','Marca japonesa conocida por sus modelos económicos','Japón'),(10,'Volkswagen','Fabricante alemán de vehículos confiable','Alemania');
/*!40000 ALTER TABLE `MARCA` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PERSONA`
--

DROP TABLE IF EXISTS `PERSONA`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `PERSONA` (
  `idPersona` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(20) NOT NULL,
  `paterno` varchar(20) NOT NULL,
  `materno` varchar(20) DEFAULT NULL,
  `direccion` varchar(50) DEFAULT NULL,
  `telefono` varchar(12) DEFAULT NULL,
  `email` varchar(64) DEFAULT NULL,
  `fecha_nacimiento` date NOT NULL,
  PRIMARY KEY (`idPersona`)
) ENGINE=InnoDB AUTO_INCREMENT=1216 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PERSONA`
--

LOCK TABLES `PERSONA` WRITE;
/*!40000 ALTER TABLE `PERSONA` DISABLE KEYS */;
INSERT INTO `PERSONA` VALUES (1004,'Maria','Perez','Sanchez','Calle Flores, Oruro','78901234','maria.perez@example.com','1985-12-02'),(1023,'Luis','Martinez','Soto','Calle 5, La Paz','71234567','luis.martinez@example.com','1990-05-12'),(1039,'Oscar','Rivero','Perez','Av. San Martin, La Paz','76789012','oscar.rivero@example.com','1991-08-22'),(1056,'Andrea','Lopez','Rios','Calle 12, Cochabamba','71234890','andrea.lopez@example.com','1988-07-22'),(1075,'Carla','Mendoza','Alvarez','Calle Bolivar, Beni','77123456','carla.mendoza@example.com','1986-11-30'),(1088,'Diego','Salazar','Garcia','Av. Sucre, Potosi','71230678','diego.salazar@example.com','1995-03-14'),(1112,'Raquel','Paredes','Gutierrez','Calle 10, Santa Cruz','75432109','raquel.paredes@example.com','1989-02-17'),(1129,'Carlos','Gomez','Torrez','Av. Blanco, Sucre','72345678','carlos.gomez@example.com','1992-10-03'),(1145,'Jorge','Vargas','Mendoza','Av. Blanco Galindo, Cochabamba','71239876','jorge.vargas@example.com','1993-04-27'),(1203,'Ana','Fernandez','Romero','Calle Colon, Tarija','78905432','ana.fernandez@example.com','1987-06-09');
/*!40000 ALTER TABLE `PERSONA` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `REALIZA`
--

DROP TABLE IF EXISTS `REALIZA`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `REALIZA` (
  `idCliente` int NOT NULL,
  `idVehiculo` int NOT NULL,
  `idTransaccion` int NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `fecha` date NOT NULL,
  PRIMARY KEY (`idCliente`,`idVehiculo`,`idTransaccion`),
  KEY `idVehiculo` (`idVehiculo`),
  KEY `idTransaccion` (`idTransaccion`),
  CONSTRAINT `realiza_fk_idCliente` FOREIGN KEY (`idCliente`) REFERENCES `CLIENTE` (`idCliente`) ON DELETE CASCADE,
  CONSTRAINT `realiza_ibfk_2` FOREIGN KEY (`idVehiculo`) REFERENCES `VEHICULO` (`idVehiculo`),
  CONSTRAINT `realiza_ibfk_3` FOREIGN KEY (`idTransaccion`) REFERENCES `TRANSACCION` (`idTransaccion`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `REALIZA`
--

LOCK TABLES `REALIZA` WRITE;
/*!40000 ALTER TABLE `REALIZA` DISABLE KEYS */;
INSERT INTO `REALIZA` VALUES (142,1,11,15000.00,'2025-01-27'),(142,8,8,450.00,'2024-10-19'),(147,3,3,650.00,'2024-10-14');
/*!40000 ALTER TABLE `REALIZA` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `REPUESTOS`
--

DROP TABLE IF EXISTS `REPUESTOS`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `REPUESTOS` (
  `idRepuestos` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(30) NOT NULL,
  `descripcion` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`idRepuestos`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `REPUESTOS`
--

LOCK TABLES `REPUESTOS` WRITE;
/*!40000 ALTER TABLE `REPUESTOS` DISABLE KEYS */;
INSERT INTO `REPUESTOS` VALUES (1,'Filtro de aire','Filtro de aire para motor'),(2,'Pastillas de freno','Pastillas de freno delanteras y traseras'),(3,'Bujías','Bujías para motor de 4 cilindros'),(4,'Aceite sintético','Aceite de motor 5W-30'),(5,'Filtro de aceite','Filtro de aceite para motor'),(6,'Amortiguador','Amortiguador delantero'),(7,'Correa de distribución','Correa para el sistema de distribución'),(8,'Batería','Batería para sistema de encendido'),(9,'Neumático','Neumático radial 195/65 R15'),(10,'Espejo lateral','Espejo lateral derecho');
/*!40000 ALTER TABLE `REPUESTOS` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `RESERVA`
--

DROP TABLE IF EXISTS `RESERVA`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `RESERVA` (
  `idReserva` int NOT NULL AUTO_INCREMENT,
  `idCliente` int NOT NULL,
  `idEmpleado` int NOT NULL,
  `fechaInicio` date NOT NULL,
  `fechaFin` date NOT NULL,
  `contrato` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`idReserva`),
  KEY `idEmpleado` (`idEmpleado`),
  KEY `fk_reserva_idCliente` (`idCliente`),
  CONSTRAINT `fk_reserva_idCliente` FOREIGN KEY (`idCliente`) REFERENCES `CLIENTE` (`idCliente`) ON DELETE CASCADE,
  CONSTRAINT `reserva_fk_idCliente` FOREIGN KEY (`idCliente`) REFERENCES `CLIENTE` (`idCliente`) ON DELETE CASCADE,
  CONSTRAINT `reserva_ibfk_2` FOREIGN KEY (`idEmpleado`) REFERENCES `EMPLEADO` (`idEmpleado`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=412 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `RESERVA`
--

LOCK TABLES `RESERVA` WRITE;
/*!40000 ALTER TABLE `RESERVA` DISABLE KEYS */;
INSERT INTO `RESERVA` VALUES (403,142,210,'2023-07-10','2023-07-25','R-003'),(405,118,210,'2024-01-15','2024-01-30','R-005'),(408,147,205,'2023-05-15','2023-05-25','R-008'),(410,155,213,'2024-08-05','2024-08-20','R-010'),(411,142,211,'2025-01-23','2025-01-31','R-15');
/*!40000 ALTER TABLE `RESERVA` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SEGUIMIENTO_VEHICULO`
--

DROP TABLE IF EXISTS `SEGUIMIENTO_VEHICULO`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SEGUIMIENTO_VEHICULO` (
  `id` int NOT NULL AUTO_INCREMENT,
  `idVehiculo` int NOT NULL,
  `ubicacionActual` varchar(50) DEFAULT NULL,
  `ultimaFechaActualizacion` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idVehiculo` (`idVehiculo`),
  CONSTRAINT `seguimiento_vehiculo_ibfk_1` FOREIGN KEY (`idVehiculo`) REFERENCES `VEHICULO` (`idVehiculo`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SEGUIMIENTO_VEHICULO`
--

LOCK TABLES `SEGUIMIENTO_VEHICULO` WRITE;
/*!40000 ALTER TABLE `SEGUIMIENTO_VEHICULO` DISABLE KEYS */;
INSERT INTO `SEGUIMIENTO_VEHICULO` VALUES (1,1,'Sede Principal','2024-10-15'),(2,2,'Sucursal Norte','2024-10-14'),(3,3,'Sucursal Oeste','2024-10-13'),(4,4,'Sucursal Sur','2024-10-12'),(5,5,'Sede Principal','2024-10-11'),(6,6,'Sucursal Este','2024-10-10'),(7,7,'Sucursal Norte','2024-10-09'),(8,8,'Sucursal Oeste','2024-10-08'),(9,9,'Sede Principal','2024-10-07'),(10,10,'Sucursal Sur','2024-10-06');
/*!40000 ALTER TABLE `SEGUIMIENTO_VEHICULO` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SEGURO`
--

DROP TABLE IF EXISTS `SEGURO`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `SEGURO` (
  `idSeguro` int NOT NULL AUTO_INCREMENT,
  `idVehiculo` int NOT NULL,
  `idAseguradora` int NOT NULL,
  `fechaInicio` date NOT NULL,
  `fechaFin` date NOT NULL,
  `tipoSeguro` varchar(20) DEFAULT NULL,
  `costo` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`idSeguro`),
  KEY `idVehiculo` (`idVehiculo`),
  KEY `idAseguradora` (`idAseguradora`),
  CONSTRAINT `seguro_ibfk_1` FOREIGN KEY (`idVehiculo`) REFERENCES `VEHICULO` (`idVehiculo`),
  CONSTRAINT `seguro_ibfk_2` FOREIGN KEY (`idAseguradora`) REFERENCES `ASEGURADORA` (`idAseguradora`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SEGURO`
--

LOCK TABLES `SEGURO` WRITE;
/*!40000 ALTER TABLE `SEGURO` DISABLE KEYS */;
INSERT INTO `SEGURO` VALUES (1,1,1,'2024-01-01','2025-01-01','Cobertura Completa',1500.00),(2,2,2,'2024-02-15','2025-02-15','Responsable Civil',1200.00),(3,3,3,'2024-03-10','2025-03-10','Cobertura Total',1800.00),(4,4,4,'2024-04-05','2025-04-05','Cobertura Completa',1700.00),(5,5,5,'2024-05-20','2025-05-20','Riesgo de Daños',1300.00),(6,6,1,'2024-06-15','2025-06-15','Cobertura Completa',1400.00),(7,7,2,'2024-07-01','2025-07-01','Responsable Civil',1150.00),(8,8,3,'2024-08-10','2025-08-10','Cobertura Completa',1650.00),(9,9,4,'2024-09-12','2025-09-12','Cobertura Completa',1550.00),(10,10,5,'2024-10-20','2025-10-20','Cobertura Completa',1450.00);
/*!40000 ALTER TABLE `SEGURO` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TIPO_CAMBIO`
--

DROP TABLE IF EXISTS `TIPO_CAMBIO`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `TIPO_CAMBIO` (
  `idTipoCambio` int NOT NULL AUTO_INCREMENT,
  `fechaTipoCambio` date NOT NULL,
  `valorDolar` decimal(10,2) NOT NULL,
  PRIMARY KEY (`idTipoCambio`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TIPO_CAMBIO`
--

LOCK TABLES `TIPO_CAMBIO` WRITE;
/*!40000 ALTER TABLE `TIPO_CAMBIO` DISABLE KEYS */;
INSERT INTO `TIPO_CAMBIO` VALUES (1,'2024-10-10',6.91),(2,'2024-10-11',6.89),(3,'2024-10-12',6.92),(4,'2024-10-13',6.90),(5,'2024-10-14',6.93),(6,'2024-10-15',6.94),(7,'2024-10-16',6.95),(8,'2024-10-17',6.90),(9,'2024-10-18',6.89),(10,'2024-10-19',6.88);
/*!40000 ALTER TABLE `TIPO_CAMBIO` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TRANSACCION`
--

DROP TABLE IF EXISTS `TRANSACCION`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `TRANSACCION` (
  `idTransaccion` int NOT NULL AUTO_INCREMENT,
  `idCliente` int NOT NULL,
  `tipoTransaccion` varchar(20) NOT NULL,
  `fechaTransaccion` date NOT NULL,
  `costo` decimal(10,2) NOT NULL,
  `idTipoCambio` int NOT NULL,
  PRIMARY KEY (`idTransaccion`),
  KEY `idTipoCambio` (`idTipoCambio`),
  KEY `fk_transaccion_idCliente` (`idCliente`),
  CONSTRAINT `fk_transaccion_idCliente` FOREIGN KEY (`idCliente`) REFERENCES `CLIENTE` (`idCliente`) ON DELETE CASCADE,
  CONSTRAINT `transaccion_ibfk_1` FOREIGN KEY (`idCliente`) REFERENCES `CLIENTE` (`idCliente`),
  CONSTRAINT `transaccion_ibfk_2` FOREIGN KEY (`idTipoCambio`) REFERENCES `TIPO_CAMBIO` (`idTipoCambio`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TRANSACCION`
--

LOCK TABLES `TRANSACCION` WRITE;
/*!40000 ALTER TABLE `TRANSACCION` DISABLE KEYS */;
INSERT INTO `TRANSACCION` VALUES (3,142,'Alquiler','2024-10-14',650.00,3),(5,118,'Alquiler','2024-10-16',500.00,5),(7,139,'Venta','2024-10-18',21000.00,7),(8,147,'Alquiler','2024-10-19',450.00,8),(10,155,'Alquiler','2024-10-21',400.00,10),(11,142,'Venta','2025-01-27',15000.00,1),(15,142,'Alquiler','2025-01-27',960.00,1);
/*!40000 ALTER TABLE `TRANSACCION` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `USUARIO`
--

DROP TABLE IF EXISTS `USUARIO`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `USUARIO` (
  `idUsuario` int NOT NULL AUTO_INCREMENT,
  `idEmpleado` int DEFAULT NULL,
  `nombreUsuario` varchar(20) NOT NULL,
  `contrasena` varchar(60) NOT NULL,
  `rolUsuario` enum('Admin','User') NOT NULL,
  `idCliente` int DEFAULT NULL,
  PRIMARY KEY (`idUsuario`),
  KEY `fk_usuario_cliente` (`idCliente`),
  KEY `fk_usuario_empleado` (`idEmpleado`),
  CONSTRAINT `fk_usuario_cliente` FOREIGN KEY (`idCliente`) REFERENCES `CLIENTE` (`idCliente`) ON DELETE CASCADE,
  CONSTRAINT `fk_usuario_empleado` FOREIGN KEY (`idEmpleado`) REFERENCES `EMPLEADO` (`idEmpleado`) ON DELETE CASCADE,
  CONSTRAINT `chk_one_relationship` CHECK ((((`idCliente` is not null) and (`idEmpleado` is null)) or ((`idCliente` is null) and (`idEmpleado` is not null))))
) ENGINE=InnoDB AUTO_INCREMENT=319 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `USUARIO`
--

LOCK TABLES `USUARIO` WRITE;
/*!40000 ALTER TABLE `USUARIO` DISABLE KEYS */;
INSERT INTO `USUARIO` VALUES (301,210,'luis_m','$2b$12$kvuJAWnKqj.d.IrZZVLv0OuSO9eFvrdTGx/G7Acnz0xAFDX7iEDYi','Admin',NULL),(302,205,'andrea_l','$2b$12$BkvjoMOgDBZI5Bd/te1GfO8DV72Jy/7LzwPHRPUe/yNrSp8mYkYlq','Admin',NULL),(303,NULL,'carlos_g','$2b$12$WbZA53JARuR2lejzx9IvP.juNMu3puyJIHzKIw0Ts2Fv3SfL3BgWO','User',142),(304,212,'maria_p','$2b$12$uZcN2I6aOXEvbsL8QL2xWOEy4owvNt3anOqcrlIUUJkBbpO8h70a6','Admin',NULL),(305,NULL,'diego_s','$2b$12$XSAdt.MT20xSwU1PfhwWTuOYEW7I6QtGP5f0aTs3iCa.WwkhuUop.','User',118),(306,211,'ana_f','$2b$12$U9aGmlAse/krzYDn70VIhOdE0Nr5dIDG5C63e6ZSeAdTPDNw6cLK2','Admin',NULL),(307,NULL,'jorge_v','$2b$12$d322Db8068Ug6r7ma2nF4ex15ms2PagFrI/9nB.TJdfiAFDxYZ7Nu','User',139),(308,NULL,'raquel_p','$2b$12$IESZbJlpYzcbd06KLFNCDuSSBg4KCxMF6vBt7Pp6xAFoHxr6pYUMa','User',147),(309,213,'oscar_r','$2b$12$b577KBI6JVngCbP9q20y5OvQp0/f1i5iHG5u0ugTnvufrDJansuq.','Admin',NULL),(310,NULL,'carla_m','$2b$12$C5XllHKSa5uYQj6WBw5wo.VOuDgV6X3aOxoTYj.3nHTZz1zo35Sta','User',155);
/*!40000 ALTER TABLE `USUARIO` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `VEHICULO`
--

DROP TABLE IF EXISTS `VEHICULO`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `VEHICULO` (
  `idVehiculo` int NOT NULL AUTO_INCREMENT,
  `anio` int NOT NULL,
  `modelo` varchar(70) NOT NULL,
  `precioDiario` decimal(10,2) NOT NULL,
  `precioDolar` decimal(10,2) NOT NULL,
  `caracteristicas` varchar(200) DEFAULT NULL,
  `idEstadoVehiculo` int NOT NULL,
  `idMarca` int NOT NULL,
  `IMAGEN_URL` varchar(50) DEFAULT NULL,
  `combustible` varchar(20) DEFAULT NULL,
  `kilometraje` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`idVehiculo`),
  KEY `idEstadoVehiculo` (`idEstadoVehiculo`),
  KEY `idMarca` (`idMarca`),
  CONSTRAINT `vehiculo_ibfk_1` FOREIGN KEY (`idEstadoVehiculo`) REFERENCES `ESTADO_VEHICULO` (`idEstadoVehiculo`),
  CONSTRAINT `vehiculo_ibfk_2` FOREIGN KEY (`idMarca`) REFERENCES `MARCA` (`idMarca`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=58 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `VEHICULO`
--

LOCK TABLES `VEHICULO` WRITE;
/*!40000 ALTER TABLE `VEHICULO` DISABLE KEYS */;
INSERT INTO `VEHICULO` VALUES (1,2020,'Corolla',55.00,15000.00,'Compacto, eficiente en combustible',4,1,'corolla2020','Gasolina',0.00),(2,2019,'Focus',50.00,14000.00,'Compacto, motor turbo',3,2,'focus2019','Gasolina',0.00),(3,2022,'X5',120.00,60000.00,'SUV de lujo, gran capacidad',3,3,'x52022','Gasolina',0.00),(4,2018,'Cruze',45.00,13000.00,'Sedán, económico y espacioso',1,4,'cruze2018','Gasolina',0.00),(5,2021,'Elantra',53.00,15500.00,'Compacto, tecnología avanzada',1,5,'elantra2021','Hibrido',0.00),(6,2019,'Civic',55.00,14500.00,'Compacto deportivo',2,6,'civic2019','Gasolina',0.00),(7,2020,'Sportage',70.00,18000.00,'SUV, gran espacio',1,7,'sportage2020','Gasolina',0.00),(8,2021,'A4',115.00,55000.00,'Sedán de lujo',3,8,'a42021','Gasolina',0.00),(9,2017,'Sentra',42.00,12000.00,'Compacto asequible',4,9,'sentra2017','Gasolina',0.00),(10,2018,'Jetta',50.00,16000.00,'Compacto confiable',5,10,'jetta2018','Diesel',0.00),(11,2021,'Camry',70.00,24000.00,'Sedán mediano, cómodo y confiable',1,1,'camry2021','Gasolina',1000.00),(12,2020,'RAV4',80.00,28000.00,'SUV compacto, ideal para la familia',1,1,'rav42020','Gasolina',5000.00),(13,2018,'Highlander',90.00,32000.00,'SUV grande, espacioso y potente',2,1,'highlander2018','Gasolina',20000.00),(14,2022,'Corolla Cross',75.00,26000.00,'SUV compacto basado en el Corolla',1,1,'corollacross2022','Gasolina',500.00),(15,2019,'Prius',65.00,22000.00,'Híbrido eficiente en consumo de combustible',3,1,'prius2019','Híbrido',30000.00),(16,2021,'Tacoma',85.00,30000.00,'Pickup mediana, ideal para trabajo',1,1,'tacoma2021','Gasolina',8000.00),(17,2020,'Avalon',95.00,35000.00,'Sedán grande de lujo',1,1,'avalon2020','Gasolina',12000.00),(18,2019,'4Runner',90.00,33000.00,'SUV todoterreno, resistente y confiable',2,1,'4runner2019','Gasolina',25000.00),(19,2017,'Sequoia',100.00,45000.00,'SUV de gran tamaño, ideal para la familia',3,1,'sequoia2017','Gasolina',40000.00),(20,2022,'Supra',150.00,55000.00,'Deportivo con diseño aerodinámico',1,1,'supra2022','Gasolina',2000.00),(21,2018,'Sienna',85.00,31000.00,'Minivan espaciosa y cómoda',2,1,'sienna2018','Gasolina',30000.00),(22,2021,'Land Cruiser',200.00,85000.00,'SUV de lujo, todoterreno',1,1,'landcruiser2021','Gasolina',10000.00),(23,2020,'Yaris',50.00,18000.00,'Compacto económico y práctico',1,1,'yaris2020','Gasolina',8000.00),(24,2021,'C-HR',75.00,25000.00,'SUV subcompacto con diseño único',1,1,'chr2021','Gasolina',3000.00),(25,2019,'Tundra',110.00,45000.00,'Pickup de tamaño completo',2,1,'tundra2019','Gasolina',35000.00),(26,2022,'Mirai',120.00,60000.00,'Sedán de hidrógeno, innovador',1,1,'mirai2022','Hidrógeno',500.00),(27,2018,'FJ Cruiser',95.00,40000.00,'SUV todoterreno, diseño retro',3,1,'fjcruiser2018','Gasolina',50000.00),(28,2022,'Venza',85.00,34000.00,'SUV híbrida, elegante y eficiente',1,1,'venza2022','Híbrido',1000.00),(29,2020,'Hilux',100.00,37000.00,'Pickup compacta, confiable y resistente',1,1,'hilux2020','Gasolina',12000.00),(30,2021,'GR86',140.00,40000.00,'Coupé deportivo, ligero y ágil',1,1,'gr862021','Gasolina',3000.00),(31,2022,'Mustang',120.00,55000.00,'Deportivo de alto rendimiento, motor V8',1,2,'mustang2022','Gasolina',0.00),(32,2021,'F-150',100.00,45000.00,'Camioneta todoterreno, capacidad de carga alta',1,2,'f1502021','Gasolina',10000.00),(33,2023,'Explorer',90.00,40000.00,'SUV familiar, amplio espacio interior',1,2,'explorer2023','Gasolina',5000.00),(34,2022,'Ranger',85.00,38000.00,'Pickup versátil, ideal para trabajo y recreación',1,2,'ranger2022','Diesel',15000.00),(35,2023,'Raptor',150.00,65000.00,'Camioneta de alto desempeño todoterreno',1,2,'raptor2023','Gasolina',2000.00),(36,2022,'Expedition',110.00,60000.00,'SUV premium, ideal para familias grandes',2,2,'expedition2022','Gasolina',8000.00),(37,2023,'M4 CS',200.00,80000.00,'Deportivo de lujo, motor turbo de alto desempeño',1,3,'m4_cs2023','Gasolina',0.00),(38,2022,'X6',150.00,70000.00,'SUV de lujo, diseño deportivo, tecnología avanzada',1,3,'x6_2022','Gasolina',5000.00),(39,2021,'M2 LCI',180.00,65000.00,'Coupé compacto de alto rendimiento, motor turbo',1,3,'m2_lci2021','Gasolina',10000.00),(40,2023,'Captiva',70.00,25000.00,'SUV versátil y espaciosa, diseño moderno',1,4,'captiva2023','Gasolina',0.00),(41,2022,'Onix',50.00,18000.00,'Compacto eficiente, tecnología avanzada',1,4,'onix2022','Gasolina',5000.00),(42,2023,'Tracker',65.00,22000.00,'SUV compacto, ideal para ciudad y carretera',1,4,'tracker2023','Gasolina',0.00),(43,2023,'Tahoe',120.00,60000.00,'SUV grande de lujo, ideal para familias',2,4,'tahoe2023','Gasolina',0.00),(44,2023,'Camaro',150.00,55000.00,'Deportivo icónico, diseño aerodinámico',1,4,'camaro2023','Gasolina',0.00),(45,2024,'Equinox EV',90.00,40000.00,'SUV eléctrica, autonomía extendida y diseño futurista',2,4,'equinox_ev2024','Eléctrico',0.00),(46,2023,'A3',80.00,35000.00,'Sedán compacto de lujo, diseño elegante y eficiente',1,4,'a3_2023','Gasolina',0.00),(47,2022,'Q2',85.00,37000.00,'SUV compacto premium, ideal para la ciudad',1,4,'q2_2022','Gasolina',5000.00),(48,2023,'SQ5',120.00,60000.00,'SUV deportivo con motor de alto rendimiento',1,4,'sq5_2023','Gasolina',0.00),(49,2024,'e-tron',140.00,80000.00,'SUV eléctrica de lujo, autonomía extendida y tecnología avanzada',1,4,'etron_2024','Eléctrico',0.00),(50,2023,'Kicks',60.00,21000.00,'SUV compacto, diseño moderno y eficiente en combustible',1,9,'kicks_2023','Gasolina',200.00),(51,2023,'Qashqai',75.00,25000.00,'SUV versátil con tecnología avanzada',1,9,'qashqai_2023','Gasolina',100.00),(52,2022,'X-Trail',90.00,32000.00,'SUV espaciosa, ideal para viajes largos y familiares',2,9,'x_trail_2022','Gasolina',5000.00),(53,2024,'Patrol',150.00,80000.00,'SUV premium todoterreno con capacidades avanzadas',3,9,'patrol_2024','Gasolina',0.00),(54,2023,'Versa',50.00,18000.00,'Sedán compacto, ideal para uso urbano y económico',1,9,'versa_2023','Gasolina',0.00),(55,2023,'Amarok',120.00,45000.00,'Camioneta robusta y versátil, ideal para trabajos pesados y aventuras',1,10,'amarok_2023','Diesel',300.00),(56,2023,'T-Cross',80.00,25000.00,'SUV compacto, diseño moderno y eficiente para la ciudad',2,10,'t_cross_2023','Gasolina',100.00),(57,2022,'Golf',70.00,30000.00,'Hatchback icónico con excelente desempeño y comodidad',1,10,'golf_2022','Gasolina',4000.00);
/*!40000 ALTER TABLE `VEHICULO` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-28  0:50:34
