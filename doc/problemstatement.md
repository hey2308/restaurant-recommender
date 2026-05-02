# Problem Statement: AI-Powered Restaurant Recommendation System (Zomato Use Case)

Build an intelligent restaurant recommendation application inspired by Zomato. The system should combine structured restaurant data with a Large Language Model (LLM) to deliver personalized and explainable suggestions based on each user's preferences.

## Objective

Design and implement an application that can:

- Capture user preferences such as location, budget, cuisine, and minimum rating.
- Use a real-world restaurant dataset.
- Generate personalized, human-like recommendations using an LLM.
- Present recommendations in a clear, useful, and user-friendly format.

## System Workflow

### 1) Data Ingestion

- Load and preprocess the Zomato dataset from Hugging Face:  
  [https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation](https://huggingface.co/datasets/ManikaSaini/zomato-restaurant-recommendation)
- Extract relevant fields such as:
  - Restaurant name
  - Location
  - Cuisine
  - Estimated cost
  - Rating
  - Other useful metadata

### 2) User Input Collection

Collect user preferences, including:

- Location (for example, Delhi or Bangalore)
- Budget range (low, medium, high)
- Preferred cuisine (for example, Italian or Chinese)
- Minimum acceptable rating
- Optional preferences (for example, family-friendly, quick service, outdoor seating)

### 3) Integration Layer

- Filter and prepare restaurant records based on user preferences.
- Convert shortlisted results into structured context for the LLM.
- Use a well-designed prompt to help the LLM compare and rank candidates accurately.

### 4) Recommendation Engine

Use the LLM to:

- Rank the best restaurant options.
- Explain why each recommendation matches the user profile.
- Optionally provide a short summary of trade-offs across top choices.

### 5) Output Presentation

Display the top recommendations with:

- Restaurant name
- Cuisine type
- Rating
- Estimated cost
- AI-generated explanation of fit

