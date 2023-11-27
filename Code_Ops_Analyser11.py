# %% [markdown]
# **NOTES**

# %%
## dash app to download word file from browser to local

##dash app using dash bootstrap component with input textarea, submit button, emailto button, and output textarea which will display output in output textarea when submit button is pressed and will open a popup window which will take output to send email when emailto button is pressed

# %%


# %% [markdown]
# **PACKAGE INSTALLATION**

# %%
# !pip install dash --upgrade
# !pip install dash-bootstrap-components 
# !pip install openai
# !pip install python-docx
# !pip install pandas
# !pip uninstall dash jupyter_dash
# !pip install jupyter-dash
# !pip install dash --upgrade
# !pip install dash-bootstrap-components 
# !pip install flask_mail
# !pip install flask flask-wtf flask-bootstrap email-validator
# !pip install pytesseract

# %% [markdown]
# **IMPORTING LIBRARIES**

# %%
import os
import openai
import docx
import pandas as pd
import re
import tkinter as tk
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import webbrowser
import datetime
import dash
from dash import Input, Output, dcc, html
import base64
from jupyter_dash import JupyterDash
from dash.exceptions import PreventUpdate
import pytesseract
from PIL import ImageTk, Image
import io
import time
import sqlite3
import logging
from cryptography.fernet import Fernet
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
from Google import Create_Service
import io
from googleapiclient.http import MediaIoBaseDownload
import uuid
import random
#from pysqlcipher3 import dbapi2 as sqlcipher
# %%

logging.basicConfig(filename='applogs.log',level=logging.ERROR)
# %% [markdown]
# **SQL Query generation**

# %%
# Preset 01: Generate SQL Queries
def run_preset_01(query):
  
  response = openai.Completion.create(
    # The engine, or model, which will generate the completion. Some engines are suitable for natural language tasks, others specialize in code  
    engine="code-davinci-001",
    # the query to be completed in natural language. i.e. prompt="### Postgres SQL tables, with their properties:\n#\n# Employee(id, name, department_id)\n# Department(id, name, address)\n# Salary_Payments(id, employee_id, amount, date)\n#\n### A query to list the names of the departments which employed more than 10 employees in the last 3 months\nSELECT",
    prompt=query,
    # The temperature controls the randomness of the answer. 0.0 is the most deterministic and repetitive value
    temperature=0,
    # The maximum number of tokens to generate
    max_tokens=150,
    # Controls diversity via nucleus sampling. 0.5 means all of all likeliwood-weighted options are considered
    top_p=1.0,
    # Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.
    frequency_penalty=0.0,
    # Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.
    presence_penalty=0.0,
    # Up to 4 sequences where the API will stop generating further tokens. The returned text will not contain the stop sequence.
    stop=["#", ";"]
  )

  return response.choices[0].text


# %% [markdown]
# **Simple Java Class generation**

# %%
# Preset 07: Java Code generation
def run_preset_07(query):
  
  response = openai.Completion.create(
    engine="code-davinci-001",
    # i.e. prompt="/* A Java class used to represent a person with name, age and gender attributs */\npublic class Person",
    prompt=query,
    temperature=0,
    max_tokens=300,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=["/*"]
  )

  return response.choices[0].text

# %% [markdown]
# **Python Developper Task List**

# %%
# Preset 08: Python Developper Task list
def run_preset_08(query):
 
  response = openai.Completion.create(
    engine="code-davinci-001",
    # i.e. prompt="\"\"\"\n1. Create a list of first names\n2. Create a list of last names\n3. Combine them randomly into a list of 100 full names\n\"\"\"",
    prompt=query,
    temperature=0,
    max_tokens=500,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
  )

  return response.choices[0].text

# %% [markdown]
# **Summerize a text**

# %%
# Preset 09: Summerize a text
def run_preset_09(query):

  response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=f"""Summarize the following text: "{query}" """,
    temperature=0.7,
    max_tokens=2000,
    top_p=0.90,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    ##stop=["\n"]
  )

  return response.choices[0].text

# %% [markdown]
# **Simplify a text**

# %%
# Preset 10: Simplify a text
def run_preset_10(query):

  response = openai.Completion.create(
    engine="text-davinci-003",
    # i.e. prompt="My ten-year-old asked me what this passage means:\n\"\"\"\nA neutron star is the collapsed core of a massive supergiant star, which had a total mass of between 10 and 25 solar masses, possibly more if the star was especially metal-rich.[1] Neutron stars are the smallest and densest stellar objects, excluding black holes and hypothetical white holes, quark stars, and strange stars.[2] Neutron stars have a radius on the order of 10 kilometres (6.2 mi) and a mass of about 1.4 solar masses.[3] They result from the supernova explosion of a massive star, combined with gravitational collapse, that compresses the core past white dwarf star density to that of atomic nuclei.\n\"\"\"\n\nI rephrased it for him, in plain language a ten-year-old can understand:\n\"\"\"\n",
    prompt=f"""Simplify the following text for ten-year old - '{query}' """,
    temperature=1,
    max_tokens=2000,
    top_p=0.88,
    frequency_penalty=0,
    presence_penalty=0,
  )

  return response.choices[0].text

# %% [markdown]
# **Free Text**

# %%
def run_preset_11(query):
  query = query.strip()
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": query}],
    # prompt=query,
    temperature=0.2,
    max_tokens=1500,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
)
  return response.choices[0].message.content

# %% [markdown]
# **Code Generation**

# %%
def run_preset_12(query):
  response = openai.Completion.create(
    model="code-davinci-003",
    prompt=query,
    temperature=0.2,
    max_tokens=700,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    #stop=[" Human:", " AI:"]
)
  return response.choices[0].text

# %%
def run_preset_13(query):
  query = query.strip()
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": query + " Only give the analysis and steps to solve the issue everything in english."}],
    # prompt=query,
    temperature=0.2,
    max_tokens=1500,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
)
  return response.choices[0].message.content

def run_preset_14(query):
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": query}],
    # prompt=query,
    temperature=0.2,
    max_tokens=1500,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.6,
    stop=[" Human:", " AI:"]
)
  return response.choices[0].text

def get_sentiments_from_openai(textarea):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt = f"Statement:\n\"मैं आज़ादपुर, दिल्ली मे रहता हुँ। मेरे मोबाइल मे नेटवर्क होने के बावजूद इंटरनेट नही चलता। कृपया, कुछ करे। @cankkasera Jio का नेटवर्क जिस तरह से चल रहा है न, सरकार को इसका नाम बदलकर... घुट घुट के जियो कर देना चाहिये\"  1st (write 3 one word sentiments with emoji comma separated), 2nd (describe intentions of speaker in atmost 3 sentences). 3rd (tell the product and services used by customer). 4th (write a twitter response to manage customer's sentiments). 5th (suggest the actions for the operation team step by step). 6th (give estimated net promoter score in scale of 5 show 👍 if greater than 2 or 👎 if less than 3)\n\nAnswer:\nDisappointed 😞, Frustrated 😠, Helpless 🥺\n\nThe speaker is expressing their frustration and disappointment with the Jio network not working despite having signal. They are requesting help from the service provider.\n\nThe customer is using Jio network for their mobile service.\n\n\"We apologize for the inconvenience caused. Our team is working to resolve the issue as soon as possible. Please share your contact details via DM so that we can assist you better. #JioNetworkIssue #CustomerService 🙏\"\n\n1._Acknowledge_the_complaint_and_express_empathy_towards_the_customer's_issue. 2._Investigate_the_issue_and_determine_the_root_cause. 3._Provide_regular_updates_to_the_customer_on_the_progress_of_the_investigation_and_resolution. 4._Take_necessary_actions_to_fix_the_issue_and_ensure_that_it_does_not_happen_again. 5._Follow_up_with_the_customer_to_ensure_that_their_issue_has_been_resolved_satisfactorily.\n\n2\n\n👎\n##\n\nStatement:\n\"{textarea}\" 1st (write 3 one word sentiments with emoji comma separated), 2nd (describe intentions of speaker in atmost 3 sentences). 3rd (tell the product and services used by customer). 4th (write a twitter response to manage customer's sentiments). 5th (suggest the actions for the operation team step by step). 6th (give estimated net promoter score in scale of 5 show 👍 if greater than 2 or 👎 if less than 3)\n\nAnswer:",
        # prompt=f"Statement:\n\"Thank you so much! for such a lovely gift. \" 1st write 3 one word sentiments with emoji comma separated, 2nd describe intentions of speaker in atmost 3 sentences, 3rd tell the product and services used by customer in and write a twitter response with emojis to manage customer's sentiments.\n\nAnswer:\nGratitude 🙏, Appreciation 🥰, Happiness 😊\n\nThe speaker's intentions are to express their gratitude and appreciation for the lovely gift they have received. The speaker's tone and choice of words suggest that they are feeling a sense of joy and delight in the gesture. The phrase \"thank you so much!\" conveys the speaker's heartfelt appreciation for the thoughtful gift and their sincere gratitude for the kindness shown.\n\nUnspecified gift\n\n\"Thank you for your kind gesture! 🙏🎁❤️ I appreciate your thoughtfulness and the effort you put into selecting such a wonderful gift. It really made my day! 😊\"\n##\n\nStatement:\n\"{textarea}\" \n\nAnswer:\n",
        temperature=0.4,
        max_tokens=1500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["##"]
        )
    return response.choices[0].text

def get_functional_test_response(textarea):
    metadata = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Statement:\n\"To verify the agent is able to add order for an New Customer BYOD(Retail) for a postpaid-4gb\" write a functional test case having the followings - \n1. Test Case Name\n2. Test Objective\n3. Preconditions\n4. Inputs\n5. Pass Criteria\n6. Fail Criteria\n\nAnswer:\n1. Test Case Name: Add Order - New Customer BYOD (Retail) - Postpaid 4GB.\n2. Test Objective: Verify if the agent is able to add an order for a new customer with BYOD (Retail) option for a postpaid 4GB plan.\n3. Preconditions: The agent is logged in and has access to the order management system.\n4. Inputs: Customer details, BYOD option, Postpaid 4GB plan selection.\n5. Pass Criteria: The order creation process completes without any errors or exceptions.\n6. Fail Criteria: The order fails to be added or encounters errors during the process.\n\n\n##\nStatement:\n\"{textarea}\" write a functional test case having the followings - \n1. Test Case Name\n2. Test Objective\n3. Preconditions\n4. Inputs\n5. Pass Criteria\n6. Fail Criteria\n\nAnswer:",
        temperature=0.25,
        max_tokens=800,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["##"]
    )

    time.sleep(30)

    test_result = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Statement:\n\"To verify the agent is able to add order for an New Customer BYOD(Retail) for a postpaid-4gb\" write a functional test case on the following statement and expected result in next line after each test case with same number. \n\nAnswer:\n1. Open the salesforce application by entering the UR \n1. Salesforce should be launched successfully and login page should be opened\n2. Provide Username and Password \n2. Login should be successful\n3. Click on the new buy flow in the salesforce \n3. Salesforce should show a pop-up with options of mobile and Fixed for selection\n4. Click on the Mobile Icon. \n4. Salesforce should show a pop-up with options of postpaid and prepaid for selection\n5. Click on postpaid \n5. Store selection page should be displayed\n6. Select store name and click on next \n6. SSN and Credit check page should be displayed\n7. Enter SSN and confirm SSN and click on check SSN \n7. All the relevant ID fields should be displayed\n8. Fill the data for all available fields under ID Section - like ID Type as \"Puerto Rico Driver License, ID Number, ID Expiration Date, Title, First Name, Last Name, Date of Birth. \n8. Agent must be able to provide all required details\n9. Click on credit check(Check box) and retrieve credit rating\n9. Credit score should be displayed\n10. Click on Continue button. \n10. View should be navigated to Create New Customer Screen.\n11. Fill the data for all available fields under Contact section - like Primary Contact Number, Secondary Contact Number, Email and select the Preferred Language. \n11. Agent must be able to provide all required details\n12. Click on validate Billing address \n12. Agent must be able to confirm that the Address is validated\n13. Click on Create Account button \n13. View should be navigated to Select device page\n14. Select BYOD and click on next \n14. View should navigated to select offer page\n15. Select 4gb plan and click on next \n15.My cart details should be show\n16. Click on next button. \n16. View should be navigated to Billing Details Screen.\n17. Choose desired bill cycle and select Payment method as credit card and provide all values for all relevant fields like bill cycle date, card holder name, card number, expiration date ,postal code and click on save payment method \n17. Agent must be able to provide all required details\n18. Click on Next button \n18. View should be navigated to Delivery Method screen.\n19. Select the SIM details like MSISDN, First name, Last name ,ICCID, SKU number \n19. Agent must be able to provide all required details\n20. Click on next button \n20. View should be navigated to summary page\n21. Check the customer details \n21. Agent should be able to view customer details\n22. Click on next \n22. View should be navigated to Terms & Condition page\n23. Select the Autopay and terms & condition check box \n23. Agent should be able to select check box\n24. Click on next \n24. View should be navigated to Consent page\n25. Select Email me check box \n25. Agent should be able to select Email me check box\n26. Click on Sumbit button \n26. View should be navigated to customer 360 page\n27. Click on order number. \n27. View should be navigated to Orchestration Page\n28. Click on Orchestration Number \n28. Agent should see the Orchestration plan.\n29. Check the orchestration is pass \n29. Orchestration should be passed(All green)\n\n##\nStatement:\n\"{textarea}\" write a functional test case on the following statement and expected result in next line after each test case with same number.\n\nAnswer:",
        temperature=0.25,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["##"]
    )

    time.sleep(30)

    test_data = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Statement:\n\"To verify the agent is able to add order for an New Customer BYOD(Retail) for a postpaid-4gb\" write test data for this functional test case.\n\nAnswer:\n1. Customer Details:\n    • Name: John Smith\n    • Email: john.smith@example.com\n    • Phone Number: 1234567890\n    • Address: 123 Main Street, Anytown, USA\n\n2. Order Details:\n    • Order Type: New Customer BYOD (Retail)\n    • Plan: Postpaid 4GB\n    • Device: None (BYOD)\n    • SIM Card Type: Nano SIM\n    • Activation Date: [Choose a specific date]\n\n3. Billing Information:\n    • Billing Address: Same as customer address\n\n4. Payment Details:\n    • Payment Method: Credit Card\n    • Credit Card Number: [Provide a test credit card number]\n    • Expiration Date: [Choose a future date]\n    • CVV: [Provide a test CVV]\n\n5. Additional Information:\n    • Marketing Opt-in: Yes\n    • Promotional Code: [Leave blank if not applicable]\n\n##\nStatement:\n\"{textarea}\" write test data for this functional test case.\n\nAnswer:",
        temperature=0.25,
        max_tokens=800,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["##"]
    )

    test_result = test_result.choices[0].text
    test_result = test_result.strip()
    test_result = test_result.split('\n')
    switch = 0
    test_result_action = ''
    test_result_expectation = ''
    for i in test_result:
        if switch%2 == 0:
            test_result_action = test_result_action + "\n" + i
        else:
            test_result_expectation = test_result_expectation + "\n" + i
        switch = switch + 1
    print(test_result)
    print(metadata.choices[0].text)
    print(test_data.choices[0].text)
    return metadata.choices[0].text, test_result_action, test_result_expectation, test_data.choices[0].text


def get_test_case_from_openai(code_input, action_selected, code_language):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Satement:\ntest data to use in unit testing that test multiplication of three numbers in python. first write the code then at last write Test Case Name, Test Objective, Unit under test, Preconditions, Inputs, Expected Results, Pass Criteria, Fail Criteria after three backslashes '///'\n\nAnswer:\nimport unittest\n\nclass TestMultiplication(unittest.TestCase):\n\n    def test_multiply_three_numbers(self):\n        # Test Case 1\n        result = multiply(2, 3, 4)\n        self.assertEqual(result, 24)\n\n        # Test Case 2\n        result = multiply(-2, 3, 5)\n        self.assertEqual(result, -30)\n\n        # Test Case 3\n        result = multiply(1.5, 2.5, 3.5)\n        self.assertAlmostEqual(result, 13.125)\n\n        # Test Case 4\n        result = multiply(0, 1, 2)\n        self.assertEqual(result, 0)\n        \n        # Test Case 5\n        result = multiply(4, 5, 0.5)\n        self.assertAlmostEqual(result, 10.0)\n        \n        # Test Case 6\n        result = multiply(10, -2, -0.5)\n        self.assertAlmostEqual(result, 1.0)\n\n///\nTest Case Name: Addition of Two Numbers\nTest Objective: To verify the correctness of the addition operation\nUnit under test: Addition class or method\nPreconditions: None\nInputs: Two numbers to be added\nExpected Results: The expected sum of the two numbers\nPass Criteria: The actual sum matches the expected sum\nFail Criteria: The actual sum does not match the expected sum\n##\nSatement:\ntest data to use in unit testing that test "+code_input+" in "+code_language+". first write the code then at last write Test Case Name, Test Objective, Unit under test, Preconditions, Inputs, Expected Results, Pass Criteria, Fail Criteria after three backslashes '///'\n\nAnswer:",
        temperature=0.25,
        max_tokens=2652,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["##"]
    )

    return response.choices[0].text

def sqloptimizer(textarea):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "user",
                "content": "SELECT customer.name, order.order_date, product.name, quantity FROM customer JOIN order ON customer.id = order.customer_id JOIN product ON order.product_id = product.id WHERE order.order_date BETWEEN '2023-01-01' AND '2023-12-31' AND product.category = 'Electronics' AND quantity > 10 2 Questions, 1. is there a optimization problem exists, if yes what are those ? 2 .now following the above best practices , optimize this query "
            },
            {
                "role": "assistant",
                "content": "1. Potential Optimization Issues\na. Indexing: If the columns used in the JOIN and WHERE clauses (customer.id, order.customer_id, order.product_id, product.id, order.order_date, product.category, and quantity) are not indexed, the query may be slower, especially if the tables have a large number of records.\nDatabase Statistics: If the database statistics are outdated, the database might not choose the best execution plan for this query. Keeping statistics up to date helps in optimizing the performance.\nSelecting Necessary Columns: The query seems to be selecting only the necessary columns, which is good. This aspect doesn't require optimization.\nData Segmentation and Partitioning: If the tables are very large, segmenting data using partitioning can be considered to speed up the query, especially focusing on columns used in the WHERE clause, like order_date and category.\n\n2. Optimized Query Following Best Practices\n\nFirst, let's make sure that the necessary indexes are created on the relevant columns to optimize the JOIN and WHERE operations.\n\nCREATE INDEX idx_customer_id ON customer (id);\nCREATE INDEX idx_order_customer_id ON order (customer_id);\nCREATE INDEX idx_order_product_id ON order (product_id, order_date, quantity);\nCREATE INDEX idx_product_id_category ON product (id, category);\nSELECT \n    c.name, \n    o.order_date, \n    p.name, \n    o.quantity \nFROM \n    customer c\nJOIN \n    order o ON c.id = o.customer_id\nJOIN \n    product p ON o.product_id = p.id\nWHERE \n    o.order_date BETWEEN '2023-01-01' AND '2023-12-31'\n    AND p.category = 'Electronics'\n    AND o.quantity > 10;\n\nExplanation:\n\ni. Added indexes to potentially enhance the performance of the JOIN and WHERE operations.\nii. Used aliases for table names to make the query more readable and potentially slightly faster, as it reduces the amount of data that needs to be parsed."
            },
            {
                "role": "user",
                "content": f"{textarea}\n\n2 Questions, 1. is there a optimization problem exists, if yes what are those ? 2 .now following the above best practices , optimize this query "
            }
        ],
        temperature=0,
        max_tokens=1558,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    return response.choices[0].message.content

