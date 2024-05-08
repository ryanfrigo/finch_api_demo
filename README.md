# Finch API Demo

This is a simple streamlit app that integrates with the Finch API Sandbox. 

All 29 mock providers are supported.

The access_token for the provider selected is only saved in the current browser session. 

The following endpoints are used:
- sandbox/create
- employer/company
- employer/directory
- employer/individual
- employer/employment

To run this app, create a new virtualenv:
```virtualenv venv```

If you don't have virtualenv, install it:
```pip install virtualenv```

Activate it:
```. venv/bin/activate```

Install streamlit: 
```pip install -r requirements.txt```

Run the app:
```streamlit run app.py```