# Asismetro Automations

Este proyecto permite consultar y actualizar información de [asismetro.org](https://asismetro.org/) de forma automática.

En lugar de entrar en la web y hacer todos los pasos manualmente, otra aplicación puede enviar una petición a esta API. El proyecto abre un navegador, inicia sesión en Asismetro y realiza la tarea solicitada.

## Añade los turnos a tu calendario personal

Esta automatización se puede utilizar junto con [Calendar Subscription Hub](https://calendar-subscription-hub.ismola.dev/) para añadir automáticamente los turnos de Asismetro a tu calendario personal.

De esta forma, los turnos aparecen en la aplicación de calendario que utilizas habitualmente y se mantienen actualizados sin tener que copiarlos uno por uno.

## ¿Qué puede hacer?

### Consultar el calendario

Devuelve los turnos del mes actual y del mes siguiente, incluyendo:

- Los días y horarios.
- Las personas asignadas a cada turno.
- El estado de cada turno.
- Los turnos que todavía se pueden solicitar.

Ruta: `POST /get-calendar`

### Registrar la actividad de un curso bíblico

Rellena en Asismetro un nuevo registro con:

- La fecha.
- El turno.
- El tipo de actividad.
- La cantidad indicada.

Después devuelve la lista actualizada de registros.

Ruta: `POST /course_registration`

## ¿Cómo funciona?

1. Una aplicación envía a la API las credenciales de Asismetro y los datos necesarios.
2. El proyecto abre Asismetro en un navegador automático.
3. Inicia sesión y realiza la consulta o el registro.
4. Devuelve el resultado en formato JSON.
5. Cierra el navegador.

Este proyecto no es una API oficial de Asismetro. Automatiza su página web con Selenium, por lo que puede necesitar cambios si la web de Asismetro modifica su diseño.

## Ejemplo: consultar el calendario

```bash
curl -X POST http://localhost:3000/get-calendar \
  -H "Authorization: Bearer sample" \
  -H "Content-Type: application/json" \
  -d '{"username":"usuario","password":"clave"}'
```

## Ejemplo: crear un registro

```bash
curl -X POST http://localhost:3000/course_registration \
  -H "Authorization: Bearer sample" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "usuario",
    "password": "clave",
    "date": "04/05/2026",
    "shift": "1",
    "activity": "Curso Bíblico Iniciado",
    "number": "1"
  }'
```

Los valores permitidos para `shift` son `1`, `2`, `3` y `4`. Los tipos de actividad disponibles son:

- `Curso Bíblico Iniciado`
- `Sin Cursos Bíblicos`
- `Turno Anulado`

## Cómo ejecutarlo

La forma más sencilla es utilizar Docker:

```bash
cp .env.example .env
docker compose up --build
```

La API estará disponible en `http://localhost:3000`.

Antes de usarla, edita `.env` y cambia al menos estas variables:

```env
STAGE=staging
VALID_TOKEN=un_token_secreto
```

- `VALID_TOKEN` es la clave necesaria para llamar a la API.
- `STAGE=staging` permite hacer pruebas sin guardar realmente un registro.
- `STAGE=production` realiza las acciones reales en Asismetro.

## Rutas disponibles

| Ruta | Para qué sirve |
|---|---|
| `GET /` | Comprueba que el servicio está funcionando. |
| `POST /get-calendar` | Consulta el calendario actual y el siguiente. |
| `POST /course_registration` | Crea un registro de actividad. |

Todas las rutas de trabajo necesitan el token configurado en `.env`:

```text
Authorization: Bearer un_token_secreto
```

La documentación técnica completa de las peticiones y respuestas está en [API_REFERENCE.md](API_REFERENCE.md).

## Seguridad

Las peticiones contienen las credenciales de Asismetro y las respuestas del calendario pueden incluir nombres y teléfonos. En producción se debe usar HTTPS, un token seguro y limitar quién puede acceder a la API.

## Pruebas

```bash
pytest
```

## Licencia

Consulta [LICENSE.md](LICENSE.md).