# %%
def run_preset_None(query):
    return "Enter an action from above"

# %% [markdown]
# **Hide Demographic Information**

# %%
def hideDemogrphics(textarea):
    name_pattern = re.compile(r'\b([A-Z][a-z]*\s*){1,2}\b')
    phone_pattern = re.compile(r'\d{3}[-.\s]??\d{3}[-.\s]??\d{4}')
    email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')

    masked_text = textarea

    #masked_text = name_pattern.sub('***',masked_text)
    masked_text = phone_pattern.sub('9999999999', masked_text)
    masked_text = email_pattern.sub('ad*****@****.com', masked_text)
    return masked_text

def mask_api_key(key):
    if len(key) == 0:
        return "Not Available"
    masked_string = key[:3] + "***" + key[-3:]
    return masked_string

# %% [markdown]
# **DEFINING APP**

# %%
# app = DashProxy(external_stylesheets=['https://use.fontawesome.com/releases/v5.15.3/css/all.css',dbc.themes.DARKLY],prevent_initial_callbacks = True,transforms=[MultiplexerTransform()])
# https://use.fontawesome.com/releases/v5.15.3/css/all.css
app = dash.Dash(external_stylesheets=['https://use.fontawesome.com/releases/v5.15.3/css/all.css',dbc.themes.DARKLY],prevent_initial_callbacks=False,suppress_callback_exceptions=True)
# Define the app's layout using dcc.Location to switch between pages
# app.config.suppress_callback_exceptions = True
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])

app.title = "Synapt-GDK"
openai.api_key = "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"
user_email_address = ""
user_email_password = ""
CLIENT_SECRET_FILE = 'SecretKey.json'
API_NAME = 'drive'
API_VERSION = 'v3'
FOLDER_ID = '13G3Xn9wSfTJCtIZOCRMyqi8VosmV-40z'
SCOPE = ['https://www.googleapis.com/auth/drive']

def send_email(body):
    global user_email_address
    global user_email_password
    sender_email = user_email_address
    receiver_email = 'amitkumar.n@prodapt.com'
    # receiver_email = 'sparshsaxena.a@prodapt.com'
    subject = 'Code Ops Analyser System'
    body = body
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    with smtplib.SMTP('outlook.prodapt.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(sender_email, user_email_password)
        smtp.send_message(msg)
        smtp.quit()

# %% [markdown]
# **Connect to Database**

#%%
##now using sqlite3
# mydb = mysql.connector.connect(
#     host = "localhost",
#     user = "root",
#     password = "admin",
# )

##create database if not exist
# sql_query = "create database if not exists code_ops_analyser"
# cursor = mydb.cursor()
# cursor.execute(sql_query)
# mydb.commit()

##Use database
# sql_query = "use code_ops_analyser"
# cursor = mydb.cursor()
# cursor.execute(sql_query)
# mydb.commit()

##create table if not exist
# sql_query = "create table if not exists fault_tolerance(issue_id int primary key auto_increment,timestamp_ varchar(50),action_selected varchar(100),intent varchar(2000),systems_involved varchar(100),error_message varchar(4000),ocr_text varchar(4000),prompt_selected varchar(2000),result varchar(4000),exe_time float(9,4))"
# cursor = mydb.cursor()
# cursor.execute(sql_query)
# mydb.commit()

##create api table
# sql_query = "create table if not exists user_api_key(api_key_id int primary key auto_increment,api_key varchar(100))"
# cursor = mydb.cursor()
# cursor.execute(sql_query)
# mydb.commit()
try:
    conn = sqlite3.connect('code_ops_analyser.db')
    sql_query = "create table if not exists fault_tolerance(id INTEGER PRIMARY KEY AUTOINCREMENT,timestamp_ TEXT,action_selected TEXT,intent TEXT,systems_involved TEXT,error_message TEXT,ocr_text TEXT,prompt_selected TEXT,result TEXT,exe_time NUMERIC(10,4))"
    conn.execute(sql_query)
    conn.commit()
    conn.close()
    logging.debug('Table fault_tolerance created or already exists')
except Exception as e:
    logging.error(f"Failed to connect/create table fault_tolerance - \n {str(e)}")

try:
    conn = sqlite3.connect('code_ops_analyser.db')
    sql_query = "create table if not exists sentiment_analysis(id INTEGER PRIMARY KEY AUTOINCREMENT, comment TEXT, customer_intentions TEXT, sentiment_classification TEXT, impacted_services TEXT, social_media_handler_action TEXT, action_to_operation TEXT,exe_time NUMERIC(10,4))"
    conn.execute(sql_query)
    conn.commit()
    conn.close()
    logging.debug('Table sentiment_analsis created or already exists')
except Exception as e:
    logging.error(f"Failed to connect/create table sentiment_analysis - \n {str(e)}")

try:
    conn = sqlite3.connect('code_ops_analyser.db')
    sql_query = "create table if not exists code_analysis(id INTEGER PRIMARY KEY AUTOINCREMENT, action_selected TEXT, code_language TEXT, input_code TEXT, prompt_selected TEXT, result TEXT, exe_time NUMERIC(10,4))"
    conn.execute(sql_query)
    conn.commit()
    conn.close()
    logging.debug('Table code_analysis created or already exists')
except Exception as e:
    logging.error(f"Failed to connect/create table code_analysis - \n {str(e)}")

try:
    conn = sqlite3.connect('code_ops_analyser.db')
    sql_query = 'create table if not exists code_generation(id INTEGER PRIMARY KEY AUTOINCREMENT, action_selected TEXT, code_language TEXT, input TEXT, result TEXT, exe_time NUMERIC(10,4))'
    conn.execute(sql_query)
    conn.commit()
    conn.close()
    logging.debug('Table code_generation created or already exists')
except Exception as e:
    logging.error(f"Failed to connect/create table code_generation - \n {str(e)}")

try:
    conn = sqlite3.connect('code_ops_analyser.db')
    sql_query = "create table if not exists doc_generation(id INTEGER PRIMARY KEY AUTOINCREMENT, dropdown TEXT, topic TEXT, output TEXT, exe_time NUMERIC(10,4))"
    conn.execute(sql_query)
    conn.commit()
    conn.close()
    logging.debug('Table doc_generation created or already exists')
except Exception as e:
    logging.error(f"Failed to connect/create table doc_generation - \n {str(e)}")

try:
    conn= sqlite3.connect('user.db')
    sql_query = "create table if not exists user_credentials(id Integer Primary Key, email Text, password Text, apikey Text, key Text)"
    conn.execute(sql_query)
    conn.commit()
    conn.close()
except Exception as e:
    logging.error(f"Failed to connect/create table user_credentials - \n {str(e)}")
# app.config.serve_locally = False

# %% [markdown]
# **HOME LAYOUT**

# %%
home_layout = html.Div(
    children=[
        dbc.Container(
            className="pt-5",
            children=[
                html.H1("Synapt-GDK", className="text-center"),
                # html.Div([
                #     html.Img(src='/assets/MicrosoftTeams-image.png', style={'width': '50px', 'height': '50px', 'float': 'left'}),
                #     html.Div("Desktop Edition (Beta)", style={"color": "red", "font-weight": "bold", "margin-left": "60px"}),
                # ], style={"position": "absolute", "top": 10, "right": 0}),

                html.Div([
                    html.Img(src='/assets/Prodapt-Logo.png', style={'width': '180px', 'height': 'auto', 'float': 'left'}),
                    html.Div("Desktop Edition (Beta)", style={"color": "red", "font-weight": "bold", "display": "inline-block", "float":"right"}),
                ], style={"position": "absolute", "top": 10, "right": 1, "width": "100%", "text-align": "right"}),

                # html.P(id="email-address-output", style={"position": "absolute", "top": 20, "right": 0}),
                # html.P(id="user-password-output", style={"position": "absolute", "top": 40, "right": 0}),
                # html.P(id="api-key-output", style={"position": "absolute", "top": 60, "right": 0}),
                html.Br(),
                html.Br(),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            html.I(
                                className="fas fa-file-invoice fa-lg",
                                style={
                                    "font-size": "48px",
                                    "width": "100%",
                                    "height": "100px",
                                    "line-height": "100px",
                                    "text-align": "center",
                                },
                            )
                        ),
                        dbc.Col(
                            html.I(
                                className="fas fa-file-code fa-lg",
                                style={
                                    "font-size": "48px",
                                    "width": "100%",
                                    "height": "100px",
                                    "line-height": "100px",
                                    "text-align": "center",
                                },
                            )
                        ),
                        dbc.Col(
                            html.I(
                                className="fas fa-code fa-lg",
                                style={
                                    "font-size": "48px",
                                    "width": "100%",
                                    "height": "100px",
                                    "line-height": "100px",
                                    "text-align": "center",
                                },
                            )
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button(
                                "Doc Generation",
                                color="primary",
                                style={"width": "100%", "font-size": "27px"},
                                href="/docgeneration",
                            )
                        ),
                        dbc.Col(
                            dbc.Button(
                                "Code Analysis",
                                color="primary",
                                style={"width": "100%", "font-size": "27px"},
                                href="/codeanalysis",
                            )
                        ),
                        dbc.Col(
                            dbc.Button(
                                "Code Generation",
                                color="primary",
                                style={"width": "100%", "font-size": "27px"},
                                href="/codegeneration",
                            )
                        ),
                    ]
                ),
                html.Br(),
                html.Br(),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            html.I(
                                className="fas fa-bug fa-lg",
                                style={
                                    "font-size": "48px",
                                    "width": "100%",
                                    "height": "100px",
                                    "line-height": "100px",
                                    "text-align": "center",
                                },
                            )
                        ),
                        dbc.Col(
                            html.I(
                                className="fas fa-language fa-lg",
                                style={
                                    "font-size": "48px",
                                    "width": "100%",
                                    "height": "100px",
                                    "line-height": "100px",
                                    "text-align": "center",
                                    "color": "white",
                                },
                            )
                        ),
                        dbc.Col(
                            html.I(
                                className="fas fa-bug fa-lg",
                                style={
                                    "font-size": "48px",
                                    "width": "100%",
                                    "height": "100px",
                                    "line-height": "100px",
                                    "text-align": "center",
                                },
                            )
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button(
                                "Test Scenario Generation",
                                color="primary",
                                style={"width": "100%", "font-size": "27px"},
                                href="/test-scenario-generation",
                            )
                        ),
                        dbc.Col(
                            dbc.Button(
                                "Auto Test Generator",
                                color="primary",
                                style={"width": "100%", "font-size": "27px"},
                                href="/testgenius",
                            )
                        ),
                        dbc.Col(
                            dbc.Button(
                                "Fault Lens",
                                color="primary",
                                style={"width": "100%", "font-size": "27px"},
                                href="/fault_analysis",
                            )
                        ),
                    ]
                ),
                html.Br(),
                html.Br(),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(
                            html.I(
                                className="fas fa-file-code fa-lg",
                                style={
                                    "font-size": "48px",
                                    "width": "100%",
                                    "height": "100px",
                                    "line-height": "100px",
                                    "text-align": "center",
                                },
                            )
                        ),
                        dbc.Col(
                            html.I(
                                className="fas fa-user fa-lg",
                                style={
                                    "font-size": "48px",
                                    "width": "100%",
                                    "height": "100px",
                                    "line-height": "100px",
                                    "text-align": "center",
                                },
                            )
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Button(
                                "RCA",
                                color="primary",
                                style={"width": "100%", "font-size": "27px"},
                                href="/api-analysis",
                            )
                        ),
                        dbc.Col(
                            dbc.Button(
                                "Usage Insights",
                                color="primary",
                                style={"width": "100%", "font-size": "27px"},
                                href="/user_stats",
                            )
                        ),
                    ]
                ),
                html.Br(),
                html.Br(),
                # dbc.Row(
                #     [
                #         dbc.Col(
                #             dbc.Input(
                #                 type="text",
                #                 id="api-key-input",
                #                 placeholder="Enter your OpenAI API key here...",
                #                 style={"margin": "16px 0px 0px 0px"},
                #             ),
                #             width=4,
                #         ),
                #         dbc.Col(
                #             dbc.Input(
                #                 type="text",
                #                 id="email-address-input",
                #                 placeholder="Enter your email address",
                #                 style={"margin": "16px 0px 0px 0px"},
                #             ),
                #             width=4,
                #         ),
                #         dbc.Col(
                #             dbc.Input(
                #                 type="password",
                #                 id="user-password-input",
                #                 placeholder="Enter your email password...",
                #                 style={"margin": "16px 0px 0px 0px"},
                #             ),
                #             width=3,
                #         ),
                #         dbc.Col(
                #             dbc.Button(
                #                 "Submit",
                #                 id="user-credentials-submit-button",
                #                 color="primary",
                #                 className="mt-3",
                #             ),
                #             width=1,
                #         ),
                #     ]
                # ),
                # dbc.Row(
                #     [
                #         dbc.Col(
                #             html.A("Find your API Key here", href="https://platform.openai.com/account/api-keys", target="_blank"),
                #             width=3,
                #         ),
                #         dbc.Col(width=2),
                #         dbc.Col(
                #             html.P(
                #                 "Enter only the fields which you want to update (check top right corner for info.)",
                #                 style={"color": "#666666", "margin": "0px 0px 0px 109px"},
                #             )
                #         ),
                #     ],
                #     style={"align-content": "center"},
                # ),
            ],
        ),
    ]
)

def get_user_credentials():
    conn = sqlite3.connect('user.db')
    sql_query = "Select email, password, apikey, key from user_credentials where id =?"
    query_values = (1,)
    data = conn.execute(sql_query,query_values)
    data = data.fetchall()
    conn.close()
    if len(data) == 0:
        user_email, user_password, user_apikey, user_key, data_present = "","","","",0
    else:
        user_email, encrypt_password, user_apikey, user_key, data_present= data[0][0], data[0][1], data[0][2], data[0][3], len(data)
        f = Fernet(user_key)
        user_password = f.decrypt(encrypt_password).decode('utf-8')
    return user_email, user_password, user_apikey, user_key, data_present

def delete_user_credentials():
    conn = sqlite3.connect('user.db')
    sql_query = "DELETE from user_credentials where id = ?"
    query_values = (1,)
    conn.execute(sql_query,query_values)
    conn.commit()
    conn.close()

def insert_user_credentials(new_email_address, new_user_password, new_api_key):
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypt_password = f.encrypt(new_user_password.encode('utf-8'))
    conn = sqlite3.connect('user.db')
    sql_query = "Insert into user_credentials(id, email, password, apikey, key) Values (?,?,?,?,?)"
    query_values = (1, new_email_address, encrypt_password, new_api_key, key)
    conn.execute(sql_query,query_values)
    conn.commit()
    conn.close()

@app.callback(
    # Output('api-key-output','children'),
    # Output('email-address-output','children'),
    # Output('user-password-output','children'),
    Output('api-key-input','value'),
    Output('email-address-input','value'),
    Output('user-password-input','value'),
    Input('user-credentials-submit-button','n_clicks'),
    State('api-key-input','value'),
    State('email-address-input','value'),
    State('user-password-input','value'),
)
def show_input(n_clicks, new_api_key, new_email_address, new_user_password):
    data_present = 0
    user_email, user_password, user_apikey, user_key, data_present = get_user_credentials()
    global user_email_address
    global user_email_password
    user_email_address = user_email
    user_email_password = user_password

    if user_email == '':
        user_email_status = "Not Set"
    else:
        user_email_status = "Set"
    if user_password == '':
        user_password_status = "Password Not Set"
    else:
        user_password_status = "Password Set"

    if n_clicks is None:
        openai.api_key = user_apikey
        return "Your API key- "+mask_api_key(user_apikey),"Email id "+ user_email_status, user_password_status,"","",""
    if data_present == 0:
        insert_user_credentials(new_email_address, new_user_password, new_api_key)
    else:
        if new_api_key == '':
            new_api_key = user_apikey
        if new_email_address == '':
            new_email_address = user_email
        if new_user_password == '':
            new_user_password = user_password
        delete_user_credentials()
        insert_user_credentials(new_email_address, new_user_password, new_api_key)
    user_email, user_password, user_apikey, user_key, data_present = get_user_credentials()
    if user_email == '':
        user_email_status = "Not Set"
    else:
        user_email_status = "Set"
    if user_password == '':
        user_password_status = "Password Not Set"
    else:
        user_password_status = "Password Set"
    openai.api_key = user_apikey
    
    # return "Your API key- "+mask_api_key(user_apikey), "Email id "+ user_email_status, user_password_status,'','',''

# %% [markdown]
# **FAULT ANALYSIS PAGE LAYOUT AND FUNCTIONALITY**
new_systems_involved = [
    {'label': html.Span('Siebel CRM', style={'color': '#0778EB'}), 'value': 'Siebel CRM'},
    {'label': html.Span('BRM', style={'color': '#0778EB'}),'value':'BRM'},
    {'label': html.Span('AIA', style={'color': '#0778EB'}), 'value': 'AIA'},
    {'label': html.Span('UIM', style={'color': '#0778EB'}), 'value': 'UIM'},
    {'label': html.Span('OSM', style={'color': '#0778EB'}), 'value': 'OSM'},
    {'label': html.Span('Andes', style={'color': '#0778EB'}), 'value': 'Andes'},
    {'label': html.Span('Hensen', style={'color': '#0778EB'}), 'value': 'Hensen'},

]

