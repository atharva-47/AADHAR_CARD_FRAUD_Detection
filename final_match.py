import pandas as pd
def put_final_result(filename):
    df = pd.read_excel(filename)
    df['Overall Match'] = df[['UID Match Score', 'Final Address Match Score', 'Name Match Score']].mean(axis=1)
    for i in range (len(df)):
        if df['UID Match Score'][i] == 100 and df['Final Address Match Score'][i] > 80 and df['Name Match Score'][i] >= 90:
            df['Final Remarks'][i] = "Aadhar Card Verified Successfully ."
        if df['UID Match Score'][i] < 100 or df['Final Address Match Score'][i] < 80 or df['Name Match Score'][i] < 90:
            df['Final Remarks'][i] = "Couldn't Verify Your aadhar card ."
        if df['UID Match Score'][i] == 0 and df['Final Address Match Score'][i] == 0 and df['Name Match Score'][i] == 0:
            df['Final Remarks'][i] = "The Image is not aadhar card."
    df.to_excel('output.xlsx', index=False)