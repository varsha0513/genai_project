# AI Data Analyst - React Frontend

Modern React-based dashboard for the AI Data Analyst backend system.

## Features

- 📤 **Dataset Upload**: Easy CSV file upload with validation
- 👁️ **Data Preview**: View first rows of your dataset
- 🔍 **Natural Language Queries**: Ask questions in plain English
- 📊 **Interactive Visualizations**: Histogram, scatter plots, bar charts
- 💡 **AI Insights**: Get intelligent analysis from Mistral LLM
- ⬇️ **Data Export**: Download processed datasets as Excel files

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn

### Installation

```bash
cd frontend
npm install
```

### Running the Development Server

```bash
npm start
```

The application will open at `http://localhost:3000`

### Building for Production

```bash
npm run build
```

## API Configuration

The frontend connects to the backend at `http://localhost:8000` by default.

To change the API URL, modify the `API_BASE_URL` in [src/App.js](src/App.js):

```javascript
const API_BASE_URL = 'http://your-api-url:8000';
```

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── FileUpload.js          # CSV upload component
│   │   ├── DataPreview.js         # Dataset preview table
│   │   ├── QueryInterface.js      # Query input interface
│   │   ├── VisualizationDisplay.js # Chart display
│   │   └── StatisticsDisplay.js   # Statistics results
│   ├── App.js                      # Main application
│   ├── App.css                     # App styles
│   ├── index.js                    # React entry point
│   └── index.css                   # Global styles
├── package.json
└── .gitignore
```

## UI Components

### FileUpload
- Handles CSV file selection and upload
- Shows upload progress indicator
- Validates file type and size

### DataPreview
- Displays dataset preview in table format
- Shows first 5 rows with all columns
- Responsive table design

### QueryInterface
- Text input for natural language queries
- Quick query buttons for common operations
- Loading indicator during processing

### VisualizationDisplay
- Renders Plotly charts as iframe
- Shows chart metadata (type, axes)
- Displays AI-generated insights

### StatisticsDisplay
- Shows statistical analysis results
- Formats data in tables or JSON
- Handles different response types

## Usage Examples

### Upload Dataset
1. Click "📤 Upload Dataset" tab
2. Select a CSV file
3. Click "📤 Upload" button

### Query the Data
1. Go to "🔍 Analysis" tab
2. Enter a natural language query:
   - "Show me a histogram of age"
   - "What is the average salary?"
   - "Remove missing values"
3. Click "✨ Analyze"

### View Results
- Charts appear in interactive Plotly format
- Statistics display in formatted tables
- AI insights provide additional analysis

## Technologies Used

- **React 18**: Modern UI library
- **Axios**: HTTP client for API communication
- **React Bootstrap**: UI component library
- **Plotly.js**: Interactive charting
- **CSS3**: Modern styling and animations

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Future Enhancements

- Real-time data processing indicators
- Dashboard layout customization
- Export analysis as PDF
- Multi-language support
- Dark mode theme
- Advanced filter options

## Troubleshooting

### CORS Error
If you see CORS errors, ensure the backend has CORS enabled or is running on the same domain.

### API Not Responding
- Check if backend is running on `http://localhost:8000`
- Verify network connectivity
- Check browser console for detailed errors

### Chart Not Displaying
- Ensure Ollama/Mistral is running for AI insights
- Check if chart HTML file is generated
- Verify file paths in network responses

## License

MIT

## Support

For issues or questions, please check the main project README or contact the development team.
