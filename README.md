# 🍽️ Uber Eats Bangalore Restaurant Intelligence 
# & Decision Support System

## 📌 Problem Statement
Uber Eats operates a large-scale restaurant marketplace 
where business success depends on location strategy, 
pricing, cuisine mix, customer ratings, and platform 
features like online ordering and table booking.

This project analyzes Uber Eats Bangalore restaurant data 
and builds a decision support system answering critical 
business questions using Python and SQL — presenting 
results as clean tabular DataFrame outputs in Streamlit.

---

## 🛠️ Tech Stack
| Tool | Purpose |
|---|---|
| Python | Data processing |
| Pandas | Data cleaning |
| SQLite | Database layer |
| Streamlit | Web application |
| Google Colab | Development environment |

---

## 📁 Project Structure
```
ubereats_project/
│
├── notebook1_restaurants.ipynb  # Cleaning + SQL queries
├── notebook2_orders.ipynb       # Orders analysis
├── app.py                       # Streamlit application
├── ubereats.db                  # SQLite database
└── README.md                    # Documentation
```

---

## 📊 Dataset
| Dataset | Records | Columns |
|---|---|---|
| Uber_Eats_data.csv | 16,618 (cleaned) | 11 |
| orders.json | 25,000 | 6 |

**Key Columns:**
- restaurant: name, location, cuisines, rate, votes
- orders: restaurant_name, order_value, payment_method

---

## 🔍 Data Cleaning Steps
1. Fixed `rate` column — removed `/5` suffix → float
2. Fixed `approx_cost` — removed commas → int
3. Dropped NaN ratings (unreliable data)
4. Dropped useless columns (phone, listed_in_city)
5. Removed duplicates AFTER dropping columns
6. Renamed SQL-unfriendly column names

---

## ❓ Business Questions Answered

### Restaurant Analysis (Q1-Q10)
| Q# | Question | Key Finding |
|---|---|---|
| Q1 | Highest rated locations | Lavelle Road (4.21) |
| Q2 | Over-saturated locations | Koramangala 5th (1213) |
| Q3 | Online ordering impact | Minimal (3.92 vs 3.99) |
| Q4 | Table booking impact | Significant (4.18 vs 3.83) |
| Q5 | Best price range | Premium wins |
| Q6 | Price segment performance | Premium > Mid > Low |
| Q7 | Most common cuisines | North Indian (7164) |
| Q8 | Highest rated cuisines | Cantonese (4.6) |
| Q9 | Niche opportunities | Belgian, Cantonese |
| Q10 | Cost vs Rating | Higher cost = higher rating |

### Orders Analysis
| Q# | Question | Key Finding |
|---|---|---|
| OQ1 | Discount impact | Discounts → ₹327 more spend |
| OQ2 | Revenue by day | Monday highest |
| OQ3 | Top restaurants | Evenly distributed |
| OQ4 | Monthly revenue | January leads |
| OQ5 | Payment + Discount | Card+Discount highest |

---

## 🚀 How To Run

### Prerequisites
```bash
pip install streamlit pandas
```

### Steps
```bash
# 1. Clone repository
git clone https://github.com/pravinkumardatafreak/ubereats_project

# 2. Add ubereats.db to project folder

# 3. Run app
streamlit run app.py

# 4. Open browser
http://localhost:8501
```

---

## 📱 App Features

### 🏠 Dashboard Page
- Filter by location, online order, table booking
- Rating slider filter
- Dynamic SQL-based results

### ❓ Q&A Page  
- 10 predefined business questions
- SQL-computed answers
- DataFrame table display

### 📦 Orders Page
- 6 orders analytics queries
- Revenue by payment, day, month
- Discount impact analysis

---

## 📈 Key Business Insights
1. **Koramangala** dominates — highest rated AND most restaurants
2. **Table booking** drives quality — 0.35 rating difference
3. **Discounts** boost revenue — customers spend ₹327 more
4. **Niche cuisines** (Cantonese, Belgian) outperform popular ones
5. **Premium pricing** correlates with higher satisfaction

---

## 👨‍💻 Author
**pravinkumar**
GUVI HCL Data Science Program
Domain: SQL / Data Engineering / Python / Data Science
