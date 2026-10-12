# Employee Attrition Prediction System

Full-stack educational starter using Python, Flask, scikit-learn, React, and Vite. It compares Logistic Regression and Random Forest, saves a preprocessing/model pipeline, and provides a form that calls a prediction API.

## Dataset
A small **synthetic demo dataset** is included so you can test the flow immediately. It is not real employee data and the model metrics are not meaningful for real-world or assignment reporting. Replace `data/Employee.csv` with your official assignment dataset before training or reporting results.

Required columns: `Education`, `JoiningYear`, `City`, `PaymentTier`, `Age`, `Gender`, `EverBenched`, `ExperienceInCurrentDomain`, `LeaveOrNot`. `LeaveOrNot`: 0 = stay, 1 = leave.

## Run on Windows PowerShell
Run these commands from the project root (`employee-attrition-prediction-system`).

1. Install Python packages:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\python.exe -m pip install --upgrade pip
   .\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
   ```
2. Train and save the model:
   ```powershell
   .\.venv\Scripts\python.exe backend\train_model.py
   ```
   Generates `backend/model/pipeline.pkl` and `backend/model/metrics.json`. The script reports accuracy, precision, recall, F1, ROC-AUC, confusion matrices and feature importance where supported.
3. Start Flask in a terminal:
   ```powershell
   .\.venv\Scripts\python.exe backend\app.py
   ```
   API: `http://127.0.0.1:5000`; health: `/health`; model metrics: `/model-info`; prediction: `POST /predict`.
4. Open a second terminal and start React:
   ```powershell
   cd frontend
   npm install
   npm run dev
   ```
   Open the Vite URL shown, usually `http://127.0.0.1:5173`.

## Sample prediction JSON
```json
{
  "Education": "Bachelors",
  "JoiningYear": 2022,
  "City": "Bangalore",
  "PaymentTier": 2,
  "Age": 28,
  "Gender": "Male",
  "EverBenched": "No",
  "ExperienceInCurrentDomain": 2
}
```

## GitHub
Do not upload `.venv` or `node_modules`. Review dataset licensing and institutional requirements before publishing data. The demo dataset is synthetic.
```bash
git init
git add .
git commit -m "Initial employee attrition prediction system"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

## Responsible use
This is an educational demo, not a validated HR decision system. Predictions may be wrong and may reflect bias in the data. Do not use outputs as the sole basis for hiring, firing, promotion, or other consequential employment decisions. The training script is a simple single train/test split; use a separate validation set for rigorous model selection.
