# app.py
import streamlit as st
from datetime import datetime
import pandas as pd
from db_utils import connect_to_mysql, create_table, insert_food_data, edit_log, delete_log, save_daily_notes, get_daily_notes
from api_utils import fetch_nutrient_data
from ai_utils import initialize_llm, create_chain
from data_utils import clean_ai_output
import json
import os
from PIL import Image

# Initialize the LLM and chain
llm = initialize_llm()
chain = create_chain(llm)

# Directory to save uploaded images
UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Streamlit app
st.title("📖 Food Diary Chatbot")
st.write("Welcome to your personal food diary! Describe your meal, and I'll help you log it.")

# Sidebar for navigation and additional features
with st.sidebar:
    st.header("🗓️ Navigation")
    log_date = st.date_input("📅 Select the date for your meal log:", datetime.today())

    st.write("---")
    st.header("📝 Daily Notes")

    # Connect to database
    connection = connect_to_mysql()

    # Fetch existing notes for the selected date
    existing_notes = get_daily_notes(connection, log_date)

    # Use session state to store and update notes
    if "daily_notes" not in st.session_state or log_date != st.session_state.get("last_selected_date"):
        st.session_state["daily_notes"] = existing_notes
        st.session_state["last_selected_date"] = log_date

    daily_notes = st.text_area("Write about your day:", height=150, key="daily_notes")

    if st.button("💾 Save Notes"):
        save_daily_notes(connection, log_date, daily_notes)
        st.session_state["last_selected_date"] = log_date
        st.success("✅ Notes saved successfully!")

    connection.close()

# State to hold the meal description
if "meal_description" not in st.session_state:
    st.session_state["meal_description"] = ""

# User input for meal description
st.header("🍽️ Log Your Meal")
meal_description = st.text_input("✍️ Describe your meal:", value=st.session_state["meal_description"], key="meal_input")

# File uploader for meal image
uploaded_file = st.file_uploader("📷 Upload a picture of your meal (optional):", type=["jpg", "jpeg", "png"])

