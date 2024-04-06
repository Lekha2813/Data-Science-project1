"""
Created on Sat Oct 21 19:36:24 2023

@author: Lekha Bhoyar
"""


import streamlit as st
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image



# Load the model and scaler
model = joblib.load('C:/Users/himan/Downloads/excelr project grp2/gb1_model.joblib')
scaler = joblib.load('C:/Users/himan/Downloads/excelr project grp2/standard_scaler.joblib')


mode=option_menu(
    menu_title=None,
    options=['Home','Visualization','Prediction','About Us'],
    icons=['house','graph-up-arrow','globe-central-south-asia','heart-fill'],
    menu_icon='cast',
    default_index=0,
    orientation='horizontal')

def user_input_features():
    temperature = st.slider('TEMPERATURE(Degrees)', 1.81, 37.11, step=0.1)
    exhaust_vacuum = st.slider('EXHAUST_VACUUM(cm Hg)', 25.36, 81.56, step=0.1)
    amb_pressure = st.slider('AMBIENT_PRESSURE(mb)', 992.89, 1033.3, step=0.1)
    r_humidity = st.slider('RELATIVE_HUMIDITY(%)', 25.56, 100.16, step=0.1)

    # Create a DataFrame with the user input
    data = {
        'temperature': temperature,
        'exhaust_vacuum': exhaust_vacuum,
        'amb_pressure': amb_pressure,
        'r_humidity': r_humidity
    }
    features = pd.DataFrame(data, index=[1])
    return features
if mode=="Home":
    st.title('COMBINED CYCLE POWER PLANT: HOW IT WORKS')
    html_temp = """
    <div style="background-color:red;padding:10px">
    <h2 style="color:white;text-align:center;">ENERGY PRODUCTION PREDICTION </h2>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    
    image_path = "C:/Users/himan/Downloads/ccpp.jpg"  # Replace with the path to your image file
    image = Image.open(image_path)
    st.image(image,
            caption="Renewable Energy",
            use_column_width=True,
            output_format="auto",
            )
    st.markdown('A Combined Cycle Power Plant (CCPP) is a type of power generation facility that combines two thermodynamic cycles: the Brayton cycle (gas turbine) and the Rankine cycle (steam turbine).')
    st.markdown('Gas Turbine (Brayton Cycle):The Gas turbine is the primary component responsible for converting fuel energy into mechanical energy through combustion and expansion of hot gases.')
    st.markdown('Steam Turbine (Rankine Cycle):The Steam turbine utilizes the heat generated by the exhaust gases from the gas turbine to produce additional mechanical energy through the expansion of steam.')
if mode == "Prediction":
 # Streamlit Prediction Section
 st.title('COMBINED CYCLE POWER PLANT')
 st.subheader("Enter values to predict energy production")

 # Get user input
 df = user_input_features()
 st.subheader('User Input parameters')
 st.write(df)

 # Ensure the DataFrame has the same column order as during training
 df = df[['temperature', 'exhaust_vacuum', 'amb_pressure', 'r_humidity']]

 # Check if scaler has a transform method
 if not hasattr(scaler, 'transform'):
     st.error("Scaler does not have a 'transform' method.")
     st.stop()

 # Scale the user input features using the loaded scaler
 new_data_points_scaled = scaler.transform(df)

 # Make predictions
 prediction = model.predict(new_data_points_scaled)

 # Display predictions
 if st.button('Predict'):
     st.subheader('Energy production Predicted')
     st.info(prediction.round(2))


    
if mode == 'Visualization':
	st.subheader(' **Uploaded Data Set:**')
	uploaded_file = st.sidebar.file_uploader("Choose a file")
	if uploaded_file is not None:
		df = pd.read_csv(uploaded_file)
		st.write(df)
		global numeric_columns
		global non_numeric_columns
		try:
			numeric_columns = list(df.select_dtypes(['int', 'float']).columns)
			non_numeric_columns = list(df.select_dtypes(['object']).columns)
			non_numeric_columns.append(None)
			print(non_numeric_columns)
		except Exception as e:
			print(e)
         
if mode == 'Visualization':
    st.subheader(' **Plots :**')
    chart_select = st.sidebar.selectbox(label="Select the chart type",options=['Select','Scatterplots', 'Lineplots', 'Histogram','3D Plot'])
    if chart_select == 'Scatterplots':
    	st.sidebar.subheader("Scatterplot Settings")
    	try:
    		x_values = st.sidebar.selectbox('X axis', options=numeric_columns)
    		y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
    		plot = px.scatter(data_frame=df, x=x_values, y=y_values)
    		# display the chart
    		st.plotly_chart(plot)
    	except Exception as e:
    			print(e)
    if chart_select == 'Lineplots':
    	st.sidebar.subheader("Line Plot Settings")
    	try:
    		x_values = st.sidebar.selectbox('X axis', options=numeric_columns)
    		y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
    		plot = px.line(data_frame=df, x=x_values, y=y_values)
    		st.plotly_chart(plot)
    	except Exception as e:
    		print(e)
            
    if chart_select == 'Histogram':
    	st.sidebar.subheader("Histogram Settings")
    	try:
    		x = st.sidebar.selectbox('X axis', options=numeric_columns)
    		#bin_size = st.sidebar.slider("Number of Bins", min_value=10,max_value=100, value=40)
    		plot = px.histogram(x=x, data_frame=df)
    		st.plotly_chart(plot)

    	except Exception as e:
    		print(e)
            

    if chart_select == '3D Plot':
        st.sidebar.subheader("3D Plot Settings")
    try:
        x_values = st.sidebar.selectbox('X axis', options=numeric_columns)
        y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
        z_values = st.sidebar.selectbox('Z axis', options=numeric_columns)
        
        color_value = st.sidebar.selectbox('color', options=numeric_columns)
        
        plot = px.scatter_3d(data_frame=df, x=x_values, y=y_values, z=z_values, color=color_value)
        st.plotly_chart(plot)

    except Exception as e:
        print(e)

if mode == 'About Us':
    image_path2 = "C:/Users/himan/Downloads/images.jfif"  # Replace with the path to your image file
    image = Image.open(image_path2)
    st.image(image,
            use_column_width=True,
            output_format="auto",
            )
    
    st.title("P324 Group 2")
    st.header('Team Members')
    st.write("* *Lekha Bhoyar*")
    st.write("* *Harshada Yewale*")
    st.write("* *Disha.A M*")
    st.write("* *Vasundhra*")
    st.write("* *Gayatri pawar*")
    st.header('Guided By')
    st.write("* *Mr.Karthik Muskula*")



if __name__ == '__user_input_features__':
    user_input_features()
	

 
