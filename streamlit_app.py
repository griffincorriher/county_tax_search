import streamlit as st
import censusgeocode as cg

st.subheader("Enter an address")
tab1, tab2 = st.tabs(["Enter Address", "Paste Address"])

with tab1:
    col1, col2, col3, col4 = st.columns([2, 1, 1,1]) 
    with col1:
        address = st.text_input("Address", placeholder="164 S Main St", key='address')
    with col2:
        city = st.text_input("City", placeholder="Kannapolis", key='city')
    with col3:
        state = st.text_input("State", placeholder="NC", key='state')
    with col4:
        zip = st.text_input("Zip Code", placeholder="28081", key='zip')
    if address and city and state and zip:
        full_address = f"{address}, {city}, {state}, {zip}"
    else:
        st.error("Please fill in all the fields.")
    if isinstance(address,str):
        try:
            results = cg.onelineaddress(full_address)
            if len(results) > 0:
                st.header("Found a matching address!")
                st.write(f"{results[0]['matchedAddress']}")    
                latitude = results[0]['coordinates']['y']  
                longitude = results[0]['coordinates']['x']
                latitude_str = str(results[0]['coordinates']['y'])
                longitude_str = str(results[0]['coordinates']['x'])
                data = {
                'latitude': [latitude],
                'longitude': [longitude]
                }

                result = results[0]['geographies']['Counties'][0]['NAME']
                st.subheader(f"{result}")
                st.map(data,
                        latitude=latitude_str,
                        longitude=longitude_str, 
                        use_container_width=True,
                        zoom=14)
            else:
                st.write("There was a problem with the address.")
        except NameError as e:
            pass
with tab2:
    st.write("Feature in progress")
    # full_address = st.text_input(label='Full address', placeholder='164 S Main St Kannapolis, NC 28081')


