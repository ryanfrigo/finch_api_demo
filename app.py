import streamlit as st
import requests
import json

base_url = 'https://sandbox.tryfinch.com/api/'

provider_dict = {
    'ADP Run': 'adp_run',
    'Bamboo HR': 'bamboo_hr',
    'Bamboo HR (API)': 'bamboo_hr_api',
    'HiBob': 'bob',
    'Gusto': 'gusto',
    'Humaans': 'humaans',
    'Insperity': 'insperity',
    'Justworks': 'justworks',
    'Namely': 'namely',
    'Paychex Flex': 'paychex_flex',
    'Paychex Flex (API)': 'paychex_flex_api',
    'Paycom': 'paycom',
    'Paycom (API)': 'paycom_api',
    'Paylocity': 'paylocity',
    'Paylocity (API)': 'paylocity_api',
    'Personio': 'personio',
    'Quickbooks': 'quickbooks',
    'Rippling': 'rippling',
    'Sage HR': 'sage_hr',
    'Sapling': 'sapling',
    'Squoia One': 'sequoia_one',
    'Square Payroll': 'square_payroll',
    'Trinet': 'trinet',
    'Trinet (API)': 'trinet_api',
    'Ulti Pro': 'ulti_pro',
    'Wave': 'wave',
    'Workday': 'workday',
    'Zenefits': 'zenefits',
    'Zenefits (API)': 'zenefits_api'
}

endpoint_dict = {
    'Employee Directory': 'employer/directory'
}

def create_provider(provider_id, employee_size=10):
    url = f'{base_url}/sandbox/create'
    headers = {
        'Content-Type': 'application/json'
    }
    data = {
        'provider_id': provider_id,
        'products': ['company', 'directory', 'individual', 'employment'],
        'employee_size': employee_size
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def get_request(access_token, endpoint):
    url = f'{base_url}{endpoint}'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 501:
        st.error("Finch does not support this specific endpoint for this specific provider.")
        return None
    return response.json()

def individual_data(access_token, individual_ids, endpoint):
    url = f'{base_url}{endpoint}'
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "requests": [{"individual_id": ind_id} for ind_id in individual_ids]
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 501:
        st.error("Finch does not support this specific endpoint for this specific provider.")
        return None
    return response.json()

def main():
    st.title('Finch API Sandbox Demo')

    if 'access_token' not in st.session_state:
        st.session_state['access_token'] = None

    provider = st.selectbox('Select a Provider', list(provider_dict.keys()))

    if st.button('sandbox/create'):
        provider_json = create_provider(provider_dict[provider])
        if provider_json:
            st.session_state['access_token'] = provider_json.get('access_token')
            st.json(provider_json, expanded=False)

    if st.session_state['access_token']:
        company_info = get_request(st.session_state['access_token'], 'employer/company')
        if company_info:
            st.markdown('## employer/company')
            st.json(company_info, expanded=False)

        employee_directory = get_request(st.session_state['access_token'], 'employer/directory')
        if employee_directory:
            st.markdown('## employer/directory')
            st.json(employee_directory, expanded=False)

            individual_names = [f"{ind['first_name']} {ind['last_name']}" for ind in employee_directory['individuals']]
            selected_name = st.selectbox("Select an individual:", individual_names, key='individual_selector')

            selected_individual_id = next(ind['id'] for ind in employee_directory['individuals'] if f"{ind['first_name']} {ind['last_name']}" == selected_name)

            individual_details = individual_data(st.session_state['access_token'], [selected_individual_id], 'employer/individual')
            if individual_details:
                st.markdown('### employer/individual')
                st.json(individual_details)

            employment_details = individual_data(st.session_state['access_token'], [selected_individual_id], 'employer/employment')
            if employment_details:
                st.markdown('### employer/employment')
                st.json(employment_details)


if __name__ == '__main__':
    main()