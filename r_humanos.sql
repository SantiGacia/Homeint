-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 01-11-2021 a las 18:58:30
-- Versión del servidor: 10.4.19-MariaDB
-- Versión de PHP: 8.0.7

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `r_humanos`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `anuncio`
--

CREATE TABLE `anuncio` (
  `idAnuncio` int(11) NOT NULL,
  `idSolicitud` int(11) NOT NULL,
  `Num_Solicitantes` int(11) NOT NULL,
  `FechaPublicacion` date NOT NULL,
  `FechaCierre` date NOT NULL,
  `idcontacto` int(11) NOT NULL,
  `idMedioPublicidad` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `anuncio`
--

INSERT INTO `anuncio` (`idAnuncio`, `idSolicitud`, `Num_Solicitantes`, `FechaPublicacion`, `FechaCierre`, `idcontacto`, `idMedioPublicidad`) VALUES
(1, 1, 3, '2021-11-01', '2021-11-06', 1, 1),
(2, 2, 1, '2021-11-01', '2021-11-07', 2, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `area`
--

CREATE TABLE `area` (
  `idArea` int(11) NOT NULL,
  `AreaDescripcion` varchar(100) DEFAULT NULL,
  `AreaNombre` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `area`
--

INSERT INTO `area` (`idArea`, `AreaDescripcion`, `AreaNombre`) VALUES
(1, 'Desarrollo BackEnd', 'Desarrollo de sistemas web'),
(2, 'Diseñadores de elementos necesarios para web', 'Diseño de creativos'),
(3, 'Mantenimiento del equipo de computo', 'Soporte de equipo de computo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `candidato`
--

CREATE TABLE `candidato` (
  `Curp` varchar(18) NOT NULL,
  `RFC` varchar(13) DEFAULT NULL,
  `Nombre` varchar(45) DEFAULT NULL,
  `nacionalidad` text NOT NULL,
  `Domicilio` varchar(45) DEFAULT NULL,
  `Telefono` varchar(10) DEFAULT NULL,
  `E_Mail` varchar(45) DEFAULT NULL,
  `Sexo` varchar(45) DEFAULT NULL,
  `Edad` tinyint(2) DEFAULT NULL,
  `NSS` varchar(11) NOT NULL,
  `Fotografia` blob DEFAULT NULL,
  `idEstadoCivil` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `candidato`
--

INSERT INTO `candidato` (`Curp`, `RFC`, `Nombre`, `nacionalidad`, `Domicilio`, `Telefono`, `E_Mail`, `Sexo`, `Edad`, `NSS`, `Fotografia`, `idEstadoCivil`) VALUES
('COCR800325HASDDNB3', 'COCR800325NB3', 'CORONA CORONA ROBERTO', 'Mexicana', 'AVENIDA NIÑOS HEROES NO. 3 #502 20345', '4499707510', 'COC@GMAIL.COM', 'M', 41, '23597329246', NULL, 1),
('GAMS040407HASRRNA5', 'GAMS0404074T7', 'Garcia Martinez Santiago', 'Mexicana', 'Casiopea #408 ', '4491115555', 'ssantig07@gmail.com', 'M', 18, '44190407518', NULL, 1),
('MORJ000106HASRVSA4', 'MORJ040106VSA', 'MORALES RUVALCABA JESUS EMMANUEL', 'Mexicana', 'Hacienda Boca de Ortega 105, Haciendas de Agu', '4491234444', 'jesusghoul2016@gmail.com', 'M', 21, '31241251213', NULL, 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `candidato_has_habilidad`
--

CREATE TABLE `candidato_has_habilidad` (
  `Curp` varchar(18) NOT NULL,
  `idHabilidad` int(11) NOT NULL,
  `Experiencia` varchar(45) NOT NULL,
  `valida` varchar(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `candidato_has_habilidad`
--

INSERT INTO `candidato_has_habilidad` (`Curp`, `idHabilidad`, `Experiencia`, `valida`) VALUES
('COCR800325HASDDNB3', 4, '15 años', 'Si'),
('GAMS040407HASRRNA5', 1, '3 años', 'Si'),
('MORJ000106HASRVSA4', 4, '3 años', 'Si');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `candidato_has_idioma`
--

CREATE TABLE `candidato_has_idioma` (
  `Curp` varchar(18) NOT NULL,
  `idIdioma` int(11) NOT NULL,
  `NIvel` varchar(45) NOT NULL,
  `valida` varchar(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `candidato_has_idioma`
--

INSERT INTO `candidato_has_idioma` (`Curp`, `idIdioma`, `NIvel`, `valida`) VALUES
('COCR800325HASDDNB3', 1, 'Avanzado', 'Si'),
('GAMS040407HASRRNA5', 1, 'Medio', 'Si'),
('MORJ000106HASRVSA4', 1, 'Medio', 'Si');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `candidato_has_nivelacademico`
--

CREATE TABLE `candidato_has_nivelacademico` (
  `Curp` varchar(18) NOT NULL,
  `idNivelAcademico` int(11) NOT NULL,
  `idCarrera` int(11) NOT NULL,
  `Institucion` varchar(20) DEFAULT NULL,
  `valida` varchar(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `candidato_has_nivelacademico`
--

INSERT INTO `candidato_has_nivelacademico` (`Curp`, `idNivelAcademico`, `idCarrera`, `Institucion`, `valida`) VALUES
('COCR800325HASDDNB3', 2, 4, 'UVM', ''),
('GAMS040407HASRRNA5', 1, 3, 'DGETI', 'Si'),
('MORJ000106HASRVSA4', 1, 3, 'DGETI', 'Si'),
('MORJ000106HASRVSA4', 2, 2, 'UVM', 'Si');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carrera`
--

CREATE TABLE `carrera` (
  `idCarrera` int(11) NOT NULL,
  `Descripcion` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `carrera`
--

INSERT INTO `carrera` (`idCarrera`, `Descripcion`) VALUES
(1, 'Técnico en electrónica'),
(2, 'Diseño Gráfico.'),
(3, 'Ingeniería en Tecnologías de la Información y Comunicaciones.'),
(4, 'Animación digital');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `contacto`
--

CREATE TABLE `contacto` (
  `idcontacto` int(11) NOT NULL,
  `Nombre` varchar(45) NOT NULL,
  `Domicilio` varchar(45) DEFAULT NULL,
  `Razon_Social` varchar(45) DEFAULT NULL,
  `Telefono` varchar(10) DEFAULT NULL,
  `Email` varchar(45) NOT NULL,
  `Link` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `contacto`
--

INSERT INTO `contacto` (`idcontacto`, `Nombre`, `Domicilio`, `Razon_Social`, `Telefono`, `Email`, `Link`) VALUES
(1, 'Dana Moreno', 'Cetis155', 'Home-int S.A', '4499998888', 'homeint_contacto1@gmail', 'homeint_contacto1'),
(2, 'Daniel ', 'Cetis155', 'Home-int S.A', '4499998888', 'homeint_contacto2@gmail', 'Empresa1_2');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `contrato`
--

CREATE TABLE `contrato` (
  `IdContrato` int(18) NOT NULL,
  `Curp` varchar(18) NOT NULL,
  `idPuesto` int(11) NOT NULL,
  `idArea` int(11) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `idJornada` int(11) NOT NULL,
  `horas_semana` varchar(100) NOT NULL,
  `horario` text NOT NULL,
  `Salario` varchar(50) NOT NULL,
  `dias_de_pago` varchar(100) NOT NULL,
  `lugar_firma` varchar(100) NOT NULL,
  `fecha_firma` date NOT NULL,
  `SalarioL` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `contrato`
--

INSERT INTO `contrato` (`IdContrato`, `Curp`, `idPuesto`, `idArea`, `fecha_inicio`, `fecha_fin`, `idJornada`, `horas_semana`, `horario`, `Salario`, `dias_de_pago`, `lugar_firma`, `fecha_firma`, `SalarioL`) VALUES
(3, 'GAME040217HASLXDA3', 15, 1, '2021-12-06', '2022-03-06', 4, '4', 'Lunes a Viernes', '107800', 'Dia viernes', '', '2021-12-06', 'CIENTO SIETE MIL OCHOCIENTOS  PESOS '),
(4, 'GAMS040407HASRRNA5', 1, 1, '2021-11-08', '2022-02-08', 2, '2', 'Lunes a Sabado', '143000', 'Quincena y día 29 del mes', '', '2021-11-08', 'CIENTO CUARENTA Y TRES MIL  PESOS '),
(6, 'MORJ000106HASRVSA4', 15, 2, '2021-11-22', '2021-11-29', 2, '2', 'Lunes a Viernes', '108000', 'Viernes', '', '2021-11-22', 'CIENTO OCHO MIL  PESOS ');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `datos_de_empresa`
--

CREATE TABLE `datos_de_empresa` (
  `idEmpresa` int(11) NOT NULL,
  `Nombre_de_empresa` varchar(45) NOT NULL,
  `Descripcion` varchar(45) DEFAULT NULL,
  `Telefono` varchar(10) DEFAULT NULL,
  `Domicilio` varchar(100) DEFAULT NULL,
  `E_Mail` varchar(45) DEFAULT NULL,
  `RazonSocial` varchar(45) DEFAULT NULL,
  `Estructura_Juridica` varchar(45) DEFAULT NULL,
  `Encargado` varchar(45) DEFAULT NULL,
  `CIF_Empresa` varchar(45) DEFAULT NULL,
  `Acta_constitutiva` varchar(100) NOT NULL,
  `No_Escriturapub` varchar(24) NOT NULL,
  `Libro_Escriturapub` varchar(100) NOT NULL,
  `Fecha_Escriturapub` date NOT NULL,
  `Fe_Escriturapub` varchar(100) NOT NULL,
  `NP_Escriturapub` varchar(24) NOT NULL,
  `Ciu_Escriturapub` varchar(100) NOT NULL,
  `No_EscriturapubL` varchar(100) NOT NULL,
  `RepresentanteLegal` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `datos_de_empresa`
--

INSERT INTO `datos_de_empresa` (`idEmpresa`, `Nombre_de_empresa`, `Descripcion`, `Telefono`, `Domicilio`, `E_Mail`, `RazonSocial`, `Estructura_Juridica`, `Encargado`, `CIF_Empresa`, `Acta_constitutiva`, `No_Escriturapub`, `Libro_Escriturapub`, `Fecha_Escriturapub`, `Fe_Escriturapub`, `NP_Escriturapub`, `Ciu_Escriturapub`, `No_EscriturapubL`, `RepresentanteLegal`) VALUES
(1, 'Homeint S.A.', 'Cosas invocadoras de desarrollo', '4499998888', 'Av Perseo 301, Primo Verdad Inegi, 20267 Aguascalientes, Ags.', 'homeintmaster@homeint.com', 'Sociedad Anonima', 'Física', 'Uvuvwevwevwe Onyetenyevwe Ugwemuhwem Osas', 'B77431213', 'Acta', '200899', 'Homeint Escritura publica', '2021-10-07', 'HUMBERTO GUAR IRACHETA', '47', 'Aguascalientes', 'DOSCIENTOS  MIL OCHOCIENTOS NOVENTA Y NUEVE  ', 'Bad bunny ');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleado`
--

CREATE TABLE `empleado` (
  `Curp` varchar(18) NOT NULL,
  `RFC` varchar(13) NOT NULL,
  `Nombre` varchar(45) NOT NULL,
  `nacionalidad` text NOT NULL,
  `Domicilio` varchar(45) NOT NULL,
  `Telefono` varchar(10) NOT NULL,
  `E_mail` varchar(45) NOT NULL,
  `Sexo` varchar(2) NOT NULL,
  `Edad` int(11) NOT NULL,
  `NSS` varchar(11) NOT NULL,
  `idEstadoCivil` int(11) NOT NULL,
  `Conyuje_Concubino` varchar(45) NOT NULL,
  `tel_emergencia` varchar(10) NOT NULL,
  `nombre_emergencia` varchar(45) NOT NULL,
  `no_infonavit` varchar(20) NOT NULL,
  `No_contrato` int(11) NOT NULL,
  `Contrato_Definitivo` varchar(100) NOT NULL,
  `Contrato_Temporal` varchar(100) NOT NULL,
  `ContratoTemporal_Val` varchar(2) NOT NULL DEFAULT 'No'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `empleado`
--

INSERT INTO `empleado` (`Curp`, `RFC`, `Nombre`, `nacionalidad`, `Domicilio`, `Telefono`, `E_mail`, `Sexo`, `Edad`, `NSS`, `idEstadoCivil`, `Conyuje_Concubino`, `tel_emergencia`, `nombre_emergencia`, `no_infonavit`, `No_contrato`, `Contrato_Definitivo`, `Contrato_Temporal`, `ContratoTemporal_Val`) VALUES
('GAME040217HASLXDA3', 'GAME040217DA3', 'GALLEGO MUÑOZ EDGAR MARIO', 'Mexicana', 'conocido', '4499915555', 'mariochikito11@gmail.com', 'M', 20, '44190407518', 4, 'A', '4491115555', 'Hermana de mario', '...', 0, '', '', 'Si'),
('GAMS040407HASRRNA5', 'GAMS0404074T7', 'Garcia Martinez Santiago Octavio', 'Mexicana', 'Casiopea #408 Gomez Portugal 20250', '4491115555', 'ssantig07@gmail.com', 'M', 20, '2147483647', 1, '', '4495691241', 'María José Garcia Martínez', '', 0, '', '', 'Si'),
('MORJ000106HASRVSA4', 'MORJ040106VSA', 'MORALES RUVALCABA JESUS EMMANUEL', 'Mexicana', 'Hacienda Boca de Ortega 105, Haciendas de Agu', '4491234444', 'jesusghoul2016@gmail.com', 'M', 21, '31241251213', 4, '', '', '', '', 0, '', '', 'Si');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleado_has_habilidad`
--

CREATE TABLE `empleado_has_habilidad` (
  `Curp` varchar(18) NOT NULL,
  `idHabilidad` int(11) NOT NULL,
  `Experiencia` varchar(45) NOT NULL,
  `valida` varchar(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `empleado_has_habilidad`
--

INSERT INTO `empleado_has_habilidad` (`Curp`, `idHabilidad`, `Experiencia`, `valida`) VALUES
('GAME040217HASLXDA3', 4, '5 años', ''),
('GAMS040407HASRRNA5', 1, '3 años', 'Si'),
('MORJ000106HASRVSA4', 4, '3 años', 'Si');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleado_has_idioma`
--

CREATE TABLE `empleado_has_idioma` (
  `Curp` varchar(18) NOT NULL,
  `idIdioma` int(11) NOT NULL,
  `Nivel` varchar(45) NOT NULL,
  `valida` varchar(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `empleado_has_idioma`
--

INSERT INTO `empleado_has_idioma` (`Curp`, `idIdioma`, `Nivel`, `valida`) VALUES
('GAME040217HASLXDA3', 2, 'Medio', ''),
('GAMS040407HASRRNA5', 1, 'Medio', 'Si'),
('MORJ000106HASRVSA4', 1, 'Medio', 'Si');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleado_has_nivelacademico`
--

CREATE TABLE `empleado_has_nivelacademico` (
  `Curp` varchar(18) NOT NULL,
  `idNivelAcademico` int(11) NOT NULL,
  `idCarrera` int(11) NOT NULL,
  `Institucion` varchar(20) NOT NULL,
  `valida` varchar(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `empleado_has_nivelacademico`
--

INSERT INTO `empleado_has_nivelacademico` (`Curp`, `idNivelAcademico`, `idCarrera`, `Institucion`, `valida`) VALUES
('GAME040217HASLXDA3', 2, 2, 'UAA', ''),
('GAMS040407HASRRNA5', 1, 3, 'DGETI', 'Si'),
('MORJ000106HASRVSA4', 1, 3, 'DGETI', 'Si'),
('MORJ000106HASRVSA4', 2, 2, 'UVM', 'Si');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estadocivil`
--

CREATE TABLE `estadocivil` (
  `idEstadoCivil` int(11) NOT NULL,
  `Descripcion` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `estadocivil`
--

INSERT INTO `estadocivil` (`idEstadoCivil`, `Descripcion`) VALUES
(1, 'Soltero'),
(2, 'Casado'),
(3, 'Union Libre'),
(4, 'Divorcio');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estatus_candidato`
--

CREATE TABLE `estatus_candidato` (
  `EstatusProceso` int(11) NOT NULL,
  `Descripcion` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `estatus_candidato`
--

INSERT INTO `estatus_candidato` (`EstatusProceso`, `Descripcion`) VALUES
(1, 'Seleccionado'),
(2, 'Calif.Psicologica'),
(3, 'Calif.Medica'),
(4, 'Validado.Tec');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estatus_solicitud`
--

CREATE TABLE `estatus_solicitud` (
  `idEstatus_Solicitud` int(11) NOT NULL,
  `Descripcion` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `estatus_solicitud`
--

INSERT INTO `estatus_solicitud` (`idEstatus_Solicitud`, `Descripcion`) VALUES
(1, 'Pendiente'),
(2, 'Aprobada'),
(3, 'Publicado'),
(4, 'En proceso'),
(5, 'Terminada'),
(6, 'Cancelado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `habilidad`
--

CREATE TABLE `habilidad` (
  `idHabilidad` int(11) NOT NULL,
  `Descripcion` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `habilidad`
--

INSERT INTO `habilidad` (`idHabilidad`, `Descripcion`) VALUES
(1, 'Desarrollador de Css'),
(2, 'Desarrollador de Html'),
(3, 'Desarrollador de JavaScript'),
(4, 'Manejo de Adobe'),
(5, 'Manejo de Blender 3D'),
(6, 'Instalación de tarjetas de control');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `idioma`
--

CREATE TABLE `idioma` (
  `idIdioma` int(11) NOT NULL,
  `Lenguaje` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `idioma`
--

INSERT INTO `idioma` (`idIdioma`, `Lenguaje`) VALUES
(1, 'Ingles'),
(2, 'Español'),
(3, 'Chino Mandarín');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `jordesc`
--

CREATE TABLE `jordesc` (
  `iddesc` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `IdJornada` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `jordesc`
--

INSERT INTO `jordesc` (`iddesc`, `name`, `IdJornada`) VALUES
(1, 'De 8 horas a 14 horas', 1),
(2, 'De 12horas  a 16 horas', 2),
(3, 'De 21 horas a 7 horas', 3),
(4, 'De 22 horas a 8 horas', 4);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `jornada`
--

CREATE TABLE `jornada` (
  `IdJornada` int(11) NOT NULL,
  `jornombre` varchar(100) NOT NULL,
  `Descripcion` varchar(100) NOT NULL,
  `val` varchar(11) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `jornada`
--

INSERT INTO `jornada` (`IdJornada`, `jornombre`, `Descripcion`, `val`) VALUES
(1, 'Diurna ', 'De 8 horas a 14 horas', '0'),
(2, 'Diurna 2', 'De 12horas  a 16 horas', '0'),
(3, 'Nocturna', 'De 21 horas a 7 horas', '0'),
(4, 'Nocturna 2', 'De 22 horas a 8 horas', '0');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `mediopublicidad`
--

CREATE TABLE `mediopublicidad` (
  `idMedioPublicidad` int(11) NOT NULL,
  `Descripcion` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `mediopublicidad`
--

INSERT INTO `mediopublicidad` (`idMedioPublicidad`, `Descripcion`) VALUES
(1, 'Facebook.'),
(2, 'Radio'),
(3, 'LinkedIn.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `nivelacademico`
--

CREATE TABLE `nivelacademico` (
  `idNivelAcademico` int(11) NOT NULL,
  `Descripcion` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `nivelacademico`
--

INSERT INTO `nivelacademico` (`idNivelAcademico`, `Descripcion`) VALUES
(1, 'Técnico'),
(2, 'Licenciatura'),
(3, 'Maestría.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `perfil_admo`
--

CREATE TABLE `perfil_admo` (
  `idPerfil` int(11) NOT NULL,
  `Descripcion` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `perfil_admo`
--

INSERT INTO `perfil_admo` (`idPerfil`, `Descripcion`) VALUES
(1, 'Administrador'),
(2, 'Director'),
(3, 'Gerente de desarrollo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `perfil_has_proceso`
--

CREATE TABLE `perfil_has_proceso` (
  `idPerfil` int(11) NOT NULL,
  `idProceso` int(11) NOT NULL,
  `idPermiso` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `perfil_has_proceso`
--

INSERT INTO `perfil_has_proceso` (`idPerfil`, `idProceso`, `idPermiso`) VALUES
(1, 10, 1),
(3, 13, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `permisos`
--

CREATE TABLE `permisos` (
  `id_permiso` int(11) NOT NULL,
  `Descripcion` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `permisos`
--

INSERT INTO `permisos` (`id_permiso`, `Descripcion`) VALUES
(1, 'Lectura'),
(2, 'Edicion');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proceso`
--

CREATE TABLE `proceso` (
  `idProceso` int(11) NOT NULL,
  `Descripcion` varchar(70) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `proceso`
--

INSERT INTO `proceso` (`idProceso`, `Descripcion`) VALUES
(1, 'Nivel Academico'),
(2, 'Carrera'),
(3, 'idioma'),
(4, 'Habilidad'),
(5, 'Area'),
(6, 'HMedio de Publicidad\r\n'),
(7, 'Contacto'),
(8, 'Datos de la Empresa'),
(9, 'Puesto'),
(10, 'Solicitud de Personal'),
(11, 'Autorización de Solicitud'),
(12, 'Publicación de Oferta'),
(13, 'Solicitante'),
(14, 'Calificación Psiclologica'),
(15, 'Calificación medica'),
(16, 'Validación de Referencias'),
(17, 'Selección de candidatos');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `puesto`
--

CREATE TABLE `puesto` (
  `idPuesto` int(11) NOT NULL,
  `Nombrepuesto` varchar(45) DEFAULT NULL,
  `Descripcion` varchar(200) DEFAULT NULL,
  `SalarioMensual` int(11) DEFAULT NULL,
  `Beneficios` varchar(250) DEFAULT NULL,
  `Bonos` int(11) DEFAULT NULL,
  `Aprobacion` tinyint(1) DEFAULT NULL,
  `SalarioL` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `puesto`
--

INSERT INTO `puesto` (`idPuesto`, `Nombrepuesto`, `Descripcion`, `SalarioMensual`, `Beneficios`, `Bonos`, `Aprobacion`, `SalarioL`) VALUES
(1, 'Desarrollador de paginas web', 'paginas web', 144000, 'De ley', 50000, 0, 'CIENTO CUARENTA Y CUATRO MIL  PESOS '),
(14, 'Técnico en sistema de cómputos', '1.Mantenimiento de computo. 2. Instalación de hardware y software necesarios en la empresa.', 600000, 'de ley', 55000, 0, 'SEISCIENTOS  MIL  PESOS '),
(15, 'Diseñador de Creativos - Diseñador Gráfico ', 'Diseñar elementos visuales para la web', 108000, 'De ley', 30000, 1, 'CIENTO OCHO MIL  PESOS ');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `puesto_has_habilidad`
--

CREATE TABLE `puesto_has_habilidad` (
  `idPuesto` int(11) NOT NULL,
  `idHabilidad` int(11) NOT NULL,
  `Experiencia` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `puesto_has_habilidad`
--

INSERT INTO `puesto_has_habilidad` (`idPuesto`, `idHabilidad`, `Experiencia`) VALUES
(1, 1, '5 años'),
(1, 2, '5 años'),
(1, 3, '5 años');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `puesto_has_idioma`
--

CREATE TABLE `puesto_has_idioma` (
  `idPuesto` int(11) NOT NULL,
  `idIdioma` int(11) NOT NULL,
  `Nivel` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `puesto_has_idioma`
--

INSERT INTO `puesto_has_idioma` (`idPuesto`, `idIdioma`, `Nivel`) VALUES
(1, 1, 'Avanzado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `resultadocandidato`
--

CREATE TABLE `resultadocandidato` (
  `EstatusProceso` varchar(45) NOT NULL,
  `Comentarios_area` varchar(45) NOT NULL,
  `Comentarios_ofertas_salario` varchar(45) NOT NULL,
  `Comentarios_area_seleccion` varchar(45) NOT NULL,
  `estatus` varchar(45) NOT NULL,
  `idSolicitud` int(11) NOT NULL,
  `Curp` varchar(18) NOT NULL,
  `id_actitud` int(11) NOT NULL,
  `Coeficiente_Intelectual` int(11) NOT NULL,
  `Personalidad` longtext NOT NULL,
  `apto_psico` int(3) NOT NULL,
  `Validar_ref` varchar(11) NOT NULL,
  `Calificacion_Medica` varchar(11) NOT NULL,
  `validacion` varchar(11) NOT NULL,
  `Calificacion` varchar(11) NOT NULL,
  `Califica_el_Perfil` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `resultadocandidato`
--

INSERT INTO `resultadocandidato` (`EstatusProceso`, `Comentarios_area`, `Comentarios_ofertas_salario`, `Comentarios_area_seleccion`, `estatus`, `idSolicitud`, `Curp`, `id_actitud`, `Coeficiente_Intelectual`, `Personalidad`, `apto_psico`, `Validar_ref`, `Calificacion_Medica`, `validacion`, `Calificacion`, `Califica_el_Perfil`) VALUES
('3', '', '', '', 'Si', 1, 'GAMS040407HASRRNA5', 0, 100, 'Bueno', 0, 'Si', 'Apto', 'Si', 'Apto', '10'),
('3', '', '', '', 'Si', 2, 'COCR800325HASDDNB3', 0, 10, 'Bueno', 0, 'Si', 'Apto', 'Si', 'Apto', '10'),
('3', '', '', '', 'Pendiente', 2, 'MORJ000106HASRVSA4', 0, 100, 'Bueno', 0, 'Pendiente', 'Apto', 'Si', 'No Apto', '10');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `solicitud`
--

CREATE TABLE `solicitud` (
  `idSolicitud` int(11) NOT NULL,
  `FechaSolicitud` date DEFAULT NULL,
  `NumeroVacante` int(11) DEFAULT NULL,
  `idArea` int(11) NOT NULL,
  `idPuesto` int(11) NOT NULL,
  `idNivelAcademico` int(11) NOT NULL,
  `idCarrera` int(11) NOT NULL,
  `idEstatus_Solicitud` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `solicitud`
--

INSERT INTO `solicitud` (`idSolicitud`, `FechaSolicitud`, `NumeroVacante`, `idArea`, `idPuesto`, `idNivelAcademico`, `idCarrera`, `idEstatus_Solicitud`) VALUES
(1, '2021-10-27', 3, 1, 1, 2, 3, 3),
(2, '2021-10-25', 1, 2, 15, 2, 2, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `turno`
--

CREATE TABLE `turno` (
  `idTurno` int(2) NOT NULL,
  `Tipo` varchar(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `turno`
--

INSERT INTO `turno` (`idTurno`, `Tipo`) VALUES
(1, 'Matutino'),
(2, 'Vespertino'),
(3, 'Nocturno');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `idUsuario` int(11) NOT NULL,
  `usuario` varchar(10) NOT NULL,
  `password` varchar(20) NOT NULL,
  `nombre` varchar(70) NOT NULL,
  `Perfil` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`idUsuario`, `usuario`, `password`, `nombre`, `Perfil`) VALUES
(1, 'Fernando', 'abcd1234', 'Luis Fernando', 1),
(2, 'Juanpe', 'aaaa1111', 'Juan Carloz Lopez', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `anuncio`
--
ALTER TABLE `anuncio`
  ADD PRIMARY KEY (`idAnuncio`),
  ADD KEY `fk_Anuncio_Contacto1` (`idcontacto`),
  ADD KEY `fk_Anuncio_Solicitud1` (`idSolicitud`),
  ADD KEY `fk_Anuncio_Publicidad1` (`idMedioPublicidad`);

--
-- Indices de la tabla `area`
--
ALTER TABLE `area`
  ADD PRIMARY KEY (`idArea`);

--
-- Indices de la tabla `candidato`
--
ALTER TABLE `candidato`
  ADD PRIMARY KEY (`Curp`),
  ADD KEY `fk_Candidato_EstadoCivil1` (`idEstadoCivil`);

--
-- Indices de la tabla `candidato_has_habilidad`
--
ALTER TABLE `candidato_has_habilidad`
  ADD PRIMARY KEY (`Curp`,`idHabilidad`),
  ADD KEY `fk_Candidato_has_Habilidad_Habilidad1` (`idHabilidad`);

--
-- Indices de la tabla `candidato_has_idioma`
--
ALTER TABLE `candidato_has_idioma`
  ADD PRIMARY KEY (`Curp`,`idIdioma`),
  ADD KEY `fk_Candidato_has_Idioma_Idioma1` (`idIdioma`);

--
-- Indices de la tabla `candidato_has_nivelacademico`
--
ALTER TABLE `candidato_has_nivelacademico`
  ADD PRIMARY KEY (`Curp`,`idNivelAcademico`,`idCarrera`),
  ADD KEY `fk_Candidato_has_NivelAcademico_NivelAcademico1` (`idNivelAcademico`),
  ADD KEY `fk_Candidato_has_NivelAcademico_Carrera1` (`idCarrera`);

--
-- Indices de la tabla `carrera`
--
ALTER TABLE `carrera`
  ADD PRIMARY KEY (`idCarrera`);

--
-- Indices de la tabla `contacto`
--
ALTER TABLE `contacto`
  ADD PRIMARY KEY (`idcontacto`);

--
-- Indices de la tabla `contrato`
--
ALTER TABLE `contrato`
  ADD PRIMARY KEY (`IdContrato`),
  ADD KEY `fk_Contrato_CURP` (`Curp`) USING BTREE,
  ADD KEY `fk_Contrato_Jornada` (`idJornada`) USING BTREE,
  ADD KEY `fk_Contrato_Area` (`idArea`) USING BTREE,
  ADD KEY `fk_Contrato_Puesto` (`idPuesto`) USING BTREE;

--
-- Indices de la tabla `datos_de_empresa`
--
ALTER TABLE `datos_de_empresa`
  ADD PRIMARY KEY (`idEmpresa`);

--
-- Indices de la tabla `empleado`
--
ALTER TABLE `empleado`
  ADD PRIMARY KEY (`Curp`);

--
-- Indices de la tabla `empleado_has_habilidad`
--
ALTER TABLE `empleado_has_habilidad`
  ADD PRIMARY KEY (`Curp`,`idHabilidad`),
  ADD KEY `idHabilidad` (`idHabilidad`);

--
-- Indices de la tabla `empleado_has_idioma`
--
ALTER TABLE `empleado_has_idioma`
  ADD PRIMARY KEY (`Curp`,`idIdioma`),
  ADD KEY `idIdioma` (`idIdioma`);

--
-- Indices de la tabla `empleado_has_nivelacademico`
--
ALTER TABLE `empleado_has_nivelacademico`
  ADD PRIMARY KEY (`Curp`,`idNivelAcademico`,`idCarrera`),
  ADD KEY `idNivelAcademico` (`idNivelAcademico`,`idCarrera`),
  ADD KEY `idCarrera` (`idCarrera`);

--
-- Indices de la tabla `estadocivil`
--
ALTER TABLE `estadocivil`
  ADD PRIMARY KEY (`idEstadoCivil`);

--
-- Indices de la tabla `estatus_candidato`
--
ALTER TABLE `estatus_candidato`
  ADD PRIMARY KEY (`EstatusProceso`);

--
-- Indices de la tabla `estatus_solicitud`
--
ALTER TABLE `estatus_solicitud`
  ADD PRIMARY KEY (`idEstatus_Solicitud`);

--
-- Indices de la tabla `habilidad`
--
ALTER TABLE `habilidad`
  ADD PRIMARY KEY (`idHabilidad`);

--
-- Indices de la tabla `idioma`
--
ALTER TABLE `idioma`
  ADD PRIMARY KEY (`idIdioma`);

--
-- Indices de la tabla `jordesc`
--
ALTER TABLE `jordesc`
  ADD PRIMARY KEY (`iddesc`),
  ADD KEY `jornada id` (`IdJornada`);

--
-- Indices de la tabla `jornada`
--
ALTER TABLE `jornada`
  ADD PRIMARY KEY (`IdJornada`);

--
-- Indices de la tabla `mediopublicidad`
--
ALTER TABLE `mediopublicidad`
  ADD PRIMARY KEY (`idMedioPublicidad`);

--
-- Indices de la tabla `nivelacademico`
--
ALTER TABLE `nivelacademico`
  ADD PRIMARY KEY (`idNivelAcademico`);

--
-- Indices de la tabla `perfil_admo`
--
ALTER TABLE `perfil_admo`
  ADD PRIMARY KEY (`idPerfil`);

--
-- Indices de la tabla `perfil_has_proceso`
--
ALTER TABLE `perfil_has_proceso`
  ADD PRIMARY KEY (`idPerfil`,`idProceso`),
  ADD KEY `fk_PERFIL_HAS_PROCESO_PROCESO` (`idProceso`),
  ADD KEY `fk_PERFIL_HAS_PROCESO_PERMISOO` (`idPermiso`);

--
-- Indices de la tabla `permisos`
--
ALTER TABLE `permisos`
  ADD PRIMARY KEY (`id_permiso`);

--
-- Indices de la tabla `proceso`
--
ALTER TABLE `proceso`
  ADD PRIMARY KEY (`idProceso`);

--
-- Indices de la tabla `puesto`
--
ALTER TABLE `puesto`
  ADD PRIMARY KEY (`idPuesto`);

--
-- Indices de la tabla `puesto_has_habilidad`
--
ALTER TABLE `puesto_has_habilidad`
  ADD PRIMARY KEY (`idPuesto`,`idHabilidad`),
  ADD KEY `fk_Puesto_has_habilidad_habilidad` (`idHabilidad`);

--
-- Indices de la tabla `puesto_has_idioma`
--
ALTER TABLE `puesto_has_idioma`
  ADD PRIMARY KEY (`idPuesto`,`idIdioma`),
  ADD KEY `fk_Puesto_has_habilidad_Idioma` (`idIdioma`);

--
-- Indices de la tabla `solicitud`
--
ALTER TABLE `solicitud`
  ADD PRIMARY KEY (`idSolicitud`),
  ADD KEY `fk_Solicitud_Area1` (`idArea`),
  ADD KEY `fk_Solicitud_Puesto1` (`idPuesto`),
  ADD KEY `fk_Solicitud_Nivel_Academico1` (`idNivelAcademico`),
  ADD KEY `fk_Solicitud_Carrera1` (`idCarrera`),
  ADD KEY `fk_Solicitud_Estatus_Solicitud1` (`idEstatus_Solicitud`);

--
-- Indices de la tabla `turno`
--
ALTER TABLE `turno`
  ADD PRIMARY KEY (`idTurno`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`idUsuario`),
  ADD KEY `fk_usuario_perfil` (`Perfil`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `anuncio`
--
ALTER TABLE `anuncio`
  MODIFY `idAnuncio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `area`
--
ALTER TABLE `area`
  MODIFY `idArea` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `carrera`
--
ALTER TABLE `carrera`
  MODIFY `idCarrera` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `contacto`
--
ALTER TABLE `contacto`
  MODIFY `idcontacto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `contrato`
--
ALTER TABLE `contrato`
  MODIFY `IdContrato` int(18) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `datos_de_empresa`
--
ALTER TABLE `datos_de_empresa`
  MODIFY `idEmpresa` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `estadocivil`
--
ALTER TABLE `estadocivil`
  MODIFY `idEstadoCivil` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `estatus_candidato`
--
ALTER TABLE `estatus_candidato`
  MODIFY `EstatusProceso` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `estatus_solicitud`
--
ALTER TABLE `estatus_solicitud`
  MODIFY `idEstatus_Solicitud` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `habilidad`
--
ALTER TABLE `habilidad`
  MODIFY `idHabilidad` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `idioma`
--
ALTER TABLE `idioma`
  MODIFY `idIdioma` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `jordesc`
--
ALTER TABLE `jordesc`
  MODIFY `iddesc` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `jornada`
--
ALTER TABLE `jornada`
  MODIFY `IdJornada` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `mediopublicidad`
--
ALTER TABLE `mediopublicidad`
  MODIFY `idMedioPublicidad` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `nivelacademico`
--
ALTER TABLE `nivelacademico`
  MODIFY `idNivelAcademico` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `perfil_admo`
--
ALTER TABLE `perfil_admo`
  MODIFY `idPerfil` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT de la tabla `permisos`
--
ALTER TABLE `permisos`
  MODIFY `id_permiso` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `proceso`
--
ALTER TABLE `proceso`
  MODIFY `idProceso` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT de la tabla `puesto`
--
ALTER TABLE `puesto`
  MODIFY `idPuesto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `solicitud`
--
ALTER TABLE `solicitud`
  MODIFY `idSolicitud` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `idUsuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `anuncio`
--
ALTER TABLE `anuncio`
  ADD CONSTRAINT `fk_Anuncio_Contacto1` FOREIGN KEY (`idcontacto`) REFERENCES `contacto` (`idcontacto`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Anuncio_MedioPublicidad1` FOREIGN KEY (`idMedioPublicidad`) REFERENCES `mediopublicidad` (`idMedioPublicidad`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Anuncio_Publicidad1` FOREIGN KEY (`idMedioPublicidad`) REFERENCES `mediopublicidad` (`idMedioPublicidad`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Anuncio_Solicitud1` FOREIGN KEY (`idSolicitud`) REFERENCES `solicitud` (`idSolicitud`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `candidato`
--
ALTER TABLE `candidato`
  ADD CONSTRAINT `fk_Candidato_EstadoCivil1` FOREIGN KEY (`idEstadoCivil`) REFERENCES `estadocivil` (`idEstadoCivil`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `candidato_has_habilidad`
--
ALTER TABLE `candidato_has_habilidad`
  ADD CONSTRAINT `fk_Candidato_has_Habilidad_Candidato1` FOREIGN KEY (`Curp`) REFERENCES `candidato` (`Curp`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_Candidato_has_Habilidad_Habilidad1` FOREIGN KEY (`idHabilidad`) REFERENCES `habilidad` (`idHabilidad`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `candidato_has_idioma`
--
ALTER TABLE `candidato_has_idioma`
  ADD CONSTRAINT `fk_Candidato_has_Idioma_Candidato1` FOREIGN KEY (`Curp`) REFERENCES `candidato` (`Curp`) ON DELETE NO ACTION ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_Candidato_has_Idioma_Idioma1` FOREIGN KEY (`idIdioma`) REFERENCES `idioma` (`idIdioma`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `candidato_has_nivelacademico`
--
ALTER TABLE `candidato_has_nivelacademico`
  ADD CONSTRAINT `fk_Candidato_has_NivelAcademico_Candidato1` FOREIGN KEY (`Curp`) REFERENCES `candidato` (`Curp`) ON DELETE CASCADE ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Candidato_has_NivelAcademico_Carrera1` FOREIGN KEY (`idCarrera`) REFERENCES `carrera` (`idCarrera`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Candidato_has_NivelAcademico_NivelAcademico1` FOREIGN KEY (`idNivelAcademico`) REFERENCES `nivelacademico` (`idNivelAcademico`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `contrato`
--
ALTER TABLE `contrato`
  ADD CONSTRAINT `contrato_ibfk_1` FOREIGN KEY (`idArea`) REFERENCES `area` (`idArea`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `contrato_ibfk_2` FOREIGN KEY (`idPuesto`) REFERENCES `puesto` (`idPuesto`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `contrato_ibfk_3` FOREIGN KEY (`idJornada`) REFERENCES `jornada` (`IdJornada`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `contrato_ibfk_4` FOREIGN KEY (`Curp`) REFERENCES `empleado` (`Curp`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Filtros para la tabla `empleado_has_habilidad`
--
ALTER TABLE `empleado_has_habilidad`
  ADD CONSTRAINT `empleado_has_habilidad_ibfk_1` FOREIGN KEY (`idHabilidad`) REFERENCES `habilidad` (`idHabilidad`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `empleado_has_habilidad_ibfk_2` FOREIGN KEY (`Curp`) REFERENCES `empleado` (`Curp`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `empleado_has_idioma`
--
ALTER TABLE `empleado_has_idioma`
  ADD CONSTRAINT `empleado_has_idioma_ibfk_1` FOREIGN KEY (`idIdioma`) REFERENCES `idioma` (`idIdioma`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `empleado_has_idioma_ibfk_2` FOREIGN KEY (`Curp`) REFERENCES `empleado` (`Curp`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `empleado_has_nivelacademico`
--
ALTER TABLE `empleado_has_nivelacademico`
  ADD CONSTRAINT `empleado_has_nivelacademico_ibfk_1` FOREIGN KEY (`idNivelAcademico`) REFERENCES `nivelacademico` (`idNivelAcademico`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `empleado_has_nivelacademico_ibfk_2` FOREIGN KEY (`idCarrera`) REFERENCES `carrera` (`idCarrera`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `empleado_has_nivelacademico_ibfk_3` FOREIGN KEY (`Curp`) REFERENCES `empleado` (`Curp`) ON DELETE CASCADE ON UPDATE NO ACTION;

--
-- Filtros para la tabla `jordesc`
--
ALTER TABLE `jordesc`
  ADD CONSTRAINT `jornada id` FOREIGN KEY (`IdJornada`) REFERENCES `jornada` (`IdJornada`) ON DELETE CASCADE;

--
-- Filtros para la tabla `perfil_has_proceso`
--
ALTER TABLE `perfil_has_proceso`
  ADD CONSTRAINT `fk_PERFIL_HAS_PROCESO_PERMISOO` FOREIGN KEY (`idPermiso`) REFERENCES `permisos` (`id_permiso`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_PERFIL_HAS_PROCESO_PROCESO` FOREIGN KEY (`idProceso`) REFERENCES `proceso` (`idProceso`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_PERFIL_HAS_PROCESO_perfil` FOREIGN KEY (`idPerfil`) REFERENCES `perfil_admo` (`idPerfil`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `puesto_has_habilidad`
--
ALTER TABLE `puesto_has_habilidad`
  ADD CONSTRAINT `fk_Puesto_has_habilidad_habilidad` FOREIGN KEY (`idHabilidad`) REFERENCES `habilidad` (`idHabilidad`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Puesto_has_habilidad_puesto` FOREIGN KEY (`idPuesto`) REFERENCES `puesto` (`idPuesto`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `puesto_has_idioma`
--
ALTER TABLE `puesto_has_idioma`
  ADD CONSTRAINT `fk_Puesto_has_Idioma_Puesto` FOREIGN KEY (`idPuesto`) REFERENCES `puesto` (`idPuesto`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Puesto_has_habilidad_Idioma` FOREIGN KEY (`idIdioma`) REFERENCES `idioma` (`idIdioma`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `solicitud`
--
ALTER TABLE `solicitud`
  ADD CONSTRAINT `fk_Solicitud_Area1` FOREIGN KEY (`idArea`) REFERENCES `area` (`idArea`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Solicitud_Carrera1` FOREIGN KEY (`idCarrera`) REFERENCES `carrera` (`idCarrera`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Solicitud_Estatus_Solicitud1` FOREIGN KEY (`idEstatus_Solicitud`) REFERENCES `estatus_solicitud` (`idEstatus_Solicitud`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Solicitud_Nivel_Academico1` FOREIGN KEY (`idNivelAcademico`) REFERENCES `nivelacademico` (`idNivelAcademico`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Solicitud_Puesto1` FOREIGN KEY (`idPuesto`) REFERENCES `puesto` (`idPuesto`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD CONSTRAINT `fk_usuario_perfil` FOREIGN KEY (`Perfil`) REFERENCES `perfil_admo` (`idPerfil`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
