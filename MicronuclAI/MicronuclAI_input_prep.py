#!/usr/bin/env python3
import pandas as pd
from pathlib import Path

# Paths to the folders
images_dir = Path("/gpfs/bwfor/work/ws/hd_vh340-MCmicro_exemplar/segmentation_input/registration/")
segmentation_dir = Path("/gpfs/bwfor/work/ws/hd_vh340-MCmicro_exemplar/segmentation_input/segmentation/")

def generate_samples_csv(output_csv="sampleshit_main.csv"):
    """
    Generate a CSV for MicronuclAI with columns: sample,image,segmentation
    """
    data = []
    
    # Iterate over all .ome.tif files in the registration folder
    for img_path in sorted(images_dir.glob("*.ome.tif")):
        sample_name = img_path.with_suffix('').with_suffix('').name # filename without extension
        
        # Construct the corresponding segmentation path
        seg_path = segmentation_dir / f"mesmer-{sample_name}" / "cell.tif"
        
        # Ensure the segmentation file exists
        if not seg_path.exists():
            print(f"Warning: segmentation file not found for {sample_name}")
            continue
        
        # Append row
        data.append({
            "sample": sample_name,
            "image": str(img_path.resolve()),
            "segmentation": str(seg_path.resolve())
        })
    
    # Save to CSV
    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)
    print(f"CSV written to {output_csv} with {len(df)} samples")

if __name__ == "__main__":
    generate_samples_csv()
