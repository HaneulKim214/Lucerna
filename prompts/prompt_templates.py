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

prompt_company_info = """
You are a value investor with decades of experience. Let's perform a extensive research on {company} to create a report for clients on the buy-side. 
Let's follow steps below:
1. Gather information about the services and products of the {company} and provide statistics.
2. For each service and product, provide information about its market, market share, its major clients (provide company names) and its competitors. 
3. What risks are associated with current company? (e.g. geopolitical risk in semiconductor industry, oil price in transportation induestry, etc...)

As our clients have high mathematical and finance aptitude, provide table and numbers to explain concisely and clearly.
Do not provide code or explanation of how chart should be created.

Please begin your answer with "<company name> Analysis: A Value Investor's Perspective" 
"""
