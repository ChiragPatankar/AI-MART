# Multi-Agent E-Commerce Recommendation System

A sophisticated recommendation system that uses multiple AI agents to provide personalized product recommendations to users.

## Features

- Multiple recommendation algorithms (Collaborative Filtering, Content-Based, Sequential Pattern Mining, Hybrid)
- Real-time user feedback processing
- Personalized product recommendations
- Admin dashboard for system monitoring
- Modern React.js frontend
- FastAPI backend with async support

## Project Structure

```
.
├── frontend/              # React.js frontend
├── src/
│   ├── api/              # API endpoints and routes
│   ├── algorithms/       # Recommendation algorithms
│   ├── agents/          # AI agents implementation
│   ├── database/        # Database models and connection
│   └── utils/           # Utility functions
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
└── .env                # Environment variables
```

## Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-mart
```

2. Set up the backend:
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your configuration
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

## Running the Application

1. Start the backend server:
```bash
# From the project root
uvicorn main:app --reload
```

2. Start the frontend development server:
```bash
# From the frontend directory
npm start
```

The application will be available at:
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000
- API Documentation: http://localhost:8000/docs

## API Documentation

The API documentation is available at `/docs` when running the backend server. It provides detailed information about all available endpoints, request/response formats, and authentication requirements.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FastAPI for the amazing backend framework
- React.js for the frontend framework
- All contributors and maintainers 