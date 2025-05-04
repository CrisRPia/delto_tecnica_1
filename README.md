# Ejecución

Ejecutar mediante [uv](https://docs.astral.sh/uv/)

```bash
uv run --env-file .env dev
```

Incluir los campos de [el archivo de ejemplo](./env.example) en .env.

### TODOs

- [ ] Utilizar botones para realizar acciones.
- [x] Implementar contador
- [ ] Implementar clima.
- [ ] Implementar IA.

### Notas

- No utilizo una librería para realizar llamadas a la api de openweather ya que:

    1. La [librería recomendada por openweather](url) no incluye stubs (no es
       tipada).
    2. La misma librería creashea al ejecutarse en mi computadora, y no
       [está mantenida](https://github.com/csparpa/pyowm?tab=readme-ov-file#maintainer-wanted-).
    3. El resto de librerías que encontré son muy impopulares, por lo que no
       confío en ellas.

- Persisto estado mediante sqlite para que les resulte más sencillo ejecutar el
  proyecto, ya que python incluye sqlite en su intérprete. Es posible que esto
  sea redundante si decido añadir Docker al proyecto.
