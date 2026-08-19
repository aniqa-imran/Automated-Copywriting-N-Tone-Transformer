import os
import asyncio
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from engine import run_batch_pipeline
from schemas import CopywritingOutput

st.set_page_config(page_title="Copywriting & Tone Engine", page_icon="⚡", layout="wide")

# Custom CSS Styling
st.markdown("""
<style>
    .stApp { background-color: #0B0E14; color: #E2E8F0; }
    .main-header { background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); padding: 1.5rem; border-radius: 12px; border: 1px solid #334155; margin-bottom: 1.5rem; }
    .result-box { background: #1E293B; padding: 1.25rem; border-radius: 10px; border: 1px solid #334155; margin-bottom: 1rem; }
    .stButton>button { background: linear-gradient(90deg, #2563EB 0%, #3B82F6 100%); color: white; border: none; font-weight: 600; width: 100%; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h2 style='margin:0;'>⚡ Automated Copywriting & Tone Transformer</h2>
    <p style='color:#94A3B8; margin-top:5px;'>Dual Pipeline Content Generation Framework</p>
</div>
""", unsafe_allow_html=True)

# Helper function to execute async tasks safely in Streamlit
def run_async(coro):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

with st.sidebar:
    selected_mode = option_menu(None, ["Single Generation", "Bulk Batch Processing"], icons=["lightning", "table"], default_index=0)
    st.markdown("---")
    temp_val = st.slider("Temperature", 0.0, 1.0, 0.7, 0.05)
    max_tokens_val = st.slider("Max Output Tokens", 500, 3000, 1500)
    concurrency_limit = st.slider("Semaphore Gate Limit", 1, 10, 3)

if selected_mode == "Single Generation":
    col1, col2 = st.columns(2, gap="large")
    with col1:
        prod_name = st.text_input("Product Name", value="", placeholder="Enter product name (e.g., Wireless Earbuds)")
        platform_choice = st.selectbox("Platform", ["LinkedIn", "Instagram", "Email", "Twitter"])
        tone_choice = st.selectbox("Tone", ["Professional", "Witty & Casual", "Urgent", "Technical"])
        raw_desc = st.text_area("Product Description", value="", placeholder="Enter product features and details here...", height=120)
        run_btn = st.button("Generate Copy")

    with col2:
        if run_btn:
            if not prod_name.strip() or not raw_desc.strip():
                st.warning("Please enter both Product Name and Description before generating!")
            else:
                with st.spinner("Processing through Async Engine & Pydantic Validator..."):
                    payload = [{"product_name": prod_name, "description": raw_desc, "platform": platform_choice, "tone": tone_choice}]
                    results = run_async(run_batch_pipeline(payload, max_concurrency=1, temperature=temp_val, max_tokens=max_tokens_val))
                    res = results[0]
                    
                    if isinstance(res, CopywritingOutput):
                        st.subheader("📌 Headline")
                        st.write(res.headline)
                        st.subheader("📝 Content Body")
                        st.write(res.body_text)
                        st.subheader("🎯 Call To Action")
                        st.info(res.call_to_action)
                        st.subheader("🏷️ Hashtags")
                        st.write(" ".join(res.hashtags))
                    else:
                        st.error(f"Error: {res}")

elif selected_mode == "Bulk Batch Processing":
    st.subheader("Batch CSV Pipeline")
    uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head(), use_container_width=True)
        if st.button("Run Bulk Engine"):
            items = df.to_dict(orient="records")
            
            with st.spinner("Processing batch jobs asynchronously..."):
                results = run_async(run_batch_pipeline(items, max_concurrency=concurrency_limit, temperature=temp_val, max_tokens=max_tokens_val))
            
            headlines = []
            bodies = []
            
            for r in results:
                if isinstance(r, CopywritingOutput):
                    headlines.append(r.headline)
                    bodies.append(r.body_text)
                else:
                    headlines.append("Error Generating Content")
                    bodies.append(str(r))
            
            df["generated_headline"] = headlines
            df["generated_body"] = bodies
            
            st.success("Batch Processing Completed!")
            st.dataframe(df, use_container_width=True)
