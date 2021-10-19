-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 11-10-2021 a las 04:37:49
-- Versión del servidor: 10.4.20-MariaDB
-- Versión de PHP: 8.0.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `re_humanos`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `actitud`
--

CREATE TABLE `actitud` (
  `idActitud` int(11) NOT NULL,
  `Descripcion` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
(21, 31, 3, '2021-04-08', '2021-04-09', 3, 8),
(22, 31, 3, '2021-04-08', '2021-04-09', 4, 6),
(23, 32, 2, '2021-10-05', '2021-10-06', 3, 7);

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
(5, 'Desarrollo de sistemas WEB y móviles para Android..', 'Desarrollo de sistemas web'),
(6, 'Integración de sistemas electrónicos ', 'Integración de electrónica');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `candidato`
--

CREATE TABLE `candidato` (
  `Curp` varchar(18) NOT NULL,
  `RFC` varchar(13) DEFAULT NULL,
  `Nombre` varchar(45) DEFAULT NULL,
  `Domicilio` varchar(45) DEFAULT NULL,
  `Telefono` varchar(10) DEFAULT NULL,
  `E_Mail` varchar(45) DEFAULT NULL,
  `Sexo` varchar(45) DEFAULT NULL,
  `Edad` tinyint(2) DEFAULT NULL,
  `NSS` int(11) DEFAULT NULL,
  `Fotografia` blob DEFAULT NULL,
  `idEstadoCivil` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `candidato`
--

INSERT INTO `candidato` (`Curp`, `RFC`, `Nombre`, `Domicilio`, `Telefono`, `E_Mail`, `Sexo`, `Edad`, `NSS`, `Fotografia`, `idEstadoCivil`) VALUES
('COCR800325HASDD03', 'COCR80032', 'CORONA CORONA ROBERTO', 'conocido', '99999999', 'COC@GMAIL.COM', 'M', 40, 155545445, NULL, 2),
('FEEA770826MPLRSL72', 'FEEA770828SE5', 'Fernandez Espinoza Alejandra', 'conocido', '9999999999', 'COC@GMAIL.com', 'F', 20, 3124125, NULL, 1),
('GOML900330MASDD03', 'GOML900330', 'GONZALEZ MARTINEZ LAURA', 'conocido', '999999999', 'GOML@GMAIL.COM', 'F', 30, 15544545, NULL, 2),
('MAMA770826HSLRRI22', 'MAMA770826JVP', 'MARTINEZ MORENO ALEJANDRO', 'Conocido', '4491915799', 'sgamer.garcia@gmail.com', 'M', 20, 1234567, NULL, 3);

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
('COCR800325HASDD03', 9, '5 años ', 'Si'),
('COCR800325HASDD03', 10, '5 años ', 'Si'),
('GOML900330MASDD03', 9, '2 años ', 'Si'),
('GOML900330MASDD03', 10, '2 años ', 'Si'),
('MAMA770826HSLRRI22', 9, '1 year', 'Si');

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
('COCR800325HASDD03', 7, 'Experto', 'Si'),
('COCR800325HASDD03', 9, 'Medio', ''),
('GOML900330MASDD03', 7, 'Experto', 'Si'),
('GOML900330MASDD03', 8, 'Básico', 'No'),
('MAMA770826HSLRRI22', 7, '1 year', 'No');

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
('COCR800325HASDD03', 11, 8, 'UAA', 'No'),
('GOML900330MASDD03', 11, 8, 'UAA', 'Si'),
('MAMA770826HSLRRI22', 11, 8, 'abc', 'Si');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carrera`
--

CREATE TABLE `carrera` (
  `idCarrera` int(11) NOT NULL,
  `Descripcion` varchar(45) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `carrera`
--

INSERT INTO `carrera` (`idCarrera`, `Descripcion`) VALUES
(8, 'Ingeniería en sistemas computacionales'),
(9, 'Técnico en electrónica');

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
(3, 'Contacto de contratación 1', 'conocido', 'SR', '4495566907', '', ''),
(4, 'Contacto de contratación 2 ', 'conocido', 'SR', '2147483647', '', '');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `contrato`
--

CREATE TABLE `contrato` (
  `IdContrato` int(18) NOT NULL,
  `CURP` varchar(18) NOT NULL,
  `idPuesto` int(11) NOT NULL,
  `idArea` int(11) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `idJornada` int(11) NOT NULL,
  `horas_semana` int(11) NOT NULL,
  `horario` text NOT NULL,
  `Salario` float NOT NULL,
  `dias_de_pago` varchar(100) NOT NULL,
  `lugar_firma` varchar(100) NOT NULL,
  `fecha_firma` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `datos_de_empresa`
--

CREATE TABLE `datos_de_empresa` (
  `idEmpresa` int(11) NOT NULL,
  `Nombre_de_empresa` varchar(45) NOT NULL,
  `Descripcion` varchar(45) DEFAULT NULL,
  `Telefono` varchar(10) DEFAULT NULL,
  `Domicilio` varchar(45) DEFAULT NULL,
  `E_Mail` varchar(45) DEFAULT NULL,
  `RazonSocial` varchar(45) DEFAULT NULL,
  `Estructura_Juridica` varchar(45) DEFAULT NULL,
  `Encargado` varchar(45) DEFAULT NULL,
  `CIF_Empresa` varchar(9) DEFAULT NULL,
  `Acta_constitutiva` varchar(100) NOT NULL,
  `No_Escriturapub` varchar(24) NOT NULL,
  `Libro_Escriturapub` varchar(24) NOT NULL,
  `Fecha_Escriturapub` date NOT NULL,
  `Fe_Escriturapub` varchar(24) NOT NULL,
  `NP_Escriturapub` varchar(24) NOT NULL,
  `Ciu_Escriturapub` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `datos_de_empresa`
--

INSERT INTO `datos_de_empresa` (`idEmpresa`, `Nombre_de_empresa`, `Descripcion`, `Telefono`, `Domicilio`, `E_Mail`, `RazonSocial`, `Estructura_Juridica`, `Encargado`, `CIF_Empresa`, `Acta_constitutiva`, `No_Escriturapub`, `Libro_Escriturapub`, `Fecha_Escriturapub`, `Fe_Escriturapub`, `NP_Escriturapub`, `Ciu_Escriturapub`) VALUES
(1, 'PruebaSist S.A ', 'Empresa de prueba para el sistema ', '449-999-88', 'Cetis155', 'pruebasist@pruebasist.com.mx', 'PruebaSist S.A.', 'S.A', 'Nombre del CEO ', '?????????', 'Acta Prueba', '2008', 'libro prueba', '2021-10-07', 'fe prueba', '2008', 'Aguascalientes');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleado`
--

CREATE TABLE `empleado` (
  `Curp` varchar(18) NOT NULL,
  `RFC` varchar(13) NOT NULL,
  `Nombre` varchar(45) NOT NULL,
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
  `idArea` int(11) NOT NULL,
  `idPuesto` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Volcado de datos para la tabla `empleado`
--

INSERT INTO `empleado` (`Curp`, `RFC`, `Nombre`, `Domicilio`, `Telefono`, `E_mail`, `Sexo`, `Edad`, `NSS`, `idEstadoCivil`, `Conyuje_Concubino`, `tel_emergencia`, `nombre_emergencia`, `no_infonavit`, `idArea`, `idPuesto`) VALUES
('COCR800328HASRRB47', 'COCR800325B29', 'CORONA CORONA ROBERTO', 'conocido', '99999999', 'COC@GMAIL.COM', 'F', 40, '155545445', 2, '', '', '', '', 5, 20),
('FEEA770826MPLRSL72', 'FEEA770828SE5', 'Fernandez Espinoza Alejandra', 'Conocido', '4492123453', 'correo@gmail.com', 'F', 30, '12341234124', 1, '...', '449234765', 'Fernandez Espinoza Alejandro', '...', 0, 0),
('GGJJ770826HZSRTS68', 'JJGG770827UR2', 'Garza Guitierrez Jose de Jesus', 'conocido', '9999999999', 'Garzagjose12@gmail.com', 'M', 35, '1424532', 2, 'Señora Garza', '4449931212', 'María José ', '12414142315', 0, 0);

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
('COCR800328HASRRB47', 9, '5 años ', 'Si'),
('COCR800328HASRRB47', 10, '5 años ', 'Si'),
('FEEA770826MPLRSL72', 9, '5 años', '');

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
('COCR800328HASRRB47', 7, 'Experto', 'Si'),
('COCR800328HASRRB47', 9, 'Medio', ''),
('FEEA770826MPLRSL72', 7, 'Medio', '');

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
('COCR800328HASRRB47', 11, 8, 'UAA', 'No'),
('FEEA770826MPLRSL72', 11, 8, 'UAA', '');

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
(9, 'Desarrollo de sistemas WEB'),
(10, 'Desarrollo de sistema Móviles Android '),
(11, 'Instalación de tarjetas de control');

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
(7, 'Ingles'),
(8, 'Frances'),
(9, 'Japones');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `jornada`
--

CREATE TABLE `jornada` (
  `IdJornada` int(11) NOT NULL,
  `descripción` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
(6, 'Radio'),
(7, 'Televisión '),
(8, 'Diarios locales ');

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
(10, 'Tecnico'),
(11, 'Licenciatura'),
(12, 'Maestría ');

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
  `Descripcion` varchar(45) DEFAULT NULL,
  `SalarioAnual` int(11) DEFAULT NULL,
  `Beneficios` varchar(250) DEFAULT NULL,
  `Bonos` int(11) DEFAULT NULL,
  `Aprobacion` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `puesto`
--

INSERT INTO `puesto` (`idPuesto`, `Descripcion`, `SalarioAnual`, `Beneficios`, `Bonos`, `Aprobacion`) VALUES
(20, 'Desarrollador de sistemas WEB y Móviles ', 1500000, 'de ley ', 0, 0),
(21, 'Técnico en electrónica', 1500000, 'De ley', 30000, 0);

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
(20, 9, '2 años '),
(20, 10, '2 años '),
(21, 11, '5 años');

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
(20, 7, 'Experto'),
(20, 8, 'Básico'),
(21, 7, 'Medio');

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
('3', '', '', '', 'Si', 31, 'COCR800325HASDD03', 0, 100, 'Bueno', 0, 'Si', 'No Apto', 'Si', 'No Apto', 'bueno'),
('3', '', '', '', 'No', 31, 'GOML900330MASDD03', 0, 50, 'Regular', 0, 'Si', 'Apto', 'No', 'No Apto', '75'),
('3', '', '', '', 'Si', 31, 'MAMA770826HSLRRI22', 0, 100, 'si', 0, 'Si', 'Apto', 'Si', 'Apto', '100'),
('2', '', '', '', 'Pendiente', 32, 'MAMA770826HSLRRI22', 0, 1000, 'Bueno', 0, 'Pendiente', 'Pendiente', 'Pendiente', 'Apto', '10');

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
(31, '2021-04-06', 3, 5, 20, 11, 8, 3),
(32, '2021-10-05', 2, 6, 21, 10, 9, 3);

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
  ADD PRIMARY KEY (`Curp`,`idNivelAcademico`),
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
  ADD KEY `fk_Contrato_CURP` (`CURP`) USING BTREE,
  ADD KEY `fk_Contrato_Puesto` (`idPuesto`) USING BTREE,
  ADD KEY `fk_Contrato_Area` (`idArea`) USING BTREE,
  ADD KEY `fk_Contrato_Jornada` (`idJornada`) USING BTREE;

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
  ADD PRIMARY KEY (`Curp`,`idNivelAcademico`),
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
  MODIFY `idAnuncio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;

--
-- AUTO_INCREMENT de la tabla `area`
--
ALTER TABLE `area`
  MODIFY `idArea` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `carrera`
--
ALTER TABLE `carrera`
  MODIFY `idCarrera` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `contacto`
--
ALTER TABLE `contacto`
  MODIFY `idcontacto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

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
  MODIFY `idHabilidad` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `idioma`
--
ALTER TABLE `idioma`
  MODIFY `idIdioma` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `mediopublicidad`
--
ALTER TABLE `mediopublicidad`
  MODIFY `idMedioPublicidad` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `nivelacademico`
--
ALTER TABLE `nivelacademico`
  MODIFY `idNivelAcademico` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

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
  MODIFY `idPuesto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT de la tabla `solicitud`
--
ALTER TABLE `solicitud`
  MODIFY `idSolicitud` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

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
  ADD CONSTRAINT `fk_Candidato_has_Idioma_Candidato1` FOREIGN KEY (`Curp`) REFERENCES `candidato` (`Curp`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Candidato_has_Idioma_Idioma1` FOREIGN KEY (`idIdioma`) REFERENCES `idioma` (`idIdioma`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `candidato_has_nivelacademico`
--
ALTER TABLE `candidato_has_nivelacademico`
  ADD CONSTRAINT `fk_Candidato_has_NivelAcademico_Candidato1` FOREIGN KEY (`Curp`) REFERENCES `candidato` (`Curp`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Candidato_has_NivelAcademico_Carrera1` FOREIGN KEY (`idCarrera`) REFERENCES `carrera` (`idCarrera`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `fk_Candidato_has_NivelAcademico_NivelAcademico1` FOREIGN KEY (`idNivelAcademico`) REFERENCES `nivelacademico` (`idNivelAcademico`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `contrato`
--
ALTER TABLE `contrato`
  ADD CONSTRAINT `contrato_ibfk_1` FOREIGN KEY (`idArea`) REFERENCES `area` (`idArea`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `contrato_ibfk_2` FOREIGN KEY (`idPuesto`) REFERENCES `puesto` (`idPuesto`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `contrato_ibfk_3` FOREIGN KEY (`idJornada`) REFERENCES `jornada` (`IdJornada`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  ADD CONSTRAINT `contrato_ibfk_4` FOREIGN KEY (`CURP`) REFERENCES `empleado` (`Curp`) ON DELETE NO ACTION ON UPDATE NO ACTION;

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
  ADD CONSTRAINT `empleado_has_nivelacademico_ibfk_3` FOREIGN KEY (`Curp`) REFERENCES `empleado` (`Curp`) ON DELETE CASCADE ON UPDATE CASCADE;

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
