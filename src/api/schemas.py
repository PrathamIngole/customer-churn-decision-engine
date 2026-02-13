from pydantic import BaseModel

class CustomerData(BaseModel):
    Gender: str
    Senior_Citizen: str
    Partner: str
    Dependents: str
    Tenure_Months: int
    Phone_Service: str
    Multiple_Lines: str
    Internet_Service: str
    Online_Security: str
    Online_Backup: str
    Device_Protection: str
    Tech_Support: str
    Streaming_TV: str
    Streaming_Movies: str
    Contract: str
    Paperless_Billing: str
    Payment_Method: str
    Monthly_Charges: float
    Total_Charges: float


## "'CustomerID', 'Count', 'Country', 'State', 'City', 'Zip Code',
    #    'Lat Long', 'Latitude', 'Longitude', 'Gender', 'Senior Citizen',
    #    'Partner', 'Dependents', 'Tenure Months', 'Phone Service',
    #    'Multiple Lines', 'Internet Service', 'Online Security',
    #    'Online Backup', 'Device Protection', 'Tech Support', 'Streaming TV',
    #    'Streaming Movies', 'Contract', 'Paperless Billing', 'Payment Method',
    #    'Monthly Charges', 'Total Charges', 'Churn Label', 'Churn Value',
    #    'Churn Score', 'CLTV', 'Churn Reason'"