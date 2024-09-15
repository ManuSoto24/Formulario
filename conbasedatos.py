import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import base64

# Pega el contenido del archivo credentials_base64.txt aquí como una cadena larga
credentials_base64 = """
ewogICJ0eXBlIjogInNlcnZpY2VfYWNjb3VudCIsCiAgInByb2plY3RfaWQiOiAicmVnaXN0cm8tZGUtdGVycmVub3MtY2htbCIsCiAgInByaXZhdGVfa2V5X2lkIjogIjA0YTkwMzNjZjkwNWFkOGUzMjgwZDkxNWJmNzA5MmYzYzIyODZjMGQiLAogICJwcml2YXRlX2tleSI6ICItLS0tLUJFR0lOIFBSSVZBVEUgS0VZLS0tLS1cbk1JSUV2UUlCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQktjd2dnU2pBZ0VBQW9JQkFRQzA0R3M1SUdVM24rRGlcbndGNm1QTHQ4MERzb0djdzFuYmhSdjJrY3FiN3pyUUE2c1NJUDhqRzNPWCtvQVZLNkhWSzB4VjI2K2Zha2pCVHhcbkVYeWRIMlpkSFppcHB1dk5KbWN6SW9NbGU4aHBjcU5zTnZtNTVxY2JER0hsZGV5WElPRGY3K2hXOWpTTU9TZ0xcbnBYeGVNQWJRUEJsQ1hnN0htNmd5UGxFOTRJbjZ1bnJ6dzVSZTJETnVCQTJ6MTNieEs5Qm9KbHY3RFNHOS9Tb3VcbmtjMkt3RWc0bGF3VTEyRjhqdGh4SWR5K0hMUDNQWmxZdGdmMjl6ZjNpZ0NObVRnR3A0a1IveXgxdFRaVGpBWmJcblJGODduakNrN252MU52YjNnQVcwQlhvbkM0RUFTenl5SE5MUlpITlFkYlFaWXdQYXNYOEx1M3FqTkp2RE9obWZcblJkSzBKT3R4QWdNQkFBRUNnZ0VBQ1NDa0RkNGJ6WHFmYmhjNEQ0VXBaRUNHZVFlOWt0MFNmcFE5V1Nsd1l6cVJcbk5EcFpGakNVeXExaVN1enZnRWlDTW5ESDdKWU5tTHNnUkJRQS9sVjdKR3JJYlQzbysxRndvV3pMUW0vUEtyeG9cbkVSOXJGYkwvMlhFVUJadDFwTXRreUZndEdOVCt6TmxiaUhtVzM1S1JNc2s5bXhMdnNGU2pZR1JkcVgrSnZFeHBcbks1QndKaVMvK1dHdE1TczhGcXFvMktWN0NzSmVtKy90akI1ZWFYOFlZVk5SUmNOTk5iL2xkeFdLODM0bVhVZzJcbnRHTy8wd2o3VnRnVzBYNzdBY2NNNllCcHBTMzcwM0tvYi9wbVFDTkJpcGxraE9KMHNnVm12T1RUbFhWdkNudXFcbmE2WVBtNTRSOC9qVjdsYlFncnl2clhhNTNlUWhaZTQraXZZdXVscVVjd0tCZ1FEM3BETTFqYmJTWVI3dWdXY2NcbkJOc3IzSVB2UXNYRDZHQW80ajNHMFVsclVPdEJWRGt2MGZEZFJFOWdaYndLMnJyT0JiNmk5aVZBTk9OeG1QSUpcbnVnZ2xoaTc2L09YaTR4K0lXMzNzeFhiS3BzNDAvNjMxeTJZY1NyUFY1S09FQ0k2K1RiV2xycjdpVksxVHorTE9cbmZqSFF6dkZJRWdIbk10Rm15TVhET3NjQmp3S0JnUUM2KzFLNWQ4VmxsTm1SekZGc2ZVZkVBNGJKMlRXdEdoY2tcbmc5bFI0b1ArT09CM1BCQ0RxYnRLQkN0djhjREY4M1A0d1I3OEllMU5iT2JCWisyNWpIRFcyb3ptMkFMa1UyV3RcbklUMm1iTXpLc3NaYjZrWTRyT01jNTBHVXpyRjhtMEhDS2dBWjMzRndrbisxODNGMkJMM3ZsVzNXWjRCWlBvQXJcbkJldTRSWVRDL3dLQmdHV2JuODlYYUM0RjMzVW83eStWNW4rbXFST2dxQmhyM2hpb1M0U3FGcC9Md2RzNlBZU2JcbmRXSzBSb1ZjK0x6VFpsWm1FUVE0VHF4N2h0N3pURXdsWW5aVENpKzlXRzJ4bHh5UnZhZEtsaVVzTCt1YkJMdVhcblN6eE1nbUUrd01ESjZoZTNOdExXVWtmM1NtN2JHMHB5aU9vT0h2M2ROWjZ4UVM0Vkx0K2QzRTJOQW9HQUxzdkxcbmptTnRZZGo1QXNaUjhvY0FPUXh3NVgrWk1YT0FLMEZjV0dRS2lNdVBVZ2dVVWY5ZXdrMTgyWTExbzVVa2h6TStcbkgvZ1Z2ZlR0WTZZeEZ1a1JMSlNTQXd3NDNSQUtPR1JEVzYyTEs0ZkdvU1ptNExSVU90MmR5akpZdFVqZUVrd1VcbnJtVC9yUjdkRzVxTDRPK2E0YVZTVWdDaFhMU0p1enJHSGQ0NE5kMENnWUVBdUNncGVJNVVNeEZ1b3dXMXRwaHpcbkxCMGorVmNNZG10cUlBOW92bkRhK2JLUFg2aGttemlYSXpaM3QzNEZ5T2RFSldUSGFKYlRUMHAwa0RrYzlST3VcblpycVErTWxGVWpJRTc4aHVFYlc1WjQ5U0NBY0xUakdhejNUMWxaQmJkdkFIeGhJZFovak9RUVR6d3hPc2hpYmpcblFWTUptVGRlaG82ODZuWWk1MXRMV2RjPVxuLS0tLS1FTkQgUFJJVkFURSBLRVktLS0tLVxuIiwKICAiY2xpZW50X2VtYWlsIjogInRlcnJlbm9zY2htbEByZWdpc3Ryby1kZS10ZXJyZW5vcy1jaG1sLmlhbS5nc2VydmljZWFjY291bnQuY29tIiwKICAiY2xpZW50X2lkIjogIjExMDg2Njg2MjI4OTYwODc1ODg2NiIsCiAgImF1dGhfdXJpIjogImh0dHBzOi8vYWNjb3VudHMuZ29vZ2xlLmNvbS9vL29hdXRoMi9hdXRoIiwKICAidG9rZW5fdXJpIjogImh0dHBzOi8vb2F1dGgyLmdvb2dsZWFwaXMuY29tL3Rva2VuIiwKICAiYXV0aF9wcm92aWRlcl94NTA5X2NlcnRfdXJsIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL29hdXRoMi92MS9jZXJ0cyIsCiAgImNsaWVudF94NTA5X2NlcnRfdXJsIjogImh0dHBzOi8vd3d3Lmdvb2dsZWFwaXMuY29tL3JvYm90L3YxL21ldGFkYXRhL3g1MDkvdGVycmVub3NjaG1sJTQwcmVnaXN0cm8tZGUtdGVycmVub3MtY2htbC5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsCiAgInVuaXZlcnNlX2RvbWFpbiI6ICJnb29nbGVhcGlzLmNvbSIKfQo=

"""

