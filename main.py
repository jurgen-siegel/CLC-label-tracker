import streamlit as st
import pandas as pd
from pymongo import MongoClient
import io
import matplotlib.pyplot as plt

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

# App title
st.title('Label Progress')

page = st.radio("Pages", ["Manage Tickets", "Display Tickets"])

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
    else:
        st.write("No tickets available to delete.")

    # Edit a ticket
    st.subheader('Edit Ticket')

    # Check if there are any tickets to edit
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
        else:
            st.warning("Selected ticket not found!")
            ticket_num_edit = st.text_input('Edit Ticket #', value='')
            customer_edit = st.text_input('Edit Customer', value='')
            description_edit = st.text_input('Edit Description', value='')
            artwork_received_edit = st.checkbox('Edit Artwork Received', value=False)
            physical_proof_edit = st.checkbox('Edit Physical Proof', value=False)
            digital_approved_edit = st.checkbox('Edit Digital Approved', value=False)
            sample_edit = st.checkbox('Edit Sample', value=False)
            quote_edit = st.checkbox('Edit Quote', value=False)

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


else:  # Display Tickets
    st.subheader('All Tickets')

    tickets = list(collection.find({}))
    for ticket in tickets:
        ticket['Completed'] = all([ticket['Artwork Received'], ticket['Physical Proof'], ticket['Digital Approved'], ticket['Sample'], ticket['Quote']])
        del ticket['_id']
    df = pd.DataFrame(tickets)

    # Check if there are any tickets to display
    if not df.empty:
        # Excel download button
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Tickets', index=False)
        excel_data = output.getvalue()
        st.download_button(
            label="Download Excel file",
            data=excel_data,
            file_name="tickets.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

        # Search functionality
        search_query = st.text_input("Search tickets (by Ticket #, Customer, etc.)")
        if search_query:
            df = df[df[['Ticket #', 'Customer']].apply(lambda row: row.astype(str).str.contains(search_query).any(), axis=1)]

        # Generate HTML table with color coding
        def generate_html_table(dataframe):
            styles = []
            rows = []
            for _, row in dataframe.iterrows():
                checks_count = row[['Artwork Received', 'Physical Proof', 'Digital Approved', 'Sample', 'Quote']].sum()
                if checks_count == 1:
                    style = 'background-color: red;'
                elif checks_count == 5:
                    style = 'background-color: green;'
                else:
                    style = ''
                styles.append(style)

            for (index, row), style in zip(dataframe.iterrows(), styles):
                row_str = f'<tr style="{style}">' + ''.join(f'<td>{cell}</td>' for cell in row) + '</tr>'
                rows.append(row_str)

            headers = '<tr>' + ''.join(f'<th>{col}</th>' for col in dataframe.columns) + '</tr>'
            table = f'<table>{headers}' + ''.join(rows) + '</table>'
            return table

        html_string = generate_html_table(df)
        st.markdown(html_string, unsafe_allow_html=True)

        # Pie chart data
        df['completed'] = df[['Artwork Received', 'Physical Proof', 'Digital Approved', 'Sample', 'Quote']].sum(axis=1) == 5
        completed_count = df['completed'].sum()
        total_tickets = len(df)

        labels = ['Completed', 'Incomplete']
        sizes = [completed_count, total_tickets - completed_count]

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['green', 'red'],
               textprops={'color': 'white'})
        ax.axis('equal')

        # Set background color of the pie chart to transparent
        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')

        st.pyplot(fig)
    else:
        st.write("No tickets available to display.")
st.write("--------------------------------------------------------------------------")
st.markdown("**Note: To manage tickets, follow these steps:**")
st.write("1. Write down the ticket number, name, and description.")
st.write("2. Check the appropriate boxes to indicate progress.")
st.write("3. Click 'Add Ticket' to create a new ticket.")

st.write("To edit an existing ticket:")
st.write("1. Pick the ticket number you want to modify.")
st.write("2. Make the necessary changes.")
st.write("3. Click 'Update Ticket' to save your changes.")

st.write("To view all tickets, click on 'Display Tickets' at the top of the page.")