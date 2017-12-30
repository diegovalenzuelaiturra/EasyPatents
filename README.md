# EasyPatents
Buscador/Comparador de textos enfocado en Análisis de Patentes de Invención

# Descripción


En estos códigos implementamos la búsqueda de patentes de invención utilizando el criterio de similaridad y sentence embeddings construidos de acuerdo al paper [A Simple but Tough-to-Beat Baseline for Sentence Embeddings](https://openreview.net/forum?id=SyK00v5xx)

* Actualmente los autores del paper han publicado los códigos de su implementación en https://github.com/PrincetonML/SIF . Éstos no estaban disponibles públicamente durante el período en el que nosotros realizamos la implementación.

El código que presentamos permite realizar una búsqueda semántica de patentes de invención, ingresando el texto de búsqueda en un formulario en Typeform. El texto de búsqueda es comparado vectorialmente con todos los abstracts de patentes de invención contenidos en bases de datos locales mediante el cosine similarity de los sentence embeddings.

Adicionalemnte, los resultados de la búsqueda se envían de manera automática por correo.

Éstos resultados se entregan en un reporte en PDF que contiene los top K resultados de la búsqueda, ordenados de mayor a menor significancia de acuerdo un score que representa la similaridad semántica entre el texto de búsqueda y el abstract de las patentes de invención.


# Códigos


* Database.py
    * Genera base de datos local que contiene información de las patentes de invención y el *Sentence Embedding* de cada Abstract.


* EPmail.py
    * Clase para simplificar el envío de mensajes mediante la API de [Mailgun](https://www.mailgun.com)


* Report.py
    * Contiene funciones que permiter realizar un reporte en PDF que contiene los resultados a entregar, ordenados por mayor significancia de acuerdo al criterio de similaridad.


* Scores.py
    * Contiene funciones que permiten construir los Sentence Embeddings a partir de los Word Embeddings y realizar las diferentes operaciones necesarias para calcular Scores o medidas de similaridad, entre otros.
    

* ipc_database.py
    * Genera base de datos con los codigos ipc de las patentes y descripciones


* linkTypeform.py
    * Contiene funciones que permiten realizar la conexión con [Typeform](https://www.typeform.com), obtener las respuestas ingresadas a través de los formularios


* search_db.py y search_wipo.py

    * Clases que facilitan la búsqueda en las bases de datos locales de patentes


* text_processing.py
    * Contiene funciones que permiten realizar el preprocesamiento de los datos, construir vectores, generar archivos csv con los vectores de abstract y también enviar mail que contiene el reporte generado con los resultados ordenados por mayor significancia.


* version2.py
    * Código que obtiene desde un formulario [Typeform](https://www.typeform.com) las respuestas ingresadas, realiza el preprocesamiento de éstas, y con ello realiza búsquedas en las bases de datos locales de patentes de invención (previamente transformada a vector) utilizando criterio de similaridad (adicionalmente se realiza una similaridad con la clase IPC).


# API Keys y otros


* EPmail.py
    * Ingresar apiurl y apikey de usuario en [Mailgun](https://www.mailgun.com)


* linkTypeform.py
    * Ingresar typeform_UID y apikey de formulario en [Typeform](https://www.typeform.com)


# COSAS POR HACER #

* Abrir cuentas en la EPO  [check]

* Terminar página Web [check]
* Construir diccionario [check]
* Construir Array de Arrays [check]

* Congelar versión  [check]


# Autores:

> * Roberto Ibañez
> * Mauricio Morales
> * Diego Valenzuela

www.easypatents.cl