fault_analysis_new_layout = html.Div([
    dbc.Navbar(children=[
        dbc.NavItem(html.A(html.I(className="fas fa-home"), href="/",style={"margin":"0px 0px 0px 20px","font-size":"30px","color":"white"})),
        dbc.NavbarBrand("Fault Lens", className="mx-auto",style={"text-align":"center","font-size":"35px","font-weight":"bold"}), 
        dbc.NavItem("Synapt-GDK", style={"margin-right": "20px", "color":"red","font-weight":"bold"})],color="dark",dark=True),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
            id='fault-analysis-new-dropdown',
            options=new_systems_involved,
            placeholder='Systems Involved',
            style={'background-color':'#444444','color':'yellow'},
            className="my-placeholder",
            value=None,
            multi=True
            )
        ],width=11),
        dbc.Col([
            dbc.Button([html.I(' Start',className='fas fa-paper-plane')], color='primary', id = "fault-analysis-new-start", style={'justify-content': 'center','width':'120px','margin': '47px 0px 0px 0px'}),
        ],className='d-flex flex-column align-items-center'),

    ],style = {'margin':'20px 0px'}),
    dcc.Loading(id='fault-analysis-new-loading', children=[
        html.Div(id='fault-analysis-new-loading-output'),
    ], type='circle', fullscreen=False),
    dbc.Row([
        dbc.Col([
            html.H3("Logs:", style={'font-size': '30px'}),
            html.Div(id='fault-analysis-new-logs', children=[]),
        ], width=12),
    ], style={'margin': '20px 0px'}),
])

@app.callback(
    Output('fault-analysis-new-logs','children'),
    Output('fault-analysis-new-loading','fullscreen'),
    Output('fault-analysis-new-loading-output','children'),
    Input('fault-analysis-new-start','n_clicks'),
    State('fault-analysis-new-loading','fullscreen'),
    State('fault-analysis-new-logs','children')
)
def start_processing(n_clicks, fullscreen,logs):
    logging.debug(os.getcwd())
    os.chdir(os.getcwd())
    if logs is None:
        logs = []
    if n_clicks is None:
        return logs,False,""
    else:
        with open('data.json') as json_data:
            data = json.load(json_data)
        
        issues = []
        for i in data.values():
            issues.append(i)

        fullscreen = True
        for issue in issues:
            now = datetime.datetime.now()
            try:
                result = globals()['run_preset_11'](issue + "\n Analyse the error and give solution step by step in bullet points. Use communication language as english" )
            except Exception as e:
                logging.error(f"Error Occured on calling function 'run_preset_11' \n{str(e)}")
                result =  "Error occured while establishing connection to OpenAI\n1. Check your internet connection\n2. Make sure you entered your API key Correctly.\n3. Wait for some time and try again\n\nSee logs for troubleshooting" 
            log_message = f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] \nInput: {issue}, \nResult: {result.strip()}"
            new_textarea = dbc.Textarea(id=f'textarea-{n_clicks}', style={'margin': '0px 0px 10px 0px','height': '150px','white-space': 'pre-line', 'word-wrap':'break-word', 'overflow-wrap':'break-word','background-color': '#444444', 'color': 'white'},value=log_message,readOnly=True)
            logs.append(new_textarea)
        fullscreen = False

    return logs, fullscreen, ""


# %%
# Define options for the dropdown for fault analysis 
#Adding more option here will require adding key values for log dictionary below
fault_analysis_dropdown_options = [
    {'label': 'Q&A', 'value': '11'},
    {'label': 'Analyze error in English','value':'13'},
    # {'label': 'Generate Code', 'value': '12'},
    # {'label': 'Generate an SQL query', 'value': '01'},
    # {'label': 'A simple Java Class', 'value': '07'},
    # {'label': 'Developer Task List', 'value': '08'},
    # {'label': 'Summarize a text', 'value': '09'},
    # {'label': 'Simplify a text', 'value': '10'}
]

preset_label = {
             '11':'Q&A',
             '01':'Generate an SQL Query',
             '07':'A Simple Java Class',
             '08':'Developer Task List',
             '09':'Summarize a text',
             '10':'Simplify a text',
             '13':'Analyze the error in English',
}


output_required = [
    {'label': 'Step by Step', 'value': '01'},
]

output_required_label = {
    '01':'Step by Step',
    '02':'Not Selected'
}

systems_involved = [
    # {'label': html.Span('Nova Explorer', style={'color': '#0778EB'}), 'value': 'Nova Explorer'},
    # {'label': html.Span('cProbe CP', style={'color': '#0778EB'}), 'value': 'cProbe CP'},
    # {'label': html.Span('Nova Fiber', style={'color': '#0778EB'}), 'value': 'Nova Fiber'},
    # {'label': html.Span('Remedy', style={'color': '#0778EB'}), 'value': 'Remedy'},
    # {'label': html.Span('BPT', style={'color': '#0778EB'}), 'value': 'BPT'},
    # {'label': html.Span('FieldTech', style={'color': '#0778EB'}), 'value': 'FieldTech'},
    # {'label': html.Span('SMS Web Service', style={'color': '#0778EB'}), 'value': 'SMS Web Service'},
    # {'label': html.Span('Volt Order Entry', style={'color': '#0778EB'}), 'value': 'Volt Order Entry'},
    # {'label': html.Span('iCare', style={'color': '#0778EB'}), 'value': 'iCare'},
    # {'label': html.Span('Launchpad', style={'color': '#0778EB'}), 'value': 'Launchpad'},
    # {'label': html.Span('GCOMMS', style={'color': '#0778EB'}), 'value': 'GCOMMS'},
    # {'label': html.Span('SVS', style={'color': '#0778EB'}), 'value': 'SVS'},
    # {'label': html.Span('MyVM', style={'color': '#0778EB'}), 'value': 'MyVM'},
    # {'label': html.Span('OneCMS', style={'color': '#0778EB'}), 'value': 'OneCMS'},
    {'label': html.Span('Vlocode', style={'color': '#0778EB'}), 'value': 'Vlocode'},
    {'label': html.Span('Java', style={'color': '#0778EB'}), 'value': 'Java'},
    {'label': html.Span('Apigee', style={'color': '#0778EB'}), 'value': 'Apigee'},
    {'label': html.Span('Liferay', style={'color': '#0778EB'}), 'value': 'Liferay'},
    {'label': html.Span('Provar', style={'color': '#0778EB'}), 'value': 'Provar'},
    {'label': html.Span('Selenium', style={'color': '#0778EB'}), 'value': 'Selenium'},
    {'label': html.Span('Google Cloud Platform', style={'color': '#0778EB'}), 'value': 'Google Cloud Platform'},
    {'label': html.Span('BMC Helix', style={'color': '#0778EB'}), 'value': 'BMC Helix'},
    {'label': html.Span('Amdocs', style={'color': '#0778EB'}), 'value': 'Amdocs'},
    {'label': html.Span('Siebel CRM', style={'color': '#0778EB'}), 'value': 'Siebel CRM'},
    {'label': html.Span('BRM', style={'color': '#0778EB'}),'value':'BRM'},
    {'label': html.Span('AIA', style={'color': '#0778EB'}), 'value': 'AIA'},
    {'label': html.Span('UIM', style={'color': '#0778EB'}), 'value': 'UIM'},
    {'label': html.Span('OSM', style={'color': '#0778EB'}), 'value': 'OSM'},
    {'label': html.Span('Andes', style={'color': '#0778EB'}), 'value': 'Andes'},
    {'label': html.Span('Hensen', style={'color': '#0778EB'}), 'value': 'Hensen'},
    {'label': html.Span('Salesforce', style={'color': '#0778EB'}), 'value': 'Salesforce'},
]

systems_involved_label = {
    '01':'Siebel CRM',
    '02':'BRM',
    '03':'AIA',
    '04':'UIM',
    '05':'OSM',
    '06':'ANDES',
    '07':'Hensen',
    '08':'Not Selected'
}


fault_analysis_page = html.Div([
    dbc.Navbar(children=[
        dbc.NavItem(html.A(html.I(className="fas fa-home"), href="/",style={"margin":"0px 0px 0px 20px","font-size":"30px","color":"white"})),
        dbc.NavbarBrand("Fault Lens", className="mx-auto",style={"text-align":"center","font-size":"35px","font-weight":"bold"}),
        dbc.NavItem("Synapt-GDK", style={"margin-right": "20px", "color":"red","font-weight":"bold"})],color="dark",dark=True),

    # dbc.Row([
    #     dbc.NavItem(html.A(html.I(className="fas fa-home"), href="/",style={"font-size": "20px","width": "100%","height": "100%","text-align":"center"})),
    #     #Heading
    #     html.H1('Fault Analysis', className="text-center"),
    # ]),
    dcc.Store(id="fault-analysis-word-output-alert"),
    dcc.Store(id='fault-analysis-intermediate-value'),
    dcc.Store(id='fault-analysis-prompt'),
    dbc.Row([
        dbc.Col([
            #html.H3("Select an Action:"),
            dbc.Select(
                id='fault-analysis-dropdown',
                options=fault_analysis_dropdown_options,
                style={'background-color': '#444444','color':'white'},
                placeholder="Select an Action",
                value = None
            ),
        ], width=4),
        dbc.Col([
            dbc.Textarea(id='fault-analysis-intent-dropdown',value = None, placeholder='Intent...', style={'height': '10px', 'resize': 'none','background-color': '#444444', 'color': 'white'})
        ], width=4),
        dbc.Col([
            #html.H3("Systems Involved"),
            dcc.Dropdown(
                id='fault-analysis-systems-involved-dropdown',
                options=systems_involved,
                placeholder="Systems Involved",
                style={'background-color': '#444444',"color":"yellow"},
                className = "my-placeholder",
                value = None,
                multi = True
            ),
        ], width=4),
    ], style={'margin': '20px 0px'}),
    
    dbc.Row([
        dbc.Col([
            html.H3("1. ❌Error Message:", style={'font-size': '30px'}),
            dbc.Textarea(id='fault_analysis-input-box', placeholder='Type here...', style={'height': '150px', 'resize': 'none','background-color': '#444444', 'color': 'white'})
        ], width=4),
        dbc.Col([
            dcc.Upload(id='fault-analysis-upload-image',children = ([html.Br(),html.Br(),html.I(className='fas fa-upload fa-lg'),html.Br(),'Drag and Drop or ',html.A('Select Image')]),style={'background-color': '#444444',"height":'148px','margin': '45px 0px 0px 0px',"borderRadius":"5px","text-align":"center",'justify-content': 'center'},multiple =False),
        ], className='d-flex flex-column align-items-center',width=1),
        dbc.Col([
            html.H3("2. 📷Image Text", style={'font-size': '30px'}),
            dbc.Textarea(id='fault_analysis-ocr-text', placeholder='Nothing Uploaded...', style={'height': '150px', 'resize': 'none','background-color': '#444444', 'color': 'white'})
        ], width=3),
        dbc.Col([
            html.H3("3. 💭Prompt Selected", style={'font-size': '30px'}),
            dbc.Textarea(id='fault-analysis-prompt-box',placeholder='Prompt appears here as you select...', style={'height': '150px', 'resize': 'none','word-wrap':'break-word', 'overflow-wrap':'break-word','background-color': '#444444', 'color': 'white'},readOnly=True)
        ], width=3),
        #placeholder='Prompt appears here as you select...'
        dbc.Col([
            dbc.Button([html.I(' Submit',className='fas fa-paper-plane')], color='primary', id = "fault-analysis-submit", style={'justify-content': 'center','width':'120px','margin': '47px 0px 0px 0px'}),
            dbc.Button([html.I(' Download',className='fas fa-download')], color="primary",href="",download="example.docx",target="_blank", style={'justify-content': 'center','width':'120px','margin': '16px 0px 0px 0px'},id = "fault-analysis-save"),
            dbc.Button([html.I(' Email',className='fas fa-envelope')], color="success", style={'justify-content': 'center','width':'120px','margin': '16px 0px 0px 0px'},id = "fault-analysis-email"),
        ], className='d-flex flex-column align-items-center'),
    ], style={'margin': '20px 0px'}),
    # html.Div(id = 'fault-analysis-email-recipients',children=[]),

    dbc.Row([
        dbc.Col([
            html.H3("Result:", style={'font-size': '30px'}),
            dbc.Textarea(id='fault-analysis-output-box',placeholder='Nothing generated yet...', style={'height': '500px', 'resize': 'none', 'word-wrap':'break-word', 'overflow-wrap':'break-word','background-color': '#444444', 'color': 'white'},readOnly = True)
        ], width=12),
    ], style={'margin': '20px 0px'}),
    dcc.Loading(id='fault-analysis-loading', children=[
        html.Div(id='fault-analysis-loading-output'),
    ], type='circle', fullscreen=False),
    dcc.Loading(id='ocr-text-loading', children=[
        html.Div(id='ocr-text-loading-output'),
    ], type='circle', fullscreen=False),
    #Logs
    dbc.Row([
        dbc.Col([
            html.H3("Logs:", style={'font-size': '30px'}),
            html.Div(id='fault-analysis-logs', children=[]),
        ], width=12),
    ], style={'margin': '20px 0px'}),
    html.P(id="ocr-hidden",hidden=True)
])

@app.callback(
        Output("fault-analysis-prompt-box","value"),
        Input("fault-analysis-systems-involved-dropdown","value"),
)
def fill_prompt(systems_involved_value):
    try:
        display_line = ""
        prompt = ""
        if systems_involved_value is None:
            systems_involved_prompt = ""
        else:
            display_line = "where system involved are-: "
            systems_involved_prompt =  ", ".join(systems_involved_value)
        prompt = display_line + systems_involved_prompt + " give solution step by step" ##+output_required_prompt
        return prompt.strip()
    except Exception as e:
        logging.error(f'Some error Occured in callback fill_prompt\n{str(e)}')
        return "#Callback Error# See logs for more information"

##
## Called when Preset dropdown is selected
##
def parse_contents(contents):
    pytesseract.pytesseract.tesseract_cmd = r'./Tesseract-OCR/tesseract.exe'
    image = Image.open(io.BytesIO(base64.b64decode(contents.split(',')[1])))
    text = pytesseract.image_to_string(image)
    return text,None

@app.callback(
        Output("fault_analysis-ocr-text","value"),
        Output('ocr-text-loading', 'fullscreen'), 
        Output('ocr-text-loading-output', 'children'),
        Input("fault-analysis-upload-image","contents"),
        State("fault_analysis-ocr-text","value"),
        State('ocr-text-loading','fullscreen'),
)
def display_ocr(contents,previous_text,fullscreen):
    try:
        ocr_text = ""
        if previous_text is None:
            previous_text = ""
        if contents is None:
            contents = ""
        else:
            fullscreen = True
            ocr_text, contents = parse_contents(contents)
            fullscreen = False
        return previous_text + "\n" + ocr_text, False,""
    except Exception as e:
        logging.error(f"Some error Occured in callback display_ocr\n{str(e)}")
        return "#Callback Error# See logs for more information",fullscreen,""

@app.callback(
    Output(component_id='fault_analysis-input-box', component_property='value'),
    Input(component_id='fault-analysis-dropdown', component_property='value'),
)
def update_output(dropdown):
    try:
        if dropdown is None:
            return ''
        return get_query_from_preset(dropdown)
    except Exception as e:
        logging.error(f"Some error Occured in callback update_output\n{str(e)}")
        return "#Callback Error# See logs for more information"
    
def get_query_from_preset(preset):
  query = '' 
  if preset == '01':
        query = '### Postgres SQL tables, with their properties:\n#\n# Employee(id, name, department_id)\n# Department(id, name, address)\n# Salary_Payments(id, employee_id, amount, date)\n#\n### A query to list the names of the departments which employed more than 10 employees in the last 3 months\nSELECT'
  elif preset == '02':
        query = "generate a python code that prints my S3 buckets list then create a new bucket named 'test\'"
  elif preset == '03':
        query = "###Generate a python code that creates a CloudWatch Alarm named 'test_alarm_osy' which triggers when server CPU exceeds 70%"
  elif preset == '04':      
        query = "#Generate a python code that creates a user named 'osadey' with password 'abcde'\nimport boto3"
  elif preset == '05': 
        query = "predict the salary with criteria like age, position, experience, using random forest algorithm"
  elif preset == '06': 
        query = "/* generate a ReactJS code with a button that displays a message 'Hello GPT-3' when the user clicks on it */"
  elif preset == '07': 
        query = "/* A Java class used to represent a person with name, age and gender attributs */\npublic class Person"
  elif preset == '08': 
        query = "1. Create a list of first names\n2. Create a list of last names\n3. Combine them randomly into a list of 100 full names\n4. Print the full names in a nicely formatted way\n5. Print the number of full names that contain a 'K'"
  elif preset == '09': 
        query = "Summarize the following text:\nOne month after the United States began what has become a troubled rollout of a national COVID vaccination campaign, the effort is finally gathering real steam. Close to a million doses -- over 951,000, to be more exact -- made their way into the arms of Americans in the past 24 hours, the U.S. Centers for Disease Control and Prevention reported Wednesday. That's the largest number of shots given in one day since the rollout began and a big jump from the previous day, when just under 340,000 doses were given, CBS News reported. That number is likely to jump quickly after the federal government on Tuesday gave states the OK to vaccinate anyone over 65 and said it would release all the doses of vaccine it has available for distribution. Meanwhile, a number of states have now opened mass vaccination sites in an effort to get larger numbers of people inoculated, CBS News reported.\n"
  elif preset == '10': 
        query = "My ten-year-old asked me what this passage means:\n\"A neutron star is the collapsed core of a massive supergiant star, which had a total mass of between 10 and 25 solar masses, possibly more if the star was especially metal-rich.[1] Neutron stars are the smallest and densest stellar objects, excluding black holes and hypothetical white holes, quark stars, and strange stars.[2] Neutron stars have a radius on the order of 10 kilometres (6.2 mi) and a mass of about 1.4 solar masses.[3] They result from the supernova explosion of a massive star, combined with gravitational collapse, that compresses the core past white dwarf star density to that of atomic nuclei.\"\n\nI rephrased it for him, in plain language a ten-year-old can understand:"
  elif preset == '11':
        query = ""
  elif preset == '12':
        query = ""
  elif preset == '13':
        query = ""
  return query

