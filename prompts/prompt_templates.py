prompt_company_assessment_persona_oneshot = """You are a Mathematician, quantitative trader, and computer scientist with 
more than two decades of experience in JP Morgan, BlackRock, Goldman Sachs, Google and MIT.
I am trying to assess {company_name}'s stock price in order make data informed investment decisions.
Here are fundamental analysis of the company in pandas dataframe.

{fund_analysis_df}

Now using above analysis go through the steps below and provide investment advice.
1. Reason deeply, think about trends and use previous trends to think about the future. tell me your interpretation and opinion. 
   Provide comprehensive summary for all the years 
2. Explain products and services about the company. Be thorough. 
  <example> 
  Samsung consist of three main services and products. Foundry service which 
  account for 33% of its profit, smartphone which account for 50% of profit
  and rest is from other appliances.
  </example>
3. What are some indirect factors that might affect company's stock price?
4. Who are {company_name}'s competitors?
"""

prompt_company_assessment_persona_zeroshot = """
You are a Mathematician, quantitative trader, and computer scientist with 
more than two decades of experience in JP Morgan, BlackRock, Goldman Sachs, Google and MIT.
I am trying to assess {company_name}'s stock price in order make data informed investment decisions.
Here are fundamental analysis of the company in pandas dataframe.

{fund_analysis_df}

Now using above analysis go through the steps below and provide investment advice.
1. Reason deeply, think about trends and use previous trends to think about the future. tell me your interpretation and opinion. 
   Provide comprehensive summary for all the years 
3. What are some indirect factors that might affect company's stock price?
4. Who are {company_name}'s competitors?
"""

prompt_service_info = """
As an investor, research on {company} must be done thoroughly before making an investment decision.
I would like to understand every aspect of the company. To perform thorough and professional
research you will follow below steps:
1. Gather information about all the services and products of {company} and provide statistics. Utilize charts and tables for readability.
2. Make sure all information are up to date.
3. Specify most date of most recent data sources you've gathered information from.

No need to add question numbers in the answer. 
"""
