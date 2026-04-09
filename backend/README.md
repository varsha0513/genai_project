# AI Data Analyst - Backend System

Complete FastAPI backend for AI-powered natural language data analysis.

## Features

### Core Features
- ✅ **Dataset Upload**: Support for CSV files up to 100MB
- ✅ **Smart Data Preview**: View dataset samples
- ✅ **Dataset Metadata**: Automatic column detection (numeric/categorical)
- ✅ **Data Cleaning**: Remove missing values and duplicates
- ✅ **Statistical Analysis**: Min, max, mean, median, sum, std, summary
- ✅ **Visualization**: Histogram, scatter plots, bar charts
- ✅ **AI Insights**: Mistral LLM integration for intelligent analysis
- ✅ **Data Export**: Download as Excel files

### Advanced Features
- ✅ **Fuzzy Column Matching**: Smart column detection from natural language
- ✅ **Natural Language Processing**: Flexible query understanding
- ✅ **Error Handling**: Comprehensive error messages
- ✅ **CORS Support**: Ready for frontend integration
- ✅ **Session Management**: Multi-user support foundation
- ✅ **Multiple Visualizations**: Generate multiple charts in one request

## Requirements

- Python 3.8+
- pip
- Ollama with Mistral model (for AI features)

## Installation

### 1. Create Virtual Environment

```bash
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Ollama (for AI features)

Download and install Ollama from https://ollama.ai

Then pull the Mistral model:
```bash
ollama pull mistral
```

Start Ollama service:
```bash
ollama serve
```

## Running the Backend

```bash
python -m uvicorn backend.main:app --reload
```

The API will be available at: `http://localhost:8000`

API Documentation (Swagger UI): `http://localhost:8000/docs`

## API Endpoints

### Health Check
- `GET /` - Check API status

### Dataset Management
- `POST /upload` - Upload CSV dataset
- `GET /preview` - Get dataset preview
- `GET /info` - Get dataset metadata
- `GET /download` - Download processed dataset

### Analysis
- `POST /query` - Process natural language query
- `POST /analyze/multiple-charts` - Generate multiple visualizations

## Query Examples

### Data Cleaning
```
"remove missing values"
"remove duplicates"
```

### Statistical Analysis
```
"minimum salary"
"maximum age"
"average experience"
"median salary"
"show summary"
"standard deviation"
```

### Visualization
```
"histogram age"
"scatter plot salary vs experience"
"bar chart department"
"show me age distribution"
```

### General Analysis
```
"What are the trends in this data?"
"Analyze this dataset"
"Give me insights"
```

## Project Structure

```
backend/
├── main.py              # FastAPI application
├── analyzer.py          # Core analysis engine
├── schemas.py           # Pydantic models
├── utils.py             # Utility functions
├── charts/              # Generated visualizations
├── requirements.txt     # Python dependencies
└── processed_data.xlsx  # Output files
```

## Code Architecture

### main.py
- FastAPI app initialization
- API endpoints
- Session management
- CORS configuration
- Error handling

### analyzer.py
- **DataAnalyzer class**: Core analysis engine
  - `clean_missing_values()`: Data cleaning
  - `clean_duplicates()`: Duplicate removal
  - `analyze_statistics()`: Statistical calculations
  - `create_visualization()`: Chart generation
  - `generate_ai_analysis()`: LLM-based insights

### schemas.py
- Pydantic models for request/response validation
- Type hints and documentation

### utils.py
- `fuzzy_match_column()`: Intelligent column detection
- `extract_columns_from_query()`: Extract column references
- `detect_query_intent()`: Identify query type
- `get_numeric_and_categorical_columns()`: Column classification

## Key Improvements

### 1. Modular Architecture
- Separated concerns (analysis, schemas, utilities)
- Reusable components
- Easy to extend

### 2. Error Handling
- Try-catch blocks for all operations
- Detailed error messages
- HTTP exception handling

### 3. Fuzzy Matching
- Intelligent column detection
- Handles typos and variations
- 60% similarity threshold

