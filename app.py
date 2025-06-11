import streamlit as st

# ---- Adicione o caminho da sua logo aqui ----
st.markdown(
    """
    <div style='display: flex; justify-content: center; align-items: center;'>
        <img src='https://i.imgur.com/RWobbXK.jpeg' width='180' style='margin-bottom: 10px;'/>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    "<h2 style='text-align: center; color: #2C3E50;'>Simulador de Autonomia para Modelos Smartway</h2>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; font-size: 0.9em; color: #7F8C8D;'>Este simulador fornece apenas uma estimativa. A autonomia pode variar conforme o uso, os cuidados do usuário e as condições específicas.</p>",
    unsafe_allow_html=True,
)

# --------- DADOS DOS MODELOS ---------
modelos = {
    "Smartway Family 500W": {"vel_max": 32, "potencia": 500, "peso_max": 250, "bateria": "48V 15Ah", "autonomia": 30, "aro": 8, "peso_bruto": 77, "bateria_removivel": "Não", "tipo": "triciclo"},
    "Smartway Evolution 1000W": {"vel_max": 32, "potencia": 1000, "peso_max": 250, "bateria": "60V 15Ah", "autonomia": 30, "aro": 10, "peso_bruto": 89, "bateria_removivel": "Não", "tipo": "triciclo"},
    "Smartway Route 350W": {"vel_max": 32, "potencia": 350, "peso_max": 120, "bateria": "48V 15Ah", "autonomia": 30, "aro": 14, "peso_bruto": 50, "bateria_removivel": "Sim", "tipo": "duas rodas"},
    "Smartway Austin 1000W": {"vel_max": 32, "potencia": 1000, "peso_max": 160, "bateria": "60V 15Ah", "autonomia": 30, "aro": 8, "peso_bruto": 62, "bateria_removivel": "Não", "tipo": "duas rodas"},
    "Smartway Confort 500W": {"vel_max": 32, "potencia": 500, "peso_max": 120, "bateria": "48V 15Ah", "autonomia": 30, "aro": 14, "peso_bruto": 50, "bateria_removivel": "Não", "tipo": "duas rodas"},
    "Smartway City 350W": {"vel_max": 32, "potencia": 350, "peso_max": 120, "bateria": "48V 15Ah", "autonomia": 30, "aro": 14, "peso_bruto": 50, "bateria_removivel": "Não", "tipo": "duas rodas"},
    "Smartway Evomax 1000W": {"vel_max": 32, "potencia": 1000, "peso_max": 250, "bateria": "60V 15Ah", "autonomia": 30, "aro": 10, "peso_bruto": 50, "bateria_removivel": "Não", "tipo": "duas rodas"},
    "Smartway Power 600W": {"vel_max": 32, "potencia": 600, "peso_max": 250, "bateria": "48V 15Ah", "autonomia": 30, "aro": 8, "peso_bruto": 77, "bateria_removivel": "Não", "tipo": "triciclo"},
    "Smartway Save 350W": {"vel_max": 32, "potencia": 350, "peso_max": 120, "bateria": "48V 15Ah", "autonomia": 30, "aro": 14, "peso_bruto": 50, "bateria_removivel": "Não", "tipo": "duas rodas"},
    "Smartway Route 500W": {"vel_max": 32, "potencia": 500, "peso_max": 120, "bateria": "48V 15Ah", "autonomia": 30, "aro": 14, "peso_bruto": 50, "bateria_removivel": "Sim", "tipo": "duas rodas"},
    "Smartway Wasp 800W": {"vel_max": 25, "potencia": 800, "peso_max": 150, "bateria": "48V 15Ah", "autonomia": 30, "aro": 10, "peso_bruto": 50, "bateria_removivel": "Não", "tipo": "duas rodas"},
    "Smartway Turbo 1000W": {"vel_max": 32, "potencia": 1000, "peso_max": 120, "bateria": "48V 15Ah", "autonomia": 30, "aro": 14, "peso_bruto": 50, "bateria_removivel": "Não", "tipo": "duas rodas"},
    "Smartway Turbo 500W": {"vel_max": 32, "potencia": 500, "peso_max": 120, "bateria": "48V 15Ah", "autonomia": 30, "aro": 14, "peso_bruto": 50, "bateria_removivel": "Não", "tipo": "duas rodas"},
    "Smartway Ultra 1000W": {"vel_max": 32, "potencia": 1000, "peso_max": 250, "bateria": "48V 15Ah", "autonomia": 30, "aro": 8, "peso_bruto": 77, "bateria_removivel": "Não", "tipo": "triciclo"}
}

def calcular_capacidade_bateria(bateria_str):
    try:
        voltage_str, capacity_str = bateria_str.split()
        voltage = float(voltage_str.replace("V", ""))
        capacity = float(capacity_str.replace("Ah", ""))
        return voltage * capacity
    except:
        return 720

def calcular_autonomia(modelo, peso_usuario, velocidade_media, terreno, carga_adicional):
    declared_autonomy = modelos[modelo]["autonomia"]
    vehicle_weight = modelos[modelo]["peso_bruto"]
    motor_power = modelos[modelo]["potencia"]
    wheel_size = modelos[modelo]["aro"]
    battery_capacity_wh = calcular_capacidade_bateria(modelos[modelo]["bateria"])
    base_consumption = battery_capacity_wh / declared_autonomy
    standard_total_weight = vehicle_weight + 80
    total_weight = vehicle_weight + peso_usuario + carga_adicional
    weight_factor = total_weight / standard_total_weight if standard_total_weight > 0 else 1
    terrain_factor = 1
    if terreno == "moderado":
        terrain_factor = 1.1
    elif terreno == "morro":
        terrain_factor = 1.25
    speed_factor = 1.1 if velocidade_media > 25 else 1
    power_factor = 1 + (motor_power - 350) / 350 * 0.1 if motor_power > 350 else 1
    wheel_factor = 1.1 if wheel_size < 10 else 1
    adjusted_consumption = base_consumption * weight_factor * terrain_factor * speed_factor * power_factor * wheel_factor
    autonomy = battery_capacity_wh / adjusted_consumption if adjusted_consumption > 0 else declared_autonomy
    return round(autonomy, 1)

# --- Caixas/inputs em colunas para responsividade ---
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h4>Informe seus dados</h4>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    peso_usuario = st.number_input("Peso corporal (kg)", 0, 300, 80)
    terreno = st.selectbox("Tipo de terreno", ["plano", "moderado", "morro"])
with col2:
    velocidade_media = st.number_input("Velocidade média (km/h)", 0, 32, 20)
    carga_adicional = st.number_input("Carga adicional (kg)", 0, 100, 0)

st.markdown("<h4>Escolha o modelo</h4>", unsafe_allow_html=True)
modelo_selecionado = st.selectbox("Modelo", list(modelos.keys()))

st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
simular = st.button("🚀 Gerar Simulação")

if simular:
    autonomia = calcular_autonomia(modelo_selecionado, peso_usuario, velocidade_media, terreno, carga_adicional)
    bateria_capacidade = calcular_capacidade_bateria(modelos[modelo_selecionado]["bateria"])
    st.session_state['resultados'] = {
        "modelo": modelo_selecionado,
        "autonomia": autonomia,
        "vel_max": modelos[modelo_selecionado]['vel_max'],
        "potencia": modelos[modelo_selecionado]['potencia'],
        "peso_bruto": modelos[modelo_selecionado]['peso_bruto'],
        "peso_max": modelos[modelo_selecionado]['peso_max'],
        "bateria": modelos[modelo_selecionado]['bateria'],
        "aro": modelos[modelo_selecionado]['aro'],
        "autonomia_base": modelos[modelo_selecionado]['autonomia'],
        "bateria_removivel": modelos[modelo_selecionado]['bateria_removivel'],
        "bateria_capacidade": bateria_capacidade
    }

if 'resultados' in st.session_state:
    r = st.session_state['resultados']
    st.markdown(
        f"""
        <div style='background-color: #F6F9FB; border-radius: 18px; padding: 18px; margin-top: 12px;'>
            <h5 style='color: #2C3E50;'>Resultados para <b>{r['modelo']}</b></h5>
            <ul>
                <li><b>Autonomia estimada:</b> {r['autonomia']} km</li>
                <li><b>Velocidade máxima:</b> {r['vel_max']} km/h</li>
                <li><b>Potência:</b> {r['potencia']} W</li>
                <li><b>Peso bruto:</b> {r['peso_bruto']} kg</li>
                <li><b>Peso máximo:</b> {r['peso_max']} kg</li>
                <li><b>Bateria:</b> {r['bateria']} ({r['bateria_capacidade']} Wh)</li>
                <li><b>Tamanho das rodas:</b> {r['aro']}''</li>
                <li><b>Bateria removível:</b> {r['bateria_removivel']}</li>
            </ul>
            <div style='margin-top: 8px; color:#626B7B; font-size: 15px;'>
                <b>Tempo de recarga:</b> média de 6 horas<br>
                <b>Vida útil da bateria:</b> média de 500 ciclos<br>
                <b>Garantia/Assistência:</b> Disponível pela Smartway
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    comparar = st.checkbox("Comparar com outros modelos")
    if comparar:
        modelos_comparar = st.multiselect("Selecione modelos", list(modelos.keys()))
        if modelos_comparar:
            st.markdown("<h6>Comparação de autonomia estimada:</h6>", unsafe_allow_html=True)
            for m in modelos_comparar:
                aut = calcular_autonomia(m, peso_usuario, velocidade_media, terreno, carga_adicional)
                st.markdown(f"<b>{m}:</b> {aut} km", unsafe_allow_html=True)

# Rodapé discreto para mobile
st.markdown(
    "<div style='text-align:center; font-size:13px; color:#9AA6B2; margin-top:40px;'>Smartway Motors © 2025</div>",
    unsafe_allow_html=True,
)
