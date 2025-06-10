import streamlit as st

# Dados dos modelos
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

# Função para calcular capacidade da bateria em Wh
def calcular_capacidade_bateria(bateria_str):
    try:
        voltage_str, capacity_str = bateria_str.split()
        voltage = float(voltage_str.replace("V", ""))
        capacity = float(capacity_str.replace("Ah", ""))
        return voltage * capacity
    except:
        return 720  # Valor padrão caso o parsing falhe

# Função para calcular autonomia ajustada
def calcular_autonomia(modelo, peso_usuario, velocidade_media, terreno, carga_adicional):
    declared_autonomy = modelos[modelo]["autonomia"]  # 30 km
    vehicle_weight = modelos[modelo]["peso_bruto"]
    motor_power = modelos[modelo]["potencia"]
    wheel_size = modelos[modelo]["aro"]
    battery_capacity_wh = calcular_capacidade_bateria(modelos[modelo]["bateria"])
    
    # Taxa de consumo base (Wh/km) com base na autonomia declarada
    base_consumption = battery_capacity_wh / declared_autonomy
    
    # Peso total
    standard_total_weight = vehicle_weight + 80
    total_weight = vehicle_weight + peso_usuario + carga_adicional
    weight_factor = total_weight / standard_total_weight if standard_total_weight > 0 else 1
    
    # Fator de terreno
    terrain_factor = 1
    if terreno == "moderado":
        terrain_factor = 1.1
    elif terreno == "morro":
        terrain_factor = 1.25
    
    # Fator de velocidade
    speed_factor = 1.1 if velocidade_media > 25 else 1
    
    # Fator de potência do motor (motores mais potentes consomem mais)
    power_factor = 1 + (motor_power - 350) / 350 * 0.1 if motor_power > 350 else 1
    
    # Fator de tamanho da roda (rodas menores aumentam consumo)
    wheel_factor = 1.1 if wheel_size < 10 else 1
    
    # Taxa de consumo ajustada
    adjusted_consumption = base_consumption * weight_factor * terrain_factor * speed_factor * power_factor * wheel_factor
    
    # Autonomia ajustada
    autonomy = battery_capacity_wh / adjusted_consumption if adjusted_consumption > 0 else declared_autonomy
    return round(autonomy, 1)

# Interface Streamlit
st.title("Simulador de Autonomia - Smartway Scooters")

# Inputs do usuário
st.header("Dados do Usuário")
peso_usuario = st.number_input("Peso corporal (kg)", min_value=0, max_value=300, value=80)
velocidade_media = st.number_input("Velocidade média desejada (km/h)", min_value=0, max_value=32, value=20)
terreno = st.selectbox("Tipo de terreno", ["plano", "moderado", "morro"])
carga_adicional = st.number_input("Peso de objetos/passageiros adicionais (kg)", min_value=0, max_value=100, value=0)

# Seleção de modelo
st.header("Selecione o Modelo")
modelo_selecionado = st.selectbox("Escolha um modelo", list(modelos.keys()))

# Botão para gerar simulação
if st.button("Gerar Simulação"):
    autonomia = calcular_autonomia(modelo_selecionado, peso_usuario, velocidade_media, terreno, carga_adicional)
    
    # Armazenar resultados no session_state com bateria_capacidade
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

# Exibir resultados se existirem no session_state
if 'resultados' in st.session_state:
    resultados = st.session_state['resultados']
    st.header("Resultados")
    st.write(f"**Modelo:** {resultados['modelo']}")
    st.write(f"**Autonomia estimada:** média de {resultados['autonomia']} km")
    st.write(f"**Especificações:**")
    st.write(f"- Velocidade máxima: {resultados['vel_max']} km/h")
    st.write(f"- Potência: {resultados['potencia']} W")
    st.write(f"- Peso bruto: {resultados['peso_bruto']} kg")
    st.write(f"- Peso máximo suportado: {resultados['peso_max']} kg")
    st.write(f"- Bateria: {resultados['bateria']} ({resultados['bateria_capacidade']} Wh)")
    st.write(f"- Tamanho das rodas: {resultados['aro']} polegadas")
    st.write(f"- Autonomia declarada: média de {resultados['autonomia_base']} km")

    st.header("Vantagens do Modelo")
    st.write(f"- **Bateria removível:** {resultados['bateria_removivel']}")
    st.write(f"- **Tempo de recarga:** média de 6 horas")
    st.write(f"- **Vida útil da bateria:** média de 500 ciclos")
    st.write("- **Garantia/Assistência:** Disponível pela Smartway (consulte o fabricante)")

    comparar = st.checkbox("Comparar com outros modelos")
    if comparar:
        modelos_comparar = st.multiselect("Selecione modelos para comparar", list(modelos.keys()))
        if modelos_comparar:
            st.write("**Comparação de Autonomia Estimada:**")
            for m in modelos_comparar:
                aut = calcular_autonomia(m, peso_usuario, velocidade_media, terreno, carga_adicional)
                st.write(f"- **{m}:** média de {aut} km")

if __name__ == "__main__":
    pass
