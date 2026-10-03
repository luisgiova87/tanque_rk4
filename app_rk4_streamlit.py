import streamlit as st
import random
import math

st.set_page_config(page_title="Tutor RK4 - Vaciado de Tanque", page_icon="💧", layout="centered")

st.title("💧 Tutor Interactivo RK4 - Ingeniería Civil")
st.markdown("### Simulación y Aprendizaje del Método de Runge-Kutta de Orden 4 (Vaciado de Tanque)")

# Inicializar el estado de la sesión para mantener los datos entre interacciones de Streamlit
if "initialized" not in st.session_state:
    st.session_state.h0 = round(random.uniform(1.5, 2.5), 2)
    st.session_state.k = round(random.uniform(1.1, 1.4), 2)
    st.session_state.dt = 1.0
    st.session_state.curr_h = st.session_state.h0
    st.session_state.curr_t = 0.0
    st.session_state.iteracion = 1
    st.session_state.logs = []
    st.session_state.completed = False
    st.session_state.initialized = True

def reiniciar_simulacion():
    st.session_state.h0 = round(random.uniform(1.5, 2.5), 2)
    st.session_state.k = round(random.uniform(1.1, 1.4), 2)
    st.session_state.curr_h = st.session_state.h0
    st.session_state.curr_t = 0.0
    st.session_state.iteracion = 1
    st.session_state.logs = []
    st.session_state.completed = False

# Botón para reiniciar
if st.button("🔄 Reiniciar con Nuevos Valores"):
    reiniciar_simulacion()
    st.rerun()

# Mostrar parámetros del problema utilizando sintaxis completamente segura sin f-string para evitar errores de escape
st.info(
    "**Parámetros del Problema (Ley de Torricelli):**\n"
    "* **Altura Inicial ($h_0$):** {} m\n".format(st.session_state.h0) +
    "* **Coeficiente de descarga ($k$):** {}\n".format(st.session_state.k) +
    "* **Tamaño de paso ($\Delta t$):** {} s\n".format(st.session_state.dt) +
    "* **Ecuación Diferencial:** $\\frac{dh}{dt} = -k \\sqrt{h}$"
)

# Mostrar estado actual
if st.session_state.curr_h > 0.001 and not st.session_state.completed:
    st.warning("📌 **Iteración {}** | Tiempo actual ($t$) = **{:.2f} s** | Nivel de agua actual ($h$) = **{:.4f} m**".format(
        st.session_state.iteracion, st.session_state.curr_t, st.session_state.curr_h
    ))
    
    # Calcular valores reales de k para el paso actual
    h_curr = st.session_state.curr_h
    k_val = st.session_state.k
    dt_val = st.session_state.dt
    
    k1_real = -k_val * math.sqrt(max(0.0, h_curr))
    k2_real = -k_val * math.sqrt(max(0.0, h_curr + 0.5 * dt_val * k1_real))
    k3_real = -k_val * math.sqrt(max(0.0, h_curr + 0.5 * dt_val * k2_real))
    k4_real = -k_val * math.sqrt(max(0.0, h_curr + dt_val * k3_real))
    
    reales = {'k1': k1_real, 'k2': k2_real, 'k3': k3_real, 'k4': k4_real}

    with st.form(key="form_iter_{}".format(st.session_state.iteracion)):
        st.markdown("#### Calcula e ingresa los coeficientes $k$ del método RK4:")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            u_k1 = st.number_input("k1", value=0.0, format="%.4f")
        with col2:
            u_k2 = st.number_input("k2", value=0.0, format="%.4f")
        with col3:
            u_k3 = st.number_input("k3", value=0.0, format="%.4f")
        with col4:
            u_k4 = st.number_input("k4", value=0.0, format="%.4f")
            
        submit_button = st.form_submit_button(label="Verificar y Avanzar Paso")
        
        if submit_button:
            iter_logs = ["--- Resultados Iteración {} (t = {:.2f}s) ---".format(st.session_state.iteracion, st.session_state.curr_t)]
            user_vals = {'k1': u_k1, 'k2': u_k2, 'k3': u_k3, 'k4': u_k4}
            
            for name, r_val in reales.items():
                u_val = user_vals[name]
                if abs(u_val - r_val) < 0.2:
                    iter_logs.append("  {}: ¡Correcto! (Ingresado: {}, Real: {:.4f})".format(name, u_val, r_val))
                else:
                    iter_logs.append("  {}: Incorrecto. (Ingresado: {}, Valor exacto: {:.4f})".format(name, u_val, r_val))
            
            # Actualizar RK4
            delta_h = (dt_val / 6.0) * (k1_real + 2*k2_real + 2*k3_real + k4_real)
            st.session_state.curr_h = max(0.0, st.session_state.curr_h + delta_h)
            st.session_state.curr_t += dt_val
            st.session_state.iteracion += 1
            
            iter_logs.append(" >> Nuevo nivel de agua calculado: {:.4f} m\n".format(st.session_state.curr_h))
            
            for lg in iter_logs:
                st.session_state.logs.append(lg)
                
            if st.session_state.curr_h <= 0.001:
                st.session_state.completed = True
                st.session_state.logs.append("==========================================")
                st.session_state.logs.append(" ¡FELICIDADES! El tanque se ha vaciado por completo.")
                st.session_state.logs.append("==========================================")
            
            st.rerun()

else:
    st.success("🎉 ¡El tanque se ha vaciado por completo exitosamente!")
    st.balloons()

# Historial y retroalimentación didáctica
st.markdown("### 📜 Historial y Retroalimentación Didáctica")
log_text = "\n".join(st.session_state.logs)
st.text_area("Consola de Resultados:", value=log_text, height=250)
