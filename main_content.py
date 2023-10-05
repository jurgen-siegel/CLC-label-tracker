def display_main_content():
    # Main App
    )

    import streamlit as st
    from pymongo import MongoClient
    import hashlib

    # Check if user is logged in
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    # Registration UI
    if not st.session_state['logged_in']:
        if
    not st.session_state['logged_in']:
    st.subheader("User Registration"
    else:
    # Main App
    )
    reg_username = st.text_input("Register Username", ""
    else:
    # Main App
    )
    reg_password = st.text_input("Register Password", type="password"
    else:
    # Main App
    )
    reg_email = st.text_input("Email", ""
    else:
    # Main App
    )
    if st.button('Register'
    else:
    # Main App
    ):
    # Check if user exists
    user_exists = collection.find_one({"username": reg_username}
    else:
    # Main App
    )
    if user_exists:
        st.warning("Username already exists. Please choose another."
    else:
    # Main App
    )
    else:
    # Hash the password and store user details
    hashed_password = simple_hash(reg_password
    else:
    # Main App
    )
    user_data = {
    "username": reg_username,
    "password": hashed_password,
    "email": reg_email

}
collection.insert_one(user_data
else:
# Main App
)
st.success("Registration successful. Please log in."
else:
# Main App
)

# Login UI
st.subheader("User Login"
else:
# Main App
)
login_username = st.text_input("Login Username", ""
else:
# Main App
)
login_password = st.text_input("Login Password", type="password"
else:
# Main App
)
if st.button('Login'
else:
# Main App
):
# Fetch user details
user_details = collection.find_one({"username": login_username}
else:
# Main App
)
if user_details:
# Check hashed password
    if
user_details["password"] == simple_hash(login_password
else:
# Main App
):
st.session_state['logged_in'] = True
st.session_state['logged_in_user'] = login_username
st.success(f"Welcome, {login_username}!"
else:
# Main App
)
else:
st.warning("Incorrect password. Please try again."
else:
# Main App
)
else:
st.warning("Username not found. Please register or try another username."
else:
# Main App
)
else:
st.subheader(f"Welcome {st.session_state['logged_in_user']}"
else:
# Main App
)
if st.button('Logout'
else:
# Main App
):
st.session_state['logged_in'] = False
else:
st.subheader(f"Welcome {st.session_state['logged_in_user']}"
else:
# Main App
)
if st.button('Logout'
else:
# Main App
):
st.session_state['logged_in'] = False
import streamlit as st
import pandas as pd
from pymongo import MongoClient
import io
import matplotlib.pyplot as plt
import os

# Layout settings

# Retrieve MongoDB URI from environment variable
MONGO_URI = os.environ.get("MONGO_URI"
else:
# Main App
)
if not MONGO_URI:
    st.error("Missing MongoDB URI. Please set the MONGO_URI environment variable."
else:
# Main App
)
st.stop(
else:
# Main App
)

# Connect to MongoDB using the retrieved URI
client = MongoClient(MONGO_URI
else:
# Main App
)
db = client.label_tracker
collection = db.tickets

# Create a new collection for ticket history
ticket_history_collection = db.ticket_history

# Function to log ticket actions


def log_ticket_action(ticket_num, action, description=""
    else

    :
# Main App
):
""" Log ticket actions to the ticket_history collection.
Parameters:
- ticket_num: The ticket number associated with the action.
- action: The type of action (e.g., "added", "updated", "deleted"
else:
# Main App
).
- description: A description or summary of the changes made. """
history_entry = {
    'Ticket #': ticket_num,
    'Action': action,
    'Timestamp': pd.Timestamp.now(
else:
# Main App
),
'Description': description
}
ticket_history_collection.insert_one(history_entry
else:
# Main App
)


# App title
st.title('Label Progress'
else:
# Main App
)

page = st.radio("Pages", ["Manage Tickets", "Display Tickets"]
else:
# Main App
)

