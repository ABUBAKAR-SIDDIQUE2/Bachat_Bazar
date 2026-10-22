import streamlit as st
from PIL import Image
from ai_helper import analyze_bill_and_plan

st.set_page_config(page_title="BachatBazaar - AI Bill Optimizer", page_icon="⚡", layout="wide")

st.title("⚡ BachatBazaar: Smart HESCO Bill & Slab Optimizer")
st.write("Upload your electricity bill or enter your meter units to avoid expensive tariff slab jumps!")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Your Bill / Meter Info")
    uploaded_file = st.file_uploader("Upload HESCO/WAPDA Bill Photo (Optional)", type=["jpg", "jpeg", "png"])
    image = Image.open(uploaded_file) if uploaded_file else None
    if image:
        st.image(image, caption="Uploaded Bill", width=300)

    current_reading = st.number_input("Or Enter Current Units Used This Month:", min_value=10, max_value=2000, value=185)
    days_left = st.slider("Days Left in Billing Month:", 1, 30, 6)
    appliances = st.multiselect(
        "Select Your Active Appliances:",
        ["1.5 Ton Inverter AC", "Water Motor Pump", "Electric Iron", "Refrigerator", "Ceiling Fans", "Washing Machine"],
        default=["1.5 Ton Inverter AC", "Water Motor Pump", "Electric Iron", "Refrigerator"]
    )
    language = st.radio("Explanation Language:", ["English", "Roman Urdu", "Urdu"], horizontal=True)
    analyze_btn = st.button("🚀 Generate AI Savings Plan", type="primary", use_container_width=True)

with col2:
    st.subheader("2. AI Slab Risk & Daily Survival Plan")
    if analyze_btn:
        with st.spinner("Analyzing tariff slabs and optimizing appliances..."):
            data = analyze_bill_and_plan(image, current_reading, days_left, appliances, language)

            # Visual Slab Progress Bar
            limit = max(data["next_slab_limit"], 1)
            progress = min(data["units_consumed"] / limit, 1.0)
            st.metric("Current Status", data["current_slab_status"], f"{data['units_consumed']} / {limit} Units")
            st.progress(progress)

            # Cost Comparison
            c1, c2 = st.columns(2)
            c1.success(f"Stay in Slab: ~Rs. {data['estimated_bill_now_pkr']:,}")
            c2.error(f"If Slab Crossed: ~Rs. {data['estimated_bill_if_slab_crossed_pkr']:,}")

            st.info(data["bill_explanation"])

            st.markdown("### 📅 Your Custom Appliance Schedule")
            for item in data["daily_schedule"]:
                st.markdown(f"**🔌 {item['appliance']}** — *Save ~Rs. {item['estimated_savings_pkr']}/mo*  \n{item['advice']}")
