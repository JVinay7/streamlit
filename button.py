import streamlit as st

# st.button("Reset", type="primary")
# if st.button('Say hello'):
#     st.write('Why hello there')
# else:
#     st.write('Goodbye')

# Create a Streamlit button
if st.button("Open Pop-up"):
    # When the button is clicked, set a flag to open the pop-up
    open_popup = True

# Check if the flag is set to open the pop-up
if open_popup:
    # Use st.modal to create the pop-up
    with st.modal():
        # Add content to the pop-up
        st.write("This is a pop-up!")

# Reset the flag when the pop-up is closed
if not open_popup:
    open_popup = False
    