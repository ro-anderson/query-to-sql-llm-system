## text2sql System

## What is that project?
This project aims to implenent text2sql technique trough python, LangChain and streamlit. 

### How to run?

1. create **.env** from **.dev.env**.

```bash
OPENAI_API_KEY=""
DB_HOST=""
DB_USER=""
DB_PASSWORD=""
DB_NAME=""
```

2. Config your python environment and run the server:
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

the server will be running at:
```bash
http://localhost:8501/
```

### How it works?

![app running](./images/sample.gif)
