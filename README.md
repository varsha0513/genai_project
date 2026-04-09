# AI-Powered Smart Data Analyst System

A complete AI-driven platform for natural language data analysis. Upload any dataset, ask questions in plain English, and get instant insights with beautiful visualizations.

## 🎯 Overview

This system combines:
- **FastAPI Backend**: Robust data processing and analysis engine
- **React Frontend**: Modern, responsive user interface  
- **AI Integration**: Mistral LLM for intelligent insights
- **Plotly Visualizations**: Interactive, publication-quality charts

Transform data analysis from a technical skill to something anyone can do.

## ✨ Key Features

### For Data Analysis
- 📊 **Flexible Visualizations**: Histogram, scatter plots, bar charts
- 📈 **Complete Statistics**: Min, max, mean, median, sum, std, summary
- 🧹 **Smart Data Cleaning**: Remove missing values and duplicates
- 💾 **Excel Export**: Download processed datasets

### For User Experience  
- 💬 **Natural Language Queries**: Ask questions like "Show histogram of age"
- 🧠 **AI Insights**: Get intelligent analysis from Mistral LLM
- 🔍 **Fuzzy Column Matching**: Smart detection of column names
- ⚡ **Real-time Processing**: Instant results and visualizations

### For Developers
- 🏗️ **Modular Code**: Clean separation of concerns
- 📚 **Full Documentation**: API docs and guides
- 🔌 **Easy Integration**: CORS enabled, REST API
- 🐳 **Ready for Scale**: Session management foundation

## 📋 Project Status

| Component | Status | Details |
|-----------|--------|---------|
| Backend API | ✅ Complete | All endpoints implemented |
| AI Integration | ✅ Complete | Mistral/Ollama ready |
| Visualizations | ✅ Complete | Plotly charts working |
| Natural Language | ✅ Complete | Query processing ready |
| Frontend UI | ✅ Complete | React dashboard ready |
| Error Handling | ✅ Complete | Comprehensive validation |
| Fuzzy Matching | ✅ Complete | Smart column detection |
| Documentation | ✅ Complete | Full API & setup docs |

**Overall Completion: 100% (MVP Complete)**

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- Ollama with Mistral model

### Backend Setup

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
cd backend
pip install -r requirements.txt

# Start Ollama (in another terminal)
ollama serve

# Run backend
python -m uvicorn main:app --reload
# API: http://localhost:8000/docs
```

### Frontend Setup

```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm start
# App: http://localhost:3000
```

## 📚 Usage Examples

### Upload and Analyze
```bash
# 1. Upload CSV file via UI
# 2. Ask questions:

"What's the minimum salary?"
"Show histogram of age"
"Remove missing values"
"Generate scatter plot: salary vs experience"
"Analyze this dataset"
```

### API Direct Usage
```bash
# Upload
curl -F "file=@data.csv" http://localhost:8000/upload

# Query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "histogram age"}'

# Download
curl http://localhost:8000/download > processed.xlsx
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────┐
│           React Frontend (Dashboard)                 │
│  • File Upload  • Query Interface  • Visualization   │
└──────────────────┬──────────────────────────────────┘
                   │ HTTP/REST
┌──────────────────▼──────────────────────────────────┐
│         FastAPI Backend (API Server)                 │
│  ├─ Upload Handler    (File validation)              │
│  ├─ Query Processor   (Intent detection)             │
│  ├─ Data Analyzer     (Statistics, cleaning)         │
│  ├─ Visualizer        (Plotly charts)                │
│  └─ AI Engine         (LLM integration)              │
└──────────────────┬──────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
   ┌────▼────┐        ┌──────▼──────┐
   │ Pandas  │        │  Mistral    │
   │ NumPy   │        │  (via Ollama)│
   └─────────┘        └─────────────┘
```

## 📁 Project Structure

```
genai_project/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── analyzer.py          # Analysis engine
│   ├── schemas.py           # Data models
│   ├── utils.py             # Helper functions
│   ├── requirements.txt
│   ├── README.md            # Backend docs
│   └── charts/              # Generated visualizations
│
├── frontend/
│   ├── src/
│   │   ├── App.js           # Main app
│   │   ├── components/
│   │   │   ├── FileUpload.js
│   │   │   ├── DataPreview.js
│   │   │   ├── QueryInterface.js
│   │   │   ├── VisualizationDisplay.js
│   │   │   └── StatisticsDisplay.js
│   │   └── styles
│   ├── package.json
│   ├── README.md            # Frontend docs
│   └── .gitignore
│
└── README.md (this file)
```

## 🔧 Configuration

### Backend Settings

**Change API Port:**
```python
# backend/main.py
uvicorn.run(app, host="0.0.0.0", port=5000)
```

**Adjust Fuzzy Matching:**
```python
# backend/utils.py
FUZZY_MATCH_THRESHOLD = 0.7  # 0-1, higher = stricter
```

**Change LLM Model:**
```python
# backend/analyzer.py
self.llm = OllamaLLM(model="llama2")
```

### Frontend Settings

**Change API URL:**
```javascript
// frontend/src/App.js
const API_BASE_URL = 'http://your-api-url:8000';
```

## 📖 API Documentation

Full interactive API docs available at: `http://localhost:8000/docs`

