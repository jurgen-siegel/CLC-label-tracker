import streamlit as st
import pandas as pd
from pymongo import MongoClient
import os

# Layout settings
st.set_page_config(layout="wide")

# Retrieve MongoDB URI from environment variable
MONGO_URI = os.environ.get("MONGO_URI")
if not MONGO_URI:
    st.error("Missing MongoDB URI. Please set the MONGO_URI environment variable.")
    st.stop()

# Connect to MongoDB using the retrieved URI
client = MongoClient(MONGO_URI)
db = client.label_tracker
collection = db.tickets

# Create a new collection for ticket history
ticket_history_collection = db.ticket_history

# Function to log ticket actions
def log_ticket_action(ticket_num, action, description=""):
    history_entry = {
        'Ticket #': ticket_num,
        'Action': action,
        'Timestamp': pd.Timestamp.now(),
        'Description': description
    }
    ticket_history_collection.insert_one(history_entry)

# App title
st.title('Label Progress')

page = st.radio("Pages", ["Dashboard", "Manage Tickets"])

if page == "Manage Tickets":
    # Add new ticket
    st.subheader('Add New Ticket')
    ticket_num = st.text_input('Ticket #')
    customer = st.text_input('Customer')
    description = st.text_input('Description')
    artwork_received = st.checkbox('Artwork Received')
    physical_proof = st.checkbox('Physical Proof')
    digital_approved = st.checkbox('Digital Approved')
    sample = st.checkbox('Sample')
    quote = st.checkbox('Quote')

    if st.button('Add Ticket'):
        new_data = {
            'Ticket #': ticket_num,
            'Customer': customer,
            'Description': description,
            'Artwork Received': artwork_received,
            'Physical Proof': physical_proof,
            'Digital Approved': digital_approved,
            'Sample': sample,
            'Quote': quote
        }
        log_ticket_action(ticket_num, "added", "Ticket added with details: " + str(new_data))
        collection.insert_one(new_data)

    # Display existing tickets for management
    st.subheader('Existing Tickets')
    tickets = list(collection.find({}))
    for ticket in tickets:
        ticket['_id'] = str(ticket['_id'])
    df = pd.DataFrame(tickets)
    st.write(df)

    # Delete a ticket
    st.subheader('Delete Ticket')
    if not df.empty:
        delete_ticket_num = st.selectbox('Select Ticket # to delete', df['Ticket #'].tolist())
        if st.button('Delete Selected Ticket'):
            collection.delete_one({'Ticket #': delete_ticket_num})
            log_ticket_action(delete_ticket_num, "deleted", "Ticket deleted.")
    else:
        st.write("No tickets available to delete.")

    # Edit a ticket
    st.subheader('Edit Ticket')
    if not df.empty:
        edit_ticket_num = st.selectbox('Select Ticket # to edit', df['Ticket #'].tolist())
        selected_ticket = collection.find_one({'Ticket #': edit_ticket_num})

        if selected_ticket:
            ticket_num_edit = st.text_input('Edit Ticket #', value=selected_ticket['Ticket #'])
            customer_edit = st.text_input('Edit Customer', value=selected_ticket['Customer'])
            description_edit = st.text_input('Edit Description', value=selected_ticket['Description'])
            artwork_received_edit = st.checkbox('Edit Artwork Received', value=selected_ticket['Artwork Received'])
            physical_proof_edit = st.checkbox('Edit Physical Proof', value=selected_ticket['Physical Proof'])
            digital_approved_edit = st.checkbox('Edit Digital Approved', value=selected_ticket['Digital Approved'])
            sample_edit = st.checkbox('Edit Sample', value=selected_ticket['Sample'])
            quote_edit = st.checkbox('Edit Quote', value=selected_ticket['Quote'])

            if st.button('Update Ticket'):
                updated_data = {
                    'Ticket #': ticket_num_edit,
                    'Customer': customer_edit,
                    'Description': description_edit,
                    'Artwork Received': artwork_received_edit,
                    'Physical Proof': physical_proof_edit,
                    'Digital Approved': digital_approved_edit,
                    'Sample': sample_edit,
                    'Quote': quote_edit
                }
                collection.update_one({'Ticket #': edit_ticket_num}, {'$set': updated_data})
                st.success('Ticket updated successfully!')
    else:
        st.write("No tickets available to edit.")

elif page == "Dashboard":
    st.title('Dashboard Overview')

    # Total tickets count
    total_tickets = collection.count_documents({})
    st.metric(label="Total Tickets", value=total_tickets)

    # Tickets by status
    tickets = list(collection.find({}))
    df = pd.DataFrame(tickets)
    df['Completed'] = df[['Artwork Received', 'Physical Proof', 'Digital Approved', 'Sample', 'Quote']].sum(axis=1) == 5
    status_counts = df['Completed'].value_counts()

    st.subheader('Tickets by Status')
    fig, ax = plt.subplots()
    ax.bar(status_counts.index, status_counts.values, color=['green', 'red'], tick_label=['Completed', 'In Progress'])
    st.pyplot(fig)

    # Recent activity (last 5 actions from ticket_history)
    st.subheader('Recent Activity')
    recent_activity = list(ticket_history_collection.find().sort("Timestamp", -1).limit(5))
    recent_activity_df = pd.DataFrame(recent_activity)
    st.write(recent_activity_df[['Ticket #', 'Action', 'Timestamp', 'Description']])

st.write("--------------------------------------------------------------------------")
st.markdown("**Note: To manage tickets, follow these steps:**")
st.write("1. Write down the ticket number, name, and description.")
st.write("2. Check the appropriate boxes to indicate progress.")
st.write("3. Click 'Add Ticket' to create a new ticket.")
st.write("To edit an existing ticket:")
st.write("1. Pick the ticket number you want to modify.")
st.write("2. Make the necessary changes.")
st.write("3. Click 'Update Ticket' to save your changes.")
