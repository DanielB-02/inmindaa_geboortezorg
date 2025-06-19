import pandas as pd

# 1. Bestanden inlezen
file_path = '../bewerkte_data/armoede_goed_2022.xlsx'
kwb_df = pd.read_excel(file_path)
loc_df = pd.read_excel("../bewerkte_data/locatie_coords.xlsx")

# 4. Merge op pc4_codeá
merged_df = kwb_df.merge(
    loc_df[['pc4_code', 'latitude', 'longitude']],
    on='pc4_code',
    how='left'  # behoud alle rijen uit de kwb-tabel
)

merged_df.to_excel("../bewerkte_data/kwb_2022_met_lat_lon_goed.xlsx", index=False)
