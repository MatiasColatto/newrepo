import json
import pandas as pd
import plotly.express as px


latencias = []
requests = []
errores = []


with open("results/resultado.json") as archivo:

    for linea in archivo:

        dato = json.loads(linea)


        if dato.get("type") != "Point":
            continue


        metric = dato["metric"]

        valor = dato["data"]["value"]


        if metric == "http_req_duration":

            latencias.append({
                "tiempo":
                dato["data"]["time"],

                "ms":
                valor
            })


        if metric == "http_reqs":

            requests.append({
                "tiempo":
                dato["data"]["time"],

                "requests":
                valor
            })


        if metric == "http_req_failed":

            errores.append({
                "tiempo":
                dato["data"]["time"],

                "error":
                valor
            })



df_lat = pd.DataFrame(latencias)
df_req = pd.DataFrame(requests)
df_err = pd.DataFrame(errores)



fig_lat = px.line(
    df_lat,
    y="ms",
    title="Latencia HTTP"
)


fig_req = px.line(
    df_req,
    y="requests",
    title="Requests HTTP"
)


fig_err = px.line(
    df_err,
    y="error",
    title="Errores"
)



html = f"""

<html>

<head>
<title>Reporte k6 PetClinic</title>
</head>


<body>


<h1>Performance Report - PetClinic</h1>


<h2>Latencia</h2>

{fig_lat.to_html(full_html=False)}


<h2>Requests</h2>

{fig_req.to_html(full_html=False)}


<h2>Errores</h2>

{fig_err.to_html(full_html=False)}


</body>

</html>

"""


with open(
    "reporte_k6.html",
    "w",
    encoding="utf-8"
) as f:

    f.write(html)


print("Reporte generado: reporte_k6.html")