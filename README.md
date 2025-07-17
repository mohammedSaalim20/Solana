# MEV Transaction Analyzer for Solana

This project is a Django-based MEV (Maximal Extractable Value) transaction analyzer for the Solana blockchain. It utilizes the Helius API to fetch and decode MEV-related transactions and provides a RESTful API to access the data.

---

## 📦 Project Structure

```
solana_mev/
├── manage.py
├── solana_mev/
│   └── settings.py
├── mev_analyzer/
│   └── scripts/
│       └── mev_decoder.py
├── cli_dashboard.py        # Optional (for real-time CLI monitoring)
└── .env                    # Contains HELIUS_API_KEY
```

---

## 🚀 Getting Started
### 1. Clone the repository

```bash
git clone https://github.com/mohammedSaalim20/Solana.git
cd solana-mev-analyzer
```

### 2. Create & activate a virtual environment (optional but recommended)

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your API key to the `.env` file

```
HELIUS_API_KEY=your_api_key_here
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Run the development server

```bash
python manage.py runserver
```

---

##  Fetching MEV Transactions

To pull fresh MEV data from the Helius API:

```bash
python manage.py fetch_txns
```

This will populate your database with MEV transactions fetched via your `HELIUS_API_KEY`.

---

##  API Endpoints

### 1.  Get All MEV Transactions

* **URL:** `http://127.0.0.1:8000/api/mev/`
* **Method:** GET
* **Description:** Returns all MEV transactions sorted by newest first.

### 2.  Get Transaction by Hash

* **URL:** `http://127.0.0.1:8000/api/mev/<tx_hash>/`
* **Method:** GET
* **Example:** `http://127.0.0.1:8000/api/mev/3Hd91EK1j6FG7rKrABCxyz987/`

### 3.  Filter by Wallet Address

* **URL:** `http://127.0.0.1:8000/api/mev/?wallet=<wallet_address>`
* **Example:** `http://127.0.0.1:8000/api/mev/?wallet=9Fn87xKD3xABpqRS`

### 4. ️ Filter by Platform

* **URL:** `http://127.0.0.1:8000/api/mev/?platform=<platform>`
* **Example:** `http://127.0.0.1:8000/api/mev/?platform=Jupiter`

###  Optional: Combine Filters

You can filter by both wallet and platform:

```bash
http://127.0.0.1:8000/api/mev/?wallet=9Fn87xKD3xABpqRS&platform=Jupiter
```

---

##  Optional: Live CLI Dashboard

You can add a `cli_dashboard.py` to monitor real-time transaction status in the terminal.

Example entry point:

```bash
python cli_dashboard.py
```

---

##  Environment Variables

Ensure your `.env` file includes the following:

```
HELIUS_API_KEY=<your-helius-api-key>
```

---

##  Technologies Used

* Django
* Django REST Framework
* Helius API
* Python dotenv

---