##
## Called when the Button 'Generate' is pushed
##
@app.callback(
    Output(component_id='fault-analysis-output-box', component_property='value'),
    Output('fault-analysis-intermediate-value', 'data'),
    Output('fault-analysis-logs', 'children'),
    Output('fault-analysis-loading', 'fullscreen'), 
    Output('fault-analysis-loading-output', 'children'),
    State('fault-analysis-loading','fullscreen'),
    State(component_id='fault_analysis-input-box', component_property='value'),
    State(component_id='fault-analysis-dropdown', component_property='value'),
    State(component_id="fault-analysis-intent-dropdown",component_property="value"),
    State(component_id="fault-analysis-systems-involved-dropdown",component_property="value"),
    State('fault-analysis-logs', 'children'),
    Input('fault-analysis-submit', 'n_clicks'),
    State('fault-analysis-prompt-box','value'),
    Input("fault_analysis-ocr-text","value")
)
def update_output2(fullscreen,textarea,preset,intent_dropdown,systems_involved,logs, n_clicks,prompt_generated,ocr_text):

    values = []
    if intent_dropdown is None:
        intent_dropdown = ''
    if systems_involved is None:
        systems_involved = 'Not Selected'
    if n_clicks is None or n_clicks == 0:
        return ['','',[],False,""]
    else:
        if logs is None:
             logs=[]
        ## Execute dynamically the 'run_preset_nn' function (where 'nn' is the preset number)
        #hide demographics
        textarea = hideDemogrphics(textarea)

        #get results from chat gpt
        start_time = time.time()
        try:
            fullscreen = True
            results = globals()['run_preset_%s' % preset](str(textarea)+"\n"+intent_dropdown+"\n"+ocr_text+"\n"+prompt_generated+"\nuse communication language as english")
            fullscreen = False
        except Exception as e:
            logging.error(f"Error Occured on calling function 'run_preset_{preset} \n{str(e)}'")
            results =  "Error occured while establishing connection to OpenAI\n1. Check your internet connection\n2. Make sure you entered your API key Correctly.\n3. Wait for some time and try again\n\nSee logs for troubleshooting"  
        end_time = time.time()
        total_time = end_time - start_time
        #get timestamp
        now = datetime.datetime.now()

        #create log message
        log_message = f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] \nOption: {preset_label[preset]}, \nInput: {textarea}, \nResult: {results.strip()}"
        
        #create textarea for logs
        new_textarea = dbc.Textarea(id=f'textarea-{n_clicks}', style={'margin': '0px 0px 10px 0px','height': '150px','white-space': 'pre-line', 'word-wrap':'break-word', 'overflow-wrap':'break-word','background-color': '#444444', 'color': 'white'},value=log_message,readOnly=True)
        
        #create and execute sql query
        conn = sqlite3.connect('code_ops_analyser.db')
        sql_query = "Insert into fault_tolerance (timestamp_, action_selected, intent, systems_involved, error_message, ocr_text, prompt_selected, result, exe_time) VALUES (?,?,?,?,?,?,?,?,?)"
        query_values = (
            f"{now.strftime('%Y-%m-%d %H:%M:%S')}",
            preset_label[preset],
            intent_dropdown,
            ", ".join(systems_involved),
            textarea,
            ocr_text,
            prompt_generated,
            results.strip(),
            total_time
        )
        conn.execute(sql_query,query_values)
        conn.commit()
        logging.info("1 Row inserted in fault_tolerance")
        conn.close()

        #Append values to send
        values.append(results.strip())
        values.append("Q: "+textarea.strip()+"\n    OCR Text:\n    "+ocr_text+"\nA: "+results.strip())
        logs.append(new_textarea)
        values.append(logs)
        values.append(fullscreen)
        values.append("")
        return values
    
##
## Called when the Button 'Download' is pushed
##

@app.callback(
     Output("fault-analysis-save","href"),
     Input("fault-analysis-save","n_clicks"),
     Input('fault-analysis-intermediate-value', 'data')
)
def generate_report(n_clicks,data):
     try:
        n_clicks = 0
        if n_clicks is not None or n_clicks > 0:
            doc = data.encode("utf-8")
            b64 = base64.b64encode(doc).decode()
            href = f"data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{b64}"
            return href
     except Exception as e:
         logging.error(f"error while generating fault analysis report\n{str(e)}")

##
## Called when the Button 'Email' is pushed
##
@app.callback(
     Output('fault-analysis-email-recipients','children'),
     Input('fault-analysis-email','n_clicks')
)
def open_email_recipient_box(n_clicks):
     if not n_clicks:
          raise PreventUpdate()
     elif n_clicks is not None:
          email_layout = [
               dbc.Row([
                    dbc.Col([
                        dbc.Textarea(id='email-recipient-textarea', style={'margin': '10px 0px 0px 0px','height': '10px','white-space': 'pre-line', 'word-wrap':'break-word', 'overflow-wrap':'break-word','background-color': '#444444', 'color': 'white'})
                    ],width=10),
                    dbc.Col([
                        dbc.Button([html.I(' Send',className='fas fa-envelope')], color="success", style={'justify-content': 'center','width':'120px','margin': '10px 0px 0px 7px'},id = "fault-analysis-send-email-button")
                    ],width = 1),  
                    dbc.Col([
                        dbc.Button([html.I(' Close',className='fas fa-ban')], color="danger", style={'justify-content': 'center','width':'120px','margin': '10px 0px 0px 7px'},id = "fault-analysis-close-email-button")
                    ],width = 1),              
               ], style={'margin': '20px 0px'})
          ]
          return email_layout

# %%
# Code Analysis

def call_chatGPT_for_Code_analysis(query):
    return run_preset_11(query)

code_analysis_action_dropdown_options = [
    {'label':'Analyze code dependencies', 'value': 'Analyze code dependencies'},
    {'label':'Detect duplicate code','value':'Detect duplicate code'},
    {'label':'Measure code coverage','value':'Measure code coverage'},
    {'label':'Review code for accessibility','value':'Review code for accessibility'},
    {'label':'Analyze memory usage','value':'Analyze memory usage'},
    {'label':'Check for code style consistency','value':'Check for code style consistency'},
    {'label':'Validate data input and output','value':'Validate data input and output'},
    {'label':'Assess code modularity','value':'Assess code modularity'},
    {'label':'Analyze code complexity','value':'Analyze code complexity'},
    {'label':'Review error handling and logging','value':'Review error handling and logging'},
    {'label':'Identify error in code','value':'Identify error in code'},
    {'label':'SQL Query Optimization','value':'SQL Query Optimization'}
]

code_analysis_layout = html.Div([
        dbc.Navbar(children=[
            dbc.NavItem(html.A(html.I(className="fas fa-home"), href="/",style={"margin":"0px 0px 0px 20px","font-size":"30px","color":"white"})),
            dbc.NavbarBrand("Code Analysis", className="mx-auto",style={"text-align":"center","font-size":"35px","font-weight":"bold"}),
            dbc.NavItem("Synapt-GDK", style={"margin-right": "20px", "color":"red","font-weight":"bold"})],color="dark",dark=True),
        dbc.Row([
            dbc.Col([
                dbc.Select(
                    id = 'code-analysis-action-dropdown',
                    options= code_analysis_action_dropdown_options,
                    style={'background-color': '#444444','color':'white'},
                    placeholder="Select an Action",
                    value = None
                )
            ],width=6),
            dbc.Col([
                dbc.Textarea(id='code-analysis-intent-dropdown',value = None, placeholder='Code Language (eg: C++, Java, Python)', style={'height': '10px', 'resize': 'none','background-color': '#444444', 'color': 'white',})
            ]),
        ],style={"margin":"20px 0px"}),
        dbc.Row([
            dbc.Col([
                html.H3("Enter Code:", style={'font-size': '30px'}),
                dbc.Textarea(id='code-analysis-error-input',placeholder='Type or Paste your code here....',style={'height':'150px','resize':'none','background-color':'#444444','color':'white'}),
            ],width=11),
            # dbc.Col([
            #     html.H3("Prompt Selected", style={'font-size': '30px'}),
            #     dbc.Textarea(id='code-analysis-prompt-box',placeholder='Prompt will appear here upon selecting action...',readOnly=True,style={'height':'150px','resize':'none','background-color':'#444444','color':'white'}, hidden=True),
            # ],width=0),
            dbc.Textarea(id='code-analysis-prompt-box',placeholder='Prompt will appear here upon selecting action...',readOnly=True,style={'height':'150px','resize':'none','background-color':'#444444','color':'white'}, hidden=True),
            dbc.Col([
                dbc.Button([html.I(' Submit',className='fas fa-paper-plane')], color='primary', id = "code-analysis-submit", style={'justify-content': 'center','width':'120px','margin': '47px 0px 0px 0px'}),
                dbc.Button([html.I(' Download',className='fas fa-download')], color="primary",href="",download="example.docx",target="_blank", style={'justify-content': 'center','width':'120px','margin': '16px 0px 0px 0px'},id = "code-analysis-save"),
                dbc.Button([html.I(' Email',className='fas fa-envelope')], color="success", style={'justify-content': 'center','width':'120px','margin': '16px 0px 0px 0px'},id = "code-analysis-email"),
            ], className='d-flex flex-column align-items-center'),
        ],style={'margin':'20px 0px'}),
        dbc.Row([
            dbc.Col([
                html.H3("Result:", style={'font-size': '30px'}),
                dbc.Textarea(id='code-analysis-output-box',placeholder='Nothing generated yet...', style={'height': '500px', 'resize': 'none', 'word-wrap':'break-word', 'overflow-wrap':'break-word','background-color': '#444444', 'color': 'white'},readOnly = True)
            ], width=12),
        ], style={'margin': '20px 0px'}),
        dcc.Loading(id='code-analysis-loading', children=[
        html.Div(id='code-analysis-loading-output'),
    ], type='circle', fullscreen=False),
])


##Called when dropdown of code-analysis is selected
@app.callback(
    Output('code-analysis-prompt-box','value'),
    Input('code-analysis-action-dropdown','value')
)
def code_analysis_select_dropdown(dropdown):
    return select_prompt_from_code_analysis_dropdown(dropdown, 0)

def select_prompt_from_code_analysis_dropdown(preset, returnvalue):
    prompt = ''
    if preset == 'Analyze code dependencies':
        prompt = '##List all external dependencies in the code and identify any outdated versions or potential conflicts or library imports.'
    elif preset == 'Detect duplicate code':
        prompt = '##Find duplicate code blocks in the project and suggest ways to refactor them for better maintainability.'
    elif preset == 'Measure code coverage':
        prompt = "##Evaluate the code's test coverage and provide suggestions for increasing the coverage to ensure better reliability."
    elif preset == 'Review code for accessibility':
        prompt = '##Analyze the code for accessibility compliance and provide a list of areas that need improvement to meet accessibility standards.'
    elif preset == 'Analyze memory usage':
        prompt = "##Investigate the code's memory usage and provide recommendations for reducing memory consumption and preventing memory leaks."
    elif preset == 'Check for code style consistency':
        prompt = "##Examine the code for consistency with the project's style guide and provide a list of areas that need adjustments for better consistency."
    elif preset == 'Validate data input and output':
        prompt = "##Review the code for proper data input validation and output handling, and provide a list of areas that need improvement to prevent errors and security risks."
    elif preset == 'Assess code modularity':
        prompt = "##Examine the code for modularity and organization, and provide recommendations for enhancing the separation of concerns and maintainability."
    elif preset == 'Analyze code complexity':
        prompt = "##Assess the code's complexity using metrics such as cyclomatic complexity and nesting depth, and provide recommendations for simplifying the code to improve maintainability."
    elif preset == 'Review error handling and logging':
        prompt = "##Examine the code's error handling and logging mechanisms, and provide a list of areas that need improvement to ensure robustness and easier debugging."
    elif preset == 'Identify error in code':
        prompt = "##Identify error in code"
    if returnvalue == 0:
        return ""
    else:
        return prompt
    
## Called when the 'Submit' button in code-analysis is clicked
@app.callback(
        Output('code-analysis-output-box','value'),
        Output('code-analysis-loading', 'fullscreen'), 
        Output('code-analysis-loading-output', 'children'),
        State('code-analysis-loading','fullscreen'),
        State('code-analysis-action-dropdown','value'),
        State('code-analysis-intent-dropdown','value'),
        State('code-analysis-prompt-box','value'),
        State('code-analysis-error-input','value'),
        Input('code-analysis-submit','n_clicks'),
)
def generate_code_analysis_output(fullscreen, action_selected, code_language,prompt, textarea, n_clicks):
    if n_clicks is None:
        return '',False,''
    
    start_time = time.time()
    try:
        fullscreen = True
        if action_selected == "SQL Query Optimization":
            result = sqloptimizer(textarea)
        else:
            result = globals()['run_preset_11'](select_prompt_from_code_analysis_dropdown(action_selected, 1)+" step by step\n"+textarea+" Also provide the corrected code even if it is correct")
        fullscreen = False
    except Exception as e:
        logging.error(f"Error Occured on calling function 'run_preset_11' \n{str(e)}")
        result = "Error occured while establishing connection to OpenAI\n1. Check your internet connection\n2. Make sure you entered your API key Correctly.\n3. Wait for some time and try again\n\nSee logs for troubleshooting"
    end_time = time.time()

    total_time = end_time-start_time
    ##save in sql
    conn = sqlite3.connect('code_ops_analyser.db')
    sql_query = "Insert into code_analysis(action_selected, code_language, input_code, prompt_selected, result, exe_time) VALUES (?,?,?,?,?,?)"
    query_values = (
        action_selected,
        code_language,
        textarea,
        prompt,
        result.strip(),
        total_time
    )
    conn.execute(sql_query,query_values)
    conn.commit()
    logging.info("1 row inserted in code_analysis")
    conn.close()
    return result.strip(),fullscreen,''

##Called when "Download button is clicked"
@app.callback(
    Output('code-analysis-save','href'),
    Input("code-analysis-output-box","value"),
    Input('code-analysis-prompt-box','value'),
    Input('code-analysis-error-input','value'),
    Input("code-analysis-save","n_clicks"),
)
def generate_code_analysis_report(result, prompt, input, n_clicks):
    if result is None:
        result = ""
    if prompt is None:
        prompt = ""
    if input is None:
        input = ""
    n_clicks = 0
    if n_clicks is not None or n_clicks > 0:
        document_content = "Q: "+prompt+"\n"+input+"\n\n"+"A: "+result
        doc = document_content.encode("utf-8")
        b64 = base64.b64encode(doc).decode()
        href = f"data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{b64}"
        return href
    

# %% Doc Generation

def get_SOP_document_from_openai(topic):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Question:\nThis document guides Retail agent on how to check the customer’s device status and SIM card compatibility before activating new services for Bring Your Own Device (BYOD) scenario. this document is called SOP document .\n\nAnswer:\n1. Title: Standard Operating Procedure (SOP) for Checking Device Status and SIM Card Compatibility in Bring Your Own Device (BYOD) Scenario\n\n2. Introduction\nThis Standard Operating Procedure (SOP) document provides guidelines for retail agents on how to effectively check the customer's device status and SIM card compatibility before activating new services for Bring Your Own Device (BYOD) scenarios. Adhering to these procedures will ensure a smooth onboarding process for the customers and prevent any service-related issues.\n\n3. Purpose\nThe purpose of this SOP is to:\n\na. Ensure a seamless service activation process for BYOD customers.\nb. Verify the compatibility of the customer's device and SIM card with the network.\nc. Reduce the number of post-activation issues and complaints.\n\n4. Scope\nThis SOP applies to all retail agents responsible for activating new services for customers using their own devices.\n\n5. Procedure\n\n5.1. Checking Device Status\n\na. Ask the customer for their device's make, model, and IMEI number.\nb. Check the device's compatibility with the network by entering the device details in the internal compatibility checker tool or refer to the carrier's compatibility list.\nc. Verify if the device is unlocked or locked to a specific carrier. If locked, inform the customer that they need to get their device unlocked before using it on the new network.\nd. Ensure the device has not been reported as lost or stolen by checking the IMEI number against the national blacklist database.\n\n5.2. Checking SIM Card Compatibility\n\na. Determine the required SIM card size for the customer's device (e.g., Nano, Micro, or Standard).\nb. Verify if the customer's existing SIM card is compatible with the network. If not, provide the customer with a compatible SIM card.\nc. If the customer needs a new SIM card, explain the activation process and any associated fees.\n\n5.3. Activating the Service\n\na. If the device and SIM card are compatible, proceed with the service activation process.\nb. Inform the customer about the available service plans and help them choose the best option based on their needs.\nc. Collect the required customer information and complete the service activation process as per the company's guidelines.\nd. Once the service is activated, help the customer set up their device with the new SIM card and ensure they can make calls, send messages, and access the internet.\n\n6. Documentation and Record-Keeping\na. Document the customer's device details, SIM card information, and service activation details in the customer management system.\nb. Update the customer's account with any changes in their information, plan, or service status.\nc. Keep a record of any issues encountered during the activation process and report them to the appropriate department for resolution.\n\n7. Conclusion\nFollowing this SOP will ensure that retail agents can efficiently check the customer's device status and SIM card compatibility before activating new services in a BYOD scenario. This will lead to a better customer experience and reduce the likelihood of service-related issues or complaints.\n##\nQuestion:\nThis document guides {topic} this document is called SOP document .\n\nAnswer:",
        temperature=0.7,
        max_tokens=2995,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["##"]
    )
    return response.choices[0].text

def get_faq_from_openai(topic):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Question:\ndocument guides how to check the customer’s device status and SIM card compatibility before activating new services for Bring Your Own Device (BYOD) scenario. generate a FAQ section.\n\nAnswer:\nFrequently Asked Questions (FAQ)\n\nQ. What if a customer's device is locked to a specific carrier?\nA. If a customer's device is locked to a specific carrier, they will need to contact their current carrier and request an unlock. Once the device is unlocked, they can proceed with the BYOD activation process.\n\nQ. Can a customer keep their current phone number when activating a new service?\nA. Yes, most carriers allow customers to port their current phone number during the activation process. The retail agent should guide the customer through the number porting process according to the company's guidelines.\n\nQ. What if a customer's device is not compatible with the network?\nA. If a customer's device is not compatible with the network, the retail agent should inform the customer of the incompatibility issue and recommend suitable devices that are compatible with the network.\n\nQ. How long does it take for a new service to be activated?\nA. The activation process may vary depending on the carrier and the customer's specific situation. Generally, service activation can take anywhere from a few minutes to several hours. The retail agent should provide an estimated activation time to the customer.\n\nQ. Are there any fees associated with activating a new service in a BYOD scenario?\nA. Some carriers may charge activation fees, SIM card fees, or other related fees for BYOD customers. The retail agent should clearly explain any applicable fees to the customer during the activation process.\n\nQ. What should a customer do if they face issues with their service after activation?\nA. If a customer experiences issues with their service after activation, they should contact the carrier's customer support for assistance. Retail agents should provide customers with the necessary contact information and encourage them to reach out if they encounter any problems.\n##\nQuestion:\ndocument guides {topic} generate a FAQ section.\n\nAnswer:",
        temperature=0.7,
        max_tokens=2515,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["##"]
    )
    return response.choices[0].text

def generate_doc_generation_report(data):
    doc = data.encode("utf-8")
    b64 = base64.b64encode(doc).decode()
    href = f"data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{b64}"
    return href

doc_generation_output_required = [
    {'label':'SOP Document','value':'03'},
    {'label':'Design Document','value':'02'},
    {'label':'Simplify a text','value':'01'},
    {'label':'Summarize the text','value':'04'}
]

