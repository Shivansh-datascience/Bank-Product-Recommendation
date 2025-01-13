import pymongo.mongo_client
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_ollama.llms import OllamaLLM

# Setting the title for the Chatbot application
st.title("Bank Product Recommendation System")

# Building a model for product recommendation
product_interested = st.sidebar.selectbox(
    label="Select the Type of Product you are interested in",
    options=['savings account', 'checking account', 'loan', 'credit card', 'None'],
    label_visibility="visible"
)

# Adding the session event to store the value in the browser side
if product_interested != 'None':
    st.session_state['product_interested'] = product_interested
    st.sidebar.write(f"You selected: {st.session_state['product_interested']}")
else:
    st.sidebar.error("Please select a product type.")

# Collecting income, credit score, loan amount, and repayment period from the user
income = st.sidebar.number_input(
    label="Enter your annual income",
    label_visibility="visible"
)

if income:
    st.session_state['income'] = income
    st.sidebar.write(f"You selected: {st.session_state['income']}")
else:
    st.sidebar.error("Please enter your income.")

credit_score = st.sidebar.text_input(
    label="Enter your credit score",
    label_visibility="visible"
)

if credit_score:
    st.session_state['credit_score'] = credit_score
    st.sidebar.write(f"You selected: {st.session_state['credit_score']}")
else:
    st.sidebar.error("Please enter your credit score.")

loan_amount = st.sidebar.text_input(
    "If you are looking for a loan, how much would you like to borrow?"
)

if loan_amount:
    st.session_state['loan_amount'] = loan_amount
    st.sidebar.write(f"You selected: {st.session_state['loan_amount']}")
else:
    st.sidebar.error("Please enter your loan amount.")

repayment_period = st.sidebar.text_input(
    "What is your preferred repayment period for the loan (in years)?"
)

if repayment_period:
    st.session_state['repayment_period'] = repayment_period
    st.sidebar.write(f"You selected: {st.session_state['repayment_period']}")
else:
    st.sidebar.error("Please enter your repayment period.")

# Building the customer data dictionary
customer_data = {
    'product_interested': st.session_state.get('product_interested'),
    'income': st.session_state.get('income'),
    'credit_score': st.session_state.get('credit_score'),
    'loan_amount': st.session_state.get('loan_amount'),
    'repayment_period': st.session_state.get('repayment_period')
}

# Initialize Ollama model
ollama_model = OllamaLLM(model="llama2", temperature=0.7)

# Define the Prompt template
template = """
You are a bank assistant. Based on the user's input, recommend a suitable bank product (e.g., loan, savings account, credit card, etc.).

User's input:
Product Type: {product_interested}
Income: {income}
Credit Score: {credit_score}
Loan Amount: {loan_amount}
Repayment Period: {repayment_period}

Recommend a suitable product based on these details.
"""

# Creating a prompt template with the expected input variables
prompts = PromptTemplate(
    input_variables=['product_interested', 'income', 'credit_score', 'loan_amount', 'repayment_period'],
    template=template,
    template_format="f-string"
)

# Function to generate the response
def generate_response(ollama_model, prompts, customer_data):
    chain = LLMChain(llm=ollama_model, prompt=prompts)
    response = chain.run(
        product_interested=customer_data['product_interested'],
        income=customer_data['income'],
        credit_score=customer_data['credit_score'],
        loan_amount=customer_data['loan_amount'],
        repayment_period=customer_data['repayment_period']
    )
    return response

# Recommendation button
recommendation_button = st.button(label="Get recommendation")

if recommendation_button:
    if all([customer_data['product_interested'], customer_data['income'], customer_data['credit_score'], customer_data['loan_amount'], customer_data['repayment_period']]):
        response = generate_response(ollama_model, prompts, customer_data)
        st.write(f"AI Recommendations: {response}")
    else:
        st.error("Please fill in all the fields to get a recommendation.")