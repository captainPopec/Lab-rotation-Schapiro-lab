#Merging Qunatification Csvs
import pandas as pd
from pathlib import Path

# --- configure paths ---
Qunatification_input_dir = Path("/gpfs/bwfor/work/ws/hd_vh340-MCmicro_exemplar/segmentation_input/quantification")
Micro_input_dir = Path("/gpfs/bwfor/work/ws/hd_vh340-MCmicro_exemplar/micronuclAI/results_6_55/micronuclai")
output_path = "/gpfs/bwfor/work/ws/hd_vh340-MCmicro_exemplar/micronuclAI/All_merged.csv"
PatientID_output_dir = Path("/gpfs/bwfor/work/ws/hd_vh340-MCmicro_exemplar/micronuclAI/patients")
PatientID_output_dir.mkdir(parents=True, exist_ok=True)


# --- collect and merge ---
dfs = []

for csv_file in sorted(Qunatification_input_dir.glob("*--mesmer_cell.csv")):
    # Extract sample ID (remove the "--mesmer_cell.csv" part)
    sample_id = csv_file.name.replace("--mesmer_cell.csv", "")

    # Read CSV
    df = pd.read_csv(csv_file)

    # Insert SampleID as 2nd column (after CellID)
    df.insert(1, "SampleID", sample_id)

    dfs.append(df)

# Combine all qunatification dfs into one
qmerged_df = pd.concat(dfs, ignore_index=True)

# Save
#merged_df.to_csv(output_csv, index=False)

print(f"✅ Merged {len(dfs)} CSVs, ({len(qmerged_df)} total rows)")



#Merging the micronuclAI csvs
dfs = []

for csv_file in sorted(Micro_input_dir.glob("*_cell_predictions.csv")):
    # Extract sample ID (remove the "--mesmer_cell.csv" part)
    sample_id = csv_file.name.replace("_cell_predictions.csv", "")

    # Read CSV
    df = pd.read_csv(csv_file)

    # Insert SampleID as 2nd column (after CellID)
    df.insert(1, "SampleID", sample_id)

    dfs.append(df)

# Combine all
micro_merged_df = pd.concat(dfs, ignore_index=True)

# Save
#merged_df.to_csv(output_csv, index=False)

print(f"✅ Merged {len(dfs)} CSVs, ({len(micro_merged_df)} total rows)")



#Merging the two merged csvs
import pandas as pd

# --- Input files ---
#quant_path = "C:/Users/Korisnik/Desktop/RAM/Kreso_praksa/merged_cells.csv"
#micronuclei_path = "C:/Users/Korisnik/Desktop/RAM/Kreso_praksa/merged_MicroNuclAI.csv"


# --- Read both files ---
#df_quant = pd.read_csv(quant_path)
#df_micro = pd.read_csv(micronuclei_path)
df_quant = qmerged_df
df_micro = micro_merged_df
df_micro.rename(columns={"cellID": "CellID"}, inplace=True)

# --- Keep only the unique columns from micronuclei file ---
df_micro = df_micro[["CellID", "SampleID", "score", "micronuclei"]]

# --- Merge on CellID + SampleID ---
merged = pd.merge(df_quant, df_micro, on=["CellID", "SampleID"], how="left")

# --- Apply Boolean thresholds ---
merged["CD138_pos"] = merged["CD138"] > 1.6312074160575833
merged["SOX10_pos"] = merged["SOX10"] > 1
merged["CD68_pos"] = merged["CD68"] > 1.756449425220487
merged["Micronuclei_pos"] = merged["micronuclei"] > 0

# --- Save final result ---
merged.to_csv(output_path, index=False)
print(f"✅ Merged CSV written to: {output_path}")
print(f"Columns in final CSV: {list(merged.columns)}")


#Separating by patient IDs

# --- Extract PatientID from SampleID ---
# Remove the trailing "_<digits>-<digits>" part
merged["PatientID"] = merged["SampleID"].str.replace(r"_[0-9]+-[0-9]+$", "", regex=True)

# --- Group by patient and export ---
for patient_id, sub_df in merged.groupby("PatientID"):
    patient_df = sub_df
    
    # Build output path
    out_path = PatientID_output_dir / f"{patient_id}.csv"
    
    # Save each patient file
    patient_df.to_csv(out_path, index=False)
    print(f"✅ Saved {out_path} ({len(patient_df)} cells)")

print(f"\nAll patient CSVs written to: {PatientID_output_dir}")