docGeneration_Layout = html.Div([
    dbc.Navbar(children=[
        dbc.NavItem(html.A(html.I(className="fas fa-home"), href="/",style={"margin":"0px 0px 0px 20px","font-size":"30px","color":"white"})),
        dbc.NavbarBrand("Doc Generation", className="mx-auto",style={"text-align":"center","font-size":"35px","font-weight":"bold"}),
        dbc.NavItem("Synapt-GDK", style={"margin-right": "20px", "color":"red","font-weight":"bold"})],color="dark",dark=True),
    dbc.Row([
        dbc.Col([
            dbc.Select(
                id = 'doc-generation-output-required-dropdown',
                options = doc_generation_output_required,
                style={'background-color': '#444444','color':'white'},
                placeholder="Select an Action",
                value = None
            )
        ]),
    ],style={'margin':'20px 0px'}),
    dbc.Row([
        dbc.Col([
            html.H3("Enter Topic:", style = {'font-size':'30px'}),
            dbc.Textarea(id = "doc-generation-topic",placeholder="Enter here...",style={'height': '150px', 'resize': 'none','word-wrap':'break-word', 'overflow-wrap':'break-word','background-color': '#444444', 'color': 'white'})
        ],width = 11),
        # dbc.Col([
        #     html.H3("💭Prompt Selected:", style={'font-size': '30px'}),
        #     dbc.Textarea(id='doc-generation-prompt-box',placeholder='Prompt appears here as you select...', style={'height': '150px', 'resize': 'none','word-wrap':'break-word', 'overflow-wrap':'break-word','background-color': '#444444', 'color': 'white'},readOnly=True)
        # ], width=5),
        dbc.Col([
            dbc.Button([html.I(' Submit',className='fas fa-paper-plane')], color='primary', id = "doc-generation-submit", style={'justify-content': 'center','width':'120px','margin': '47px 0px 0px 0px'}),
            dbc.Button([html.I(' Download',className='fas fa-download')], color="primary",href="",download="example.docx",target="_blank", style={'justify-content': 'center','width':'120px','margin': '16px 0px 0px 0px'},id = "doc-generation-save"),
            dbc.Button([html.I(' Email',className='fas fa-envelope')], color="success", style={'justify-content': 'center','width':'120px','margin': '16px 0px 0px 0px'},id = "doc-generation-email"),
        ], className='d-flex flex-column align-items-center'),
        ], style={'margin': '20px 0px'}),
        dcc.Loading(id='doc-generation-loading', children=[
            html.Div(id='doc-generation-loading-output'),
        ], type='circle', fullscreen=False),
    dbc.Row([
        dbc.Row([
        dbc.Col([
            html.H3("Result:", style={'font-size': '30px'}),
            dbc.Textarea(id='doc-generation-output-box',placeholder='Nothing generated yet...', style={'height': '500px', 'resize': 'none', 'word-wrap':'break-word', 'overflow-wrap':'break-word','background-color': '#444444', 'color': 'white'},readOnly = True)
        ], width=12),
    ], style={'margin': '20px 0px'}),

    ])
    ])

@app.callback(
    Output("doc-generation-topic",'value'),
    Input('doc-generation-output-required-dropdown','value')
)
def clear_input(output_required):
    return ""

@app.callback(
    Output("doc-generation-output-box","value"),
    Output('doc-generation-loading', 'fullscreen'), 
    Output('doc-generation-loading-output', 'children'),
    Input("doc-generation-submit","n_clicks"),
    State("doc-generation-topic","value"),
    State('doc-generation-output-required-dropdown','value'),
    State('doc-generation-loading','fullscreen'),
)
def generate_doc_generation_output(n_clicks, topic, output_required,fullscreen):
    if n_clicks is None:
        return "",False,""

    if topic[-1] != '.':
        topic = topic+'.'

    start_time = time.time()
    if output_required == '03':
        fullscreen = True
        try:
            sop_document = get_SOP_document_from_openai(topic)
            sop_document = sop_document.strip()
            faq = get_faq_from_openai(topic)
            faq = "\n\n" + faq.strip()
            response = sop_document + faq
        except Exception as e:
            logging.error(f"Some error occurred\n{str(e)} ")
            response = "Error occured while establishing connection to OpenAI\n1. Check your internet connection\n2. Make sure you entered your API key Correctly.\n3. Wait for some time and try again\n\nSee logs for troubleshooting"
        fullscreen = False

    elif output_required == '05':
        fullscreen = True
        try:
            functional_test_document = get_functional_test_response(topic)
            functional_test_document = functional_test_document.strip()
            response = functional_test_document.replace('#','-')
        except Exception as e:
            response = "Error occured while establishing connection to OpenAI\n1. Check your internet connection\n2. Make sure you entered your API key Correctly.\n3. Wait for some time and try again\n\nSee logs for troubleshooting"
            #print(str(e))
        fullscreen = False

    elif output_required == '04':
        fullscreen = True
        try:
            response = run_preset_09(topic)
        except Exception as e:
            response = "Error occured while establishing connection to OpenAI\n1. Check your internet connection\n2. Make sure you entered your API key Correctly.\n3. Wait for some time and try again\n\nSee logs for troubleshooting"
            #print(str(e))
        fullscreen = False

    elif output_required == '01':
        fullscreen = True
        try:
            response = run_preset_10(topic)
        except Exception as e:
            response = "Error occured while establishing connection to OpenAI\n1. Check your internet connection\n2. Make sure you entered your API key Correctly.\n3. Wait for some time and try again\n\nSee logs for troubleshooting"
            #print(str(e))
        fullscreen = False

    end_time = time.time()
    total_time = end_time - start_time
    try:
        conn = sqlite3.connect('code_ops_analyser.db')
        sql_query = "Insert into doc_generation (dropdown, topic, output, exe_time) Values (?,?,?,?)"
        query_values = (
            output_required,
            topic,
            response,
            total_time
        )
        conn.execute(sql_query,query_values)
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"{str(e)}")

    return response,fullscreen,""

@app.callback(
    Output('doc-generation-save','href'),
    Input('doc-generation-save','n_clicks'),
    Input('doc-generation-output-box','value')
)
def send_doc_genearation_report(n_clicks,data):
    
    n_clicks =0
    if n_clicks is not None or n_clicks > 0:
        doc = data.encode("utf-8")
        b64 = base64.b64encode(doc).decode()
        href = f"data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{b64}"
        return href

# %% Code Generation
code_generation_action_dropdown = [
    {'label':'Code Refactoring','value':'Code Refactoring'},
    {'label':'Code Generation','value':'Code Generation'},
    {'label':'Salesforce Support','value':'Salesforce Support'},
    {'label':'Generate SQL Query','value':'Generate SQL Query'}
]
code_generation_layout = html.Div([
    dbc.Navbar(children=[
        dbc.NavItem(html.A(html.I(className="fas fa-home"), href="/",style={"margin":"0px 0px 0px 20px","font-size":"30px","color":"white"})),
        dbc.NavbarBrand("Code Generation", className="mx-auto",style={"text-align":"center","font-size":"35px","font-weight":"bold"}),
        dbc.NavItem("Synapt-GDK", style={"margin-right": "20px", "color":"red","font-weight":"bold"})],color="dark",dark=True),
    dbc.Row([
        dbc.Col([
            dbc.Select(
                id = 'code-generation-action-dropdown',
                options = code_generation_action_dropdown,
                style={'background-color':'#444444','color':'white'},
                placeholder="Select an Action",
                value=None
            ),
        ],width=6),
        dbc.Col([
            dbc.Textarea(id = 'code-generation-language-textbox',value=None,placeholder='Target Code Language (eg: C++, Java, Python, etc.)',style={'height':'10px','resize':'none','background-color':'#444444','color':'white'})
        ],width=6),
    ],style={'margin':'20px 0px'}),
    dbc.Row([
        dbc.Col([
            html.H3("Type Natural Language:", style={'font-size': '30px'}),
            dbc.Textarea(id='code-generation-input-box', placeholder='Type here...', style={'height': '150px', 'resize': 'none','background-color': '#444444', 'color': 'white'})
        ], width=11),
        dbc.Col([
            dbc.Button([html.I(' Submit',className='fas fa-paper-plane')], color='primary', id = "code-generation-submit", style={'justify-content': 'center','width':'120px','margin': '47px 0px 0px 0px'}),
            dbc.Button([html.I(' Download',className='fas fa-download')], color="primary",href="",download="example.docx",target="_blank", style={'justify-content': 'center','width':'120px','margin': '16px 0px 0px 0px'},id = "code-generation-save"),
            dbc.Button([html.I(' Email',className='fas fa-envelope')], color="success", style={'justify-content': 'center','width':'120px','margin': '16px 0px 0px 0px'},id = "code-generation-email"),
        ], className='d-flex flex-column align-items-center'),
    ],style={'margin':'20px 0px'}),
    dbc.Row([
        dbc.Col([
            html.H3("Code Will Appear Here:", style={'font-size': '30px'}),
            dbc.Textarea(id='code-generation-output-box',placeholder='Nothing generated yet...', style={'height': '500px', 'resize': 'none', 'word-wrap':'break-word', 'overflow-wrap':'break-word','background-color': '#444444', 'color': 'white'},readOnly = True)
        ], width=12),
    ], style={'margin': '20px 0px'}),
    dcc.Loading(id='code-generation-loading', children=[
        html.Div(id='code-generation-loading-output'),
    ], type='circle', fullscreen=False),
])

##
## Called when submit button is clicked
##
@app.callback(
    Output('code-generation-output-box','value'),
    Output('code-generation-loading', 'fullscreen'), 
    Output('code-generation-loading-output', 'children'),
    State('code-generation-loading','fullscreen'),
    State('code-generation-input-box','value'),
    Input('code-generation-submit','n_clicks'),
    State('code-generation-language-textbox','value'),
    Input('code-generation-action-dropdown','value')
)
def show_the_code_man(fullscreen, textarea, n_clicks, language,preset):
    if n_clicks is None:
        return "",False,""
    if language is None or language == "":
        language = 'Python'
    start_time = time.time()
    try:
        fullscreen = True
        if(preset == 'Code Generation'):
            query = "Don't let them know you're an AI. Now, write a "+language+" "+textarea
            result = globals()['run_preset_11'](query)
        elif(preset == 'Code Refactoring'):
            query = 'convert this code in '+language+'\n'+textarea
            result = globals()['run_preset_11'](query)
        elif(preset == 'Salesforce Support'):
            query = "Don't let them know you're an AI. Now, write a code using Apex REST methods on"+'\n'+textarea
            result = globals()['run_preset_11'](query)
        elif(preset == 'Generate SQL Query'):
            query = "Don't let them know you're an AI, just write the code and nothing else. Now, write a SQL query on"+'\n'+textarea
            result = globals()['run_preset_11'](query)
        fullscreen = False
    except Exception as e:
        result =  "Error occured while establishing connection to OpenAI\n1. Check your internet connection\n2. Make sure you entered your API key Correctly.\n3. Wait for some time and try again\n\nSee logs for troubleshooting"
        logging.error(f"Error Occured on calling function 'run_preset_11' \n{str(e)}")
    end_time = time.time()
    total_time = end_time - start_time

    #save in sql
    conn = sqlite3.connect('code_ops_analyser.db')
    sql_query = "Insert into code_generation(action_selected, code_language, input, result, exe_time) Values (?,?,?,?,?)"
    query_values = (
        preset,
        language,
        textarea,
        result,
        total_time
    )
    conn.execute(sql_query,query_values)
    conn.commit()
    conn.close()
    return result,fullscreen,""

##Called when 'Download; button is pressed
@app.callback(
    Output('code-generation-save','href'),
    Input('code-generation-action-dropdown','value'),
    Input('code-generation-language-textbox','value'),
    Input('code-generation-input-box','value'),
    Input('code-generation-output-box','value'),
    Input('code-generation-save','n_clicks')
)
def generate_code_generation_report(preset, language, textarea, result, n_clicks):
    if preset is None:
        preset = '(Not Defined)'
    if language is None:
        language = '(Not Defined)'
    if textarea is None:
        textarea = '(None)'
    if result is None:
        result = '(None)'
    query=''
    n_clicks = 0
    if n_clicks is not None or n_clicks > 0:
        query = ''
        if(preset == 'Code Generation'):
            query = "write a "+language+" "+textarea
        elif(preset == 'Code Refactoring'):
            query = 'convert this code in '+language+'\n'+textarea
        
        document_content = "Q: "+query+"\n\n"+"A: "+result
        doc = document_content.encode("utf-8")
        b64 = base64.b64encode(doc).decode()
        href = f"data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{b64}"
        return href


#%% Test Genius

test_genius_dropdown_option = [
    {'label':'Generate unit test cases','value':'Generate unit test cases'},
    {'label':'Generate functional test cases','value':'Generate functional test cases'}
]

test_genius_layout = html.Div([
    dbc.Navbar(children=[
        dbc.NavItem(html.A(html.I(className="fas fa-home"), href="/",style={"margin":"0px 0px 0px 20px","font-size":"30px","color":"white"})),
        dbc.NavbarBrand("Auto Test Generator", className="mx-auto",style={"text-align":"center","font-size":"35px","font-weight":"bold"}),
        dbc.NavItem("Synapt-GDK", style={"margin-right": "20px", "color":"red","font-weight":"bold"})],color="dark",dark=True),
    dbc.Row([
        dbc.Col([
            dbc.Select(
                id = 'test-genius-action-dropdown',
                options= test_genius_dropdown_option,
                style={'background-color': '#444444','color':'white'},
                placeholder="Select an Action",
                value = None
            )
        ],width = 6),
        dbc.Col([
            dbc.Textarea(id='test-genius-code-language',value = None, placeholder='Code Language or Framework (eg: C++, Java, Python, etc)', style={'height': '10px', 'resize': 'none','background-color': '#444444', 'color': 'white',})
        ], width = 6),
        # dbc.Col([
        #     dbc.Textarea(id='test-genius-intent',value = None, placeholder='Framework Used or Extra Information', style={'height': '10px', 'resize': 'none','background-color': '#444444', 'color': 'white',})
        # ], width = 4),
    ],style={"margin":"20px 0px"}),
    dbc.Row([
        dbc.Col([
            html.H3("Test Case Description:", style={'font-size':'30px'}),
            dbc.Textarea(id = 'test-genius-input', placeholder= 'Type or Paste your code here...', style={'height':'150px','resize':'none','background-color':'#444444','color':'white'})
        ], width= 11),
        dbc.Col([
            dbc.Button([html.I(' Submit',className='fas fa-paper-plane')], color='primary', id = "test-genius-submit", style={'justify-content': 'center','width':'120px','margin': '47px 0px 0px 0px'}),
            dbc.Button([html.I(' Download',className='fas fa-download')], color="primary",href="",download="example.docx",target="_blank", style={'justify-content': 'center','width':'120px','margin': '16px 0px 0px 0px'},id = "test-genius-save"),
            dbc.Button([html.I(' Email',className='fas fa-envelope')], color="success", style={'justify-content': 'center','width':'120px','margin': '16px 0px 0px 0px'},id = "test-genius-email"),
        ], className='d-flex flex-column align-items-center')
    ],style={'margin':'20px 0px'}),
    dcc.Loading(id='test-genius-loading', children=[
        html.Div(id='test-genius-loading-output'),
    ], type='circle', fullscreen=False),
    dbc.Row([
        dbc.Col([
            html.H3("Test Steps", style={'font-size': '30px'}),
            dbc.Textarea(id='test-genius-test-steps',placeholder='Nothing generated yet...', style={'height': '500px', 'resize': 'none', 'word-wrap':'break-word', 'overflow-wrap':'break-word','background-color': '#444444', 'color': 'white'},readOnly = True)
        ], width=4),
        dbc.Col([
            html.H3("Test Data", style = {'font-size':'30px'}),
            dbc.Textarea(id='test-genius-test-data',placeholder='Nothing generated yet...', style={'height': '500px', 'resize': 'none', 'word-wrap':'break-word', 'overflow-wrap':'break-word','background-color': '#444444', 'color': 'white'},readOnly = True)
        ], width=4),
        dbc.Col([
            html.H3("Test Results", style = {'font-size':'30px'}),
            dbc.Textarea(id='test-genius-test-results',placeholder='Nothing generated yet...', style={'height': '500px', 'resize': 'none', 'word-wrap':'break-word', 'overflow-wrap':'break-word','background-color': '#444444', 'color': 'white'},readOnly = True)
        ], width=4),
    ], style={'margin': '20px 0px'}),
])

@app.callback(
    Output('test-genius-test-steps','value'),
    Output('test-genius-test-data','value'),
    Output('test-genius-test-results','value'),
    Output('test-genius-loading','fullscreen'),
    Output('test-genius-loading-output','children'),
    Input('test-genius-submit','n_clicks'),
    State('test-genius-input','value'),
    State('test-genius-action-dropdown','value'),
    State('test-genius-code-language','value'),
    # State("test-genius-intent",'value'),
    State('test-genius-loading','fullscreen')
)
def generate_test_genius_output(n_clicks, code_input, action_selected, code_language, fullscreen):
    result = ""
    test_data_content1 = ""
    test_data_content2 = ""
    if n_clicks is None:
        return '',"","",False,''
    if n_clicks  is not None and action_selected is None:
        return "Error - Select an Action First",'','',False,''
    if n_clicks is not None and code_language is None or code_language == '':
        code_language = 'java'
    if n_clicks is not None and code_language is None:
        return "Error - Enter Code!",'','',False,''
    if action_selected == 'Generate unit test cases':
        fullscreen = True
        result = get_test_case_from_openai(code_input, action_selected, code_language)
        result = result.split('///')
        test_data = result[0]
        result = result[1]
        result = result.split('\n')
        test_steps = ''
        test_steps_list = result[:-3]
        for i in test_steps_list:
            test_steps = test_steps + '\n' + i
        test_result = ''
        test_result_list = result[-3:]
        for i in test_result_list:
            test_result = test_result + '\n' + i
        fullscreen = False
        return test_steps.strip(), test_data.strip(), test_result.strip(), False, ""
    if action_selected == 'Generate functional test cases':
        fullscreen = True
        try:
            test_steps, test_result_action, test_result_expectation, test_data = get_functional_test_response(code_input)
            test_result = "Action (Expected result below) -\n"+test_result_action+"\n\nExpected Result-\n"+test_result_expectation
            result = test_steps.split('\n')
            test_data1 = result[-2:]
            test_data2 = result[:-2]

            for i in test_data1:
                test_data_content1 = test_data_content1 + "\n" + i
            for i in test_data2:
                test_data_content2 = test_data_content2 + "\n" + i
        except Exception as e:
            test_steps = "Some Error Occured. Please try after some time"
            test_data = ""
            test_result = ""
        fullscreen = False
        return test_data_content2.strip(),test_data.strip(),test_result.strip()+"\nFinal Results-\n"+test_data_content1, False, ''
    else:
        return "","","", False, ""

    

