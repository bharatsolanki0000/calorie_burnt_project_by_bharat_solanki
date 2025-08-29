import streamlit as st
import pandas as pd
import pickle

import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Calorie Burn Predictor by Bharat Solanki",
    page_icon="🔥",
    
)


try:
    pipe=pickle.load(open("project.pkl","rb"))
    df_exercise = pd.read_csv("exercise.csv")
    df_calories = pd.read_csv("calories.csv")
    df = pd.concat([df_exercise, df_calories], axis=1)

except Exception as e:
    st.error(f"file paht check: {e}")
    st.stop()



title=st.title("CALORIE BURNT PREDICTOR")

st.subheader("Enter your all entries and predict the calories burnt !!")


name=st.text_input("Enter your name")
age=st.number_input("Enter your age ", min_value=10, max_value=90, step=1, value=20)
gender=st.radio("Choose your gender",["Male","Female"])
heat_rate=st.number_input("Enter heartbeat rate in bpm",min_value=60, max_value=120, step=1,value=90 )
body_temp=st.number_input("Enter body temperature in Celsius",min_value=36.0, max_value=40.0, value=37.0, step=1.0 ,format="%.2f")
duration=st.number_input("Enter duration of Exercise in minutes",min_value=1,max_value=120,value=20, step=1)
height=st.number_input("Enter your height in cm",min_value=140.0,max_value=210.0,value=170.0, step=0.1,format="%.2f")
weight=st.number_input("Enter weight in kg",min_value=40.0,max_value=150.0,value=65.0, step=0.1,format="%.2f")

submit=st.button("SUBMIT!!")

if(submit):
    if not name:
        st.warning("please enter Name!!")
    else:
        input_data=pd.DataFrame({
        "Gender":gender.lower(),
        "Age":age,
        "Height":height,
        "Weight":weight,
        "Duration":duration,
        "Heart_Rate":heat_rate,
        "Body_Temp":body_temp
    }, index=[0])
        

        try:
            # Predict calories
            calorie_prediction = pipe.predict(input_data)[0]

            # Calculate average calories for input gender
            gender_lower = gender.lower()
            target_calorie = df[df['Gender'] == gender_lower]['Calories'].mean()

            
            st.success(f"Hey {name}! Based on your inputs, you've burnt approximately **{calorie_prediction:.2f} kcal** calories!")

            st.balloons()
            if calorie_prediction > target_calorie:
                st.success(f"🎉 Great job! Your predicted burn of **{calorie_prediction:.2f} kcal** is above the average for a {gender.lower()}. Stay consistent!")
            elif calorie_prediction > 50:
                st.info("A solid workout! To boost your calorie burn, try adding a few minutes to your duration.")
            else:
                st.warning("To get the most out of your exercise, a longer duration or higher is recommended.")
            
            

            # Create a DataFrame for the bar chart
            plot_df = pd.DataFrame({
                "Category": ["Your Prediction", f"Average for {gender}"],
                "Calories (kcal)": [calorie_prediction, target_calorie]
            })


            # Create the bar plot btw avg and predicted calories of given gender
            fig, ax = plt.subplots()
            
            # Using only matplotlib's plt.bar function
            ax.bar(
                plot_df["Category"], 
                plot_df["Calories (kcal)"], 
                color=['#66c2a5', '#fc8d62'] # Manually specifying colors from a similar palette
            )

            ax.set_title(f"Your Calorie Burn vs. Average Calorie Burn of {gender}")
            ax.set_xlabel("")
            ax.set_ylabel("Calories (kcal)")

            st.pyplot(fig)
            
        except Exception as e:
            st.error(f"Something went wrong during prediction or visualization: {e}")
            
st.subheader("What-If Scenario 🎯")
st.markdown("See what it takes to hit your target calorie goal.")
target_calories=st.number_input("enter target calorie you want to burn!",min_value=1.0,max_value=314.0,value=100.0, step=.1)
calculate_what_if=st.button("what if")
if calculate_what_if:
    if (not name):
        st.warning("Please enter your name and Submit to proceed with the What-If analysis!")
    else:
        st.markdown(f"#### To burn {target_calories:.0f} kcal:")

        
        what_if_data = pd.DataFrame({
            "Gender": gender.lower(),
            "Age": age,
            "Height": height,
            "Weight": weight,
            "Duration": duration,
            "Heart_Rate": heat_rate,
            "Body_Temp": body_temp
        }, index=[0])

        current_prediction = pipe.predict(what_if_data)[0]

       
        duration_factor = target_calories / current_prediction
        new_duration = duration * duration_factor
        st.info(f"You would need to exercise for **{new_duration:.2f} minutes** to reach your goal, keeping all other factors the same.")


        plot_duration = pd.DataFrame({
                "": ["Your Duration", f"Targeted Duration"],
                "time in min": [duration, new_duration]
            })


        
        fig, ax = plt.subplots()
            
        # Use ax.bar() directly, passing the x and y values
        ax.bar(
            plot_duration[""],
            plot_duration["time in min"],
            color=["#1f77b4", "#ff7f0e"] # You can specify colors here
        )

        ax.set_xlabel("")
        ax.set_ylabel("time in min")
        ax.set_title("Your Duration vs. Targeted Duration")
        

        st.pyplot(fig)

st.markdown("---")
st.markdown("Made by **Bharat Solanki**")