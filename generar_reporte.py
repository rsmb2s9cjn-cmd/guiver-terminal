import os
import json
import datetime
import google.generativeai as genai

# 1. Configurar la API de Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-pro')

# 2. Generar fecha actual
hoy = datetime.datetime.now()
fecha_str = hoy.strftime("%d de %B de %Y").replace("October", "Octubre").replace("November", "Noviembre")
fecha_corta = hoy.strftime("%d %b %Y").upper().replace("OCT", "OCT").replace("NOV", "NOV")

# 3. Prompt estricto para extraer el JSON
prompt = f"""
Actúa como Jerson Rondal, director de GUIVER Research. Escribe un reporte geopolítico Deep Dive para hoy ({fecha_str}).
Focalízate en causalidad política (omite impacto financiero) sobre: 1) EE. UU. e Irán, 2) China y Taiwán, 3) Yemen y Arabia Saudita.
Devuelve ÚNICAMENTE un objeto JSON válido con esta estructura exacta (sin formato markdown, solo el JSON puro):
{{
  "id": "guiver-deepdive-{hoy.strftime('%d%m%Y')}",
  "title": "Deep Dive {fecha_corta}: [Titular impactante]",
  "mapAlert": "ALERTA ORMUZ // ALERTA TAIWÁN // ALERTA MAR ROJO",
  "articlesHTML": "<article class='theater' data-tone='red'>...[Bloques HTML con t-head, prose, inset]...</article><article class='theater' data-tone='blue'>...</article><article class='theater' data-tone='orange'>...</article>",
  "metricsHTML": "<article class='metric' data-tone='red'>...[Bloques de métricas]...</article><article class='metric' data-tone='blue'>...</article><article class='metric' data-tone='orange'>...</article>"
}}
"""

# 4. Llamar a la IA
print("Generando reporte de inteligencia...")
response = model.generate_content(prompt)
texto_respuesta = response.text.strip()

if texto_respuesta.startswith("```json"):
    texto_respuesta = texto_respuesta[7:-3]
elif texto_respuesta.startswith("```"):
    texto_respuesta = texto_respuesta[3:-3]

# 5. Procesar y estructurar el nuevo reporte para el HTML
try:
    datos = json.loads(texto_respuesta.strip())
    
    nuevo_bloque_js = f"""
            {{
                id: "{datos['id']}",
                date: "{fecha_str}",
                category: "diario",
                badge: "HOY // DEEP DIVE 24H",
                badgeClass: "",
                theaters: ["Ormuz", "Taiwán", "Mar Rojo"],
                title: "{datos['title']}",
                html: buildInteractiveReportHTML({{
                    title: "Jerson Rondal | GUIVER Research — Deep Dive {fecha_corta}",
                    heading: "Deep Dive Geopolítico — {fecha_str}",
                    subtitle: "Análisis Exclusivo de Causalidad Política en Oriente Medio, Indo-Pacífico y Mar Rojo",
                    mapAlert: "{datos['mapAlert']}",
                    articlesHTML: `{datos['articlesHTML']}`,
                    metricsHTML: `{datos['metricsHTML']}`
                }})
            }},"""

    # 6. Insertar en el HTML
    with open("index.html", "r", encoding="utf-8") as file:
        html_content = file.read()

    nuevo_html = html_content.replace("// [MARKER_NUEVO_REPORTE]", f"// [MARKER_NUEVO_REPORTE]\n{nuevo_bloque_js}")

    with open("index.html", "w", encoding="utf-8") as file:
        file.write(nuevo_html)
        
    print("Reporte integrado en index.html con éxito.")

except Exception as e:
    print(f"Error procesando el JSON: {e}")
