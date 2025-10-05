# 🪐 Exoplanet Classifier with XGBoost

An intelligent exoplanet classification system that uses machine learning to distinguish between real exoplanets and false positives based on observational astronomical characteristics.

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![XGBoost](https://img.shields.io/badge/XGBoost-Latest-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🌐 Live Demo

**🚀 Try the application online**: [https://exoplanet-classifier-spaceappschallenge.streamlit.app/](https://exoplanet-classifier-spaceappschallenge.streamlit.app/)

The application is fully functional and ready to use! No installation required.

## 🌟 Features

- **Modern Web Interface**: Streamlit interface with custom space theme
- **Individual Classification**: Analyze astronomical objects one by one
- **Batch Import**: Process multiple objects via Excel/CSV spreadsheet
- **XGBoost Model**: Optimized machine learning algorithm
- **Multi-Mission Data**: Support for Kepler, TOI, and K2 data
- **Interactive Visualization**: Results with probabilities and metrics

## 🚀 Demo

### Main Interface
- **Tab 1**: Individual classification with interactive form
- **Tab 2**: Batch import with data validation

### Features
- ✅ Automatic data validation
- ✅ Real-time results preview
- ✅ CSV results download
- ✅ Example template for import
- ✅ Missing values handling

## 📋 Prerequisites

- Python 3.9 or higher
- pip (Python package manager)

## 🛠️ Installation

### Option 1: Use Online (Recommended)
**No installation required!** Use the live application at: [https://exoplanet-classifier-spaceappschallenge.streamlit.app/](https://exoplanet-classifier-spaceappschallenge.streamlit.app/)

### Option 2: Run Locally
If you want to run the application locally:

#### 1. Clone the repository
```bash
git clone https://github.com/GuiAntunes04/exoplanet-classifier.git
cd exoplanet-classifier
```

#### 2. Install dependencies
```bash
pip install -r requirements.txt
```

#### 3. Run the application
```bash
streamlit run app.py
```

The application will automatically open in your browser at `http://localhost:8501`

## 📊 How to Use

### Individual Classification
1. Go to the "🔬 Individual Classification" tab
2. Fill in the astronomical parameters
3. Configure the false positive flags
4. Click "🚀 Classify Object"
5. View the result with probability

### Batch Import
1. Go to the "📊 Batch Import" tab
2. Download the example template
3. Fill your spreadsheet with data
4. Upload the Excel/CSV file
5. Click "🚀 Process Spreadsheet"
6. Download the results

## 📁 Project Structure

```
exoplanet-classifier/
├── app.py                          # Main Streamlit application
├── data/
│   ├── model_and_features.pkl      # Trained model + features
│   └── exoplanet_unified_results.xlsx  # Example results
├── example_exoplanet_spreadsheet.csv   # Import template
├── units_documentation.md              # Units documentation
├── requirements.txt                    # Python dependencies
└── README.md                          # This file
```

## 🔬 Astronomical Parameters

The system uses 24 astronomical characteristics:

### Transit Parameters
- Orbital Period (days)
- Transit Duration (hours)
- Depth (ppm)
- Impact Parameter

### Planetary Properties
- Planet Radius (R⊕)
- Equilibrium Temperature (K)
- Insolation (S⊕)

### Stellar Characteristics
- Stellar Temperature (K)
- Stellar Radius (R☉)
- Stellar Mass (M☉)
- Kepler Magnitude (mag)

### Quality Flags
- 4 binary flags for false positives
- Mission context (Kepler/TOI/K2)

## 📈 Model Performance

- **Algorithm**: XGBoost (Gradient Boosting)
- **Type**: Binary classification
- **Features**: 24+ astronomical characteristics
- **Preprocessing**: One-hot encoding, missing value imputation
- **Validation**: Multi-mission space data

## 🎨 Interface

- **Space Theme**: Modern design with star animations
- **Responsive**: Works on desktop and mobile
- **Interactive**: Real-time visual feedback
- **Accessible**: Intuitive and well-documented interface

## 📝 Data Format

### Import Spreadsheet
- **Accepted formats**: Excel (.xlsx, .xls) or CSV (.csv)
- **Columns**: 24 columns in specific order
- **Missing values**: Leave blank or use NaN
- **Flags**: Use 0 or 1 for binary flags

### Example Template
Download the `example_exoplanet_spreadsheet.csv` file as reference.

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Data from Kepler, TESS (TOI), and K2 missions
- Streamlit community
- XGBoost developers
- Astronomical community

## 📞 Support

If you encounter any issues or have questions:

1. Check the [documentation](units_documentation.md)
2. Try the [live application](https://exoplanet-classifier-spaceappschallenge.streamlit.app/) first
3. Open an [issue](https://github.com/GuiAntunes04/exoplanet-classifier/issues)
4. Contact via GitHub discussions

---

**Developed with ❤️ for the astronomical community**

⭐ If this project was useful to you, consider giving it a star on GitHub!
