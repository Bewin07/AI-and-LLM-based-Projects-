
import pandas as pd

print(pd.__version__)

df=pd.DataFrame(columns=["Ticket_ID",
        "Type",
        "Status",
        "Priority",
        "Assigned_To"])

df.to_excel('Tickets.xlsx',index=False)