# Proyecto

Un bot de telegram con funcionalidad para obtener información de clima, contar,
y generar mensajes de IA. Hecho como parte de mi prueba técnica en
[Delto](https://www.delto.com/en)

### Comandos disponibles

Al abrir el bot por primera vez (o borrar el historial, en caso reutilizar un
bot), debería ver el listado de comandos. De todas formas, son

- `/start`: Inicia la interacción con el bot y muestra un mensaje de bienvenida.
- `/count`: Incrementa un contador interno.
- `/weather `: Muestra el clima de una ubicación especificada. Para elegir
  ubicación, el usuario la comparte como en cualquier otro chat.
- `/ai `: La IA hará un mensaje en base a la información que ha conseguido en el
  chat.

Puede ver las explicaciones de cada comando en
[el archivo de configuración de comandos](./src/commands.py)

### Ejecución

Ejecutar mediante [uv](https://docs.astral.sh/uv/). Asumiendo que tenga uv
instalado, todas las dependencias se deberían instalar solas.

```bash
uv run --env-file .env dev
```

Incluir los campos de [el archivo de ejemplo](./env.example) en .env.

### Configuración

Para ejecutar el bot, necesitas configurar las claves API necesarias. Crea un
archivo `.env` en la raíz del proyecto basándote en `.env.example`. Debe
contener las siguientes variables:

- `TELEGRAM_API_KEY`: Tu token de bot de Telegram. Debes obtenerlo a través de
  [BotFather](https://core.telegram.org/bots/api#botfather).
- `OPENWEATHER_API_KEY`: Tu clave API para acceder al servicio de
  OpenWeatherMap. Puedes obtenerla en
  [su sitio web](https://home.openweathermap.org/api_keys).
- `GROQ_API_KEY`: Tu clave API para utilizar el servicio de IA de Groq. La
  consigues en [Groq Console](https://groq.com/).

Asegúrate de mantener tu archivo `.env` privado y no subirlo al repositorio.

### TODOs

- [x] Implementar autocompletado de comandos.
- [x] Implementar contador
- [x] Implementar clima.
- [x] Notificar errores al usuario.
- [x] Implementar IA.

### Notas

- No utilizo una librería para realizar llamadas a la api de openweather ya que:

    1. La [librería recomendada por openweather](url) no incluye stubs (no es
       tipada).
    2. La misma librería creashea al ejecutarse en mi computadora, y no
       [está mantenida](https://github.com/csparpa/pyowm?tab=readme-ov-file#maintainer-wanted-).
    3. El resto de librerías que encontré son muy impopulares, por lo que no
       confío en ellas.

- Persisto estado mediante sqlite para que les resulte más sencillo ejecutar el
  proyecto, ya que python incluye sqlite en su intérprete.

- Tanto el código como los comentarios de la aplicación están en inglés. Esto es
  porque prefiero tener los archivos enteros en un solo lenguaje, y siempre el
  código contiene inglés. Si esto causa problemas para la evaluación, por favor
  avisenme. De todas formas, el bot sigue estando en español.

> Viendo los commits, este proyecto te llevó bastante más de 4 horas, ¿no?

Si, me entretuve.

- Utilicé IA para explorar documentación y escribir algo de boilerplate
  (incluyendo partes del README). La gran mayoría del código está escrito por
  mí.

- No hay tests unitarios, solo ejecuté pruebas manuales.

- En el código hay comentarios con una firma (`-- CR`). Hago eso cuando estoy
  dando una opinión. La firma es redundante al ser yo el único desarrollador,
  pero igualmente no es larga.
