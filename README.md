# Flash Card App

The following app allows users to add flashcards to a deck, view the questions and answers, edit and delete the flashcards.

## Stack Components

| Layer | Technology |
|-------|-----------|
| **Frontend** | React |
| **Styling** | CSS |
| **Routing** | RESTful API |
| **Backend** | FastAPI (Python) |
| **Database** | MongoDB |

## Feature List

* Responsive mobile design
* Create, edit, and delete flashcards
* Flip cards to reveal answers
* Local storage persistence
* Simple and clean user interface

## Folder Structure

```bash
flashcard_app
├── .vscode
├── backend
│    └─── flashcard_app.py                 #FastAPI server initialization, CORS setup, and REST API endpoints
│    └─── flashcard_crud.py                #Database models, Pydantic schemas, and CRUD operation handlers for MongoDB
├── frontend
│    └─── src
│          └─── components
│               └─── FlashCardApp.css      #Styling for flashcards
│               └─── FlashCardApp.jsx      #Core component managing state, API calls, and all CRUD operations
│          └─── App.css                    #Global styling for app
│          └─── App.jsx                    #Root component that wraps FlashCardApp
├── node_modules
├── README.md
├── flashcarddb.flashcards.json            #Database export with sample flashcard data
├── package-lock.json
└── package.json

```

## Challenges overcome
Initially the app was designed to use MySQL instead of MongoDB. However during the development process, the schema for MySQL was too rigid and did not allow `Date.now()` as an id for the flashcard. I tried to use a different id, but I believe MySQL was too complex for this web app. Therefore, I decided to use MongoDB that has a document-based approach and has a much simpler schema and allowed any type of data for the id. Integrating the frontend and the backend was challenging as well. Sometimes when the connection with the database failed the UI did not show the appropriate messages. Therefore, I added appropriate messages, error handling and made sure the UI reflected the latest server state.
    
## How to run

### Prerequisites

Before starting, ensure you have the following installed:

- **Node.js** 18+ ([Download](https://nodejs.org/)) - for React frontend
- **Python** 3.8+ ([Download](https://www.python.org/)) - for FastAPI backend
- **MongoDB** ([Download](https://www.mongodb.com/try/download/community)) - for database
- **Git** ([Download](https://git-scm.com/)) - for cloning the repository

Verify installations:
```bash
node --version      # Should show v18.x.x or higher
python --version    # Should show 3.8 or higher
git --version       # Should show 2.x.x or higher
```

### Step 1: Start MongoDB (Using Compass)

#### 1.1 Open MongoDB Compass
- Launch MongoDB Compass from your applications  
- It will automatically detect your local MongoDB instance  
- You should see a connection string like: `mongodb://localhost:27017`  

#### 1.2 Connect to MongoDB
- Click Connect
- You should see the Databases panel on the left  
- If you see `admin`, `config`, `local` databases, MongoDB is running

### Step 2: Setup Backend (FastAPI)

#### 2.1 Navigate to Backend Folder
```bash
cd backend
```

#### 2.2 Create Python Virtual Environment (Windows)
```bash
python -m venv venv
venv\Scripts\activate
```

#### 2.3 Install Python Dependencies
```bash
pip install -r requirements.txt
```
Expected output: Should install `fastapi`, `uvicorn`, `pymongo`, `python-dotenv`, `pydantic`

#### 2.4 Run the Backend Server
```bash
python -m uvicorn flash_card_app:app --reload
```
Press `Ctrl+C` to quit

### Step 3: Setup Frontend

#### 3.1 Open a new terminal and keep the backend running

#### 3.2 Navigate to Frontend Folder
```bash
cd frontend
```

#### 3.3 Install Node Dependencies
```bash
npm install
```

#### 3.4 Start the Frontend Dev Server
```bash
npm run dev
```
Press `Ctrl+C` to quit

### Step 4: Access the Web App
Open browser and go to:

http://localhost:5173
