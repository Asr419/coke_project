# 🧪 Coke Blend Processor

**Advanced coal quality analysis and custom blend creation tool**

A sophisticated Streamlit application for creating, analyzing, and optimizing coal/coke blends with customizable quality indices and scoring formulas.

## ✨ Features

### 📤 Step 1: Blend Selection
- Select up to **7 different vessel sources** for blending
- Set **custom percentage ratios** for each vessel (0-100%)
- Real-time validation ensuring **total composition = 100%**
- Interactive UI with status indicators (Active/Inactive)

### 📊 Step 2: Blend Properties Analysis
- Select which coal quality **properties to analyze**
- Automatic calculation of **weighted property values** based on blend ratios
- **Example**: If blend ratio is 40% and property value is 8, result = 0.4 × 8 = 3.2
- **Total Blend Row** showing combined values across all selected properties

### 📈 Step 3: Custom Index Creation
- Create **custom quality indices** from multiple properties
- Define **flexible formulas** combining different properties
- **Example formulas**:
  - `{ASH} * 0.3 + {Fixed Carbon} * 0.7`
  - `0.78 + 0.4 * {Ash}`
  - `({Volatile Matter} + {Fixed Carbon}) / 2`
- Add multiple indices for comprehensive analysis
- View all indices with their calculated values

### 🎯 Step 4: Final CSN Score
- Combine multiple indices into a **final Coke Strength Number (CSN)**
- Define **custom weighting formulas** for indices
- **Example formulas**:
  - `{Index1} * 0.6 + {Index2} * 0.4`
  - `{QualityIndex} - 0.1 * {ImpurityIndex}`
- Download comprehensive **CSN reports** with all calculations

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- pip (Python package manager)

### Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd coke_project
```

2. **Create and activate virtual environment**:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
source venv/bin/activate
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📋 Usage Workflow

### Complete Example:

1. **Upload Data**
   - Upload coal quality Excel file (.xlsx, .xls, or .csv)
   - Verify file loads successfully

2. **Create Blend (Step 1)**
   - Select 3-4 vessels from dropdown
   - Assign percentages: Vessel A (40%), Vessel B (35%), Vessel C (25%)
   - Total automatically validates to 100%

3. **Select Properties (Step 2)**
   - Choose key properties: ASH, Fixed Carbon, Volatile Matter, Sulphur
   - System calculates weighted values for each property
   - View TOTAL BLEND row with combined values

4. **Create Indices (Step 3)**
   - **Index 1**: "Combustion Quality" = `{ASH} * 0.3 + {Fixed Carbon} * 0.5 + {Volatile Matter} * 0.2`
   - **Index 2**: "Purity Score" = `100 - {Sulphur} * 50`
   - View both indices with their values

5. **Calculate CSN (Step 4)**
   - Formula: `{Combustion Quality} * 0.7 + {Purity Score} * 0.3`
   - Get final CSN Score
   - Download complete report

## 📁 Project Structure

```
coke_project/
├── app.py                 # Main Streamlit application
├── coke_test.xlsx         # Sample coal quality data
├── requirements.txt       # Python dependencies
├── .github/
│   └── copilot-instructions.md
├── README.md             # This file
└── venv/                 # Virtual environment (local)
```

## 🔧 Technical Details

### Formula Evaluation
- Supports all standard Python mathematical operators: `+`, `-`, `*`, `/`, `**`, `()`
- Supports functions: `abs()`, `max()`, `min()`, `sqrt()` etc.
- Properties and indices referenced with `{curly braces}`

### Data Storage
- Files uploaded in-memory (not persisted)
- Calculations done on total blend values
- Session state maintains user selections during session

### Export Options
- **Blend Table**: CSV export of weighted properties
- **CSN Report**: CSV export of indices and final score
- All calculations preserved in exported files

## 📊 Sample Data Format

Your Excel file should contain coal quality data with columns like:
- Vessel Code : Name
- Total Moisture
- Inherent Moisture
- Volatile Matter
- ASH
- Fixed Carbon
- Sulphur
- CSN
- HGI
- Rank
- And other coal quality properties

## 🎨 Frontend Features

- **Modern UI** with gradient headers and color-coded status indicators
- **Real-time validation** with visual feedback
- **Interactive components** for easy formula entry
- **Responsive design** working on desktop and tablets
- **Metric cards** showing key values
- **Success/error messages** with clear communication

## 📥 Deployment

### Local Deployment
Already running at `http://localhost:8501`

### Cloud Deployment (e.g., Streamlit Cloud)
```bash
git push origin main
# Deploy from GitHub repo at https://share.streamlit.io
```

## 🐛 Troubleshooting

### Issue: "Module not found" errors
**Solution**: Ensure virtual environment is activated
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: Formula returns error
**Solution**: Check that property/index names match exactly and are in `{curly braces}`

### Issue: File upload fails
**Solution**: Ensure file is .xlsx, .xls, or .csv format with "Vessel Code : Name" column

## 📝 Example Formulas

### Index Formulas
```
# Simple weighted average
{ASH} * 0.3 + {Fixed Carbon} * 0.5 + {Volatile Matter} * 0.2

# With constants
0.78 + 0.4 * {Ash}

# Complex expression
({Index1} + {Index2}) * 0.5 - {Index3} * 0.1
```

### CSN Formulas
```
# Two indices weighted
{Combustion Quality} * 0.7 + {Purity Score} * 0.3

# Multiple indices
{Index1} * 0.4 + {Index2} * 0.35 + {Index3} * 0.25

# With calculations
({Index1} + {Index2}) / 2 * {Index3}
```

## 📞 Support

For issues, questions, or suggestions, please:
1. Check the troubleshooting section above
2. Review the formula examples
3. Ensure data format matches requirements

## 📄 License

This project is available for use under standard terms.

## 👨‍💻 Author

Created for advanced coal quality analysis and blend optimization.

---

**Last Updated**: March 2026
**Version**: 1.0.0
