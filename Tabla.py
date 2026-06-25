import streamlit as st
from supabase import create_client

# CONEXIÓN A SUPABASE
url = "https://olepcfbnlraduslpoddv.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9sZXBjZmJubHJhZHVzbHBvZGR2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI0MTk1MjcsImV4cCI6MjA5Nzk5NTUyN30.lU4YsOES2psmaRavw8ek28VYSjmymRx0PraPVb2rQe4"

supabase = create_client(url, key)

st.title("CRUD DE ALUMNOS")

menu = st.sidebar.selectbox(
    "Seleccione una opción",
    ["Crear", "Consultar", "Actualizar", "Eliminar"]
)

# ---------------- CREAR ----------------
if menu == "Crear":

    st.subheader("Registrar Alumno")

    dni = st.text_input("DNI")
    ap_pat = st.text_input("Apellido Paterno")
    ap_mat = st.text_input("Apellido Materno")
    nombre = st.text_input("Nombre")

    sexo = st.selectbox(
        "Sexo",
        ["Masculino", "Femenino"]
    )

    edad = st.number_input(
        "Edad",
        min_value=1,
        max_value=100,
        step=1
    )

    if st.button("Guardar"):

        if dni and ap_pat and ap_mat and nombre:

            datos = {
                "dni": dni,
                "apellido_pat": ap_pat,
                "apellido_mat": ap_mat,
                "nombre": nombre,
                "sexo": sexo,
                "edad": int(edad)
            }

            supabase.table("alumnos").insert(datos).execute()

            st.success("Alumno registrado correctamente")

        else:
            st.warning("Complete todos los campos.")

# ---------------- CONSULTAR ----------------
elif menu == "Consultar":

    st.subheader("Lista de alumnos")

    resultado = supabase.table("alumnos").select("*").execute()

    if resultado.data:
        st.dataframe(resultado.data)
    else:
        st.info("No hay alumnos registrados.")

# ---------------- ACTUALIZAR ----------------
elif menu == "Actualizar":

    st.subheader("Actualizar Edad")

    dni = st.text_input("DNI del alumno")

    nueva_edad = st.number_input(
        "Nueva edad",
        min_value=1,
        max_value=100,
        step=1
    )

    if st.button("Actualizar"):

        buscar = supabase.table("alumnos").select("*").eq("dni", dni).execute()

        if buscar.data:

            supabase.table("alumnos") \
                .update({"edad": int(nueva_edad)}) \
                .eq("dni", dni) \
                .execute()

            st.success("Registro actualizado correctamente")

        else:
            st.error("No existe un alumno con ese DNI.")

# ---------------- ELIMINAR ----------------
elif menu == "Eliminar":

    st.subheader("Eliminar Alumno")

    dni = st.text_input("DNI del alumno")

    if st.button("Eliminar"):

        buscar = supabase.table("alumnos").select("*").eq("dni", dni).execute()

        if buscar.data:

            supabase.table("alumnos") \
                .delete() \
                .eq("dni", dni) \
                .execute()

            st.success("Registro eliminado correctamente")

        else:
            st.error("No existe un alumno con ese DNI.")