@app.callback(
    Output('test-genius-save','href'),
    Input('test-genius-save','n_clicks'),
    State('test-genius-action-dropdown','value'),
    State('test-genius-code-language','value'),
    State('test-genius-input','value'),
    State('test-genius-test-steps','value'),
    State('test-genius-test-data','value'),
    State('test-genius-test-results','value')
)
def create_test_genius_document(n_clicks, action_selected, code_language, input, test_steps, test_data, test_results):
    if code_language is None:
        code_language = 'N/A (default : Python)'
    n_clicks = 0
    if n_clicks is not None or n_clicks > 0:
        document_content = action_selected.upper()+"\n\nCode Language = "+code_language+"\n\nTest Case Description-:\n"+input.strip()+"\n\nTest Steps -:\n"+test_steps.strip()+"\n\nTest Data-: \n"+test_data.strip()+"\n\nTest Result -:\n"+test_results
        doc = document_content.encode("utf-8")
        b64 = base64.b64encode(doc).decode()
        href = f"data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{b64}"
        return href

# %% Sentiment Analysis:

sentiment_analysis_layout = html.Div([
    dbc.Navbar(children=[
        dbc.NavItem(html.A(html.I(className="fas fa-home"), href="/",style={"margin":"0px 0px 0px 20px","font-size":"30px","color":"white"})),
        dbc.NavbarBrand("Sentiment Analysis", className="mx-auto",style={"text-align":"center","font-size":"35px","font-weight":"bold"}),
        dbc.NavItem("Synapt-GDK", style={"margin-right": "20px", "color":"red","font-weight":"bold"})],color="dark",dark=True),
    dbc.Row([
        dbc.Col([
            html.H3("Social Media Comments ",style={'font-size':'30px'}),
            dbc.Textarea(id='sentiment-analysis-input-textarea',placeholder='Paste here...',style={'height': '300px', 'resize': 'none','background-color': '#444444', 'color': 'white'}),
        ],width=4),
        dbc.Col([
            html.H3("Customer's Intentions",style={'font-size':'30px'}),
            dbc.Textarea(id = 'sentiment-analysis-intentions-box',placeholder='Nothing generated yet...', style={'height': '300px', 'resize': 'none','background-color': '#444444', 'color': 'white'},readOnly = True)
        ],width=4),
        dbc.Col([
            html.H3('Sentiment Classification',style={'font-size':'30px'}),
            dbc.Textarea(id='sentiment-analysis-sentiment-output',readOnly=True,placeholder='Nothing generated yet...',style={'height': '125px', 'resize': 'none','background-color': '#444444', 'color': 'white'}),
            html.H3('Impacted Services'),
            dbc.Textarea(id='sentiment-analysis-product-output',readOnly=True,placeholder='Nothing generated yet...',style={'height': '128px', 'resize': 'none','background-color': '#444444', 'color': 'white'})
        ],width=3),
        dbc.Col([
            dbc.Button([html.I(' Submit',className='fas fa-paper-plane')], color='primary', id = "sentiment-analysis-submit", style={'height':'82px','justify-content': 'center','width':'120px','margin': '47px 0px 0px 0px'}),
            dbc.Button([html.I(' \nDownload',className='fas fa-download',style={'justify-content':'center','margin':'25px 0px 0px 0px'})], color="primary",href="",download="example.docx",target="_blank", style={'height':'82px','width':'120px','margin': '24px 0px 0px 0px'},id = "sentiment-analysis-save"),
            dbc.Button([html.I(' Share',className='fas fa-envelope')], color="success", style={'height':'82px','justify-content': 'center','width':'120px','margin': '24px 0px 0px 0px'},id = "sentiment-analysis-email"),
        ], className='d-flex flex-column align-items-center'),
    ],style={'margin':'20px 0px'}),
    dbc.Row([
        dbc.Alert("Failed to send Email. Check your password and try again", id="sentiment-email-failed", color="danger", dismissable=True, is_open=False, className="mt-3")
    ]),
    dbc.Row([
        dbc.Alert("Email sent successfully", id="sentiment-email-success", color="success", dismissable=True, is_open=False, className="mt-3")
    ]),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.H3('Social Media Handler Action'),
            dbc.Textarea(id='sentiment-analysis-action-box',placeholder='Nothing generated yet...',readOnly=True,style={'height': '300px', 'resize': 'none','background-color': '#444444', 'color': 'white'})
        ],width=4),
        dbc.Col([
            html.H3('Action to Operation'),
            dbc.Textarea(id='sentiment-analysis-operation-box',placeholder='Nothing generated yet...',readOnly=True,style={'height': '300px', 'resize': 'none','background-color': '#444444', 'color': 'white'})
        ],width=4),
        dbc.Col([
            html.H3('Sentiment Vision (wip)'),
            dbc.Textarea(id='sentiment-analysis-visualization-box',readOnly=True,style={'height': '300px', 'resize': 'none','background-color': '#444444', 'color': 'white'})
        ],width=4),
    ],style={'margin':'20px 0px'}),
    dcc.Loading(id='sentiment-loading', children=[
        html.Div(id='sentiment-loading-output'),
    ], type='circle', fullscreen=False),
])

@app.callback(
        Output('sentiment-email-failed','is_open'),
        Output('sentiment-email-success','is_open'),
        Input("sentiment-analysis-email",'n_clicks'),
        State('sentiment-email-failed','is_open'),
        State('sentiment-email-success','is_open'),
        State('sentiment-analysis-input-textarea','value'),
        State('sentiment-analysis-intentions-box','value'),
        State('sentiment-analysis-sentiment-output','value'),
        State('sentiment-analysis-product-output','value'),
        State('sentiment-analysis-action-box','value'),
        State('sentiment-analysis-operation-box','value')
)
def send_email_show_alert(n_clicks,email_failed,email_sent, social_media_comments, customer_intention, sentiment_classification, impacted_services, social_media, action_to_take):
    if n_clicks is None:
        return False,False
    if social_media_comments is None or customer_intention is None or sentiment_classification is None or impacted_services is None or social_media is None or action_to_take is None:
        return True,False
    try:
        email_body = "SOCIAL MEDIA COMMENT\n"+social_media_comments+"\n\nACTION TO OPERATION\n"+action_to_take+"\n\n\n\nThis is a computer generated response."
        send_email(email_body)
        return False,True
    except Exception as e:
        logging.error(f'str{e}')
        return True,False

@app.callback(
    Output('sentiment-analysis-sentiment-output','value'),
    Output('sentiment-analysis-intentions-box','value'),
    Output('sentiment-analysis-product-output','value'),
    Output('sentiment-analysis-action-box','value'),
    Output('sentiment-analysis-operation-box','value'),
    Output('sentiment-loading', 'fullscreen'), 
    Output('sentiment-loading-output', 'children'),
    State('sentiment-analysis-input-textarea','value'),
    State('sentiment-loading','fullscreen'),
    Input("sentiment-analysis-submit",'n_clicks'),
)
def get_sentiments(textarea,fullscreen, n_clicks):
    if n_clicks is None:
        return "","","","","",False,""
    fullscreen = True
    start_time = time.time()
    try:
        response = get_sentiments_from_openai(textarea)
        response = response.split("\n")
        operation_action = response[9].replace(' ','\n')
        operation_action = operation_action.replace('_',' ')
    except Exception as e:
        response = "Error\nError\nError\nError\nError\nError\nError\nError\nError\nError_occured_while_establishing_connection_to_OpenAI 1._Check_your_internet_connection 2._Make_sure_you_entered_your_API_key_Correctly. 3._Wait_for_some_time_and_try_again. 4._Try_with_new_api_key See_logs_for_troubleshooting\nError\nError"
        response = response.split("\n")
        operation_action = response[9].replace(' ','\n')
        operation_action = operation_action.replace('_',' ')
        logging.error(f"Error Occured while connecting to openAI \n{str(e)}'")
    fullscreen = False
    end_time = time.time()
    total_time = end_time - start_time
    

    #save in sql
    conn = sqlite3.connect('code_ops_analyser.db')
    sql_query = "Insert into sentiment_analysis(comment, customer_intentions, sentiment_classification, impacted_services, social_media_handler_action, action_to_operation, exe_time) Values (?,?,?,?,?,?,?)"
    query_values = (
        textarea,
        response[3],
        response[1],
        response[5],
        response[7],
        operation_action,
        total_time
    )
    conn.execute(sql_query,query_values)
    conn.commit()
    conn.close()
    return response[1]+"\n\nEstimated NPS - "+response[11]+" out of 5"+" "+response[13],response[3],response[5],response[7],operation_action,fullscreen,""

@app.callback(
        Output('sentiment-analysis-save','href'),
        Input('sentiment-analysis-input-textarea','value'),
        Input('sentiment-analysis-intentions-box','value'),
        Input('sentiment-analysis-sentiment-output','value'),
        Input('sentiment-analysis-product-output','value'),
        Input('sentiment-analysis-action-box','value'),
        Input('sentiment-analysis-operation-box','value'),
        Input('sentiment-analysis-save','n_clicks')
)
def generate_sentiment_analysis_report(input, intentions, sentiments, impacted_services, social_media, actions, n_clicks):
    if input is None:
        input = ""
    if intentions is None:
        intentions = ""
    if sentiments is None:
        sentiments = ""
    if impacted_services is None:
        impacted_services = ""
    if social_media is None:
        social_media = ""
    if actions is None:
        actions = ""
    n_clicks = 0
    if n_clicks is not None or n_clicks > 0: 
        document_content = "Comments:\n"+input+"\n\nIntentions:\n"+intentions+"\n\nSentiments:\n"+sentiments+"\n\nImpacted Services:\n"+impacted_services+"\n\nSocial Media Handler Action:\n"+social_media+"\n\nAction to Operation:\n"+actions
        doc = document_content.encode('utf-8')
        b64 = base64.b64encode(doc).decode()
        href = f"data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{b64}"
        return href
    
#%%
sentiment_analysis_new_layout = html.Div([
    dcc.Location(id='sentiment-google', refresh=False),
    dbc.Navbar(children=[dbc.NavItem(html.A(html.I(className="fas fa-home"), href="/",style={"margin":"0px 0px 0px 20px","font-size":"30px","color":"white"})),dbc.NavbarBrand("Sentiment Analysis", className="mx-auto",style={"text-align":"center","font-size":"35px","font-weight":"bold"})],color="dark",dark=True),
    dbc.Row([
        dbc.Col([
            html.H3("Detailed Transcript ",style={'font-size':'30px'}),
            dbc.Textarea(id='sentiment-analysis-new-input-textarea',placeholder='Nothing generated yet...',style={'height': '300px', 'resize': 'none','background-color': '#444444', 'color': 'white'},readOnly=True),
        ],width=4),
        dbc.Col([
            html.H3("Customer's Intentions",style={'font-size':'30px'}),
            dbc.Textarea(id = 'sentiment-analysis-new-intentions-box',placeholder='Nothing generated yet...', style={'height': '300px', 'resize': 'none','background-color': '#444444', 'color': 'white'},readOnly = True)
        ],width=4),
        dbc.Col([
            html.H3('Sentiment Classification',style={'font-size':'30px'}),
            dbc.Textarea(id='sentiment-analysis-new-sentiment-output',readOnly=True,placeholder='Nothing generated yet...',style={'height': '125px', 'resize': 'none','background-color': '#444444', 'color': 'white'}),
            html.H3('Impacted Services'),
            dbc.Textarea(id='sentiment-analysis-new-product-output',readOnly=True,placeholder='Nothing generated yet...',style={'height': '128px', 'resize': 'none','background-color': '#444444', 'color': 'white'})
        ],width=3),
        dbc.Col([
            dbc.Button([html.I(' Submit',className='fas fa-paper-plane')], color='primary', id = "sentiment-analysis-new-submit", style={'height':'82px','justify-content': 'center','width':'120px','margin': '47px 0px 0px 0px'}),
            dbc.Button([html.I(' \nDownload',className='fas fa-download',style={'justify-content':'center','margin':'25px 0px 0px 0px'})], color="primary",href="",download="example.docx",target="_blank", style={'height':'82px','width':'120px','margin': '24px 0px 0px 0px'},id = "sentiment-analysis-new-save"),
            dbc.Button([html.I(' Share',className='fas fa-envelope')], color="success", style={'height':'82px','justify-content': 'center','width':'120px','margin': '24px 0px 0px 0px'},id = "sentiment-analysis-new-email"),
        ], className='d-flex flex-column align-items-center'),
    ],style={'margin':'20px 0px'}),
    dbc.Row([
        dbc.Alert("Failed to send Email. Check your password and try again", id="sentiment-new-email-failed", color="danger", dismissable=True, is_open=False, className="mt-3")
    ]),
    dbc.Row([
        dbc.Alert("Email sent successfully", id="sentiment-new-email-success", color="success", dismissable=True, is_open=False, className="mt-3")
    ]),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.H3('Social Media Handler Action'),
            dbc.Textarea(id='sentiment-analysis-new-action-box',placeholder='Nothing generated yet...',readOnly=True,style={'height': '300px', 'resize': 'none','background-color': '#444444', 'color': 'white'})
        ],width=4),
        dbc.Col([
            html.H3('Action to Operation'),
            dbc.Textarea(id='sentiment-analysis-new-operation-box',placeholder='Nothing generated yet...',readOnly=True,style={'height': '300px', 'resize': 'none','background-color': '#444444', 'color': 'white'})
        ],width=4),
        dbc.Col([
            html.H3('Sentiment Vision (wip)'),
            dbc.Textarea(id='sentiment-analysis-new-visualization-box',readOnly=True,style={'height': '300px', 'resize': 'none','background-color': '#444444', 'color': 'white'})
        ],width=4),
    ],style={'margin':'20px 0px'}),
    dcc.Loading(id='sentiment-new-loading', children=[
        html.Div(id='sentiment-new-loading-output'),
    ], type='circle', fullscreen=False),
])

@app.callback(
    Output('sentiment-analysis-new-input-textarea','value'),
    Output('sentiment-analysis-new-intentions-box','value'),
    Output('sentiment-analysis-new-sentiment-output','value'),
    Output('sentiment-analysis-new-product-output','value'),
    Output('sentiment-analysis-new-action-box','value'),
    Output('sentiment-analysis-new-operation-box','value'),
    Input('sentiment-google','pathname')
)
def get_sentiments_through_pipeline(pathname):
    if pathname == '/sentimentanalysis':
        try:
            global CLIENT_SECRET_FILE
            global API_NAME
            global API_VERSION
            global FOLDER_ID
            global SCOPE

            start_time = time.time()

            service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPE)
            query = "parents = '{}' and mimeType = 'text/plain'".format(FOLDER_ID)
            results = service.files().list(q=query, fields="files(id, name, createdTime)").execute()
            #print(results)
            sorted_results = sorted(results['files'], key=lambda k: k['createdTime'], reverse=True)
            #print()
            #print(sorted_results)
            latest_file_id = sorted_results[0]['id']
            latest_file_name = sorted_results[0]['name']
            #print(latest_file_id)
            #print(latest_file_name)

            request = service.files().get_media(fileId=latest_file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            #print(f'Download {int(status.progress() * 100)}.')
            file_content = fh.getvalue().decode('utf-8')
            #print(file_content)
            file_contents = file_content.split("\n")
            operation_action = file_contents[11].replace(' ','\n')
            operation_action = operation_action.replace('_',' ')

            end_time = time.time()
            total_time = end_time - start_time

            conn = sqlite3.connect('code_ops_analyser.db')
            sql_query = "Insert into sentiment_analysis(comment, customer_intentions, sentiment_classification, impacted_services, social_media_handler_action, action_to_operation, exe_time) Values (?,?,?,?,?,?,?)"
            query_values = (
                file_contents[1],
                file_contents[5],
                file_contents[3],
                file_contents[7],
                file_contents[9],
                operation_action,
                total_time
            )
            conn.execute(sql_query,query_values)
            conn.commit()
            conn.close()

            return file_contents[1], file_contents[5], file_contents[3]+"\n\nEstimated NPS - "+ file_contents[13]+" out of 5 "+file_contents[15], file_contents[7], file_contents[9], operation_action
        
        except Exception as e:
            return str(e),'','','','',''
    else:
        return 'Path is not /sentimentanalysis','0','0','0','0','0'
    
@app.callback(
        Output('sentiment-new-email-failed','is_open'),
        Output('sentiment-new-email-success','is_open'),
        Input("sentiment-analysis-new-email",'n_clicks'),
        State('sentiment-new-email-failed','is_open'),
        State('sentiment-new-email-success','is_open'),
        State('sentiment-analysis-new-input-textarea','value'),
        State('sentiment-analysis-new-intentions-box','value'),
        State('sentiment-analysis-new-sentiment-output','value'),
        State('sentiment-analysis-new-product-output','value'),
        State('sentiment-analysis-new-action-box','value'),
        State('sentiment-analysis-new-operation-box','value')
)
def send_email_show_alert(n_clicks,email_failed,email_sent, social_media_comments, customer_intention, sentiment_classification, impacted_services, social_media, action_to_take):
    if n_clicks is None:
        return False,False
    if social_media_comments is None or customer_intention is None or sentiment_classification is None or impacted_services is None or social_media is None or action_to_take is None:
        return True,False
    try:
        email_body = "SOCIAL MEDIA COMMENT\n"+social_media_comments+"\n\nACTION TO OPERATION\n"+action_to_take+"\n\n\n\nThis is a computer generated response."
        send_email(email_body)
        return False,True
    except Exception as e:
        logging.error(f'str{e}')
        return True,False
    
@app.callback(
        Output('sentiment-analysis-new-save','href'),
        Input('sentiment-analysis-new-input-textarea','value'),
        Input('sentiment-analysis-new-intentions-box','value'),
        Input('sentiment-analysis-new-sentiment-output','value'),
        Input('sentiment-analysis-new-product-output','value'),
        Input('sentiment-analysis-new-action-box','value'),
        Input('sentiment-analysis-new-operation-box','value'),
        Input('sentiment-analysis-new-save','n_clicks')
)
def generate_sentiment_analysis_report(input, intentions, sentiments, impacted_services, social_media, actions, n_clicks):
    if input is None:
        input = ""
    if intentions is None:
        intentions = ""
    if sentiments is None:
        sentiments = ""
    if impacted_services is None:
        impacted_services = ""
    if social_media is None:
        social_media = ""
    if actions is None:
        actions = ""
    n_clicks = 0
    if n_clicks is not None or n_clicks > 0: 
        document_content = "Comments:\n"+input+"\n\nIntentions:\n"+intentions+"\n\nSentiments:\n"+sentiments+"\n\nImpacted Services:\n"+impacted_services+"\n\nSocial Media Handler Action:\n"+social_media+"\n\nAction to Operation:\n"+actions
        doc = document_content.encode('utf-8')
        b64 = base64.b64encode(doc).decode()
        href = f"data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{b64}"
        return href
    
#%% DIALOGUE DIAGNOSTICS

dialogue_diagnostic_layout = html.Div([
    dcc.Location(id='dialogue-diagnostic-google', refresh=False),
    dbc.Navbar(children=[dbc.NavItem(html.A(html.I(className="fas fa-home"), href="/",style={"margin":"0px 0px 0px 20px","font-size":"30px","color":"white"})),dbc.NavbarBrand("Dialogue Diagnostic", className="mx-auto",style={"text-align":"center","font-size":"35px","font-weight":"bold"})],color="dark",dark=True),
    dbc.Row([
        dbc.Col([
            html.H3("Detailed Transcript",style = {'font-size':'30px'}),
            dbc.Textarea(id='dialogue-diagnostic-input-textarea',placeholder='Nothing generated yet...',style={'height': '300px', 'resize': 'none','background-color': '#444444', 'color': 'white'},readOnly=True),
        ],width=4),
        dbc.Col([
            html.H3("Customer's Intentions",style={'font-size':'30px'}),
            dbc.Textarea(id = 'dialogue-diagnostic-intentions-box',placeholder='Nothing generated yet...', style={'height': '300px', 'resize': 'none','background-color': '#444444', 'color': 'white'},readOnly = True)
        ],width=4),
        dbc.Col([
            html.H3('Sentiment Classification',style={'font-size':'30px'}),
            dbc.Textarea(id='dialogue-diagnostic-sentiment-output',readOnly=True,placeholder='Nothing generated yet...',style={'height': '125px', 'resize': 'none','background-color': '#444444', 'color': 'white'}),
            html.H3('Impacted Services'),
            dbc.Textarea(id='dialogue-diagnostic-product-output',readOnly=True,placeholder='Nothing generated yet...',style={'height': '128px', 'resize': 'none','background-color': '#444444', 'color': 'white'})
        ],width=4),
    ],style={'margin':'20px 0px'}),
    dbc.Row([
        dbc.Alert("Failed to send Email. Check your password and try again", id="dialogue-diagnostic-email-failed", color="danger", dismissable=True, is_open=False, className="mt-3")
    ],style={'margin':'20px 0px'}),
    dbc.Row([
        dbc.Alert("Email sent successfully", id="dialogue-diagnostic-email-success", color="success", dismissable=True, is_open=False, className="mt-3")
    ],style={'margin':'20px 0px'}),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.H3('Transcript Summary',style={'font-size':'30px'}),
            dbc.Textarea(id='dialogue-diagnostic-action-box',placeholder='Nothing generated yet...',readOnly=True,style={'height': '300px', 'resize': 'none','background-color': '#444444', 'color': 'white'})
        ],width=4),
        dbc.Col([
            html.H3('Action to Operation',style={'font-size':'30px'}),
            dbc.Textarea(id='dialogue-diagnostic-operation-box',placeholder='Nothing generated yet...',readOnly=True,style={'height': '300px', 'resize': 'none','background-color': '#444444', 'color': 'white'})
        ]),
        dbc.Col([
            html.H3('Sentiment Vision'),
            dbc.Textarea(id='dialogue-diagnostic-visualization-box',readOnly=True,style={'height': '300px', 'resize': 'none','background-color': '#444444', 'color': 'white'})
        ],width=4),
    ],style={'margin':'20px 0px'})
])

