import streamlit as st
from datetime import date, datetime, time, timedelta
import censusgeocode as cg

st.subheader("Enter an address")
tab1, tab2 = st.tabs(["Enter Address", "Calculate time to leave"])

if 'address_history' not in st.session_state:
    st.session_state.address_history = {}

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
                
                st.session_state.address_history[results[0]['matchedAddress']] = result
            else:
                st.write("There was a problem with the address.")
        except NameError as e:
            pass

def is_date_in_range(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        year = date_obj.year
        start_date = date(year, 1, 1)  # Jan 1st
        end_date = date(year, 5, 1)    # May 1st
        return start_date <= date_obj < end_date
    except ValueError:
        return False

with tab2:
    st.subheader("Calculate time to leave")
    # Full time 40 hours during peak tax season, part time 25 hours
    hours = 40 if is_date_in_range(str(date.today())) else 25
    work_week_hours = st.number_input("How many hours are you working this week?", step=1, value=hours)
    work_time_left = st.text_input(f"How much time to reach {work_week_hours} hours?", placeholder="4:30 (HH:MM)")
    arrival_time = st.time_input("What time did you arrive today? (last day of week)", time(8, 45), step=60)
    break_minutes = st.number_input("How long is your break today?", step=5, value=15)

    try:
        hh, mm = map(int, work_time_left.split(":"))
        work_time_left = timedelta(hours=hh, minutes=mm)
    except ValueError:
        st.error("Please enter time remaining in HH:MM format.")
        work_time_left = timedelta()

    if arrival_time and work_time_left:
        arrival_dt = datetime.combine(date.today(), arrival_time)
        leave_time = arrival_dt + work_time_left + timedelta(minutes=break_minutes)
        st.write(f"You should leave at **{leave_time.strftime('%I:%M %p')}**.")

with st.sidebar:
    st.header("This sessions history")
    for k, v in reversed(list(st.session_state.address_history.items())):
        st.write(f"{k}: **{v}**")
        st.divider()

