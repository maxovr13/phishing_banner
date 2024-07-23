import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(
    page_title="Test de SpearPhishing",
    page_icon="fishing_pole_and_fish"
)

# Conexión a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
# Leer datos de la hoja de cálculo
@st.cache_data(ttl=0)  # Desactivar el caché para la lectura de datos
def load_data():
    return conn.read(worksheet="Hoja 1", ttl = 5) #importante para actualizacion inmediata

data = load_data()

df = pd.DataFrame(data)  # Convertir a DataFrame

# Actualizar el estado de acceso en la hoja de cálculo
def update_access_status(token):
    global df  # Usar el DataFrame global para actualizar
    index = df.index[df['token'] == token].tolist()
    if index:
        df.at[index[0], 'accedio'] = 1
        conn.update(worksheet = "Hoja 1", data = df)
        # Convertir DataFrame a lista de listas y actualizar la hoja de cálculo
        #records = df.values.tolist()
        #header = df.columns.values.tolist()
        #conn.write([header] + records, worksheet="Hoja 1")

# Obtener la información del docente por token
def get_docente_info(token):
    docente = df[df['token'] == token]
    if not docente.empty:
        # Convertir el valor de 'accedio' a booleano
        docente_info = docente.iloc[0].to_dict()
        docente_info['accedio'] = bool(docente_info['accedio'])
        return docente_info
    else:
        return None

def get_nombre_docente(token):
    docente = df[df['token'] == token]
    nombre_docente = docente["nombre"]
    return nombre_docente


# Obtener el token completo de los parámetros de consulta
query_params = st.query_params
token = query_params.get("token", None)
nombre_texto = get_nombre_docente(token)
# Verificar si se proporcionó un token válido
if token:
    docente = get_docente_info(token)
    if docente:
        # Mostrar la información del docente
        st.image('depto_inf_logo.png')
        st.title("¡Tranquil@!")
        st.write(f"Hola {nombre_texto.values[0]}")
        st.write("Has sido partícipe de un estudio acerca de Evaluación Automática de Vulnerabilidades de Ingeniería Social Organizacional, a cargo de Maximiliano Vergara Ríos, estudiante de la carrera de Ingeniería Informática y Ciencias de la Computación de la Universidad de Concepción en el contexto de la memoria de título “Hacia el desarrollo de una herramienta de evaluación de vulnerabilidades de ingeniería social”.")
        st.write("El correo que leíste anteriormente tenía la intención de vulnerar las posibles defensas que pueda tener una organización como la que perteneces por medio de la implementación de ingeniería social.")
        st.markdown("Destacar que al ser una prueba **ESTO NO GENERA NI UN RIESGO NI PARA TI NI PARA LA ORGANIZACIÓN A LA QUE PERTENECES**.")
        st.markdown("Además, señalar que los resultados de este test serán **ANONIMIZADOS**, es decir, nadie más que quienes trabajan en el desarrollo de este proyecto sabrán que has respondido.")
        # Actualizar el estado de acceso si aún no se ha registrado
        if not docente['accedio']:
            update_access_status(token)
            st.write("¡Muchas gracias por participar!")
        else:
            st.write("¡Muchas gracias por participar!")
    else:
        st.error("Token inválido o docente no encontrado.")
else:
    st.error("No se proporcionó un token.")
