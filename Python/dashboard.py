import streamlit as st
import joblib
import time

# Page config must be the first Streamlit command
st.set_page_config(page_title="AI Smart Home", page_icon="⚡", layout="wide")

# Custom CSS for Electronic Blue Theme with Animations
st.markdown("""
<style>
/* Main Background */
.stApp {
    background-color: #050a14;
    background-image: 
        radial-gradient(circle at 15% 50%, rgba(0, 153, 255, 0.15), transparent 25%),
        radial-gradient(circle at 85% 30%, rgba(0, 229, 255, 0.15), transparent 25%);
    color: #e0f2fe;
    font-family: 'Courier New', Courier, monospace;
}

/* Headings */
h1, h2, h3 {
    color: #00e5ff !important;
    text-shadow: 0 0 10px rgba(0, 229, 255, 0.7), 0 0 20px rgba(0, 229, 255, 0.5);
    animation: glow 1.5s ease-in-out infinite alternate;
}

@keyframes glow {
    from { text-shadow: 0 0 5px rgba(0, 229, 255, 0.5), 0 0 10px rgba(0, 229, 255, 0.3); }
    to { text-shadow: 0 0 15px rgba(0, 229, 255, 0.9), 0 0 25px rgba(0, 229, 255, 0.7); }
}

/* Glassmorphism Containers */
div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlock"] {
    background: rgba(0, 25, 50, 0.6);
    border: 1px solid rgba(0, 229, 255, 0.3);
    box-shadow: 0 4px 30px rgba(0, 229, 255, 0.1);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 15px;
    padding: 20px;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlock"]:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 40px rgba(0, 229, 255, 0.2);
    border: 1px solid rgba(0, 229, 255, 0.6);
}

/* Buttons */
.stButton > button {
    background-color: transparent;
    color: #00e5ff;
    border: 2px solid #00e5ff;
    border-radius: 8px;
    padding: 10px 24px;
    font-size: 18px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 2px;
    transition: all 0.3s ease;
    box-shadow: 0 0 10px rgba(0, 229, 255, 0.2);
    width: 100%;
}

.stButton > button:hover {
    background-color: #00e5ff !important;
    color: #050a14 !important;
    box-shadow: 0 0 20px #00e5ff, 0 0 40px #00e5ff;
    transform: scale(1.02);
}



hr {
    border-color: rgba(0, 229, 255, 0.3);
}

/* Base text */
p {
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# Load trained models
@st.cache_resource
def load_models():
    try:
        fan_model = joblib.load("../model/fan_model.pkl")
        light_model = joblib.load("../model/light_model.pkl")
        alarm_model = joblib.load("../model/alarm_model.pkl")
        return fan_model, light_model, alarm_model
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return None, None, None

fan_model, light_model, alarm_model = load_models()

st.markdown("<h1 style='text-align: center; margin-bottom: 20px;'>⚡ AI Smart Home Central Command</h1>", unsafe_allow_html=True)
st.markdown("---")

# Layout
col1, space, col2 = st.columns([1, 0.1, 1])

with col1:
    st.markdown("### 🎛️ Sensor Inputs")
    st.write("Adjust environmental parameters to simulate data:")
    temperature = st.slider("🌡 Temperature (°C)", 0.0, 50.0, 25.0)
    light = st.slider("💡 Light Sensor (Lux)", 0, 1023, 500)
    motion = st.selectbox("🚶 Motion Detected", [0, 1], format_func=lambda x: "Yes (1)" if x == 1 else "No (0)")
    
    st.markdown("<br>", unsafe_allow_html=True)
    predict_btn = st.button("🚀 EXECUTE PREDICTION")

with col2:
    st.markdown("### 🤖 System State")
    if predict_btn:
        if fan_model and light_model and alarm_model:
            with st.spinner("Analyzing neural pathways..."):
                time.sleep(0.8) # Artificial delay for visual effect
                
                # Perform prediction
                data = [[temperature, light, motion]]
                
                fan = fan_model.predict(data)[0]
                room_light = light_model.predict(data)[0]
                alarm = alarm_model.predict(data)[0]
                
                # Custom HTML for result cards
                def get_status_html(title, status, icon):
                    color = "#00e5ff" if status == "ON" else "#334155"
                    glow = "0 0 15px #00e5ff" if status == "ON" else "none"
                    return f"""
                    <div style='text-align: center; border: 1px solid {color}; padding: 15px; border-radius: 10px; box-shadow: {glow}; background: rgba(0,0,0,0.3); transition: 0.3s;'>
                        <h4 style='margin:0; color: #94a3b8;'>{icon} {title}</h4>
                        <h2 style='margin:10px 0 0 0; color: {color}; text-shadow: {glow};'>{status}</h2>
                    </div>
                    """
                
                st.markdown("<br>", unsafe_allow_html=True)
                r_col1, r_col2, r_col3 = st.columns(3)
                
                with r_col1:
                    st.markdown(get_status_html("Fan", "ON" if fan else "OFF", "💨"), unsafe_allow_html=True)
                with r_col2:
                    st.markdown(get_status_html("Light", "ON" if room_light else "OFF", "💡"), unsafe_allow_html=True)
                with r_col3:
                    st.markdown(get_status_html("Alarm", "ON" if alarm else "OFF", "🚨"), unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.success("✅ Analysis Complete. Subsystems synchronized.")
        else:
            st.warning("Models are not loaded. Please ensure models exist in the 'model' directory.")
    else:
        st.info("Awaiting sensor input to compute subsystem states...")

st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: #00e5ff; opacity: 0.6; letter-spacing: 2px;'>SECURE CONNECTION ESTABLISHED • ENCRYPTION PROTOCOL ACTIVE</p>", unsafe_allow_html=True)