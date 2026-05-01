# ================================
# 📌 IMPORTS
# ================================
import pandas as pd

# ================================
# 📌 PRICE SCORE (compare with city avg)
# ================================
def price_score(price, city, city_avg):
    avg = city_avg.get(city, price)  # fallback if city not found
    score = max(0, 100 - ((price - avg) / avg) * 100)
    return min(score, 100)

# ================================
# 📌 LOCATION SCORE (based on city growth)
# ================================
def location_score(city):
    city_growth = {
        "Bangalore": 90,
        "Hyderabad": 85,
        "Chennai": 80,
        "Mumbai": 88,
        "Delhi": 75,
        "Pune": 82,
        "Jaipur": 70
    }
    return city_growth.get(city, 70)  # default value

# ================================
# 📌 AMENITIES SCORE
# ================================
def amenities_score(count):
    return min(count * 10, 100)  # scale amenities

# ================================
# 📌 PROPERTY SCORE (based on BHK + size)
# ================================
def property_score(bhk, size):
    score = 0
    
    # BHK scoring
    if bhk >= 3:
        score += 50
    elif bhk == 2:
        score += 30
    else:
        score += 10
    
    # Size scoring
    if size > 1500:
        score += 50
    elif size > 800:
        score += 30
    else:
        score += 10
    
    return score

# ================================
# 📌 ACCESSIBILITY SCORE
# ================================
def accessibility_score(value):
    return min(value * 5, 100)

# ================================
# 📌 AGE SCORE (newer is better)
# ================================
def age_score(age):
    return max(0, 100 - age * 2)

# ================================
# 📌 FINAL INVESTMENT SCORE
# ================================
def investment_score(price, city, bhk, size, amenities, access, age, city_avg):

    p_score = price_score(price, city, city_avg)
    l_score = location_score(city)
    a_score = amenities_score(amenities)
    pr_score = property_score(bhk, size)
    ac_score = accessibility_score(access)
    ag_score = age_score(age)

    final_score = (
        p_score * 0.30 +
        l_score * 0.20 +
        a_score * 0.15 +
        pr_score * 0.15 +
        ac_score * 0.10 +
        ag_score * 0.10
    )

    return round(final_score, 2)

# ================================
# 📌 CLASSIFICATION
# ================================
def classify(score):
    if score >= 75:
        return "Excellent Investment"
    elif score >= 60:
        return "Good Investment"
    elif score >= 40:
        return "Average Investment"
    else:
        return "Risky Investment"

# ================================
# 📌 FUTURE PRICE PREDICTION
# ================================
def future_price(price, city, score):
    
    growth_rate = {
        "Bangalore": 0.10,
        "Hyderabad": 0.095,
        "Chennai": 0.085,
        "Mumbai": 0.09,
        "Delhi": 0.08,
        "Pune": 0.09
    }
    
    base = growth_rate.get(city, 0.08)
    
    # adjust growth using score
    adjusted_growth = base + (score / 100) * 0.02
    
    future = price * (1 + adjusted_growth) ** 5
    
    return round(future, 2)
