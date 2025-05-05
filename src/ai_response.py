import asyncio
from groq import AsyncGroq, BaseModel
from telegram import Update
from telegram.ext import ContextTypes
from textwrap import dedent

from apis.openweather import DEFAULT_WEATHER_CLIENT
from apis.openweather_get_response_codegen import WeatherData
from db.queries import get_user, get_users_fun_facts, insert_fun_fact


class ExpectedResponse(BaseModel):
    response_to_user: str
    fun_fact_summary: str


async def ai_response(update: Update, _context: ContextTypes.DEFAULT_TYPE):
    assert update.effective_user and update.message
    user, fun_facts = await asyncio.gather(
        get_user(update.effective_user.id),
        get_users_fun_facts(update.effective_user.id),
    )

    if not user:
        _ = await update.message.reply_text(
            '¡Déjame conocerte un poco primero! Utiliza las otras funcionalidades.'
        )
        return

    weather: WeatherData | None = None

    if user.latitude and user.longitude:
        weather = await DEFAULT_WEATHER_CLIENT.get_weather(
            {
                'lat': user.latitude,
                'lon': user.longitude,
                'lang': 'es',
                'units': 'metric',
            }
        )

    weather_prompt = (
        'El usuario no ha explorado la funcionalidad de ubicación con anterioridad, recuérdaselo amenos que ya se lo hayas recordado.'
        if not weather
        else f'Menciona algo del clima de su última ubicación, el cúal es: {weather.model_dump_json(indent=2)}'
    )

    prompt = dedent(f"""
        Eres un chatbot de Telegram desarrollado por la empresa Delto que tiene que responder al comand /ai. Hablarás con {update.effective_user.name}.
        El usuario puede ejecutar un comando para aumentar un contador. Actualmente tiene el valor {user.counter}. Dile un dato curioso sobre el mismo. Cuando el valor se repite, dile uno diferente.
        El usuario pudo haber compartido una ubicación (no necesariamente su ubicación) con el bot para pedir información del clima.
        {weather_prompt}

        Sé creativo y no hagas que tu respuesta suene como un listado. Tu propósito es entretener y educar.
        NO LE PIDAS SEGUIMIENTO A TU MENSAJE A EL USUARIO. NO IMPLIQUES QUE PUEDES RESPONDER A CUALQUIER MENSAJE.


        TU RESPUESTA, NECESARIAMENTE, TIENE QUE SER EN ESTE FORMATO JSON: {ExpectedResponse.model_json_schema()}.
        TIENES QUE HABLAR EN ESPAÑOL.

        FUN FACT SUMMARY TIENE QUE SER BREVE. ESCRÍBELO PARA RECONOCER LOS DATOS CURIOSOS QUE HAS DICHO PREVIAMENTE, Y QUÉ RECORDATORIOS HAS HECHO.
        Previamente has dicho los siguientes datos curiosos a este usuario: {str([ff.fun_fact_summary for ff in fun_facts])}. No repitas los datos. Es preferible que digas que no tienes nuevos datos curiosos a que te repitas.

        No es necesario que repitas hablar del clima si no ha cambiado desde la última vez.
        Si es posible hacer una relación, haz comentarios sobre los temas pasados, o sobre el progreso contando del usuario.
    """)

    print(prompt)

    async with AsyncGroq() as groq_client:
        result = await groq_client.chat.completions.create(
            model='deepseek-r1-distill-llama-70b',
            response_format={'type': 'json_object'},
            messages=[
                {
                    'role': 'system',
                    'content': prompt,
                }
            ],
            max_tokens=4096,
            reasoning_format="hidden"
        )

    message = result.choices[0].message.content
    print(message)
    assert message
    parsed_message = ExpectedResponse.model_validate_json(message)

    _ = await asyncio.gather(
        insert_fun_fact(
            update.effective_user.id, parsed_message.fun_fact_summary
        ),
        update.message.reply_text(parsed_message.response_to_user),
    )