### Main Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Health check |
| POST | `/upload` | Upload CSV file |
| GET | `/preview` | Get data preview |
| GET | `/info` | Get dataset metadata |
| POST | `/query` | Process natural language query |
| POST | `/analyze/multiple-charts` | Generate multiple visualizations |
| GET | `/download` | Download processed data |

See [backend/README.md](backend/README.md) for detailed endpoint documentation.

## 🎨 UI Features

### Dashboard Tabs
1. **📤 Upload Dataset** - File upload and dataset info
2. **👁️ Preview Data** - View dataset preview
3. **🔍 Analysis** - Query interface with examples
4. **📊 Results** - Visualizations and statistics

### Quick Queries
- "What is the summary of this data?"
- "Show me minimum values"
- "Show me maximum values"
- "Generate a histogram"
- "Remove missing values"

## 🔒 Security

- ✅ File type validation (CSV only)
- ✅ File size limits (100MB)
- ✅ Input validation with Pydantic
- ✅ CORS protection
- ✅ Error message sanitization

## 🚦 Troubleshooting

### LLM Not Working
```bash
# Check Ollama is running
ollama serve

# Check Mistral is installed
ollama list

# Pull if needed
ollama pull mistral
```

### Frontend Can't Connect to Backend
```javascript
// Check API URL in frontend/src/App.js
const API_BASE_URL = 'http://localhost:8000';

// Verify backend is running
curl http://localhost:8000/
```

### CSV Upload Issues
- Ensure CSV format is valid
- Check file size < 100MB
- Verify proper encoding (UTF-8)

## 📊 Sample Datasets

Test with popular datasets:

- [Titanic Dataset](https://www.kaggle.com/c/titanic/data)
- [Iris Dataset](https://archive.ics.uci.edu/ml/datasets/iris)
- [COVID-19 Dataset](https://github.com/datasets/covid-19)
- [House Prices Dataset](https://www.kaggle.com/c/house-prices-advanced-regression-techniques)

## 🔮 Future Roadmap

### Phase 2 (Next)
- [ ] User authentication & accounts
- [ ] Dataset persistence (database)
- [ ] Advanced NLP for column detection
- [ ] More chart types (pie, box plot, heatmap)
- [ ] Real-time data updates

### Phase 3 (Later)
- [ ] PDF report generation
- [ ] Support for Excel, JSON, SQL data sources
- [ ] Collaborative analysis
- [ ] Scheduled reports
- [ ] Mobile app

### Performance
- [ ] GPU acceleration
- [ ] Large dataset optimization
- [ ] Caching layer
- [ ] Async processing

## 🤝 Contributing

Contributions are welcome! Areas for improvement:

- Additional visualization types
- More statistical methods
- Better error messages
- Performance optimization
- Documentation improvements
- UI/UX enhancements

## 📄 License

MIT - See LICENSE file

## 📞 Support

### Documentation
- Backend API: [backend/README.md](backend/README.md)
- Frontend UI: [frontend/README.md](frontend/README.md)
- API Docs: http://localhost:8000/docs

### Common Issues
1. Check API is responding: `curl http://localhost:8000/`
2. Verify Ollama is running: `ollama serve`
3. Check frontend connects correctly in console

### Getting Help
- Review error messages in console
- Check API documentation
- Test with sample datasets first
- Verify all prerequisites are installed

## 🎓 Learning Resources

- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [React Documentation](https://react.dev/)
- [Pandas Data Analysis](https://pandas.pydata.org/docs/)
- [Plotly Visualization](https://plotly.com/python/)
- [LangChain](https://python.langchain.com/)

## 🎉 Key Achievements

✅ **Backend**: Robust, modular, production-ready FastAPI system  
✅ **Frontend**: Modern, responsive React dashboard  
✅ **AI**: Intelligent analysis with Mistral LLM  
✅ **UX**: Simple, intuitive interface for non-technical users  
✅ **Code Quality**: Clean, documented, maintainable code  
✅ **Error Handling**: Comprehensive validation and error messages  
✅ **Scalability**: Foundation for multi-user, multi-dataset support  
✅ **Documentation**: Complete API and setup documentation

---

**Built with ❤️ for data analysis enthusiasts**

*Turn data into insights without writing code.*