### 4. Session Management
- Foundation for multi-user support
- Dataset isolation per session
- Scalable architecture

### 5. Request Validation
- Pydantic models for all requests
- File type validation
- Size limits (100MB)

### 6. AI Integration
- Graceful fallback if LLM unavailable
- Optimized prompts for analysis
- Asynchronous processing

## Features in Detail

### Fuzzy Column Matching

Instead of exact matches, the system now understands similar column names:

```
Query: "minimum ticket price"
Columns: ["Fare", "Age", "Name"]
Result: Matches "Fare" (fare ≈ ticket price)
```

### Multi-Chart Generation

Generate multiple visualizations at once:

```
POST /analyze/multiple-charts
{
  "query": "histogram age, scatter salary vs experience, bar chart department"
}
```

### Enhanced Statistics

Automatic column selection when not specified:

```
Query: "minimum"  # Automatically selects first numeric column
```

### AI-Powered Insights

LLM generates insights for every visualization:

```
Chart → Mistral LLM → Professional Analysis
```

## Configuration

### Change API Port
```python
# In main.py's __main__ section
uvicorn.run(app, host="0.0.0.0", port=5000)  # Change from 8000
```

### Adjust Fuzzy Matching Threshold
```python
# In utils.py
FUZZY_MATCH_THRESHOLD = 0.7  # Default is 0.6 (higher = stricter)
```

### Change LLM Model
```python
# In analyzer.py
self.llm = OllamaLLM(model="neural-chat")  # Instead of "mistral"
```

## Troubleshooting

### LLM Not Available
- Ensure Ollama is running: `ollama serve`
- Check Mistral is installed: `ollama pull mistral`
- Verify connection: `http://localhost:11434`

### CORS Errors (Frontend)
- Backend already has CORS enabled for all origins
- Check frontend is connecting to correct URL

### Large File Upload
- Max size is 100MB (configurable in main.py)
- Increase: `file_size > 500 * 1024 * 1024` (for 500MB)

### Column Not Detected
- Try more specific query terms
- Use exact column names
- Check fuzzy matching threshold

## Performance Optimization

For large datasets:

1. **Batch Processing**: Process in chunks
2. **Lazy Loading**: Load data on demand
3. **Caching**: Cache analysis results
4. **Async Operations**: Use async/await

## Security Considerations

### File Upload
- ✅ File type validation (CSV only)
- ✅ Size limits (100MB)
- ✅ Unique filename generation (UUID)

### Input Validation
- ✅ Pydantic model validation
- ✅ Query length limits
- ✅ Error message sanitization

### Future Enhancements
- User authentication
- Dataset encryption
- Rate limiting
- API key management

## Testing

### Manual Testing
Use FastAPI Swagger UI: `http://localhost:8000/docs`

### Example Flow
1. Upload `/tests/sample.csv`
2. Check `/preview`
3. Get `/info`
4. Submit `/query` with "histogram age"
5. `/download` processed data

## Dependencies

- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Pandas**: Data manipulation
- **NumPy**: Numerical computing
- **Plotly**: Visualization
- **LangChain**: LLM integration
- **Ollama**: Local LLM runtime
- **Pydantic**: Data validation

## Roadmap

### Phase 2 (Planned)
- [ ] User authentication system
- [ ] Database integration (persistent storage)
- [ ] Advanced NLP for column matching
- [ ] Real-time data streaming
- [ ] Advanced statistical tests

### Phase 3 (Planned)
- [ ] PDF report generation
- [ ] More visualization types
- [ ] Support for Excel, JSON, SQL
- [ ] Performance optimization
- [ ] GPU acceleration

## Contributing

Contributions are welcome! Areas for improvement:
- More visualization types
- Additional statistical methods
- Better error messages
- Performance optimization
- Documentation improvements

## License

MIT

## Support

For issues or questions:
1. Check existing issues
2. Review API documentation
3. Test with sample datasets
4. Check Ollama connection

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [Plotly Documentation](https://plotly.com/python/)
- [LangChain Documentation](https://python.langchain.com/)
- [Ollama Documentation](https://ollama.ai/)
