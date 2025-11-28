import pandas as pd

def clean_password_txt(file_path: str, output_path: str):
    df = pd.read_table(file_path, header=None, names=['password'])

    df['password'] = df['password'].astype(str).str.strip().str.lower()

    df = df[df['password'] != '']
    df = df.drop_duplicates().reset_index(drop=True)

    df.to_csv(output_path, index=False, header=False)
    print(f"Cleaned {len(df)} unique passwords saved to {output_path}")

clean_password_txt("common_passwords.txt", "common_passwords_cleaned.txt")