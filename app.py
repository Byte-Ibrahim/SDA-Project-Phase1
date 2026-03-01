import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

class StreamlitDashboard:
    
    def write(self, records: list) -> None:
        st.set_page_config(page_title="GDP Global Analytics", layout="wide")
        st.title("GDP Data Analysis Dashboard")
        st.markdown("### Phase 2: Modular Orchestration & Dependency Inversion")
        
        df = pd.DataFrame(records)

        # Layout Columns
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Key Metrics")
            st.dataframe(df.head(10), use_container_width=True)

        with col2:
            st.subheader("GDP Trends")
            if 'gdp' in df.columns and 'year' in df.columns:
                st.line_chart(data=df, x='year', y='gdp')

        st.success("Analysis Complete. Data injected via Core Transformation Engine.")