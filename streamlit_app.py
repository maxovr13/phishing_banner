import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(
    page_title="Spear Phishing Project",
    page_icon="fishing_pole_and_fish"
)

# Conexión a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
# Leer datos de la hoja de cálculo
@st.cache_data(ttl=0)  # Desactivar el caché para la lectura de datos
def load_data():
    return conn.read(worksheet="LLMSecurityGroup", ttl = 5) #importante para actualizacion inmediata

data = load_data()

df = pd.DataFrame(data)  # Convertir a DataFrame

# Actualizar el estado de acceso en la hoja de cálculo
def update_access_status(token):
    global df  # Usar el DataFrame global para actualizar
    
    # Buscar el índice donde el token coincida con cualquiera de las columnas
    index1 = df.index[df['token1'] == token].tolist()
    index2 = df.index[df['token2'] == token].tolist()
    index3 = df.index[df['token3'] == token].tolist()
    
    if index1:
        df.at[index1[0], 'accedio1'] = 1
    elif index2:
        df.at[index2[0], 'accedio2'] = 1
    elif index3:
        df.at[index3[0], 'accedio3'] = 1
    
    # Actualizar la hoja de cálculo
    conn.update(worksheet="LLMSecurityGroup", data=df)
        # Convertir DataFrame a lista de listas y actualizar la hoja de cálculo
        #records = df.values.tolist()
        #header = df.columns.values.tolist()
        #conn.write([header] + records, worksheet="Hoja 1")

# Obtener la información del docente por token
def get_docente_info(token):
    docente = df[(df['token1'] == token) | (df['token2'] == token) | (df['token3'] == token)]
    if not docente.empty:
        # Convertir los valores de 'accedio1', 'accedio2', 'accedio3' a booleano
        docente_info = docente.iloc[0].to_dict()
        docente_info['accedio1'] = bool(docente_info['accedio1'])
        docente_info['accedio2'] = bool(docente_info['accedio2'])
        docente_info['accedio3'] = bool(docente_info['accedio3'])
        return docente_info
    else:
        return None

# Obtener el nombre del docente por token
def get_nombre_docente(token):
    docente = df[(df['token1'] == token) | (df['token2'] == token) | (df['token3'] == token)]
    if not docente.empty:
        nombre_docente = docente.iloc[0]["nombre"]
        return nombre_docente
    else:
        return None


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
        st.write(f"Hola {nombre_texto}")
        st.write("Has sido partícipe de un estudio acerca de Evaluación Automática de Vulnerabilidades de Ingeniería Social Organizacional, a cargo de Maximiliano Vergara Ríos, estudiante de la carrera de Ingeniería Informática y Ciencias de la Computación de la Universidad de Concepción en el contexto de la memoria de título “Hacia el desarrollo de una herramienta de evaluación de vulnerabilidades de ingeniería social”.")
        st.write("El correo que leíste anteriormente tenía la intención de vulnerar las posibles defensas que pueda tener una organización como la que perteneces por medio de la implementación de ingeniería social.")
        st.markdown("Destacar que al ser una prueba **ESTO NO GENERA NI UN RIESGO NI PARA TI NI PARA LA ORGANIZACIÓN A LA QUE PERTENECES**.")
        st.markdown("Además, señalar que los resultados de este test serán **ANONIMIZADOS**, es decir, nadie más que quienes trabajan en el desarrollo de este proyecto sabrán que has respondido."

        # Actualizar el estado de acceso si aún no se ha registrado
        if not (docente['accedio1'] or docente['accedio2'] or docente['accedio3']):
            update_access_status(token)
            st.write("¡Muchas gracias por participar!")
        else:
            st.write("¡Muchas gracias por participar!")
    else:
        st.error("Token inválido o docente no encontrado.")
else:
    st.error("No se proporcionó un token.")
st.title("Formulario de Pregunta")

# Pregunta y caja de texto
respuesta = st.text_area("Hola, ¿cómo estás?")

# Botón de enviar
if st.button("Submit"):
    if respuesta:
        # Obtener el token del parámetro de consulta (si es necesario para identificar la fila)
        query_params = st.query_params
        token = query_params.get("token", None)
        
        if token:
            # Buscar la fila correspondiente en el DataFrame
            index = df.index[(df['token1'] == token) | (df['token2'] == token) | (df['token3'] == token)].tolist()
            
            if index:
                # Actualizar la respuesta en la columna 'pregunta1'
                df.at[index[0], 'pregunta1'] = respuesta
                # Actualizar la hoja de cálculo
                conn.update(worksheet="LLMSecurityGroup", data=df)
                st.success("Respuesta enviada y guardada con éxito.")
            else:
                st.error("Token inválido o docente no encontrado.")
        else:
            st.error("No se proporcionó un token.")
    else:
        st.error("Por favor, ingresa una respuesta.")
