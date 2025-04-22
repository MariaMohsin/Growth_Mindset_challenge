

import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="🗂️File Converter & Cleaner", layout="wide")
st.title("📁File Converter & Cleaner")
st.write("Upload your CSV and Excel Files to clean the data and convert formats effortlessly.🚀")

files = st.file_uploader("Upload CSV or Excel Files", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.subheader(f"🔍 {file.name} - Preview")
        st.dataframe(df.head())

        if st.checkbox(f"Fill Missing Values - {file.name}"):
            df.fillna(df.select_dtypes(include="number").mean(), inplace=True)
            st.success("✅ Missing values filled successfully!")
            st.dataframe(df.head())

            selected_columns = st.multiselect(f"Select Columns - {file.name}", df.columns, default=df.columns)
            if selected_columns:
                df = df[selected_columns]
                st.dataframe(df.head())

                if st.checkbox(f"📊 Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
                    numeric_data = df.select_dtypes(include="number")
                    st.bar_chart(numeric_data.iloc[:, :2])

                format_choice = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

                # Download button outside of both CSV and Excel conditions
                if st.button(f"📥 Download {file.name} as {format_choice}", key=f"btn-{file.name}"):
                    output = BytesIO()
                    if format_choice == "CSV":
                        df.to_csv(output, index=False)
                        mime = "text/csv"
                        new_name = file.name.replace(ext, "csv")
                    else:
                        df.to_excel(output, index=False, engine='openpyxl')
                        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        new_name = file.name.replace(ext, "xlsx")

                    output.seek(0)
                    st.download_button(
                        label="📥 Download File",
                        data=output,
                        file_name=new_name,
                        mime=mime,
                        key=f"download-{file.name}"
                    )
                    st.success("Processing Complete 🎉")





