# Diet Dashboard

## Background
A dashboard that I have been using to track my macronutrient consumption after the end of the second COVID lockdown in Belgium. Specifically created in Dash to practice dashboarding in Python, as my previous similar projects were in R with Shiny.

## Functions
It operates on a simple relational database scheme: meal_types.csv stores the different food types with their macros and meals_consumed.csv stores the amount consumed from each item with a timestamp. For each day the total amcrnutrient consumption is calculated and displayed on a line chart along with the overall mean daily kcal and protein g consumption.

When a new meal is added the app looks for the most similar existing item to help avoid duplicates. If the name is an exact match, the new food type won't be recorded. The dropdown menu for selecting the eaten food item allows for searching, making navigating the large number of possible food items easier.

Besides the Graph tab with chart there is also a Table tab where the nutrient content of previously recorded food types can be inspected.
![image](https://user-images.githubusercontent.com/44137494/125782601-b189d942-0ba6-482c-95ad-2340420e0433.png)
