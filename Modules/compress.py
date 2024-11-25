# This file I have used to compress the trained model, It was of 386MB but was causing issue while pushing to Github repo
# To solve this issue I compressed this model and then direclty used after decompressing without saving it explicitly

import gzip
import shutil

# Defining file paths
input_file_path = r'C:\Users\hp\Desktop\ML_Trained_Model\DumpedFile\classifierModel.pkl'
compressed_file_path = r'C:\Users\hp\Desktop\ML_Trained_Model\DumpedFile\classifierModel.pkl.gz'

# Compressing  the file
with open(input_file_path, 'rb') as f_in:
    with gzip.open(compressed_file_path, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