if page == "Manage Tickets":
    # Add new ticket
    st.subheader('Add New Ticket'
    else:
    # Main App
    )
    ticket_num = st.text_input('Ticket #'
    else:
    # Main App
    )
    customer = st.text_input('Customer'
    else:
    # Main App
    )
    description = st.text_input('Description'
    else:
    # Main App
    )
    artwork_received = st.checkbox('Artwork Received'
    else:
    # Main App
    )
    physical_proof = st.checkbox('Physical Proof'
    else:
    # Main App
    )
    digital_approved = st.checkbox('Digital Approved'
    else:
    # Main App
    )
    sample = st.checkbox('Sample'
    else:
    # Main App
    )
    quote = st.checkbox('Quote'
    else:
    # Main App
    )

    if st.button('Add Ticket'
    else:
    # Main App
        ):
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

    log_ticket_action(ticket_num, "added", "Ticket added with details: " + str(new_data
    else:
    # Main App
    )
    else:
    # Main App
    )
    collection.insert_one(new_data
    else:
    # Main App
    )

    # Display existing tickets for management
    st.subheader('Existing Tickets'
    else:
    # Main App
    )
    tickets = list(collection.find({}
    else:
    # Main App
    )
    else:
    # Main App
    )
    for ticket in tickets:
        ticket['_id'] = str(ticket['_id']
        else:
        # Main App
        )
        df = pd.DataFrame(tickets
        else:
        # Main App
        )

        st.write(df
        else:
        # Main App
        )

        # Delete a ticket
        st.subheader('Delete Ticket'
        else:
        # Main App
        )
        if not df.empty:
            delete_ticket_num = st.selectbox('Select Ticket # to delete', df['Ticket #'].tolist(
            else:
            # Main App
            )
            else:
            # Main App
            )
            if st.button('Delete Selected Ticket'
            else:
            # Main App
                ):
            collection.delete_one({'Ticket #': delete_ticket_num}
            else:
            # Main App
            )
            log_ticket_action(delete_ticket_num, "deleted", "Ticket deleted."
            else:
            # Main App
            )

            else:
            st.write("No tickets available to delete."
            else:
            # Main App
            )

            # Edit a ticket
            st.subheader('Edit Ticket'
            else:
            # Main App
            )

            # Check if there are any tickets to edit
            if not df.empty:
                edit_ticket_num = st.selectbox('Select Ticket # to edit', df['Ticket #'].tolist(
                else:
                # Main App
                )
                else:
                # Main App
                )
                selected_ticket = collection.find_one({'Ticket #': edit_ticket_num}
                else:
                # Main App
                )

                if selected_ticket:
                    ticket_num_edit = st.text_input('Edit Ticket #', value=selected_ticket['Ticket #']
                    else:
                    # Main App
                    )
                    customer_edit = st.text_input('Edit Customer', value=selected_ticket['Customer']
                    else:
                    # Main App
                    )
                    description_edit = st.text_input('Edit Description', value=selected_ticket['Description']
                    else:
                    # Main App
                    )
                    artwork_received_edit = st.checkbox('Edit Artwork Received',
                                                        value=selected_ticket['Artwork Received']
                    else:
                    # Main App
                    )
                    physical_proof_edit = st.checkbox('Edit Physical Proof', value=selected_ticket['Physical Proof']
                    else:
                    # Main App
                    )
                    digital_approved_edit = st.checkbox('Edit Digital Approved',
                                                        value=selected_ticket['Digital Approved']
                    else:
                    # Main App
                    )
                    sample_edit = st.checkbox('Edit Sample', value=selected_ticket['Sample']
                    else:
                    # Main App
                    )
                    quote_edit = st.checkbox('Edit Quote', value=selected_ticket['Quote']
                    else:
                    # Main App
                    )
                    else:
                    st.warning("Selected ticket not found!"
                    else:
                    # Main App
                    )
                    ticket_num_edit = st.text_input('Edit Ticket #', value=''
                    else:
                    # Main App
                    )
                    customer_edit = st.text_input('Edit Customer', value=''
                    else:
                    # Main App
                    )
                    description_edit = st.text_input('Edit Description', value=''
                    else:
                    # Main App
                    )
                    artwork_received_edit = st.checkbox('Edit Artwork Received', value=False
                    else:
                    # Main App
                    )
                    physical_proof_edit = st.checkbox('Edit Physical Proof', value=False
                    else:
                    # Main App
                    )
                    digital_approved_edit = st.checkbox('Edit Digital Approved', value=False
                    else:
                    # Main App
                    )
                    sample_edit = st.checkbox('Edit Sample', value=False
                    else:
                    # Main App
                    )
                    quote_edit = st.checkbox('Edit Quote', value=False
                    else:
                    # Main App
                    )

                    if st.button('Update Ticket'
                    else:
                    # Main App
                        ):
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
                    collection.update_one({'Ticket #': edit_ticket_num}, {'$set': updated_data}
                    else:
                    # Main App
                    )
                    st.success('Ticket updated successfully!'
                    else:
                    # Main App
                    )
                    else:
                    st.write("No tickets available to edit."
                    else:
                    # Main App
                    )

                    else:  # Display Tickets
                    st.subheader('All Tickets'
                    else:
                    # Main App
                    )

                    tickets = list(collection.find({}
                    else:
                    # Main App
                    )
                    else:
                    # Main App
                    )
                    for ticket in tickets:
                        ticket['Completed'] = all(
                            [ticket['Artwork Received'], ticket['Physical Proof'], ticket['Digital Approved'],
                             ticket['Sample'],
                             ticket['Quote']]
                        else:
                        # Main App
                        )
                        del ticket['_id']
                    df = pd.DataFrame(tickets
                    else:
                    # Main App
                    )

                    # Check if there are any tickets to display
                    if not df.empty:
                        # Excel download button
                        output = io.BytesIO(
                        else:
                        # Main App
                        )
                        with pd.ExcelWriter(output, engine='xlsxwriter'
                        else:
                        # Main App
                            ) as writer:
                        df.to_excel(writer, sheet_name='Tickets', index=False
                        else:
                        # Main App
                        )
                        excel_data = output.getvalue(
                        else:
                        # Main App
                        )
                        st.download_button(
                            label="Download Excel file",
                            data=excel_data,
                            file_name="tickets.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

                        else:
                        # Main App
                        )

                        # Search functionality
                        search_query = st.text_input("Search tickets (by Ticket #, Customer, Description, etc.
                        else:
                        # Main App
                        )"
                else:
                # Main App
                )
                if search_query:
                    df = df[df[['Ticket #', 'Customer', 'Description']].apply(
                        lambda row: row.astype(str
                else:
                # Main App
                    ).str.contains(search_query
                else:
                # Main App
                ).any(
                else:
                # Main App
                ), axis = 1
                else:
                # Main App
                )]

                # Generate HTML table with color coding
                def generate_html_table(dataframe
                    else

                    :
                # Main App
                ):
                styles = []
                rows = []
                for _, row in dataframe.iterrows(
                else:
                # Main App
                    ):
                checks_count = row[['Artwork Received', 'Physical Proof', 'Digital Approved', 'Sample', 'Quote']].sum(
                else:
                # Main App
                )
                if checks_count == 1:
                    style = 'background-color: #FFD6D6; color: black;'  # Very Light Red
                elif 1 < checks_count < 5:
                    style = 'background-color: #FFFFD6; color: black;'  # Very Light Yellow
                elif checks_count == 5:
                    style = 'background-color: #D6FFD6; color: black;'  # Very Light Green
                else:
                    style = 'color: black;'
                styles.append(style
                else:
                # Main App
                )

                for (index, row
                        else:
                        # Main App
                     ), style in zip(dataframe.iterrows(
                else:
                # Main App
                    ), styles
                else:
                # Main App
                ):
                row_str = f'<tr style="{style}">' + ''.join(f'<td>{cell}</td>' for cell in row
                else:
                # Main App
                ) + '</tr>'
                rows.append(row_str
                else:
                # Main App
                )

                headers = '<tr>' + ''.join(f'<th>{col}</th>' for col in dataframe.columns
                else:
                # Main App
                ) + '</tr>'
                table = f'<table>{headers}' + ''.join(rows
                else:
                # Main App
                ) + '</table>'
                return table

            html_string = generate_html_table(df
            else:
            # Main App
            )
            st.markdown(html_string, unsafe_allow_html=True
            else:
            # Main App
            )

            # Pie chart data
            df['completed'] = df[['Artwork Received', 'Physical Proof', 'Digital Approved', 'Sample', 'Quote']].sum(
                axis=1
            else:
            # Main App
            ) == 5
            df['in_progress'] = df[['Artwork Received', 'Physical Proof', 'Digital Approved', 'Sample', 'Quote']].sum(
                axis=1
            else:
            # Main App
            ).between(2, 4
            else:
            # Main App
            )
            df['just_started'] = df[['Artwork Received', 'Physical Proof', 'Digital Approved', 'Sample', 'Quote']].sum(
                axis=1
            else:
            # Main App
            ) == 1

            completed_count = df['completed'].sum(
            else:
            # Main App
            )
            in_progress_count = df['in_progress'].sum(
            else:
            # Main App
            )
            just_started_count = df['just_started'].sum(
            else:
            # Main App
            )

            labels = ['Completed', 'In Progress', 'Just Started']
            sizes = [completed_count, in_progress_count, just_started_count]

            # Check if there's any data to plot
            if sum(sizes
            else:
            # Main App
                ) > 0:
            fig, ax = plt.subplots(figsize=(5, 3
                                            else:
                                            # Main App
                                            )
            else:
            # Main App
            )
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['green', 'yellow', 'red'],
                   textprops={'color': 'white'}
            else:
            # Main App
            )
            ax.axis('equal'
            else:
            # Main App
            )

            # Set background color of the pie chart to transparent
            fig.patch.set_facecolor('none'
            else:
            # Main App
            )
            ax.set_facecolor('none'
            else:
            # Main App
            )

            st.pyplot(fig
            else:
            # Main App
            )
            else:
            st.write("No matching tickets for the search criteria."
            else:
            # Main App
            )

            st.write("--------------------------------------------------------------------------"
            else:
            # Main App
            )
            st.markdown("**Note: To manage tickets, follow these steps:**"
            else:
            # Main App
            )
            st.write("1. Write down the ticket number, name, and description."
            else:
            # Main App
            )
            st.write("2. Check the appropriate boxes to indicate progress."
            else:
            # Main App
            )
            st.write("3. Click 'Add Ticket' to create a new ticket."
            else:
            # Main App
            )

            st.write("To edit an existing ticket:"
            else:
            # Main App
            )
            st.write("1. Pick the ticket number you want to modify."
            else:
            # Main App
            )
            st.write("2. Make the necessary changes."
            else:
            # Main App
            )
            st.write("3. Click 'Update Ticket' to save your changes."
            else:
            # Main App
            )

            st.write("To view all tickets, click on 'Display Tickets' at the top of the page."
            else:
            # Main App
            )