@app.callback(
    Output("dialogue-diagnostic-input-textarea","value"),
    Output("dialogue-diagnostic-intentions-box","value"),
    Output("dialogue-diagnostic-sentiment-output","value"),
    Output("dialogue-diagnostic-product-output","value"),
    Output("dialogue-diagnostic-action-box","value"),
    Output("dialogue-diagnostic-operation-box","value"),
    Output("dialogue-diagnostic-visualization-box","value"),
    Input("dialogue-diagnostic-google","pathname")
)
def fill_dialogue_diagnostics(pathname):
    if pathname == '/dialoguediagnostics':
        try:
            global CLIENT_SECRET_FILE
            global API_NAME
            global API_VERSION
            global FOLDER_ID
            global SCOPE

            start_time = time.time()
            service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPE)
            query = "parents = '{}' and mimeType = 'text/plain'".format(FOLDER_ID)
            results = service.files().list(q=query, fields="files(id, name, createdTime)").execute()
            #print(results)
            sorted_results = sorted(results['files'], key=lambda k: k['createdTime'], reverse=True)
            #print()
            #print(sorted_results)
            latest_file_id = sorted_results[0]['id']
            latest_file_name = sorted_results[0]['name']
            #print(latest_file_id)
            #print(latest_file_name)

            request = service.files().get_media(fileId=latest_file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            #print(f'Download {int(status.progress() * 100)}.')
            file_content = fh.getvalue().decode('utf-8')
            #print(file_content)

            end_time = time.time()
            total_time = end_time - start_time

            file_content = file_content.split("\n")

            transcript_summary = file_content[2]
            transcript_summary = transcript_summary.replace(" ","\n")
            transcript_summary = transcript_summary.replace("_"," ")

            action_to_operation = file_content[12]
            action_to_operation = action_to_operation.replace(" ","\n")
            action_to_operation = action_to_operation.replace("_"," ")

            purpose = file_content[2]
            purpose = purpose.split(" ")
            purpose = purpose[1]
            purpose = purpose.replace("_"," ")
            random_number = random.randint(1000,9999)

            return file_content[0],file_content[6],file_content[4],file_content[8],transcript_summary,action_to_operation,f"a. Estimated NPS - {file_content[14]} {file_content[16]}\n\nb. Estimated Sentiment Score - {file_content[18]}\n\nc. Ticket Information -\n    1. Ticket Number - {random_number}\n    2. Ticket Details-{purpose} \n\n(This will be pushed to ticketing tool like - JIRA or ServiceNow etc)"
        except Exception as e:
            return str(e),"","","","","",""
    else:
        return "pathname is not '/dialoguediagnostics'","","","","","",""


## RCA
rca_dropdown_option = [
    {'label':'Error Fetching','value':'API Integration'},
]

api_analysis_layout = html.Div([
    dbc.Navbar(children=[
        dbc.NavItem(html.A(html.I(className="fas fa-home"), href="/",style={"margin":"0px 0px 0px 20px","font-size":"30px","color":"white"})),
        dbc.NavbarBrand("Root Cause Analysis", className="mx-auto",style={"text-align":"center","font-size":"35px","font-weight":"bold"}),
        dbc.NavItem("Synapt-GDK", style={"margin-right": "20px", "color":"red","font-weight":"bold"})],color="dark",dark=True),
    dbc.Row([
        dbc.Col([
            dbc.Select(
                id = 'rca-action-dropdown',
                options= rca_dropdown_option,
                style={'background-color': '#444444','color':'white'},
                placeholder="Select an Action",
                value = "API Integration"
            )
        ],width = 6),
        dbc.Col([
            dbc.Textarea(id='rca-api-endpoint',value = None, placeholder='API Endpoint', style={'height': '10px', 'resize': 'none','background-color': '#444444', 'color': 'white',})
        ], width = 6),
    ],style={"margin":"20px 0px"}),
    dbc.Row([
        dbc.Col([
            html.H3("Logs:", style={'font-size':'30px'}),
            dbc.Textarea(id = 'rca-input', placeholder= 'Type or Paste logs here...', style={'height':'150px','resize':'none','background-color':'#444444','color':'white'})
        ], width= 11),
        dbc.Col([
            dbc.Button([html.I(' Submit',className='fas fa-paper-plane')], color='primary', id = "rca-submit", style={'justify-content': 'center','width':'120px','margin': '47px 0px 0px 0px'}),
            dbc.Button([html.I(' Download',className='fas fa-download')], color="primary",href="",download="example.docx",target="_blank", style={'justify-content': 'center','width':'120px','margin': '16px 0px 0px 0px'},id = "rca-save"),
            dbc.Button([html.I(' Email',className='fas fa-envelope')], color="success", style={'justify-content': 'center','width':'120px','margin': '16px 0px 0px 0px'},id = "rca-email"),
        ], className='d-flex flex-column align-items-center')
    ],style={'margin':'20px 0px'}),
    dcc.Loading(id='rca-loading', children=[
        html.Div(id='rca-loading-output'),
    ], type='circle', fullscreen=False),
    dbc.Row([
        dbc.Alert("Failed to send Email. Check your password and try again", id="rca-email-failed", color="danger", dismissable=True, is_open=False, className="mt-3")
    ]),
    dbc.Row([
        dbc.Alert("Email sent successfully", id="rca-email-success", color="success", dismissable=True, is_open=False, className="mt-3")
    ]),
    dbc.Row([
        dbc.Col([
            html.H3("Error Analysis", style = {'font-size':'30px'}),
            dbc.Textarea(id='rca-classification-box',placeholder='Nothing generated yet...', style={'height': '500px', 'resize': 'none', 'word-wrap':'break-word', 'overflow-wrap':'break-word','background-color': '#444444', 'color': 'white'},readOnly = True)
        ], width=4),
        dbc.Col([
            html.H3("5-Why Analysis", style={'font-size': '30px'}),
            dbc.Textarea(id='rca-analysis-box',placeholder='Nothing generated yet...', style={'height': '500px', 'resize': 'none', 'word-wrap':'break-word', 'overflow-wrap':'break-word','background-color': '#444444', 'color': 'white'},readOnly = True)
        ], width=4),
        dbc.Col([
            html.H3("Proposed Solution", style = {'font-size':'30px'}),
            dbc.Textarea(id='rca-proposed-solution-box',placeholder='Nothing generated yet...', style={'height': '500px', 'resize': 'none', 'word-wrap':'break-word', 'overflow-wrap':'break-word','background-color': '#444444', 'color': 'white'},readOnly = True)
        ], width=4),
    ], style={'margin': '20px 0px'}),
])

@app.callback(
    Output('rca-save', 'href'),
    Input('rca-save', 'n_clicks'),
    State('rca-input', 'value'),
    State('rca-analysis-box', 'value'),
    State('rca-classification-box', 'value'),
    State('rca-proposed-solution-box', 'value')
)
def create_rca_document(n_clicks, input, analysis, classification, solution):
    n_clicks = 0
    if n_clicks is not None or n_clicks > 0:
        document_content = f"""Error Conditions:\n{input}\n\n5 Why? Analysis:\n{analysis}\n\nError Classification:\n{classification}\n\nProposed Solution:\n{solution}"""
        doc = document_content.encode("utf-8")
        b64 = base64.b64encode(doc).decode()
        href = f"data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{b64}"
        return href
    
def get_rca_result_from_openai(input):
    my_custom_function = [
        {
            'name': 'get_rca_result_from_openai',
            'description': 'read the api error from the body of input text',
            'parameters': {
                'type': 'object',
                'properties': {
                    'classification': {
                        'type': 'string',
                        'description': 'Classify the error from following points - Incorrect API Permissions, Unsecured Endpoints and Data Access Tokens, Invalid Session Management, Expiring APIs, Bad URLs/HTTP Errors, Overly Complex API Endpoints, Exposed APIs on IPs'
                    },
                    'analysis': {
                        'type': 'string',
                        'description': r'Give analysis of the error in 5-WHY principle in generic form eg - Why did the API error occur?, Why is there maintenance or an unexpected issue?, etc. (give 5 questions and their analysis) also add ". \n" after end of each analysis '
                    },
                    'solution': {
                        'type': 'string',
                        'description': 'possible solutions considering analysis of the error in 5 points'
                    },
                    'depth_classification': {
                        'type': 'string',
                        'description': 'Classify the error in following points - 1. Request URL, 2. Error Type, 3. Error Code, 4. Error Message, 5. Request Method, 6. Category, 7. Probable Cause, 8. Context, 9. Framework version, 10. Exception Location, 11. Impacted systems, 12. Impacted services, 13. Number of lines of logs processed (count yourself), 14. Is password or sensitive information exposed? (Yes/No), 15. Is there any 3rd party system integration challenge? If yes, list them. (write in number Points and type "not available" if not found)'
                    },
                    'specific_solution': {
                        'type': 'string',
                        'description': 'possible solutions considering analysis of the error specifically error message and error type in 5 points'
                    },
                    'solution_code': {
                        'type': 'string',
                        'description': 'write only code/sample_configuration to solve this issue (No explanation and no AI like "Here is a sample code snippet..."). If not available tell recommendation in code to resolve this issue. IMPORTANT: "Write a disclaimer to check code (if any) after 1 blank line"'
                    },
                }
            }   
        }
    ]

    api_error = input

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{'role': 'user', 'content': api_error}],
        temperature=0.3,
        max_tokens=1600,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        functions = my_custom_function,
        function_call = 'auto'
    )

    answer = response.choices[0].message.function_call.arguments

    answer = json.loads(answer)

    pre_analysis = answer['analysis']
    pre_analysis = pre_analysis.replace('? ','?\n')
    pre_analysis = pre_analysis.replace('. \n','. \n\n')

    return f"{answer['classification']}\n\nDEPTH CLASSIFICATION:\n{answer['depth_classification']}", f"{answer['solution']}\n\nRecommendation for solution (Code/Recommendation):\n\n{answer['solution_code']}", f"{pre_analysis}" #

@app.callback(
    Output('rca-analysis-box', 'value'),
    Output('rca-classification-box', 'value'),
    Output('rca-proposed-solution-box', 'value'),
    Output('rca-loading','fullscreen'),
    Output('rca-loading-output','children'),
    Input('rca-submit', 'n_clicks'),
    State('rca-input', 'value'),
    State('rca-loading','fullscreen')
)
def get_rca_result(n_clicks, input, fullscreen):
    if n_clicks is None:
        return '',"","",False,''
    else:
        try:
            fullscreen = True
            classification, solution, analysis = get_rca_result_from_openai(input)
            fullscreen = False
            return analysis, classification, solution, fullscreen, ""
        except Exception as e:
            fullscreen = True
            fullscreen = False
            classification, solution, analysis = str(e), "None", str(e)
            return analysis, "Some Error Occured\nRefer Logs for solution", solution, fullscreen, ""
        
@app.callback(
    Output('rca-email-failed','is_open'),
    Output('rca-email-success','is_open'),
    Input("rca-email",'n_clicks'),
    State('rca-email-failed','is_open'),
    State('rca-email-success','is_open'),
    State('rca-input', 'value'),
    State('rca-analysis-box', 'value'),
    State('rca-classification-box', 'value'),
    State('rca-proposed-solution-box', 'value')
)
def send_rca_email(n_clicks, email_failed, email_sent, input, analysis, classification, solution):
    if n_clicks is None:
        return False,False
    try:
        document_content = f"""Error Conditions:\n{input.strip()}\n\n5 Why? Analysis:\n{analysis.strip()}\n\nError Classification:\n{classification.strip()}\n\nProposed Solution:\n{solution.strip()}""" 
        send_email(document_content)
        return False, True
    except Exception as e:
        logging.error(f'str{e}')
        return True,False
## TS Generator

ts_generator_layout = html.Div([
    dbc.Navbar(children=[
        dbc.NavItem(html.A(html.I(className="fas fa-home"), href="/",style={"margin":"0px 0px 0px 20px","font-size":"30px","color":"white"})),
        dbc.NavbarBrand("Test Scenario Generator", className="mx-auto",style={"text-align":"center","font-size":"35px","font-weight":"bold"}),
        dbc.NavItem("Synapt-GDK", style={"margin-right": "20px", "color":"red", "font-weight":"bold"})],color="dark",dark=True),
    dbc.Row([
        dbc.Col([
            html.H3("Business Case:", style={'font-size':'30px'}),
            dbc.Textarea(id = 'tsg-input', placeholder= 'Type or Paste Buisness case here...', style={'height':'150px','resize':'none','background-color':'#444444','color':'white'})
        ], width= 6),
        dbc.Col([
            html.H3("System Name:", style={'font-size':'30px'}),
            dbc.Textarea(id = 'tsg-system-input', placeholder= 'list name of systems here...', style={'height':'150px','resize':'none','background-color':'#444444','color':'white'})
        ], width= 5),
        dbc.Col([
            dbc.Button([html.I(' Submit',className='fas fa-paper-plane')], color='primary', id = "tsg-submit", style={'justify-content': 'center','width':'120px','margin': '47px 0px 0px 0px'}),
            dbc.Button([html.I(' Download',className='fas fa-download')], color="primary",href="",download="example.docx",target="_blank", style={'justify-content': 'center','width':'120px','margin': '16px 0px 0px 0px'},id = "tsg-save"),
            dbc.Button([html.I(' Email',className='fas fa-envelope')], color="success", style={'justify-content': 'center','width':'120px','margin': '16px 0px 0px 0px'},id = "tsg-email"),
        ], className='d-flex flex-column align-items-center')
    ],style={'margin':'20px 0px'}),
    dcc.Loading(id='tsg-loading', children=[
        html.Div(id='tsg-loading-output'),
    ], type='circle', fullscreen=False),
    dbc.Row([
        dbc.Alert("Failed to send Email. Check your password and try again", id="tsg-email-failed", color="danger", dismissable=True, is_open=False, className="mt-3")
    ]),
    dbc.Row([
        dbc.Alert("Email sent successfully", id="tsg-email-success", color="success", dismissable=True, is_open=False, className="mt-3")
    ]),
    dbc.Row([
        dbc.Col([
            html.H3("Functional Scenario", style = {'font-size':'30px'}),
            dbc.Textarea(id='tsg-functional-box',placeholder='Nothing generated yet...', style={'height': '500px', 'resize': 'none', 'word-wrap':'break-word', 'overflow-wrap':'break-word','background-color': '#444444', 'color': 'white'},readOnly = True)
        ], width=6),
        dbc.Col([
            html.H3("Non-Functional Scenario", style={'font-size': '30px'}),
            dbc.Textarea(id='tsg-non-functional-box',placeholder='Nothing generated yet...', style={'height': '500px', 'resize': 'none', 'word-wrap':'break-word', 'overflow-wrap':'break-word','background-color': '#444444', 'color': 'white'},readOnly = True)
        ], width=6),
    ], style={'margin': '20px 0px'})
])

