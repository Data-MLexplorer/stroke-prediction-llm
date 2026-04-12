import streamlit as st
import requests
import anthropic

# ── Config ───────────────────────────────────────────────
FASTAPI_URL = "http://localhost:8000"

# ── CSS ──────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow:wght@400;500;600;700;800;900&family=Barlow+Condensed:wght@700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Barlow', sans-serif;
    background-color: #0f0f0f;
    color: #e8e0d0;
    letter-spacing: 0.01em;
}
.stApp { background-color: #0f0f0f; }

.hero {
    background: linear-gradient(135deg, #1a1410 0%, #2a1f10 40%, #1a1208 100%);
    border-radius: 20px;
    padding: 20px 24px;
    margin-bottom: 28px;
    border: 1px solid #2e2416;
}
.hero h1 {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 48px;
    font-weight: 400;
    line-height: 0.95;
    margin: 0 0 12px 0;
    color: #ffffff;
    letter-spacing: 0.03em;
}
.hero h1 span { color: #f97316; }
.hero p { color: #9a8f80; font-size: 15px; font-weight: 500; margin: 16px 0 0; letter-spacing: 0.02em; }

.card {
    background: #161616;
    border: 1px solid #252525;
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 20px;
}
.card-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 22px;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #ffffff;
    margin-bottom: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.badge { font-size: 10px; font-weight: 700; letter-spacing: 0.12em; padding: 4px 12px; border-radius: 20px; text-transform: uppercase; font-family: 'Barlow', sans-serif; }
.badge-orange { background: #2d1a08; color: #f97316; border: 1px solid #f97316; }
.badge-green  { background: #0a2010; color: #22c55e; border: 1px solid #22c55e; }
.badge-red    { background: #2d0808; color: #ef4444; border: 1px solid #ef4444; }
.badge-amber  { background: #2d2008; color: #f59e0b; border: 1px solid #f59e0b; }

.risk-percent {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 96px;
    font-weight: 400;
    color: #ffffff;
    text-align: center;
    letter-spacing: 0.04em;
    line-height: 1;
}
.risk-sublabel { font-size: 11px; font-weight: 700; letter-spacing: 0.14em; text-transform: uppercase; color: #6b6560; text-align: center; margin-bottom: 16px; }

.gradient-bar { height: 8px; border-radius: 4px; background: linear-gradient(to right, #22c55e, #f59e0b, #ef4444); position: relative; margin: 8px 0 4px; }
.gradient-bar-marker { position: absolute; top: -5px; width: 18px; height: 18px; border-radius: 50%; background: white; border: 2px solid #0f0f0f; transform: translateX(-50%); }
.bar-labels { display: flex; justify-content: space-between; font-size: 11px; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; color: #6b6560; }

.result-row { display: flex; justify-content: space-between; align-items: center; padding: 14px 0; border-bottom: 1px solid #1e1e1e; font-size: 14px; }
.result-row .rlabel { color: #6b6560; font-weight: 600; letter-spacing: 0.04em; text-transform: uppercase; font-size: 11px; }
.result-row .rvalue { font-family: 'Barlow Condensed', sans-serif; font-weight: 800; font-size: 20px; letter-spacing: 0.04em; color: #ffffff; }

.factors-title { font-size: 11px; font-weight: 700; letter-spacing: 0.1em; text-transform: uppercase; color: #6b6560; margin: 20px 0 12px; }
.factor-row { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
.factor-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
.factor-name { font-size: 13px; color: #b0a898; flex: 1; font-weight: 500; }
.factor-bar-bg { width: 90px; height: 5px; border-radius: 999px; background: #252525; }
.factor-bar-fill { height: 5px; border-radius: 999px; }

.info-box { background: #1a1a1a; border: 1px solid #252525; border-radius: 10px; padding: 14px 16px; font-size: 12px; font-weight: 500; letter-spacing: 0.02em; color: #6b6560; margin-top: 16px; }

.chat-messages { max-height: 340px; overflow-y: auto; padding: 4px 0; }
.msg-user { display: flex; justify-content: flex-end; margin-bottom: 12px; }
.msg-user .bubble { background: #f97316; color: #1a0a00; border-radius: 16px 16px 4px 16px; padding: 10px 16px; font-size: 14px; max-width: 75%; }
.msg-ai { display: flex; justify-content: flex-start; margin-bottom: 12px; }
.msg-ai .bubble { background: #1e1e1e; color: #d0c8b8; border-radius: 16px 16px 16px 4px; padding: 10px 16px; font-size: 14px; max-width: 80%; border: 1px solid #2a2a2a; }

.stSelectbox > div > div, .stNumberInput > div > div > input, .stTextInput > div > div > input {
    background-color: #1e1e1e !important;
    border: 1px solid #2a2a2a !important;
    border-radius: 10px !important;
    color: #e8e0d0 !important;
    font-family: 'Barlow', sans-serif !important;
    font-weight: 500 !important;
}
.stSelectbox label, .stNumberInput label {
    color: #6b6560 !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}
.stButton > button {
    background: #f97316; color: #1a0a00; border: none;
    border-radius: 10px;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-weight: 900; font-size: 18px;
    letter-spacing: 0.08em; text-transform: uppercase;
    padding: 12px 0; width: 100%;
}
.stButton > button:hover { background: #ea6c0e; color: #1a0a00; }

div[data-testid="stSidebar"] { background-color: #0d0d0d; border-right: 1px solid #1e1e1e; }
div[data-testid="stSidebar"] * { color: #9a8f80 !important; }
</style>
""", unsafe_allow_html=True)


# ── Session state ────────────────────────────────────────
if "chat_history"  not in st.session_state: st.session_state.chat_history  = []
if "risk_score"    not in st.session_state: st.session_state.risk_score    = 0.0
if "risk_label"    not in st.session_state: st.session_state.risk_label    = "—"
if "patient_info"  not in st.session_state: st.session_state.patient_info  = {}
if "predicted"     not in st.session_state: st.session_state.predicted     = False


# ── Sidebar ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 Stroke Risk AI")
    st.markdown("---")
    api_key = st.text_input("Anthropic API Key", type="password", placeholder="sk-ant-...")
    st.markdown("---")
    backend_url = st.text_input("Backend URL", value=FASTAPI_URL)
    st.markdown("---")
    st.caption("FastAPI handles predictions.\nStreamlit handles the UI.\nClaude API key stays client-side.")


# ── Hero ─────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>Stroke Risk Prediction</span></h1>
    <p>AI-powered stroke risk prediction system. Enter patient data and get instant results.</p>
</div>
""", unsafe_allow_html=True)


# ── Value maps (UI label → API value) ────────────────────
WORK_TYPE_MAP = {
    "Private"       : "Private",
    "Self-employed" : "Self-employed",
    "Govt job"      : "Govt_job",
    "Never worked"  : "Never_worked",
    "Children"      : "children",
}
SMOKING_MAP = {
    "Never smoked"    : "never smoked",
    "Formerly smoked" : "formerly smoked",
    "Smokes"          : "smokes",
    "Unknown"         : "Unknown",       
}


# ── Risk factor scoring (clinical heuristic weights) ─────
def get_risk_factors(info: dict, score: float) -> list:
    """
    Returns list of (label, severity, bar_pct) sorted by severity.
    severity: 'high' | 'medium' | 'low'
    """
    factors = []

    if info.get("hypertension") == "Yes":
        factors.append(("Hypertension",        "high",   92))
    if info.get("heart_disease") == "Yes":
        factors.append(("Heart disease",        "high",   88))
    if info.get("avg_glucose", 0) > 200:
        factors.append(("Very high glucose",    "high",   80))
    elif info.get("avg_glucose", 0) > 140:
        factors.append(("Elevated glucose",     "medium", 58))
    if info.get("bmi", 0) > 40:
        factors.append(("Severe obesity (BMI)", "high",   75))
    elif info.get("bmi", 0) > 30:
        factors.append(("Obesity (BMI)",        "medium", 55))
    if info.get("smoking") == "Smokes":
        factors.append(("Active smoker",        "medium", 62))
    elif info.get("smoking") == "Formerly smoked":
        factors.append(("Former smoker",        "low",    35))
    if info.get("age", 0) >= 65:
        factors.append(("Age ≥ 65",             "high",   70))
    elif info.get("age", 0) >= 50:
        factors.append(("Age 50–64",            "medium", 48))

    # sort: high first
    order = {"high": 0, "medium": 1, "low": 2}
    factors.sort(key=lambda x: order[x[1]])
    return factors[:5]   # top 5 only


def factor_color(severity: str) -> str:
    return {"high": "#ef4444", "medium": "#f59e0b", "low": "#22c55e"}[severity]


# ── Layout ───────────────────────────────────────────────
left, right = st.columns([1.1, 0.9], gap="large")

# ── LEFT: Form ───────────────────────────────────────────
with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>Patient Information <span class='badge badge-orange'>Input Form</span></div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1: gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    with c2: age    = st.number_input("Age", min_value=1, max_value=110, value=37)

    c3, c4 = st.columns(2)
    with c3: hypertension  = st.selectbox("Hypertension",  ["No", "Yes"])
    with c4: heart_disease = st.selectbox("Heart Disease", ["No", "Yes"])

    c5, c6 = st.columns(2)
    with c5: marital   = st.selectbox("Marital Status", ["Single", "Married"])
    with c6: work_type = st.selectbox("Work Type", list(WORK_TYPE_MAP.keys()))

    c7, c8 = st.columns(2)
    with c7: residence   = st.selectbox("Residence Type",       ["Urban", "Rural"])
    with c8: avg_glucose = st.number_input("Avg. Glucose Level", min_value=50.0, max_value=300.0, value=180.0)

    c9, c10 = st.columns(2)
    with c9:  bmi     = st.number_input("BMI", min_value=10.0, max_value=60.0, value=32.0)
    with c10: smoking = st.selectbox("Smoking Status", list(SMOKING_MAP.keys()))

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Predict Stroke Risk"):
        payload = {
            "gender"            : gender,
            "age"               : float(age),
            "hypertension"      : 1 if hypertension == "Yes" else 0,
            "heart_disease"     : 1 if heart_disease == "Yes" else 0,
            "ever_married"      : 1 if marital == "Married" else 0,
            "work_type"         : WORK_TYPE_MAP[work_type],      # ✅ mapped
            "Residence_type"    : residence,
            "avg_glucose_level" : float(avg_glucose),
            "bmi"               : float(bmi),
            "smoking_status"    : SMOKING_MAP[smoking],          # ✅ mapped
        }
        try:
            res = requests.post(f"{backend_url}/predict", json=payload, timeout=10)
            res.raise_for_status()
            data = res.json()
            st.session_state.risk_score   = data["probability"] / 100
            st.session_state.risk_label   = data["label"]
            st.session_state.patient_info = {
                "age": age, "gender": gender,
                "hypertension": hypertension, "heart_disease": heart_disease,
                "avg_glucose": avg_glucose, "bmi": bmi,
                "smoking": smoking, "work_type": work_type,
                "residence": residence, "marital": marital,
            }
            st.session_state.predicted    = True
            st.session_state.chat_history = []
            st.rerun()
        except requests.exceptions.ConnectionError:
            st.error(f"❌ Cannot connect to FastAPI backend at {backend_url}")
        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown("</div>", unsafe_allow_html=True)


# ── RIGHT: Result + Chat ─────────────────────────────────
with right:
    score = st.session_state.risk_score
    label = st.session_state.risk_label
    pct   = int(score * 100)
    info  = st.session_state.patient_info

    badge_cls = {
        "Low Risk"    : "badge-green",
        "Medium Risk" : "badge-amber",
        "High Risk"   : "badge-red",
    }.get(label, "badge-orange")

    # ── Build risk factor rows HTML ───────────────────────
    factors_html = ""
    if st.session_state.predicted and info:
        factors = get_risk_factors(info, score)
        if factors:
            factors_html += "<div class='factors-title'>Contributing risk factors</div>"
            for fname, severity, bar_pct in factors:
                col = factor_color(severity)
                factors_html += f"""
                <div class='factor-row'>
                    <div class='factor-dot' style='background:{col}'></div>
                    <span class='factor-name'>{fname}</span>
                    <div class='factor-bar-bg'>
                        <div class='factor-bar-fill' style='width:{bar_pct}%;background:{col}'></div>
                    </div>
                </div>"""

    # ── Result card ───────────────────────────────────────
    st.markdown(f"""
    <div class='card'>
        <div class='card-title'>Result <span class='badge {badge_cls}'>{label}</span></div>
        <div class='risk-percent'>{pct}%</div>
        <div class='risk-sublabel'>Risk Score</div>
        <div class='gradient-bar'>
            <div class='gradient-bar-marker' style='left:{min(pct, 97)}%'></div>
        </div>
        <div class='bar-labels'><span>Low</span><span>Medium</span><span>High</span></div>
        <div class='result-row'>
            <span class='rlabel'>Risk Status</span>
            <span class='rvalue'>{label.split()[0] if label != "—" else "—"}</span>
        </div>
        <div class='result-row' style='border-bottom:none'>
            <span class='rlabel'>Probability</span>
            <span class='rvalue'>{score:.2f} ({pct}%)</span>
        </div>
        {factors_html}
        <div class='info-box'>
            Model output is a probability estimate. Consult a qualified clinician for medical decisions.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Chat card ─────────────────────────────────────────
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("""
    <div class='card-title'>
        🤖 AI Health Assistant
       
    </div>
    """, unsafe_allow_html=True)

    chat_html = ""
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            chat_html += f"<div class='msg-user'><div class='bubble'>{msg['content']}</div></div>"
        else:
            chat_html += f"<div class='msg-ai'><div class='bubble'>{msg['content']}</div></div>"

    if not chat_html:
        chat_html = "<div style='color:#3a3530;font-size:13px;text-align:center;padding:16px 0'>Ask me anything about this patient's stroke risk...</div>"

    st.markdown(f"<div class='chat-messages'>{chat_html}</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    user_input = st.text_input(
        "Your message",
        placeholder="e.g. What are the main risk factors?",
        label_visibility="collapsed"
    )

    col_send, col_clear = st.columns([3, 1])
    with col_send:  send  = st.button("Send")
    with col_clear: clear = st.button("Clear")

    if send:
        if not api_key:
            st.warning("Enter your OPEN API key in the sidebar.")
        elif not user_input.strip():
            st.warning("Type a message first.")
        else:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            try:
                # ── Build system prompt with patient context ──────────
                patient_ctx = ""
                if info:
                    factors = get_risk_factors(info, score)
                    factor_list = ", ".join(f[0] for f in factors) or "none identified"
                    patient_ctx = f"""
Current patient:
- Age: {info.get('age')}, Gender: {info.get('gender')}
- Hypertension: {info.get('hypertension')}, Heart disease: {info.get('heart_disease')}
- Avg glucose: {info.get('avg_glucose')}, BMI: {info.get('bmi')}
- Smoking: {info.get('smoking')}, Work type: {info.get('work_type')}
- Residence: {info.get('residence')}, Marital: {info.get('marital')}
- Stroke risk score: {pct}% ({label})
- Top risk factors: {factor_list}
"""

                system_prompt = f"""You are a clinical AI assistant helping interpret stroke risk predictions.
Be concise, factual, and always remind the user to consult a real clinician for medical decisions.
{patient_ctx}"""

                # ── Call Claude API directly (no backend needed) ──────
                # client = anthropic.Anthropic(api_key=api_key)
                # response = client.messages.create(
                #     model="claude-sonnet-4-20250514",
                #     max_tokens=512,
                #     system=system_prompt,
                #     messages=st.session_state.chat_history,
                # )
                # reply = response.content[0].text
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4o",
                    max_tokens=512,
                    messages=[{"role": "system", "content": system_prompt}] + st.session_state.chat_history,
                )
                reply = response.choices[0].message.content
                st.session_state.chat_history.append({"role": "assistant", "content": reply})

            # except anthropic.AuthenticationError:
            #     st.session_state.chat_history.append({
            #         "role": "assistant",
            #         "content": "⚠️ Invalid API key. Check your Anthropic API key in the sidebar."
            #     })
            except Exception as e:
                if "auth" in str(e).lower() or "api key" in str(e).lower():
                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": "⚠️ Invalid API key. Check your OpenAI API key in the sidebar."
                    })
            except Exception as e:
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"⚠️ Error: {str(e)}"
                })
            st.rerun()

    if clear:
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)