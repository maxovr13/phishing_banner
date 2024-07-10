import streamlit as st
import mysql.connector

# Configuración de la conexión a la base de datos
db_config = {
    'user': 'root',
    'password': 'Crimax123',
    'host': 'localhost',
    'database': 'docentes'
}

# Conectar a la base de datos MySQL
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Actualizar el estado de acceso en la base de datos
def update_access_status(token):
    conn = get_db_connection()
    cursor = conn.cursor()
    update_query = "UPDATE docentes SET accedio = TRUE WHERE token = %s"
    cursor.execute(update_query, (token,))
    conn.commit()
    cursor.close()
    conn.close()

# Obtener la información del docente por token
def get_docente_info(token):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    select_query = "SELECT * FROM docentes WHERE token = %s"
    cursor.execute(select_query, (token,))
    docente = cursor.fetchone()
    cursor.close()
    conn.close()
    return docente

# Obtener el token completo de los parámetros de consulta
query_params = st.query_params
token = query_params.get("token", None)

st.set_page_config(
        page_title="Speaphishing Project",
        page_icon = "fishing_pole_and_fish"
)
# Verificar si se proporcionó un token válido
if token:
    docente = get_docente_info(token)
    if docente:
        # Mostrar la información del docente
        
        st.image('depto_inf_logo.png')
        st.title("¡Tranquilo!")
        st.write(f"Hola {docente['nombre']}")
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
