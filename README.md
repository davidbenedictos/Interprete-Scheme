
# Mini Scheme Interpreter

## Descripción
Este proyecto implementa un intérprete para Mini Scheme, una versión simplificada del lenguaje Scheme, usando Python y ANTLR. Mini Scheme es un lenguaje de programación funcional que permite definir funciones, realizar operaciones matemáticas, trabajar con listas y mucho más. Este intérprete permite evaluar programas en Mini Scheme con soporte para entrada/salida, definición de funciones y constantes, y estructuras condicionales.

## Características
- **Operaciones básicas:** Soporte para `+`, `-`, `*`, `/`, `mod`, así como operadores relacionales (`<`, `>`, `<=`, `>=`, `=`, `<>`).
- **Definición de funciones y constantes:** Uso de `define` para crear funciones globales y constantes.
- **Condicionales:** Soporte para `if` y `cond`.
- **Manipulación de listas:** Funciones `car`, `cdr`, `cons`, `null?`.
- **Entrada/salida:** Uso de `read`, `display`, y `newline` para interactuar con el usuario.
- **Variables locales:** Implementación de `let` para crear variables locales dentro de una expresión.
- **Booleans:** Soporte para `#t` (true) y `#f` (false), así como operadores lógicos `and`, `or`, `not`.
- **Ejecución de `main`:** Todos los programas deben iniciar con una función `main` que se ejecuta automáticamente.

## Requisitos
- Python 3.x
- ANTLR 4 (para generar el lexer y el parser a partir de la gramática `Scheme.g4`).

## Instrucciones de uso

1. **Compilación del intérprete:**
   Asegúrate de que los archivos necesarios estén en el directorio, incluyendo `Scheme.g4`, `Scheme.py`, y el archivo `Makefile`. Luego ejecuta:
   ```bash
   make
   ```
   Esto generará los archivos necesarios utilizando ANTLR.

2. **Ejecución del programa:**
   Usa el comando:
   ```bash
   python3 Scheme.py <archivo.scm>
   ```
   Donde `<archivo.scm>` es el archivo con el código en Mini Scheme.

3. **Entrada y salida:**
   Puedes proporcionar entradas al programa a través de `stdin` y redirigir la salida a un archivo usando:
   ```bash
   python3 Scheme.py programa.scm < entrada.txt > salida.txt
   ```

## Ejemplo de uso
Archivo `mcd.scm`:
```scheme
(define (mcd a b)
  (if (= b 0)
      a
      (mcd b (mod a b))))

(define (main)
  (let ((a (read))
        (b (read)))
    (display "El máximo común divisor es: ")
    (display (mcd a b))
    (newline)))
```

Entrada (`entrada.txt`):
```
48
18
```

Comando:
```bash
python3 Scheme.py mcd.scm < entrada.txt > salida.txt
```

Salida (`salida.txt`):
```
El máximo común divisor es: 6
```

## Estructura del proyecto
- **`Scheme.g4`**: Gramática de Mini Scheme para ANTLR.
- **`Scheme.py`**: Programa principal que implementa el intérprete.
- **`Makefile`**: Archivo para automatizar la generación de código con ANTLR.
- **`tests/`**: Directorio con juegos de prueba:
  - Archivos `.scm`: Código en Mini Scheme.
  - Archivos `.inp`: Entradas para los programas.
  - Archivos `.out`: Salidas esperadas.

## Limitaciones
- Solo se admiten funciones globales (no hay funciones anónimas ni definiciones locales dentro de otras funciones).
- Las variables deben ser definidas antes de ser usadas y no pueden ser reasignadas.
- No se manejan errores semánticos ni de tipo; el comportamiento es indefinido en estos casos.

## Decisiones de diseño
- El programa comienza ejecutando automáticamente la función `main` si está definida y no tiene parámetros.
- Se utiliza una tabla de símbolos global para manejar variables y funciones.

## Contribuciones
Proyecto desarrollado como parte de la práctica de la asignatura de Llenguatges de Programació de GEI.

## Referencias
- [Documentación oficial de Scheme](https://schemers.org)
- [ANTLR 4](https://www.antlr.org/)
