# chrono_odyssey_features

# chrono_odyssey_features

Features developed with AI.

## Table of Contents

- [About](#about)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Clone the Repository](#clone-the-repository)
  - [Backend Setup (Python)](#backend-setup-python)
  - [Frontend Setup (Node.js)](#frontend-setup-nodejs)
- [Contributing](#contributing)
- [License](#license)

---

## About

This repository contains features developed with AI for the Chrono Odyssey project. It includes a Python backend and a Node.js/React frontend.

## Project Structure

```
.
├── backend/
│   └── transcripter-backend/
│       ├── src/
│       ├── requirements.txt
│       └── README.md
├── frontend/
│   ├── src/
│   ├── package.json
│   └── README.md
└── README.md
```

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/javq36/chrono_odyssey_features.git
cd chrono_odyssey_features
```

---

### Backend Setup (Python)

1. **Navigate to the backend directory:**
    ```bash
    cd backend/transcripter-backend
    ```

2. **Create and activate a virtual environment:**
    - On Windows:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the backend:**
    ```bash
    python src/app.py
    ```

---

### Frontend Setup (Node.js)

1. **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2. **Install dependencies:**
    ```bash
    npm install
    ```

3. **Run the frontend:**
    ```bash
    npm run dev
    ```

---

## Contributing

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add some feature"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a pull request.

---

## License

This project is licensed under the MIT License.
