# Project Context: AI-Powered Restaurant Recommendation System (Zomato Use Case)

This document establishes the context and outlines the requirements for building an AI-powered restaurant recommendation service inspired by Zomato, as defined in [ProblemStatemen.txt](file:///c:/Users/Rudrankar%20Raha/Documents/NextLeap%20-%20Product%20Management/Zomato%20Project/ProblemStatemen.txt).

---

## 📌 Objective
The primary goal is to design and implement an application that intelligently suggests restaurants based on user preferences by combining structured restaurant data with a Large Language Model (LLM).

The application must:
1. **Capture user preferences** (such as location, budget, cuisine, and ratings).
2. **Utilize a real-world dataset** of restaurants.
3. **Leverage an LLM** to generate personalized, natural-sounding, human-like recommendations.
4. **Display results** clearly and intuitively to the user.

---

## ⚙️ System Workflow

### 1. Data Ingestion
*   **Dataset Source:** [Hugging Face Zomato Restaurant Recommendation Dataset](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation)
*   **Preprocessing:** Load the dataset and extract key structural fields including:
    *   Restaurant Name
    *   Location (city/area)
    *   Cuisine types
    *   Cost details
    *   User ratings
    *   Additional restaurant attributes

### 2. User Input Capture
The system collects the following preferences from the user:
*   📍 **Location:** (e.g., Delhi, Bangalore, etc.)
*   💵 **Budget Category:** (Low, Medium, High)
*   🍲 **Cuisine preference:** (e.g., Italian, Chinese, Indian, etc.)
*   ⭐ **Minimum Rating:** (e.g., 3.5, 4.0, etc.)
*   🔍 **Additional Preferences:** (e.g., family-friendly, quick service, rooftop, ambient seating, etc.)

### 3. Integration Layer
*   Filter the ingested restaurant dataset according to the structured user filters (Location, Budget, Cuisine, Rating).
*   Construct a prompt for the LLM that includes the filtered, structured restaurant listings.
*   The prompt must guide the LLM to perform reasoning and rank the matching options.

### 4. Recommendation Engine
Using the LLM, the engine will:
*   Rank the top matching restaurants.
*   Provide a personalized explanation explaining *why* each restaurant fits the user's specific preferences.
*   Optionally provide a summary of the recommended choices.

### 5. Output Display
Present the final recommendations in a user-friendly format, containing:
*   🏢 **Restaurant Name**
*   🍽️ **Cuisine**
*   ⭐ **Rating**
*   💰 **Estimated Cost**
*   ✍️ **AI-Generated Explanation**

---

## 📄 Original Problem Statement Content
For reference, here is the raw content from `ProblemStatemen.txt`:

```text
Problem Statement: AI-Powered Restaurant Recommendation System (Zomato Use Case) 
You are tasked with building an AI-powered restaurant recommendation service inspired 
by Zomato. The system should intelligently suggest restaurants based on user preferences 
by combining structured data with a Large Language Model (LLM). 
Objective 
Design and implement an application that: 
● Takes user preferences (such as location, budget, cuisine, and ratings) 
● Uses a real-world dataset of restaurants 
● Leverages an LLM to generate personalized, human-like recommendations 
● Displays clear and useful results to the user 
System Workflow 
1. Data Ingestion 
○ Load and preprocess the Zomato dataset from Hugging Face 
(https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommenda
tion ) 
○ Extract relevant fields such as restaurant name, location, cuisine, cost, rating, 
etc. 
2. User Input 
○ Collect user preferences: 
■ Location (e.g., Delhi, Bangalore) 
■ Budget (low, medium, high) 
■ Cuisine (e.g., Italian, Chinese) 
■ Minimum rating 
■ Any additional preferences (e.g., family-friendly, quick service) 
3. Integration Layer 
○ Filter and prepare relevant restaurant data based on user input 
○ Pass structured results into an LLM prompt 
○ Design a prompt that helps the LLM reason and rank options 
4. Recommendation Engine 
○ Use the LLM to: 
■ Rank restaurants 
■ Provide explanations (why each recommendation fits) 
■ Optionally summarize choices 
5. Output Display 
○ Present top recommendations in a user-friendly format: 
■ Restaurant Name 
■ Cuisine 
■ Rating 
■ Estimated Cost 
■ AI-generated explanation
```
