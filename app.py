
import streamlit as st

# ==========================================
# CONFIGURACIÓN DE LA APLICACIÓN
# ==========================================

st.set_page_config(
    page_title="Sistema Experto Respiratorio",
    page_icon="🫁",
    layout="centered"
)

st.title("🫁 Sistema Experto de Orientación Respiratoria")
st.subheader("Evaluación preliminar basada en síntomas")

st.warning(
    "Prototipo académico. No proporciona diagnósticos médicos "
    "ni reemplaza la evaluación de un profesional de salud."
)


# ==========================================
# MOTOR DE INFERENCIA
# ==========================================

def motor_inferencia(datos):

    # R0: Identificación de señales de alarma
    if (
        datos["dificultad_respirar"]
        or datos["dolor_pecho"]
        or datos["labios_azulados"]
        or datos["confusion"]
    ):
        return {
            "estado": "urgencia",
            "reglas": ["R0"],
            "explicacion": "Se identificó una señal de alarma."
        }

    reglas = []

    # R1: Rinitis alérgica
    if (
        datos["picazon"]
        and datos["ojos_llorosos"]
        and datos["estornudos"]
        
    ):
        reglas.append({
            "codigo": "R1",
            "afeccion": "Rinitis alérgica",
            "explicacion": (
                "Coinciden la picazón nasal u ocular, "
                "los estornudos y los ojos llorosos, "
                "sin presencia de fiebre."
            )
        })

    # R2: Influenza
    if (
        datos["inicio"] == "Repentino"
        and datos["fiebre"]
        and (
            datos["dolor_muscular"]
            or datos["escalofrios"]
        )
        and (
            datos["tos"]
            or datos["cansancio"]
        )
    ):
        reglas.append({
            "codigo": "R2",
            "afeccion": "Influenza (gripe)",
            "explicacion": (
                "Coinciden el inicio repentino, la fiebre, "
                "los dolores musculares o escalofríos, "
                "junto con tos o cansancio."
            )
        })

    # R3: Resfriado común
    if (
        datos["inicio"] == "Gradual"
        and (
            datos["rinorrea"]
            or datos["congestion"]
        )
        and (
            datos["estornudos"]
            or datos["dolor_garganta"]
            or datos["tos"]
        )
    ):
        reglas.append({
            "codigo": "R3",
            "afeccion": "Resfriado común",
            "explicacion": (
                "Coinciden el inicio gradual, la secreción "
                "o congestión nasal y la presencia de "
                "estornudos, dolor de garganta o tos."
            )
        })

    # Evaluación de las reglas activadas

    if len(reglas) == 1:
        return {
            "estado": "orientacion",
            "reglas": reglas
        }

    elif len(reglas) > 1:
        return {
            "estado": "ambiguo",
            "reglas": reglas
        }

    else:
        return {
            "estado": "indeterminado",
            "reglas": []
        }


# ==========================================
# INTERFAZ DE USUARIO
# ==========================================

with st.form("formulario_sintomas"):

    st.subheader("1. Seleccione los síntomas")

    col1, col2 = st.columns(2)

    with col1:
        fiebre = st.checkbox("Fiebre")
        tos = st.checkbox("Tos")
        estornudos = st.checkbox("Estornudos")
        rinorrea = st.checkbox("Secreción nasal")
        congestion = st.checkbox("Congestión nasal")
        dolor_garganta = st.checkbox("Dolor de garganta")
        dolor_muscular = st.checkbox("Dolor muscular")

    with col2:
        escalofrios = st.checkbox("Escalofríos")
        cansancio = st.checkbox("Cansancio o fatiga")
        picazon = st.checkbox("Picazón en nariz u ojos")
        ojos_llorosos = st.checkbox("Ojos llorosos")

        st.markdown("**Señales de alarma**")

        dificultad_respirar = st.checkbox(
            "Dificultad para respirar"
        )
        dolor_pecho = st.checkbox(
            "Dolor o presión en el pecho"
        )
        labios_azulados = st.checkbox(
            "Labios o rostro azulados"
        )
        confusion = st.checkbox(
            "Confusión o dificultad para mantenerse alerta"
        )

    st.subheader("2. Inicio de los síntomas")

    inicio = st.radio(
        "¿Cómo comenzaron los síntomas?",
        ["Gradual", "Repentino", "No lo sé"],
        horizontal=True
    )

    evaluar = st.form_submit_button(
        "Evaluar síntomas"
    )


# ==========================================
# PROCESAMIENTO Y RESULTADOS
# ==========================================

if evaluar:

    datos = {
        "fiebre": fiebre,
        "tos": tos,
        "estornudos": estornudos,
        "rinorrea": rinorrea,
        "congestion": congestion,
        "dolor_garganta": dolor_garganta,
        "dolor_muscular": dolor_muscular,
        "escalofrios": escalofrios,
        "cansancio": cansancio,
        "picazon": picazon,
        "ojos_llorosos": ojos_llorosos,
        "dificultad_respirar": dificultad_respirar,
        "dolor_pecho": dolor_pecho,
        "labios_azulados": labios_azulados,
        "confusion": confusion,
        "inicio": inicio
    }

    resultado = motor_inferencia(datos)

    st.divider()
    st.subheader("3. Resultado del sistema experto")

    if resultado["estado"] == "urgencia":

        st.error(
            "Se identificó una señal de alarma. "
            "Busca atención médica urgente."
        )

        st.write(resultado["explicacion"])
        st.caption("Regla activada: R0")

    elif resultado["estado"] == "orientacion":

        regla = resultado["reglas"][0]

        st.success(
            "Patrón de síntomas compatible con: "
            + regla["afeccion"]
        )

        st.write("**Explicación del resultado:**")
        st.write(regla["explicacion"])

        st.caption(
            "Regla aplicada: " + regla["codigo"]
        )

    elif resultado["estado"] == "ambiguo":

        st.warning(
            "Los síntomas coinciden con más de una regla. "
            "El sistema no puede diferenciarlos con seguridad."
        )

        for regla in resultado["reglas"]:

            st.markdown(
                "**" + regla["codigo"]
                + " - " + regla["afeccion"] + "**"
            )

            st.write(regla["explicacion"])

    else:

        st.info(
            "No se activó ninguna regla de la base de conocimientos. "
            "Los datos son insuficientes para proporcionar "
            "una orientación preliminar."
        )

    st.info(
        "Este resultado es exclusivamente educativo. "
        "Si los síntomas empeoran, persisten o generan preocupación, "
        "consulta con un profesional de salud."
    )


# ==========================================
# PIE DE APLICACIÓN
# ==========================================

st.divider()

st.caption(
    "Inteligencia Artificial II | "
    "Sistema experto basado en reglas de producción."
)
