# A Streamlit app that creates a restaurant concept from scratch based on a name, location, and overall concept
# We will use langchain and OpenAI to generate the concept

# Initial imports
import streamlit as st
import openai
import os
from dotenv import load_dotenv
from langchain.prompts.prompt import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
import asyncio

# Load the API key from the .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG")

# Initialize the session state
def init_session_variables():
    # Initialize session state variables
    session_vars = [
        'restaurant_name', 'restaurant_location', 'restaurant_concept', 'current_task', 'menu', 'training_guide', 'service_strategy', 'interior_layout', 'marketing_strategy', 'page_state'
    ]
    default_values = [
        '', '', '', '', '', '', '', '', '', 'get_concept_info'
    ]

    for var, default_value in zip(session_vars, default_values):
        if var not in st.session_state:
            st.session_state[var] = default_value

# Initialize the session variables
init_session_variables()

# Create the main prompt template
main_prompt  = PromptTemplate(
    input_variables = ["name", "location", "concept", "task"],
    template = "Based on the name {name}, the location {location}, and the overall concept {concept} of a new restaurant,\
                execute the task {task} related to building out the concept."
    )

# Create a list of tasks to execute
tasks = ["create a menu", "create a very brief training guide", "create a very brief service strategy", "create a very brief interior layout", "create a very brief marketing strategy"]

# Create the chat model that we will use to generate the concept
chat = ChatOpenAI(model_name = 'gpt-3.5-turbo', temperature = 0)

# Define the main LLMChain
main_chain = LLMChain(llm=chat, prompt = main_prompt, verbose = True)

# Define a function to create the training guide
async def create_recipes(name, location, concept):
    task = "Create a food menu of 3 items that includes a name, description, and price for each item."
    # Create the input dictionary
    input_dict = {"name": name, "location": location, "concept": concept, "task": task}
    # Generate the training guide
    menu = main_chain.run(input_dict)

    return ("Menu", menu)


# Define a function to create the training guide
async def create_training_guide(name, location, concept):
    task = "create a very brief training guide"
    # Create the input dictionary
    input_dict = {"name": name, "location": location, "concept": concept, "task": task}
    # Generate the training guide
    training_guide = main_chain.run(input_dict)

    return ("Training Guide", training_guide)


# Define a function to create the service strategy
async def create_service_strategy(name, location, concept):
    task = "create a very brief service strategy"
    # Create the input dictionary
    input_dict = {"name": name, "location": location, "concept": concept, "task": task}
    # Generate the service strategy
    service_strategy = main_chain.run(input_dict)

    return ("Service Strategy", service_strategy)
   

# Define a function to create the interior layout
async def create_interior_layout(name, location, concept):
    task = "create a very brief interior layout"
    # Create the input dictionary
    input_dict = {"name": name, "location": location, "concept": concept, "task": task}
    # Generate the interior layout
    interior_layout = main_chain.run(input_dict)
    
    return ("Interior Layout", interior_layout)

# Define a function to create the marketing strategy
async def create_marketing_strategy(name, location, concept):
    task = "create a very brief marketing strategy"
    # Create the input dictionary
    input_dict = {"name": name, "location": location, "concept": concept, "task": task}
    # Generate the marketing strategy
    marketing_strategy = main_chain.run(input_dict)

    return ("Marketing Strategy", marketing_strategy)

# Define a function to take the user inputs and generate the concept
def generate_concept():
    # Create a form to collect the name, location, and concept of the restaurant
    st.title("Restaurant Concept Generator")
    name = st.text_input("Enter the name of the restaurant")
    location = st.text_input("Enter the location of the restaurant")
    concept = st.text_input("Enter the concept of the restaurant")


    # Create a button to generate the concept
    if st.button("Generate Concept"):
        with st.spinner("Generating Concept..."):
            
            # Set the session state variables
            st.session_state.restaurant_name = name
            st.session_state.restaurant_location = location
            st.session_state.restaurant_concept = concept
           
            # Change the page state to display the concept
            st.session_state.page_state = "display_concept"
            # Refresh the page
            st.experimental_rerun()

async def display_concept():
    # Create a button to go back to the main page
    if st.button("Go Back"):
        # Change the page state to get_concept_info
        st.session_state.page_state = "get_concept_info"
        # Refresh the page
        st.experimental_rerun()

    # Initialize a list of tasks
    tasks = [
        create_recipes(st.session_state.restaurant_name, st.session_state.restaurant_location, st.session_state.restaurant_concept),
        create_training_guide(st.session_state.restaurant_name, st.session_state.restaurant_location, st.session_state.restaurant_concept),
        create_service_strategy(st.session_state.restaurant_name, st.session_state.restaurant_location, st.session_state.restaurant_concept),
        create_interior_layout(st.session_state.restaurant_name, st.session_state.restaurant_location, st.session_state.restaurant_concept),
        create_marketing_strategy(st.session_state.restaurant_name, st.session_state.restaurant_location, st.session_state.restaurant_concept)
    ]

    # Display the name, location and concept
    st.title("Restaurant Concept")
    st.write("Restaurant Name: ", st.session_state.restaurant_name)
    st.write("Restaurant Location: ", st.session_state.restaurant_location)
    st.write("Restaurant Concept: ", st.session_state.restaurant_concept)

    # Create a progress bar
    progress_bar = st.progress(0)
    # Create a status text
    status_text = st.empty()

    # Create a list to store the results
    results = []

    # Loop through the tasks
    for i, task in enumerate(tasks):
        # Assign names to the tasks
        if i == 0:
            task_name = "Creating Recipes"
        elif i == 1:
            task_name = "Creating Training Guide"
        elif i == 2:
            task_name = "Creating Service Strategy"
        elif i == 3:
            task_name = "Creating Interior Layout"
        elif i == 4:
            task_name = "Creating Marketing Strategy"

        # Update the progress bar
        progress_bar.progress((i+1)/len(tasks))
        # Update the status text with the current task
        status_text.text(f"{task_name}...")
        # Run the task
        result = await task
        # Append the result to the results list
        results.append(result)

    # Display the results
    for result in results:
        st.subheader(result[0])
        st.write(result[1])




# Define the flow of the app
if st.session_state.page_state == "get_concept_info":
    generate_concept()
elif st.session_state.page_state == "display_concept":
    asyncio.run(display_concept())
   