creds_dict = json.loads(base64.b64decode(credentials_base64))
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(creds)

# Abrir la hoja de cálculo y seleccionar la hoja
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1pJ9rjiED41Zh4sENtTKzi3kfzFkP8LnIcQBJm0Xbt6Y/edit?usp=sharing").sheet1

# Función para generar el PDF
def generate_pdf(name, surname, id_number, total_score, user_data):
    pdf = FPDF()
    pdf.add_page()
    
    # Título
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "Resultado de Evaluación", ln=True, align='C')
    
    # Información Personal
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Nombre: {name}", ln=True)
    pdf.cell(200, 10, f"Apellido: {surname}", ln=True)
    pdf.cell(200, 10, f"Documento de Identidad: {id_number}", ln=True)
    
    # Puntaje Total
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, f"Puntaje Total: {total_score}", ln=True)
    
    # Información de las categorías
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, "Detalles por Categoría:", ln=True)
    for key, value in user_data.items():
        if key not in ["Nombre", "Apellido", "Documento de Identidad", "Puntaje Total"]:
            pdf.cell(200, 10, f"{key}: {value}", ln=True)
    
    # Guardar el PDF
    pdf_output = f"resultado_{name}_{surname}.pdf"
    pdf.output(pdf_output)
    
    return pdf_output

