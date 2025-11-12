import pandas as pd
from pathlib import Path

# --- Configure paths ---
input_dir = Path("/gpfs/bwfor/work/ws/hd_vh340-MCmicro_exemplar/micronuclAI/patients")  # Change to your CSV folder
output_csv = Path("/gpfs/bwfor/work/ws/hd_vh340-MCmicro_exemplar/micronuclAI/patients/Patient_summary.csv")  # Path to save aggregated CSV

# --- Initialize storage ---
patient_counts = {}

# --- Loop through all CSV files ---
for csv_file in input_dir.glob("*.csv"):
    df = pd.read_csv(csv_file)

    # Ensure columns are boolean
    df["SOX10_pos"] = df["SOX10_pos"].astype(bool)
    df["Micronuclei_pos"] = df["Micronuclei_pos"].astype(bool)

    # Loop through each patient in this file
    for patient_id, sub_df in df.groupby("PatientID"):
        if patient_id not in patient_counts:
            patient_counts[patient_id] = {"SOX10+/Micronuclei+": 0,
                                          "SOX10+/Micronuclei-": 0,
                                          "SOX10-/Micronuclei+": 0}

        # Count each category
        patient_counts[patient_id]["SOX10+/Micronuclei+"] += ((sub_df["SOX10_pos"] == True) & (sub_df["Micronuclei_pos"] == True)).sum()
        patient_counts[patient_id]["SOX10+/Micronuclei-"] += ((sub_df["SOX10_pos"] == True) & (sub_df["Micronuclei_pos"] == False)).sum()
        patient_counts[patient_id]["SOX10-/Micronuclei+"] += ((sub_df["SOX10_pos"] == False) & (sub_df["Micronuclei_pos"] == True)).sum()
        # Optionally: SOX10-/Micronuclei- is the leftover, can be ignored or added if needed

# --- Convert to DataFrame ---
summary_df = pd.DataFrame.from_dict(patient_counts, orient="index").reset_index()
summary_df.rename(columns={"index": "PatientID"}, inplace=True)

# --- Add N_count and K_count rows ---
n_classified_count = summary_df.loc[summary_df["PatientID"].str.startswith("N"), "SOX10+/Micronuclei+"].sum()
k_classifed_count = summary_df.loc[summary_df["PatientID"].str.startswith("K"), "SOX10+/Micronuclei+"].sum()
n_notclassified_count = summary_df.loc[summary_df["PatientID"].str.startswith("N"), "SOX10+/Micronuclei-"].sum()
k_notclassified_count = summary_df.loc[summary_df["PatientID"].str.startswith("K"), "SOX10+/Micronuclei-"].sum()

N_udio = n_classified_count/(n_classified_count + n_notclassified_count)
K_udio = k_classifed_count/(k_classifed_count + k_notclassified_count)

summary_df = pd.concat([
    summary_df,
    pd.DataFrame([{"PatientID": "N_count", "SOX10+/Micronuclei+": N_udio, 
                   "SOX10+/Micronuclei-": "", "SOX10-/Micronuclei+": ""}]),
    pd.DataFrame([{"PatientID": "K_count", "SOX10+/Micronuclei+": K_udio, 
                   "SOX10+/Micronuclei-": "", "SOX10-/Micronuclei+": ""}])
], ignore_index=True)

# --- Save to CSV ---
summary_df.to_csv(output_csv, index=False)
print(f"✅ Summary CSV with N_count and K_count written to: {output_csv}")