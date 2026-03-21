import streamlit as st
import pandas as pd
import io
import numpy as np

st.set_page_config(page_title="Coke Blend Processor", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .step-header {
        background: linear-gradient(90deg, #1f77b4 0%, #2ca02c 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("# 🧪 Coke Blend Processor")
st.markdown("*Advanced coal quality analysis and custom blend creation*")
st.markdown("---")

# File uploader
st.markdown("### 📤 Upload Your Coal Quality Data")
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls", "csv"], help="Upload coal quality data in .xlsx, .xls, or .csv format")

if uploaded_file is not None:
    try:
        # Read the uploaded file
        if uploaded_file.type == "text/csv":
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        st.markdown('<div class="success-box">✅ File loaded successfully!</div>', unsafe_allow_html=True)
        
        # Display basic info in columns
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 Total Rows", len(df))
        with col2:
            st.metric("📋 Total Columns", len(df.columns))
        with col3:
            st.metric("💾 File Size", f"{uploaded_file.size / 1024:.2f} KB")
            st.metric("File Size", f"{uploaded_file.size / 1024:.2f} KB")
        
        # Extract vessel codes from "Vessel Code : Name" column
        vessel_column = "Vessel Code : Name"
        if vessel_column in df.columns:
            vessel_options = ["None"] + df[vessel_column].dropna().unique().tolist()
        else:
            vessel_options = ["None"]
        
        # Blend Selection Table - Step 1
        st.markdown('<div class="step-header">⚗️ Step 1: Blend Selection</div>', unsafe_allow_html=True)
        st.markdown("*Select up to 7 vessels and their respective percentages. Total must equal 100%.*")
        
        # Initialize session state for blend selections
        if "blend_data" not in st.session_state:
            st.session_state.blend_data = [
                {"vessel": "None", "percentage": 0} for _ in range(7)
            ]
        
        # Create blend selection table
        blend_cols = st.columns([2, 1, 1])
        with blend_cols[0]:
            st.write("**🚢 Vessel Code : Name**")
        with blend_cols[1]:
            st.write("**📊 Percentage (%)**")
        with blend_cols[2]:
            st.write("**📍 Status**")
        
        st.divider()
        
        # Create 7 rows for blend selection
        for i in range(7):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                selected_vessel = st.selectbox(
                    label=f"Vessel {i+1}",
                    options=vessel_options,
                    key=f"vessel_{i}",
                    index=vessel_options.index(st.session_state.blend_data[i]["vessel"]) if st.session_state.blend_data[i]["vessel"] in vessel_options else 0
                )
                st.session_state.blend_data[i]["vessel"] = selected_vessel
            
            with col2:
                # If "None" is selected, set percentage to 0 and disable input
                if selected_vessel == "None":
                    percentage = st.number_input(
                        label=f"Percentage {i+1}",
                        min_value=0,
                        max_value=100,
                        value=0,
                        key=f"percentage_{i}",
                        disabled=True
                    )
                    st.session_state.blend_data[i]["percentage"] = 0
                else:
                    percentage = st.number_input(
                        label=f"Percentage {i+1}",
                        min_value=0,
                        max_value=100,
                        value=st.session_state.blend_data[i]["percentage"],
                        key=f"percentage_{i}"
                    )
                    st.session_state.blend_data[i]["percentage"] = percentage
            
            with col3:
                if selected_vessel == "None":
                    st.write("🔴 Inactive")
                else:
                    st.write("🟢 Active")
        
        st.divider()
        
        # Calculate total percentage
        total_percentage = sum(
            item["percentage"] for item in st.session_state.blend_data 
            if item["vessel"] != "None"
        )
        
        # Display total and validation with better styling
        col1, col2, col3 = st.columns(3)
        with col1:
            if total_percentage == 100:
                st.markdown('<div class="success-box">✅ Perfect! Total: 100%</div>', unsafe_allow_html=True)
            elif total_percentage > 100:
                st.markdown(f'<div class="error-box">❌ Total: {total_percentage}% (Exceeds 100%)</div>', unsafe_allow_html=True)
            elif total_percentage < 100 and total_percentage > 0:
                st.markdown(f'<div class="error-box">⚠️ Total: {total_percentage}% (Less than 100%)</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div style="background-color: #e3f2fd; padding: 1rem; border-radius: 0.5rem; text-align: center;">ℹ️ Total: {total_percentage}%</div>', unsafe_allow_html=True)
        
        st.divider()
        
        # Step 2: Column Selection and Blend Properties Table
        st.markdown('<div class="step-header">📊 Step 2: Blend Properties</div>', unsafe_allow_html=True)
        
        # Check if total is 100% before allowing Step 2
        if total_percentage != 100:
            st.markdown(f'<div class="error-box">⚠️ <b>Total composition must be exactly 100%</b><br>Current: {total_percentage}%</div>', unsafe_allow_html=True)
            st.stop()
        
        st.markdown('<div class="success-box">✅ Composition at 100% - Ready to analyze</div>', unsafe_allow_html=True)
        
        # Get numeric columns for selection
        numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
        
        selected_properties = st.multiselect(
            "🔍 Select properties to display in blend table:",
            options=numeric_columns,
            default=numeric_columns[:6] if len(numeric_columns) >= 6 else numeric_columns,
            key="properties_multiselect"
        )
        
        if selected_properties:
            st.divider()
            st.subheader("Blend Properties Table")
            
            # Create blend properties table
            blend_rows = []
            active_blends = [item for item in st.session_state.blend_data if item["vessel"] != "None"]
            
            # Add rows for each selected blend
            for blend_item in active_blends:
                vessel_name = blend_item["vessel"]
                ratio = blend_item["percentage"] / 100.0  # Convert percentage to ratio
                
                if vessel_name != "None":
                    # Find the row in the original dataframe
                    vessel_row = df[df["Vessel Code : Name"] == vessel_name]
                    
                    if not vessel_row.empty:
                        row_data = {"Vessel": vessel_name, "Ratio (%)": blend_item["percentage"]}
                        
                        # Calculate weighted values for each selected property
                        for prop in selected_properties:
                            if prop in vessel_row.columns:
                                original_value = vessel_row[prop].iloc[0]
                                # Handle numeric values
                                if pd.notna(original_value):
                                    try:
                                        numeric_value = float(original_value)
                                        weighted_value = ratio * numeric_value
                                        row_data[prop] = weighted_value
                                    except (ValueError, TypeError):
                                        row_data[prop] = None
                                else:
                                    row_data[prop] = None
                        
                        blend_rows.append(row_data)
            
            # Create dataframe from blend rows
            if blend_rows:
                blend_df = pd.DataFrame(blend_rows)
                
                # Calculate total blend row
                total_row = {"Vessel": "TOTAL BLEND", "Ratio (%)": total_percentage}
                for prop in selected_properties:
                    if prop in blend_df.columns:
                        total_row[prop] = blend_df[prop].sum()
                
                # Append total row
                blend_df = pd.concat([blend_df, pd.DataFrame([total_row])], ignore_index=True)
                
                # Display the blend table
                st.dataframe(blend_df, use_container_width=True, hide_index=True)
                
                # Download blend table
                csv = blend_df.to_csv(index=False)
                st.download_button(
                    label="Download Blend Table as CSV",
                    data=csv,
                    file_name="blend_table.csv",
                    mime="text/csv"
                )
            else:
                st.info("No active blends selected. Select at least one vessel with percentage > 0%.")
        
        st.divider()
        
        # Step 3: Custom Index Calculation
        st.markdown('<div class="step-header">📈 Step 3: Custom Index Calculation</div>', unsafe_allow_html=True)
        st.markdown("*Create custom quality indices based on total blend properties*")
        
        # Initialize session state for indices
        if "indices" not in st.session_state:
            st.session_state.indices = []
        
        # Add new index section
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            index_name = st.text_input("📝 Index Name", placeholder="e.g., 'Ash Content Index'", key="index_name_input")
        
        with col2:
            if selected_properties:
                selected_properties_list = st.multiselect(
                    "🔗 Select Properties",
                    options=selected_properties,
                    key="index_properties_select"
                )
            else:
                st.warning("Select properties in Step 2 first")
                selected_properties_list = []
        
        with col3:
            if st.button("➕ Add Index", key="add_index_btn", use_container_width=True):
                if index_name and selected_properties_list:
                    st.info("Enter custom formula in the text area below")
                else:
                    st.warning("Please enter index name and select at least one property")
        
        # Custom formula input for index
        if selected_properties_list:
            st.markdown("**📐 Enter Custom Formula for Index:**")
            st.info(f"Available properties: {' | '.join(selected_properties_list)}")
            
            index_formula = st.text_area(
                "Formula (use property names in curly braces):",
                placeholder="Example: {ASH} * 0.3 + {Fixed Carbon} * 0.7",
                height=80,
                key="index_formula_input"
            )
            
            if index_formula and index_name and st.button("✅ Calculate & Add Index", key="calc_index_btn", use_container_width=True):
                try:
                    if blend_rows:
                        blend_df_temp = pd.DataFrame(blend_rows)
                        
                        # Prepare formula with actual values
                        formula_eval = index_formula
                        for prop in selected_properties_list:
                            if prop in blend_df_temp.columns:
                                total_value = blend_df_temp[prop].sum()
                                formula_eval = formula_eval.replace("{" + prop + "}", str(total_value))
                        
                        # Evaluate formula
                        index_value = eval(formula_eval)
                        
                        st.session_state.indices.append({
                            "name": index_name,
                            "formula": index_formula,
                            "value": index_value
                        })
                        st.markdown(f'<div class="success-box">✅ Index "{index_name}" created with value: <b>{index_value:.4f}</b></div>', unsafe_allow_html=True)
                    else:
                        st.error("No blends to calculate from")
                except Exception as e:
                    st.error(f"❌ Error in formula: {str(e)}")
        
        # Display created indices
        if st.session_state.indices:
            st.markdown("### 📊 Created Indices")
            
            indices_cols = st.columns(len(st.session_state.indices))
            for idx, (col, index_item) in enumerate(zip(indices_cols, st.session_state.indices)):
                with col:
                    st.metric(
                        label=index_item["name"],
                        value=f"{index_item['value']:.4f}"
                    )
            
            st.divider()
            
            # Display indices as table with formula
            indices_table_data = []
            for idx, index_item in enumerate(st.session_state.indices):
                indices_table_data.append({
                    "Index Name": index_item["name"],
                    "Formula": index_item["formula"],
                    "Value": index_item["value"]
                })
            indices_df = pd.DataFrame(indices_table_data)
            st.dataframe(indices_df, use_container_width=True, hide_index=True)
            
            # Remove index button
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🗑️ Clear All Indices", use_container_width=True):
                    st.session_state.indices = []
                    st.rerun()
        
        st.divider()
        
        # Step 4: Final CSN Score Calculation
        st.markdown('<div class="step-header">🎯 Step 4: Final CSN Score</div>', unsafe_allow_html=True)
        st.markdown("*Combine indices into a final Coke Strength Number (CSN) using custom formula*")
        
        if st.session_state.indices:
            st.markdown("### 📐 CSN Calculation Formula")
            
            # Create a reference of available indices
            index_refs = " | ".join([f"{item['name']}" for item in st.session_state.indices])
            st.info(f"**Available Indices:** {index_refs}")
            
            # Create table showing index values for reference
            csn_ref_data = []
            for item in st.session_state.indices:
                csn_ref_data.append({
                    "Index": item["name"],
                    "Formula": item["formula"],
                    "Value": f"{item['value']:.4f}"
                })
            st.dataframe(pd.DataFrame(csn_ref_data), use_container_width=True, hide_index=True)
            
            st.markdown("**Enter your custom CSN formula:**")
            
            custom_csn_formula = st.text_area(
                "CSN Formula (use index names in curly braces):",
                placeholder="Example: {Index1} * 0.6 + {Index2} * 0.4",
                height=100,
                key="custom_csn_formula_input"
            )
            
            if st.button("🧮 Calculate CSN Score", key="calc_csn_btn", use_container_width=True):
                if custom_csn_formula:
                    try:
                        # Replace index names with their values
                        formula_eval = custom_csn_formula
                        for item in st.session_state.indices:
                            formula_eval = formula_eval.replace(
                                "{" + item['name'] + "}",
                                str(item['value'])
                            )
                        
                        # Evaluate the formula
                        csn_value = eval(formula_eval)
                        
                        st.session_state.csn_score = {
                            "value": csn_value,
                            "formula": custom_csn_formula
                        }
                        
                    except Exception as e:
                        st.error(f"❌ Error evaluating formula: {str(e)}")
                else:
                    st.warning("Please enter a formula")
            
            # Display CSN Score if calculated
            if "csn_score" in st.session_state:
                csn_value = st.session_state.csn_score["value"]
                csn_formula = st.session_state.csn_score["formula"]
                
                # Display CSN Score with gradient background
                st.markdown(f"""
                <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 2.5rem; border-radius: 1rem; color: white; text-align: center; margin: 2rem 0;">
                    <h2>🏆 Final CSN Score</h2>
                    <h1 style="font-size: 3.5rem; margin: 0.5rem 0; font-weight: bold;">{csn_value:.4f}</h1>
                    <p style="font-size: 1rem; opacity: 0.9;">Formula: <code>{csn_formula}</code></p>
                </div>
                """, unsafe_allow_html=True)
                
                # Download CSN report
                report_data = {
                    "Component": [item['name'] for item in st.session_state.indices] + ["FINAL CSN SCORE"],
                    "Value": [f"{item['value']:.4f}" for item in st.session_state.indices] + [f"{csn_value:.4f}"]
                }
                report_df = pd.DataFrame(report_data)
                
                csv = report_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSN Report",
                    data=csv,
                    file_name="csn_report.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        else:
            st.info("👈 Create at least one index in Step 3 to calculate CSN score")
        
        # Download processed data
        csv = df.to_csv(index=False)
        st.download_button(
            label="Download Original Data as CSV",
            data=csv,
            file_name="processed_data.csv",
            mime="text/csv"
        )
        
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
else:
    st.info("👆 Upload an Excel file to get started")