# Título de la Aplicación
st.title("Demanda de Terrenos by José Soto - si funciona la vendo")

# Botones de sesión
if st.button("Abrir Sesión"):
    st.session_state.logged_in = True
    st.success("Sesión abierta. Puedes comenzar a ingresar datos.")

if st.button("Cerrar Sesión"):
    st.session_state.logged_in = False
    st.success("Sesión cerrada.")

# Mostrar un mensaje si no se ha iniciado sesión
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.warning("Por favor, abre una sesión para ingresar datos.")
else:
    # Ingresar Datos Personales
    name = st.text_input("Nombre")
    surname = st.text_input("Apellido")
    id_number = st.text_input("Documento de Identidad")

    # Definir las categorías y sus ítems con puntajes
    criteria = {
        "Antigüedad de la solicitud": {
            "Más de 10 años": 100,
            "Entre 5 y 9 años": 50,
            "Menos 5 años": 30
        },
        "Tipo de vivienda actual": {
            "Local adaptado a vivienda": 25,
            "Vivienda precaria": 50,
            "Casa o dpto.": 15
        },
        "Cantidad de personas que duermen por habitación": {
            "Hasta 2 personas": 30,
            "Hasta 3 personas": 50,
            "4 o más": 100
        },
        "Tenencia de la vivienda": {
            "Propietario de la vivienda o terreno": 0,
            "Alquilada": 50,
            "Cedida": 15,
            "Compartida": 25
        },
        "Ubicación de la vivienda": {
            "Zona inundable": 21,
            "Zona de pendientes bardas o cañadones": 21,
            "Zona Urbana": 7,
            "Sector Basural": 21
        },
        "Grupo Familiar": {
            "Familia monoparental": 25,
            "Menores de 18 años en el hogar": 25,
            "Integrantes de la familia con discapacidad": 50
        },
        "Residencia": {
            "1 punto por cada año o fracción mayor a 6 meses de residencia cuando supere los 10 años": 100,
            "Nativo con residencia permanente": 200
        },
        "Ingresos del/los solicitantes": {
            "Menor o igual a 1 S.M.V.M.": 30,
            "Entre 1 y 3 S.M.V.M.": 50,
            "Entre 3 y 5 S.M.V.M.": 80,
            "Mayor de 6 S.M.V.M.": 100
        },
        "Estabilidad laboral - Relación de dependencia": {
            "Menor a 1 año": 10,
            "Entre 1 y 5 años": 30,
            "Entre 5 y 10 años": 50,
            "Más de 10 años": 100
        },
        "Estabilidad laboral independiente": {
            "Menor a 1 año": 10,
            "Entre 1 y 5 años": 30,
            "Entre 5 y 10 años": 50,
            "Más de 10 años": 100
        },
        "Informe de: Central de Deudores del Sistema Financiero": {
            "0 o 1": 100,
            "2": 50,
            "3 o más": 0
        },
        "Título estudios superiores": {
            "Sí": 25,
            "No": 0
        },
        "Antecedente para ejecución de obra": {
            "Planos": 50,
            "Prepago de vivienda": 100,
            "Nada": 0
        }
    }

    # Inicializar una variable para el puntaje total y un diccionario para guardar las selecciones
    total_score = 0
    user_data = {
        "Nombre": name,
        "Apellido": surname,
        "Documento de Identidad": id_number
    }

    # Crear listas desplegables para cada criterio y capturar las selecciones
    for criterion, options in criteria.items():
        selected_option = st.selectbox(f'{criterion}', options.keys())
        total_score += options[selected_option]
        user_data[criterion] = selected_option

    # Agregar el puntaje total al diccionario
    user_data["Puntaje Total"] = total_score

    # Guardar los datos en la hoja de cálculo
    if st.button("Guardar y agregar a la base de datos"):
        if name and surname and id_number:
            # Convertir el diccionario a una lista ordenada para la hoja de cálculo
            row = [user_data[key] for key in user_data.keys()]
            sheet.append_row(row)
            st.success("Datos guardados exitosamente.")
        else:
            st.error("Por favor, completa todos los campos de datos personales.")

    # Generar PDF y ofrecerlo para descargar
    if st.button("Generar PDF"):
        if name and surname and id_number:
            pdf_file = generate_pdf(name, surname, id_number, total_score, user_data)
            with open(pdf_file, "rb") as file:
                st.download_button(label="Descargar PDF", data=file, file_name=pdf_file, mime="application/pdf")
        else:
            st.error("Por favor, completa todos los campos de datos personales.")
