# Quick Reference Guide

## 🚀 Quick Start (30 seconds)

### Terminal 1 - Backend
```bash
cd d:/genai_project
venv\Scripts\activate
cd backend
python -m uvicorn main:app --reload
```
✅ Backend running: http://localhost:8000/docs

### Terminal 2 - Ollama (Keep Running)
```bash
ollama serve
```
✅ LLM service ready

### Terminal 3 - Frontend
```bash
cd d:/genai_project/frontend
npm start
```
✅ Frontend running: http://localhost:3000

---

## 📊 API Quick Reference

### Test Backend
```bash
curl http://localhost:8000/
```

### Upload Dataset
```bash
curl -F "file=@data.csv" http://localhost:8000/upload
```

### View Documentation
- Browser: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🎯 Common Queries to Try

### Data Cleaning
```
"remove missing values"
"remove duplicates"
```

### Statistics
```
"minimum"
"maximum"
"average salary"
"median age"
"show summary"
"standard deviation"
```

### Visualization
```
"histogram"
"histogram age"
"scatter plot"
"scatter salary vs experience"
"bar chart"
"bar chart by department"
```

### Analysis
```
"analyze this data"
"what are the trends?"
"summarize"
"explain"
```

---

## 🗂️ File Tree

```
├── backend/
│   ├── main.py          ← API endpoints
│   ├── analyzer.py      ← Analysis logic
│   ├── schemas.py       ← Data models
│   ├── utils.py         ← Helpers
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.js       ← Main app
│   │   └── components/  ← 5 UI components
│   └── package.json
│
├── README.md            ← Project overview
├── SETUP_GUIDE.md       ← Setup instructions
└── IMPROVEMENTS_SUMMARY.md ← Changes made
```

---

## ⚙️ Configuration Changes

### Backend Port (main.py, last line)
```python
uvicorn.run(app, host="0.0.0.0", port=5000)  # Change from 8000
```

### API URL (frontend/src/App.js, line 14)
```javascript
const API_BASE_URL = 'http://your-api:8000';
```

### Ollama Model (backend/analyzer.py, line 20)
```python
self.llm = OllamaLLM(model="llama2")  # Change from mistral
```

### Fuzzy Match Threshold (backend/utils.py, line 6)
```python
FUZZY_MATCH_THRESHOLD = 0.7  # More strict (default 0.6)
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Port already in use | `lsof -i :8000` then change port |
| LLM not working | `ollama serve` in separate terminal |
| CORS error | Clear browsers cache, try incognito |
| CSV upload fails | Check format is valid CSV, size < 100MB |
| Frontend errors | `npm install` again, clear node_modules |
| API not responding | `curl http://localhost:8000/` |

---

## 📦 Installation Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 14+ installed
- [ ] Virtual environment created
- [ ] requirements.txt installed with pip
- [ ] Ollama downloaded and running
- [ ] Mistral model pulled
- [ ] npm packages installed
- [ ] Both servers running

---

## 🧪 Test Flow

1. Open http://localhost:3000
2. Upload sample CSV
3. Check "Preview Data" tab
4. Try "What's the summary?" query
5. Try "histogram" query
6. Download processed file

---

## 📋 Endpoints Quick List

| Endpoint | Method | Purpose |
|----------|--------|---------|
| / | GET | Health check |
| /upload | POST | Upload CSV |
| /preview | GET | View data |
| /info | GET | Get metadata |
| /query | POST | Analyze data |
| /analyze/multiple-charts | POST | Multi-charts |
| /download | GET | Export Excel |

---

## 🎨 Frontend Tabs

1. 📤 Upload Dataset
2. 👁️ Preview Data
3. 🔍 Analysis
4. 📊 Results

---

## 🔧 Common Commands

```bash
# Activate virtual environment
venv\Scripts\activate

# Install Python packages
pip install -r requirements.txt

# Start backend
python -m uvicorn backend.main:app --reload

# Start frontend
npm start

# Build frontend
npm run build

# Install npm packages
npm install

# Run Ollama
ollama serve

# Pull model
ollama pull mistral

# List installed models
ollama list
```

---

## ✨ Key Features

- **Upload**: All CSV formats, up to 100MB
- **Preview**: View first 5 rows
- **Analyze**: Natural language queries
- **Visualize**: 3+ chart types
- **Export**: Download as Excel
- **AI**: Mistral LLM insights

---

## 📚 Documentation Files

| File | Content |
|------|---------|
| README.md | Project overview |
| SETUP_GUIDE.md | Installation steps |
| IMPROVEMENTS_SUMMARY.md | Changes made |
| backend/README.md | API documentation |
| frontend/README.md | UI guide |

---

## 🎁 Sample Query Path

```
1. Upload titanic.csv
2. Tab: Preview Data → See first 5 rows
3. Tab: Analysis → Query: "histogram age"
4. See interactive chart with AI insights
5. Tab: Results → View statistics
6. Download → Get processed_data.xlsx
```

---

## 🚨 Important Notes

- **Ollama MUST be running** for LLM features
- **Both services needed**: Backend + Frontend
- **Frontend connects to Backend** via API
- **Charts are HTML files** saved in /backend/charts/
- **Session data cleared** on server restart

---

## 🎓 Learning Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **React**: https://react.dev/
- **Pandas**: https://pandas.pydata.org/
- **Plotly**: https://plotly.com/python/
- **Ollama**: https://ollama.ai/

---

## ❓ FAQ

**Q: Can I use without Ollama?**
A: Yes, but LLM insights won't work. Other features work fine.

**Q: What if I don't have your exact column names?**
A: Fuzzy matching handles variations! "ticket price" matches "Fare".

**Q: Can multiple users use it?**
A: Yes, architecture supports multi-user with proper authentication.

**Q: How do I add more visualizations?**
A: Add to analyzer.py create_visualization() method.

**Q: Is it production-ready?**
A: Backend is production-ready. Add tests and deploy!

---

**Need more help? Check the full documentation files! 📚**