def get_tsg_functional_response(buisness_use_case, system_name):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-16k",
    messages=[
        {
        "role": "user",
        "content": "\"The system should be able to validate the customer's identity and eligibility for the requested product or service through the CKR system, ensuring that the customer is eligible and authorized to make such requests.\" 1st(what all things are mandatory to be part of buisness story from this use case in User interface (UI) test cases:(give answer in 5 numbered points in new line)).2nd(what all things are mandatory to be part of buisness story from this use case in Usability test cases:(give answer in 5 numbered points in new line)).3rd(what all things are mandatory to be part of buisness story from this use case in Functionality test cases:(give answer in 5 numbered points in new line)).4th(what all things are mandatory to be part of buisness story from this use case in Integration test cases(give answer in 5 numbered points in new line))."
        },
        {
        "role": "assistant",
        "content": "1st_User interface (UI) test cases:  1. The system should be able to prompt the customer for their identity and eligibility information.  2. UI should verify that all the entered information is correct and valid.  3. The system should be able to provide authentication of the customer's identity through CKR system.  4. Once successfully verified, UI should provide confirmation message displaying customer's eligibility and authorization status for requested product or service.  5. System must ensure required exception handling scenarios eg Invalid/Incorrect entries, timeout etc are handled as expected in User Interface (UI) test cases.\n2nd_Usability test cases:  1. Authentication of customer's identity and its eligibility for the requested product or service.  2. Validation of customer's authorization to make such requests.  3. Verification of customer credentials via CKR system.  4. Ensure that responses of the customer to authentication prompts are accurate and secure.  5. Testing if there are any access restrictions when accessing data held in the CKR system.\n3rd_Functionality test cases:  1. The system should be able to authenticate the customer's identity and eligibility through the CKR system.  2. The customer should be eligible and authorized to make requests for the requested product or service.  3. System should check that validations are in place and enforced when a customer attempts to make a request for a product or service.  4. Prerequisites such as entering valid credentials and ensuring applicable regulations/law is adhered must be checked at each step of authentication process.  5. System should alert in case of any abnormalities found during validation process, including missing information, unauthorized access or misuse of data by an end user..\n4th_Integration test cases:  1. The system should be able to access the CKR system and validate customer data against predefined criteria.  2. The system should ensure that only valid and authorized customers are approved for the requested product or service.  3. The system should reject requests from customers who do not meet the criteria set out in the CKR system.  4. The system should provide an appropriate response when a customer’s request is either accepted or rejected, including confirming eligibility or an indication of inaccuracy in identity verification details.  5. The system should capture customer data related to attempts at fraud or unauthorized access of the CKR system in order to identify potential risks and take suitable preventative measures as necessary."
        },
        {
        "role": "user",
        "content": f"\"{buisness_use_case}\" 1st(what all things are mandatory to be part of buisness story from this use case in User interface (UI) test cases:(give answer in 5 numbered points in new line)).2nd(what all things are mandatory to be part of buisness story from this use case in Usability test cases:(give answer in 5 numbered points in new line)).3rd(what all things are mandatory to be part of buisness story from this use case in Functionality test cases:(give answer in 5 numbered points in new line)).4th(what all things are mandatory to be part of buisness story from this use case in Integration test cases(give answer in 5 numbered points in new line))."
        }
    ],
    temperature=0.28,
    max_tokens=2000,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    response = response["choices"][0]["message"]["content"].split("\n")
    ui_response= response[0]
    ui_response = ui_response.split("  ")
    uii_response = ""
    for i , x in enumerate(ui_response):
        if(i==0):
            continue
        uii_response = uii_response + x + "\n"
    
    usability_response = response[1]
    usabilityy_response = ""
    for i , x in enumerate(usability_response):
        if(i==0):
            continue
        usabilityy_response = usabilityy_response + x + "\n"

    functionality_response = response[2]
    functionalityy_response = ""
    for i , x in enumerate(functionality_response):
        if(i==0):
            continue
        functionalityy_response = functionalityy_response + x + "\n"   

    integration_response = response[3]
    integrationn_response = ""
    for i , x in enumerate(integration_response):
        if(i==0):
            continue
        integrationn_response = integrationn_response + x + "\n"     
    
    

    return f"User interface (UI) test cases:\n{uii_response}", f"Usability test cases:\n{usabilityy_response}", f"Functionality test cases:\n{functionalityy_response}", f"Integration test cases:\n{integrationn_response}"

def get_tsg_nonfunctional_response(buisness_use_case, system_name):

    security_response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Statement:\n\"{buisness_use_case}\"\n{system_name}\nwhat all things are mandatory to be part of buisness story from this use case in Security test cases\n(give answer in 5 numbered points in new line)\n\nAnswer:",
        temperature=1,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0.62,
        presence_penalty=0.62
    )

    performnce_response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Statement:\n\"{buisness_use_case}\"\n{system_name}\nwhat all things are mandatory to be part of buisness story from this use case in Performance test cases\n(give answer in 5 numbered points in new line)\n\nAnswer:",
        temperature=1,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0.62,
        presence_penalty=0.62
    )

    security_response = security_response.choices[0].text
    security_response = security_response.strip()

    performnce_response = performnce_response.choices[0].text
    performnce_response = performnce_response.strip()

    return f"Security test cases:\n{security_response}", f"Performance test cases:\n{performnce_response}"

@app.callback(
    Output('tsg-functional-box','value'),
    Output('tsg-non-functional-box','value'),
    Output('tsg-loading','fullscreen'),
    Output('tsg-loading-output','children'),
    Input('tsg-submit','n_clicks'),
    State('tsg-input', 'value'),
    State('tsg-system-input','value'),
    State('tsg-loading','fullscreen')
)
def get_tsg_result(n_clicks, input, system_name, fullscreen):
    if n_clicks is None:
        return '',"",False,""
    if system_name is None:
        system_name = ""
    else:
        system_name = f"System name is {system_name}"

    try:
        fullscreen = True
        ui_response, usability_response, functionality_response, integration_response,  = get_tsg_functional_response(input, system_name)
        functional_scenario = f"{ui_response}\n\n{usability_response}\n\n{functionality_response}\n\n{integration_response}"

        security_response, performance_response = get_tsg_nonfunctional_response(input, system_name)
        non_functional_scenario = f"{security_response}\n\n{performance_response}"
        fullscreen = False
        return functional_scenario, non_functional_scenario, fullscreen, ""
    except Exception as e:
        return f"Error Occured:\n{str(e)}", "", False, ""

@app.callback(
    Output('tsg-save', 'href'),
    Input('tsg-save', 'n_clicks'),
    State('tsg-input', 'value'),
    State('tsg-system-input', 'value'),
    State('tsg-functional-box', 'value'),
    State('tsg-non-functional-box', 'value'),
)
def create_tsg_document(n_clicks, input, system_name, functional, nonfunctional):
    n_clicks = 0
    if n_clicks is not None or n_clicks > 0:
        document_content = f"""Business Scenario:\n{input.strip()}\n{system_name}\n\nFunctional Scenario:\n{functional.strip()}\n\nNonfunctional Scenario:\n{nonfunctional.strip()}"""
        doc = document_content.encode("utf-8")
        b64 = base64.b64encode(doc).decode()
        href = f"data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,{b64}"
        return href
    
@app.callback(
    Output('tsg-email-failed','is_open'),
    Output('tsg-email-success','is_open'),
    Input("tsg-email",'n_clicks'),
    State('tsg-email-failed','is_open'),
    State('tsg-email-success','is_open'),
    State('tsg-input', 'value'),
    State('tsg-system-input', 'value'),
    State('tsg-functional-box', 'value'),
    State('tsg-non-functional-box', 'value'),
)
def send_rca_email(n_clicks, email_failed, email_sent, input, system_name, functional, nonfunctional):
    if n_clicks is None:
        return False,False
    try:
        document_content = f"""Business Scenario:\n{input.strip()}\n{system_name}\n\nFunctional Scenario:\n{functional.strip()}\n\nNonfunctional Scenario:\n{nonfunctional.strip()}"""
        send_email(document_content)
        return False, True
    except Exception as e:
        logging.error(f'str{e}')
        return True,False

#%% Usage Insights
user_stats_layout = html.Div(
    children=[
    dbc.Navbar(children=[dbc.NavItem(html.A(html.I(className="fas fa-home"), href="/",style={"margin":"0px 0px 0px 20px","font-size":"30px","color":"white"})),dbc.NavbarBrand("User Insights", className="mx-auto",style={"text-align":"center","font-size":"35px","font-weight":"bold"})],color="dark",dark=True),
    dbc.Container(
        className='pt-5',
        children=[
            dcc.Location(id='adminurl', refresh=True),
            dbc.Row([
                dbc.Col([
                    html.H1(id="total-queries",className="display-1"),
                    html.P("Total Entries", className="lead")
                ],className='d-flex flex-column align-items-center'),
                dbc.Col([
                    html.H1(id = 'average-time',className="display-1"),
                    html.P("Total Time", className="lead")
                ],className='d-flex flex-column align-items-center')
            ]), 
            html.Br(),
            html.Br(),
            html.Br(),
            html.Br(),
            dbc.Row([
                dbc.Col(
                    html.I(className='fas fa-bug fa-lg', style={"font-size": "48px","width": "100%","height": "100px","line-height": "100px","text-align":"center"})
                ),
                dbc.Col(
                    html.I(className='fas fa-file-code fa-lg',style={"font-size": "48px","width": "100%","height": "100px","line-height": "100px","text-align":"center"})
                ),
                dbc.Col(
                    html.I(className='fas fa-code fa-lg',style={"font-size": "48px","width": "100%","height": "100px","line-height": "100px","text-align":"center"})
                )
            ]),
            dbc.Row([
                dbc.Col(
                    dbc.Button(
                        'Fault Analysis Stats',
                        color="primary",
                        style={"width": "100%","font-size":"27px"},
                        href="/fault_analysis_stats"
                    ),
                            #width={"size": 2, "offset": 2},
                ),
                dbc.Col(
                    dbc.Button(
                        'Code Analysis Stats',
                        color="primary",
                        style={"width": "100%","font-size":"27px"},
                        href="/codeanalysis_stats"
                    ),
                            #width={"size": 2, "offset": 0},
                ),
                dbc.Col(
                    dbc.Button(
                        'Code Generation Stats',
                        color="primary",
                        style={"width": "100%","font-size":"27px"},
                        href="/codegeneration_stats"
                    ),
                            #width={"size": 2, "offset": 0},
                ),
            ]),
            html.Br(),
            html.Br(),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    html.I(className='fas fa-file-invoice fa-lg', style={"font-size": "48px","width": "100%","height": "100px","line-height": "100px","text-align":"center"})
                ]),
                dbc.Col([
                    html.I(className='fas fa-language fa-lg',style={"font-size": "48px","width": "100%","height": "100px","line-height": "100px","text-align":"center",'color':'white'})
                ])
            ]),
            dbc.Row([
                dbc.Col(
                    dbc.Button(
                        'Doc Generation Stats',
                        color="primary",
                        style={"width": "100%","font-size":"27px"},
                        href="/docgeneration_stats"
                    ),
                ),
                dbc.Col(
                    dbc.Button(
                        'Sentiment Analysis Stats',
                        color="primary",
                        style={"width": "100%","font-size":"27px"},
                        href="/sentimentanalysis_stats"
                    ),
                )
            ])
        ]
    )
    ]
)

def display_total_queries():
    try:
        total_queries = 0
        tables = ['fault_tolerance','sentiment_analysis','code_analysis','code_generation','doc_generation']
        for i in tables:
            conn =  sqlite3.connect('code_ops_analyser.db')
            sql_query = f"SELECT COUNT(id) from {i}"
            data = conn.execute(sql_query)
            data = data.fetchall()
            total_queries = total_queries + data[0][0]
            conn.close()
        return total_queries
    except Exception as e:
        logging.debug(f"Database empty or some problem with db\n{str(e)}")
        return 0
    
def calc_total_time():
    try:
        avg_time = 0
        tables = ['fault_tolerance','sentiment_analysis','code_analysis','code_generation','doc_generation']
        for i in tables:
            conn = sqlite3.connect('code_ops_analyser.db')
            sql_query = f"Select SUM(exe_time) from {i}"
            data = conn.execute(sql_query)
            data = data.fetchall()
            if data[0][0] is None:
                value = 0
            else:
                value = data[0][0]
            avg_time = avg_time + value
            conn.close()
        return '%.2f sec' %avg_time
    except Exception as e:
        logging.debug(f"Database empty or some problem with db at 1723\n{str(e)}")
        return 0 

@app.callback(
    Output('total-queries','children'),
    Output('average-time','children'),
    Input('adminurl','pathname')
)
def show_overall_usage(pathname):
    if pathname == '/user_stats':
        return display_total_queries(),calc_total_time()
    else:
        return 0,0
    

# %%
# Fault_analysis_stats page


def get_stats(table_name):
    avg_time = 0
    total_queries = 0
    try:
        conn = sqlite3.connect('code_ops_analyser.db')
        sql_query = f"Select Count(id), Avg(exe_time) from {table_name}"
        data = conn.execute(sql_query)
        data = data.fetchall()
        return data[0][0],'%.2f' %data[0][1]
    except Exception as e:
        logging.error("Error Occured \n%s" %str(e))
        return 0,0

def get_table(table_name):
    conn = sqlite3.connect('code_ops_analyser.db')
    cursor = conn.execute(f"SELECT * FROM {table_name}")
    data = cursor.fetchall()
    conn.close()
    return data


wt_stats_page = html.Div([
    dcc.Location(id = "wt-stats",refresh = True),
    dbc.Navbar(
        children=[
            dbc.NavItem(html.A(html.I(className="fas fa-home"), href="/",style={"margin":"0px 0px 0px 20px","font-size":"30px","color":"white"})),
            dbc.NavItem(html.A(html.I(className="fas fa-arrow-left"), href="/user_stats",style={"margin":"0px 0px 0px 20px","font-size":"30px","color":"white"})),
            dbc.NavbarBrand(id ='wt-heading',className="mx-auto",style={"text-align":"center","font-size":"35px","font-weight":"bold"}
        )],color="dark",dark=True),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.H1(id="wt-total-queries",className="display-1"),
            html.P("Total Entries", className="lead")
        ],className='d-flex flex-column align-items-center'),
        dbc.Col([
            html.H1(id ='wt-average-time',className="display-1"),
            html.P("Average Time", className="lead")
        ],className='d-flex flex-column align-items-center')
    ]),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([
            html.Div(id='wt-stats-page-content')
        ],width=12)
    ])
])

@app.callback(
        Output("wt-total-queries","children"),
        Output("wt-average-time","children"),
        Output("wt-stats-page-content","children"),
        Output("wt-heading",'children'),
        Input("wt-stats","pathname")
)
def fault_analysis_stats(pathname):
    table = None
    total_queries = 0
    avg_time = 0
    if pathname == '/fault_analysis_stats':
        heading = 'Fault Analysis Stats'
        df = pd.DataFrame(get_table('fault_tolerance'), columns=["ID", "Timestamp", "Action", "Intent", "Systems Involved", "Error Message", "OCR Text", "Prompt Selected", "Result", "Execution Time"])
        table = dbc.Table.from_dataframe(
            df,
            id = "fault-analysis-table",
            striped=True,
            bordered=True,
            hover=True,
            dark=True,
            responsive=True,
            style = {
                "textAlign":"left",
                "overflow":"hidden",
                "textOverflow": "ellipsis",
                "height":"auto",
                "whiteSpace":"normal",
            },
        )
        total_queries, avg_time = get_stats('fault_tolerance')
    
    elif pathname == "/sentimentanalysis_stats":
        heading = 'Sentiment Analysis Stats'
        df = pd.DataFrame(get_table('sentiment_analysis'),columns=["ID","Comment","Customer Intentions","Sentiments","Impacted Services","Social Media Action","Action to Operation","Execution Time"])
        table = dbc.Table.from_dataframe(
            df,
            id = "sentiment-analysis-table",
            striped=True,
            bordered=True,
            hover=True,
            dark=True,
            responsive=True,
            style = {
                "textAlign":"left",
                "overflow":"hidden",
                "textOverflow": "ellipsis",
                "height":"auto",
                "whiteSpace":"normal",
            },
        )
        total_queries, avg_time = get_stats('sentiment_analysis')

    elif pathname == '/codeanalysis_stats':
        heading = "Code Analysis Stats"
        df = pd.DataFrame(get_table('code_analysis'),columns=["ID","Action Selected","Code Language","Input","Prompt Selected","Result","Execution Time"])
        table = dbc.Table.from_dataframe(
            df,
            id = "code-analysis-table",
            striped=True,
            bordered=True,
            hover=True,
            dark=True,
            responsive=True,
            style = {
                "textAlign":"left",
                "overflow":"hidden",
                "textOverflow": "ellipsis",
                "height":"auto",
                "whiteSpace":"normal",
            },
        )
        total_queries, avg_time = get_stats('code_analysis')

    elif pathname == '/codegeneration_stats':
        heading = 'Code Generation Stats'
        df = pd.DataFrame(get_table('code_generation'),columns = ["ID","Action Selected","Code Language","Input","Result","Execution Time"])
        table = dbc.Table.from_dataframe(
            df,
            id = "code-generation-table",
            striped=True,
            bordered=True,
            hover=True,
            dark=True,
            responsive=True,
            style = {
                "textAlign":"left",
                "overflow":"hidden",
                "textOverflow": "ellipsis",
                "height":"auto",
                "whiteSpace":"normal",
            },
        )
        total_queries, avg_time = get_stats('code_generation')
    
    elif pathname == '/docgeneration_stats':
        heading = 'Doc Generation Stats'
        df = pd.DataFrame(get_table('doc_generation'),columns = ["ID","Action Selected","Topic","Output","Execution Time"])
        table = dbc.Table.from_dataframe(
            df,
            id = "doc-generation-table",
            striped=True,
            bordered=True,
            hover=True,
            dark=True,
            responsive=True,
            style = {
                "textAlign":"left",
                "overflow":"hidden",
                "textOverflow": "ellipsis",
                "height":"auto",
                "whiteSpace":"normal",
            },
        )
        total_queries, avg_time = get_stats('doc_generation')

    return total_queries,avg_time,table,heading



# %% [markdown]
# **APP STARTING POINT**

# %%
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return home_layout
    elif pathname == '/fault_analysis':
        return fault_analysis_page
    elif pathname == '/codeanalysis':
        return code_analysis_layout
    elif pathname == '/user_stats':
        return user_stats_layout
    elif pathname == '/docgeneration':
        return docGeneration_Layout
    elif pathname == '/codegeneration':
        return code_generation_layout
    elif pathname == '/sentimentanalysis':
        return sentiment_analysis_layout
    elif pathname == '/sentimentanalysisold':
        return sentiment_analysis_new_layout
    elif pathname == '/fault_analysis_stats':
        return wt_stats_page
    elif pathname == "/sentimentanalysis_stats":
        return wt_stats_page
    elif pathname == '/codeanalysis_stats':
        return wt_stats_page
    elif pathname == '/codegeneration_stats':
        return wt_stats_page
    elif pathname == '/docgeneration_stats':
        return wt_stats_page
    elif pathname == '/fault-analysis-new':
        return fault_analysis_new_layout
    elif pathname == '/dialoguediagnostics':
        return dialogue_diagnostic_layout
    elif pathname == '/testgenius':
        return test_genius_layout
    elif pathname == '/api-analysis':
        return api_analysis_layout
    elif pathname == '/test-scenario-generation':
        return ts_generator_layout
    else:
        return '404 Page Not Found'

url = "http://localhost:8005/"
webbrowser.open_new(url)

app.run_server(debug=False,port = 8005)
# %%
