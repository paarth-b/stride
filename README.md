# Stride - Quick Start Guide

Get Stride running in 5 minutes!

## Prerequisites Checklist

Before starting, make sure you have:
- [ ] Docker Desktop installed and **running**
- [ ] Python 3.9 or higher (`python3 --version`)
- [ ] Node.js 18+ and npm (`node --version`)

## Step-by-Step Setup

### Step 1: Start PostgreSQL Database

```bash
cd stride
docker-compose up -d
docker ps
```

**Expected output:** Container named `stride-postgres` running on port 5432

### Step 2: Start Backend Server

Open a new terminal:

```bash
cd stride/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m app.main
```

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

Keep this terminal open! Backend should now be running at http://localhost:8000

### Step 3: Start Frontend

Open another new terminal:

```bash
cd stride/frontend
bun install
bun run dev
```

**Expected output:**
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
```

### Step 4: Initialize Data

1. Open your browser to http://localhost:5173
2. Click the **"Initialize Data"** button in the header
3. Wait for success message
4. Refresh the page

You should now see 20+ sneakers ready to compare!

## Quick Test

<<<<<<< HEAD
**Request:**
```json
{
  "sneaker_ids": [1, 2, 3],
  "start_date": "2025-01-01T00:00:00",
  "end_date": "2025-12-31T23:59:59"
}
```

**Response:**
```json
[
  {
    "timestamp": "2025-12-01T10:00:00",
    "price": 115.50,
    "sneaker_id": 1
  }
]
```

### POST /api/init-data
Initialize database with sample data (20 sneakers, 90 days of price history).

### GET /docs
Interactive Swagger UI documentation.

## Project Structure

```
stride/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── models.py            # SQLModel ORM models
│   │   ├── database.py          # Database connection
│   │   └── data_generator.py   # Sample data generation
│   ├── schema.sql               # Database DDL
│   ├── demo_queries.sql         # Demo SQL queries
│   ├── test_queries.py          # Python test script
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # Environment variables
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── SneakerSelect.tsx
│   │   │   ├── PriceChart.tsx
│   │   │   └── StatisticsCards.tsx
│   │   ├── hooks/
│   │   │   ├── useSneakers.ts
│   │   │   ├── usePriceHistory.ts
│   │   │   ├── useSelection.ts
│   │   │   └── useChartData.ts
│   │   ├── utils/
│   │   │   ├── api.ts
│   │   │   ├── types.ts
│   │   │   ├── helpers.ts
│   │   │   └── constants.ts
│   │   ├── App.tsx              # Main application
│   │   └── main.tsx             # Entry point
│   ├── package.json
│   └── tailwind.config.js
├── planning/
│   ├── design_doc.md
│   └── frontend.md
├── docker-compose.yml
└── README.md
```

## Data Generation

The application includes realistic market simulation:
- **90-day price history** per sneaker
- **Market volatility** (±3% daily fluctuation)
- **Hype factor multipliers** (0.8x to 3.0x retail)
- **20+ real sneakers** with actual SKUs
- **5 major brands**: Nike, Jordan, Adidas, Yeezy, New Balance
- **4 retailers**: StockX, GOAT, eBay, Flight Club

## Performance Features

- **SWR caching**: Automatic request deduplication
- **Lazy loading**: Components load on demand
- **Optimized queries**: Indexed on sneaker_id and timestamp
- **Virtual scrolling**: Handle large sneaker lists
- **Responsive design**: Mobile-first approach

## Development

### Backend Development

```bash
# Format code
black app/

# Type checking
mypy app/

# Run tests
pytest
```

### Frontend Development

```bash
# Lint code
npm run lint

# Format code
npm run format

# Type check
npm run type-check

# Build for production
npm run build
```
=======
1. Select 2-3 sneakers from the dropdown
2. View the interactive price chart
3. Check statistics cards below
>>>>>>> 70511e1 (chore: file cleanup)

## Troubleshooting

### "Cannot connect to Docker daemon"
- Start Docker Desktop application
- Wait for it to fully start (whale icon should be steady)
- Try `docker-compose up -d` again

### Backend not starting
```bash
# Make sure you're in the right directory
cd backend

# Activate virtual environment
source venv/bin/activate

# Try running directly
python -m app.main
```

### Frontend shows connection error
- Make sure backend is running at http://localhost:8000
- Check backend terminal for errors
- Try opening http://localhost:8000/docs in browser (should show Swagger UI)

### No sneakers appearing
- Click "Initialize Data" button
- Check backend terminal for error messages
- Ensure PostgreSQL is running: `docker ps`

## Quick Commands Reference

```bash
# Check if PostgreSQL is running
docker ps

# View PostgreSQL logs
docker logs stride-postgres

# Stop PostgreSQL
docker-compose down

# Restart PostgreSQL
docker-compose restart

# Access PostgreSQL directly
docker exec -it stride-postgres psql -U stride_user -d stride_db

# View backend API docs
open http://localhost:8000/docs
```

## Next Steps

- Explore the demo queries in `backend/demo_queries.sql`
- Run test queries: `cd backend && python test_queries.py`
- Read the full README.md for detailed documentation
- Check `planning/` folder for design documents

## Need Help?

1. Check the full README.md
2. Review logs in backend terminal
3. Check browser console for frontend errors
4. Ensure all 3 services are running:
   - PostgreSQL (port 5432)
   - Backend (port 8000)
   - Frontend (port 5173)

---

<<<<<<< HEAD
**Built with ❤️ for CSE 412 - Fall 2025**
=======
**Pro Tip:** Keep three terminals open - one for each service. This makes debugging much easier!
>>>>>>> 70511e1 (chore: file cleanup)
