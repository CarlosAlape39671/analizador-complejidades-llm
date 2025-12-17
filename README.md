# Analizador de Complejidades Algorítmicas Asistido por LLMs

Proyecto académico desarrollado para la asignatura **Análisis y Diseño de Algoritmos**  
Programa de Ingeniería de Sistemas  
Universidad de Caldas

---

## 1. Descripción general

Este proyecto consiste en el desarrollo de un sistema software capaz de analizar la complejidad algorítmica de algoritmos descritos en seudocódigo, utilizando tanto técnicas clásicas de análisis de algoritmos como el apoyo de Modelos de Lenguaje de Gran Escala (LLMs).

El sistema permite al usuario ingresar seudocódigo de manera manual, cargarlo desde archivos de texto o generarlo automáticamente a partir de una descripción en lenguaje natural. A partir de dicha entrada, el sistema realiza un análisis léxico y sintáctico, construye un Árbol de Sintaxis Abstracta (AST), ejecuta el algoritmo y deduce su complejidad computacional en notación **O**, **Ω** y **Θ**.

Adicionalmente, el sistema integra un LLM (Gemini) para apoyar tareas como la generación de seudocódigo y la validación del análisis de complejidad obtenido de manera automática.

---

## 2. Objetivos del proyecto

### Objetivo general
Desarrollar un analizador de complejidades algorítmicas que combine técnicas formales de análisis de algoritmos con el uso de modelos de lenguaje para apoyar la interpretación, generación y validación de resultados.

### Objetivos específicos
- Implementar un analizador léxico y sintáctico para un lenguaje de seudocódigo estructurado.
- Construir un Árbol de Sintaxis Abstracta (AST) a partir del seudocódigo ingresado.
- Ejecutar algoritmos tanto de forma completa como paso a paso, mostrando el estado de los ambientes de ejecución.
- Determinar la complejidad algorítmica en los casos peor, mejor y promedio.
- Integrar un LLM para generar seudocódigo a partir de descripciones en lenguaje natural.
- Validar, mediante un LLM, los resultados de complejidad obtenidos por el analizador.
- Proveer una interfaz gráfica que facilite la interacción con el sistema.

---

## 3. Alcance del sistema

El sistema está diseñado para analizar seudocódigo estructurado que incluya:
- Asignaciones.
- Estructuras condicionales (`if`, `else`).
- Estructuras iterativas (`for`, `while`, `repeat-until`).
- Expresiones aritméticas y relacionales básicas.

No se busca cubrir todos los lenguajes de programación reales ni realizar optimizaciones de código, sino enfocarse en el análisis académico de la complejidad algorítmica y en la visualización del comportamiento del algoritmo.

---

## 4. Arquitectura

El proyecto adopta el patrón arquitectónico **Modelo–Vista–Controlador (MVC)**, con el fin de separar claramente las responsabilidades del sistema:

- **Modelo**: Contiene la lógica central del sistema, incluyendo el lexer, parser, AST, analizador de complejidad, ejecución del algoritmo y manejo de ambientes.
- **Vista**: Gestiona la interacción con el usuario, mostrando código, resultados, errores, trazas de ejecución y ambientes.
- **Controlador**: Coordina la comunicación entre la vista y el modelo, orquestando el flujo de ejecución del sistema.
- **Servicios**: Incluye componentes auxiliares como el manejo de archivos y la integración con el modelo de lenguaje (LLM).

Esta arquitectura facilita la extensibilidad, el mantenimiento y la futura incorporación de nuevas funcionalidades.

---

## 5. Funcionalidades principales

- Ingreso de seudocódigo manualmente o mediante archivos.
- Generación automática de seudocódigo a partir de descripciones usando un LLM.
- Análisis léxico y sintáctico con reporte de errores detallados.
- Construcción y visualización del AST.
- Ejecución completa del algoritmo.
- Ejecución paso a paso con:
  - Resaltado de la línea ejecutada.
  - Visualización de ambientes de ejecución.
  - Navegación entre pasos (siguiente, anterior, reinicio).
- Análisis de complejidad algorítmica.
- Validación del análisis de complejidad mediante un LLM.

---

## 6. Tecnologías utilizadas

- **Lenguaje de programación**: Python 3
- **Arquitectura**: Modelo–Vista–Controlador (MVC)
- **Modelo de Lenguaje**: Gemini
- **Control de versiones**: Git y GitHub

---

## 7. Estado del proyecto

El proyecto se encuentra actualmente en desarrollo. En esta etapa se ha definido la arquitectura, los diagramas UML y la estructura base del sistema. La implementación del analizador y la interfaz gráfica se realizará de manera incremental.

---

## 8. Autores

Proyecto desarrollado por estudiantes del programa de **Ingeniería de Sistemas** de la **Universidad de Caldas**, como parte del curso de Análisis y Diseño de Algoritmos.
