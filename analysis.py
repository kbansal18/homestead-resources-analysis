"""
Homestead Resources - Home & Rental Services Analysis
The Data Exchange at Purdue University, Spring 2026

Analyzes client survey responses to compare service usage, housing outcomes,
satisfaction, and recommendation rates across Homestead Resources programs.

NOTE: The client survey data is confidential and is not included in this repository.
"""
import pandas as pd
import matplotlib.pyplot as plt

# === Load data ===
FILE = "Client Survey All Data Export.xlsx"
df = pd.read_excel(FILE)

# === Column name shortcuts ===
COL_Q4 = "Question 4: Which of the following Homestead Resources services have you used?"
COL_Q5 = "Question 5: If you received rental counseling, did it help you secure or maintain stable housing?"
COL_Q6 = "Question 6: If you received homeownership counseling, did it help you purchase a home?"
COL_Q7 = "Question 7: Since receiving services from Homestead Resources, have you maintained stable housing?"
COL_Q12 = "Question 12: Have you recommended programs and counseling at Homestead Resources to others?"
COL_Q13 = "Question 13: Overall, how satisfied are you with the services you received from Homestead Resources?"
COL_Q14 = "Question 14: What additional services would be most helpful to you in the future?"

# === Simplified service group from Q4 ===
def categorize_service(text):
    if pd.isna(text):
        return "Unknown/No response"
    t = str(text).lower()
    if "rental" in t:
        return "Rental services"
    if "mortgage" in t or "foreclosure" in t or "reverse mortgage" in t or "pre-purchase" in t:
        return "Homeownership/mortgage"
    if "budget" in t or "credit" in t or "financial literacy" in t or "classes at the food finders education center" in t:
        return "Financial education"
    if "home repair" in t:
        return "Home repair"
    if "never got help" in t or "don’t remember" in t or "don't remember" in t or "funds were gone" in t:
        return "No/insufficient service"
    return "Other"

df["ServiceGroup"] = df[COL_Q4].apply(categorize_service)

print("\nServiceGroup counts:")
print(df["ServiceGroup"].value_counts())

# === Plot: Service Distribution ===
plt.figure()
df["ServiceGroup"].value_counts().plot(kind="bar")
plt.title("Which Services Did Clients Receive from Homestead Resources?")
plt.xlabel("Service Type")
plt.ylabel("Number of Clients")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("plots/00_ServiceDistribution.png", dpi=150)
plt.show()


# Q5: "Yes, I maintained stable housing." is positive
df["Q5_Positive"] = df[COL_Q5].astype(str).str.startswith("Yes")

# Q6: "Yes, I successfully purchased a home." is positive
df["Q6_Positive"] = df[COL_Q6].astype(str).str.startswith("Yes")

# Q7: any answer that begins with "Yes" is treated as maintaining stable housing
df["Q7_Positive"] = df[COL_Q7].astype(str).str.startswith("Yes")


# Q4 → Q5 : Services vs Rental Counseling Impact
q4_q5 = df.groupby("ServiceGroup")["Q5_Positive"].mean().sort_values(ascending=False)

plt.figure()
q4_q5.plot(kind="bar")
plt.title("Service Type vs Rental Counseling Helped Maintain Housing (Q4 → Q5)")
plt.ylabel("Proportion Positive (Yes)")
plt.ylim(0, 1)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("plots/01_Q4_Q5_RentalCounselingImpact.png", dpi=150)
plt.show()


# Q4 → Q6 : Services vs Home Purchase Success
q4_q6 = df.groupby("ServiceGroup")["Q6_Positive"].mean().sort_values(ascending=False)

plt.figure()
q4_q6.plot(kind="bar")
plt.title("Service Type vs Home Purchase Success (Q4 → Q6)")
plt.ylabel("Proportion Positive (Yes)")
plt.ylim(0, 1)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("plots/02_Q4_Q6_HomePurchaseSuccess.png", dpi=150)
plt.show()


# Q4 → Q7 : Services vs Stable Housing
q4_q7 = df.groupby("ServiceGroup")["Q7_Positive"].mean().sort_values(ascending=False)

plt.figure()
q4_q7.plot(kind="bar")
plt.title("Service Type vs Maintaining Stable Housing (Q4 → Q7)")
plt.ylabel("Proportion Positive (Yes)")
plt.ylim(0, 1)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("plots/03_Q4_Q7_StableHousingOutcome.png", dpi=150)
plt.show()


# Retention – Q12 : Recommendation Rates
plt.figure()
df[COL_Q12].value_counts(normalize=True).sort_index().plot(kind="bar")
plt.title("Recommendation of Homestead Resources (Q12)")
plt.ylabel("Proportion of Respondents")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("plots/04_Q12_RecommendationRate.png", dpi=150)
plt.show()


# Q4 + Q13 : Service Type vs Satisfaction

# (Average satisfaction score by service group)
q4_q13 = df.groupby("ServiceGroup")[COL_Q13].mean().sort_values(ascending=False)

plt.figure()
q4_q13.plot(kind="bar")
plt.title("Service Type vs Average Satisfaction (Q4 + Q13)")
plt.ylabel("Average Satisfaction (1–5)")
plt.ylim(1, 5)
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("plots/05_Q4_Q13_ServiceSatisfaction.png", dpi=150)
plt.show()

# Q14 : Additional Services Requested

future_counts = (
    df[COL_Q14]
    .value_counts()
    .head(10)
    .sort_values(ascending=True) 
)

plt.figure(figsize=(10, 6))
plt.barh(future_counts.index, future_counts.values)

plt.title("Most Requested Future Services")
plt.xlabel("Count (Top 10)")
plt.ylabel("")

plt.tight_layout()
plt.savefig("plots/06_Q14_FutureServicesRequested.png", dpi=150)
plt.show()


# Extra Plot: Stable Housing vs Satisfaction (Q7 + Q13)

q7_q13 = df.groupby("Q7_Positive")[COL_Q13].mean()

plt.figure()
q7_q13.plot(kind="bar")
plt.title("Average Satisfaction by Stable Housing Outcome")
plt.xlabel("Maintained Stable Housing (Q7_Positive)")
plt.ylabel("Average Satisfaction Score (1–5)")
plt.ylim(1, 5)
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("plots/07_Extra_Q7_SatisfactionComparison.png", dpi=150)
plt.show()