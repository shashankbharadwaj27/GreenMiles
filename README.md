# 🌱 Green-Miles

**Green-Miles** is an intelligent system that promotes sustainable mobility by analyzing and predicting vehicle range and energy efficiency for electric and hydrogen vehicles.  
It combines machine learning models, data preprocessing pipelines, and a user-friendly frontend to help users make environmentally conscious transportation decisions.

---

## ⚙️ Tech Stack

### **Backend**

- **Language:** Python
- **Framework:** FastAPI
- **Machine Learning:** XGBoost, Scikit-Learn, NumPy, Pandas
- **Data Handling:** Pydantic (Schemas), Custom Preprocessing Scripts
- **API Routing:** FastAPI Routers (under `/routes`)

### **Frontend**

- **Framework:** React.js
- **Styling:** Tailwind CSS
- **HTTP Client:** Axios / Fetch API
- **Build Tool:** Vite

---




## 🚀 Setup Instructions

Follow these steps to get the project running locally:

### Prerequisites

- Node.js & npm / yarn (for frontend)
- Python (version x.x) & pip / venv (for backend)
- Git

### Steps

1. **Clone the repository**
   git clone https://github.com/shashankbharadwaj27/GreenMiles.git
   cd Green-Miles
2. **Backend**
    cd Backend
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    uvicorn main:app --reload
3. **Frontend**
    cd Frontend
    npm install
    npm start
4. **Access application**
    Open browser and go to http://localhost:3000
    The frontend will communicate with backend


### ScreenShots

**Homepage**
![Homepage](assets/home.png)

**EV Page**
![EV Page](assets/ev.png)

**EV Result Page**
![EV Result Page](assets/evresult.png)

**HV Page**
![HV Page](assets/hv.png)

**HV Result Page**
![HV Result Page](assets/hvresult.png)





## Folder Structure

```
Green-Miles/
├── Backend/
│ ├── app/
│ │ ├── models.py
│ │ ├── views / controllers/
│ │ ├── serializers (if API) / schemas
│ │ ├── urls / routes
│ │ └── etc.
│ ├── manage.py (or equivalent entry)
│ ├── requirements.txt
│ └── ... (other backend configs, settings, migrations)
├── Frontend/
│ ├── public/
│ ├── src/
│ │ ├── components/
│ │ ├── pages / views
│ │ ├── services / api
│ │ └── store / state
│ ├── assets / styles
│ ├── package.json
│ └── ... (other frontend config)
├── .gitignore
└── README.md
```
