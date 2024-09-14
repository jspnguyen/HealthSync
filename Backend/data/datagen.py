import pandas as pd
import numpy as np

# Set seed for reproducibility
np.random.seed(0)

# Create date range for 356 days with hourly intervals (total hours = 3,556)
start_date = '2022-01-01'
end_date = '2023-12-31'

dates = pd.date_range(start=start_date + ' 00:00', end=end_date + ' 23:59', freq='H')

data = []

for i in dates:
    # Generate random data for each column
    doctors_count = np.random.randint(120, 150)
    nurses_count = np.random.randint(250, 300)
    doctors_on_call_count = np.random.randint(5, 15)
    nurses_on_call_count = np.random.randint(10, 20)
    
    total_hospital_beds = int(np.random.uniform(500, 800))
    hospital_beds_open = int(np.random.uniform(total_hospital_beds * 0.7, total_hospital_beds * 0.9))
    hospital_beds_occupied = total_hospital_beds - hospital_beds_open
    
    ambulances_on_duty_count = np.random.randint(5, 15)
    
    medical_equipment_dict = {
        'CT Scanners': np.random.randint(1, 10),
        'X-Ray Machines': np.random.randint(2, 12),
        'Ventilators': np.random.randint(3, 20),
        'Other Equipment': np.random.randint(50, 100)
    }
    
    # Convert dictionary to DataFrame
    equipment_df = pd.DataFrame(list(medical_equipment_dict.items()), columns=['Type', 'Count'])
    
    row_data = {
        'Date Time': i,
        'Doctors (count)': doctors_count,
        'Nurses(Count)': nurses_count,
        'Doctors on-call (Count)': doctors_on_call_count,
        'Nurses on-call (Count)': nurses_on_call_count,
        'Total Hospital Beds (Count)': total_hospital_beds,
        'Hospital Beds Open (Count)': hospital_beds_open,
        'Hospital Beds Occupied (Count)': hospital_beds_occupied,
        'Ambulances On Duty (Count)': ambulances_on_duty_count
    }
    
    # Concatenate DataFrames
    data.append(row_data)
    equipment_df['Date Time'] = i
    
data = pd.DataFrame(data)

equipment_df.set_index('Date Time', inplace=True)

# Save to CSV file with hourly frequency for the date_time column
data.to_csv('Backend/data/hospital_staffing_data_hourly.csv')
equipment_df.to_csv('Backend/data/medical_equipment_counts_hourly.csv')

print(f"Data saved to hospital_staffing_data_hourly.csv and medical_equipment_counts_hourly.csv")