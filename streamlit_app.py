import streamlit as st
import censusgeocode as cg

st.subheader("Enter an address")
col1, col2, col3, col4 = st.columns([2, 1, 1,1]) 

with col1:
    address = st.text_input("Address", placeholder="164 S Main St")
with col2:
    city = st.text_input("City", placeholder="Kannapolis")    
with col3:
    state = st.text_input("State", placeholder="NC")
with col4:
    zip = st.text_input("Zip Code", placeholder="28081")
full_address = f"{address}  \n {city} {state}, {zip}"
full_address_2 = f"{address}, {city}, {state}, {zip}"
if isinstance(full_address,str):
    try:
        results = cg.onelineaddress(full_address_2)
    except:
        st.write('There is an problem with the address')
    if len(results) > 0:
        st.header("Found a matched address!")
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
    if address and city and state and zip:
        # st.success("All fields are filled out!")
        pass
    else:
        st.error("Please fill in all the fields.")