# Submit button to process the input
if st.button("📌 Log Meal"):
    if meal_description:
        try:
            # Save the uploaded image if provided
            image_path = None
            image_path_for_display = None
            
            if uploaded_file is not None:
                image_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uploaded_file.name}"
                image_path = os.path.join(UPLOAD_DIR, image_name)
                
                # Create directory if it doesn't exist
                os.makedirs(UPLOAD_DIR, exist_ok=True)
                
                with open(image_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.success(f"✅ Image uploaded successfully: {image_name}")
                
                # Store relative path for display
                image_path_for_display = os.path.join("uploaded_images", image_name)

            # Process the input using LangChain
            structured_output = chain.run({"meal_description": meal_description})
            #st.write("Raw AI Response:", structured_output)  # Debugging: Print the raw response

            # Validate and display structured output
            try:
                parsed_output = json.loads(structured_output)
                #st.write("Processed Information:", parsed_output) # Debugging: Print the response
            except json.JSONDecodeError:
                st.error("Failed to parse the structured output. Check the AI response format.")
                parsed_output = None

            # Clean and normalize the AI output
            if parsed_output:
                parsed_output["food_items"] = clean_ai_output(parsed_output["food_items"])

            # Save to MySQL database if output is valid
            if parsed_output:
                try:
                    connection = connect_to_mysql()
                    create_table(connection)
                    for item in parsed_output["food_items"]:
                        item["image_path"] = image_path_for_display  # Add image path to each food item
                    insert_food_data(connection, parsed_output["food_items"], parsed_output["meal_time"], log_date)
                    st.success("✅ Meal logged successfully!")
                    st.session_state["meal_description"] = ""  # Clear input only after successful processing
                except Exception as e:
                    st.error(f"Database error: {e}")
                finally:
                    if connection:
                        connection.close()
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Display Daily Summary
st.header("📊 Daily Summary")
try:
    connection = connect_to_mysql()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM food_logs WHERE `log_date` = %s", (log_date,))
    rows = cursor.fetchall()

    if rows:
        df = pd.DataFrame(rows, columns=[
            "ID", "Food Name", "Quantity", "Meal Time", "Category",
            "Calories", "Protein", "Carbohydrates", "Fats", "Fiber", "Sugars", "Log Date", "Image Path"
        ])

        # Calculate total nutrients for the day
        total_calories = df["Calories"].sum()
        total_protein = df["Protein"].sum()
        total_carbs = df["Carbohydrates"].sum()
        total_fats = df["Fats"].sum()

        # Display totals
        st.write(f"**Total Calories:** {total_calories:,.2f} kcal")
        st.write(f"**Total Protein:** {total_protein:,.2f} g")
        st.write(f"**Total Carbohydrates:** {total_carbs:,.2f} g")
        st.write(f"**Total Fats:** {total_fats:,.2f} g")

        # Group meals by meal time
        st.subheader("🍴 Meals by Time")
        preferred_order = ["breakfast", "brunch", "lunch", "snack", "dinner", "supper", "other"]
        meal_times = sorted(df["Meal Time"].unique(), key=lambda x: preferred_order.index(x.lower()) if x.lower() in preferred_order else len(preferred_order))

        for meal_time in meal_times:
            st.write(f"**{meal_time.capitalize()}**")
            meal_df = df[df["Meal Time"] == meal_time].copy()
            
            # Track unique images to avoid duplicates
            displayed_images = set()
            
            # First display all images for this meal
            for _, row in meal_df.iterrows():
                if row["Image Path"] and row["Image Path"] not in displayed_images:
                    try:
                        possible_paths = [
                            row["Image Path"],
                            os.path.join("uploaded_images", os.path.basename(row["Image Path"]))
                        ]
                        
                        for path in possible_paths:
                            if os.path.exists(path):
                                st.image(
                                    path,
                                    caption=f"{row['Quantity']} {row['Food Name']}",
                                    use_container_width=True
                                )
                                displayed_images.add(row["Image Path"])
                                break
                    except Exception as e:
                        st.warning(f"Couldn't display image: {str(e)}")
            
            # Then show the table - CRITICAL: Keep original index for deletion
            display_df = meal_df.drop(columns=["ID", "Log Date", "Image Path", "Meal Time"]).copy()
            display_df["Delete"] = False
            
            # Store the original indices in the dataframe
            display_df["original_index"] = meal_df.index
            
            editable_columns = ["Food Name", "Quantity"]
            edited_df = st.data_editor(
                display_df,
                column_config={
                    "Delete": st.column_config.CheckboxColumn("Delete", help="Check to delete this row"),
                    "Food Name": st.column_config.TextColumn("Food Name", help="Edit the food name"),
                    "Quantity": st.column_config.TextColumn("Quantity", help="Edit the serving size"),
                    "original_index": None  # Hide this column
                },
                disabled=set(display_df.columns) - set(editable_columns + ["Delete"]),
                key=f"data_editor_{meal_time}",
                width=None,
                hide_index=True
            )

            # Handle row deletion
            if edited_df["Delete"].any():
                rows_to_delete = edited_df[edited_df["Delete"]]
                for _, row_to_delete in rows_to_delete.iterrows():
                    # Get the original row using the stored index
                    original_row = meal_df.loc[row_to_delete["original_index"]]
                    delete_log(connection, int(original_row["ID"]))
                st.success("Selected rows deleted successfully!")
                st.rerun()

            # Handle edits to "Food Name" and "Quantity"
            for _, edited_row in edited_df.iterrows():
                original_row = meal_df.loc[edited_row["original_index"]]
                
                if (edited_row["Food Name"] != original_row["Food Name"]) or (edited_row["Quantity"] != original_row["Quantity"]):
                    query = f"{edited_row['Quantity']} {edited_row['Food Name']}"
                    nutrient_data = fetch_nutrient_data(query)

                    if nutrient_data and "items" in nutrient_data and len(nutrient_data["items"]) > 0:
                        updated_data = {
                            "food_name": edited_row["Food Name"],
                            "quantity": edited_row["Quantity"],
                            "meal_time": original_row["Meal Time"],
                            "category": original_row["Category"],
                            "calories": nutrient_data["items"][0].get("calories", 0),
                            "protein": nutrient_data["items"][0].get("protein_g", 0),
                            "carbohydrates": nutrient_data["items"][0].get("carbohydrates_total_g", 0),
                            "fats": nutrient_data["items"][0].get("fat_total_g", 0),
                            "fiber": nutrient_data["items"][0].get("fiber_g", 0),
                            "sugars": nutrient_data["items"][0].get("sugar_g", 0)
                        }
                    else:
                        updated_data = {
                            "food_name": edited_row["Food Name"],
                            "quantity": edited_row["Quantity"],
                            "meal_time": original_row["Meal Time"],
                            "category": original_row["Category"],
                            "calories": original_row["Calories"],
                            "protein": original_row["Protein"],
                            "carbohydrates": original_row["Carbohydrates"],
                            "fats": original_row["Fats"],
                            "fiber": original_row["Fiber"],
                            "sugars": original_row["Sugars"]
                        }

                    edit_log(connection, original_row["ID"], updated_data)
                    st.success(f"Updated {edited_row['Food Name']} successfully!")
                    st.rerun()
            
            st.write("---")  # Separator between meal times

    else:
        st.write(f"No meals logged for {log_date}.")
except Exception as e:
    st.error(f"Error: {e}")
finally:
    if connection:
        connection.close()
