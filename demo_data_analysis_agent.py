#!/usr/bin/env python3
"""
Grok4 Data Analysis Agent
Advanced tool use demo for data processing and analysis
"""

import os
import json
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI
from typing import Dict, List, Any
import sqlite3
from datetime import datetime, timedelta

load_dotenv()

class DataAnalysisAgent:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("XAI_API_KEY"),
            base_url="https://api.x.ai/v1"
        )
        self.setup_database()
    
    def setup_database(self):
        """Create sample database for analysis"""
        self.conn = sqlite3.connect(':memory:')
        
        # Create sample sales data
        dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')
        sales_data = []
        
        for date in dates:
            sales_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'revenue': np.random.normal(10000, 2000),
                'units_sold': np.random.poisson(100),
                'region': np.random.choice(['North', 'South', 'East', 'West']),
                'product_category': np.random.choice(['Electronics', 'Clothing', 'Books', 'Home'])
            })
        
        df = pd.DataFrame(sales_data)
        df.to_sql('sales', self.conn, index=False)
    
    def query_database(self, sql_query: str) -> Dict[str, Any]:
        """Execute SQL query and return results"""
        try:
            df = pd.read_sql_query(sql_query, self.conn)
            return {
                "success": True,
                "data": df.to_dict('records'),
                "row_count": len(df),
                "columns": list(df.columns)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def calculate_statistics(self, column: str, operation: str) -> Dict[str, Any]:
        """Calculate statistical measures on data"""
        try:
            df = pd.read_sql_query(f"SELECT {column} FROM sales", self.conn)
            data = df[column]
            
            operations = {
                'mean': data.mean(),
                'median': data.median(),
                'std': data.std(),
                'min': data.min(),
                'max': data.max(),
                'sum': data.sum(),
                'count': data.count()
            }
            
            if operation.lower() in operations:
                result = operations[operation.lower()]
                return {
                    "success": True,
                    "column": column,
                    "operation": operation,
                    "result": float(result) if pd.notna(result) else None
                }
            else:
                return {
                    "success": False,
                    "error": f"Unknown operation: {operation}"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def generate_report(self, report_type: str, filters: Dict = None) -> Dict[str, Any]:
        """Generate analytical reports"""
        try:
            base_query = "SELECT * FROM sales"
            
            if filters:
                conditions = []
                for key, value in filters.items():
                    if isinstance(value, str):
                        conditions.append(f"{key} = '{value}'")
                    else:
                        conditions.append(f"{key} = {value}")
                
                if conditions:
                    base_query += " WHERE " + " AND ".join(conditions)
            
            df = pd.read_sql_query(base_query, self.conn)
            
            if report_type == "summary":
                report = {
                    "total_revenue": df['revenue'].sum(),
                    "total_units": df['units_sold'].sum(),
                    "avg_revenue_per_day": df['revenue'].mean(),
                    "top_region": df.groupby('region')['revenue'].sum().idxmax(),
                    "top_category": df.groupby('product_category')['revenue'].sum().idxmax(),
                    "date_range": f"{df['date'].min()} to {df['date'].max()}"
                }
            elif report_type == "trends":
                df['date'] = pd.to_datetime(df['date'])
                monthly = df.groupby(df['date'].dt.to_period('M')).agg({
                    'revenue': 'sum',
                    'units_sold': 'sum'
                }).reset_index()
                
                report = {
                    "monthly_trends": monthly.to_dict('records'),
                    "growth_rate": ((monthly['revenue'].iloc[-1] - monthly['revenue'].iloc[0]) / monthly['revenue'].iloc[0] * 100)
                }
            else:
                return {"success": False, "error": f"Unknown report type: {report_type}"}
            
            return {
                "success": True,
                "report_type": report_type,
                "data": report,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_tools_definition(self):
        """Define tools for Grok4 function calling"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "query_database",
                    "description": "Execute SQL queries on the sales database",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "sql_query": {
                                "type": "string",
                                "description": "SQL query to execute"
                            }
                        },
                        "required": ["sql_query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "calculate_statistics",
                    "description": "Calculate statistical measures on data columns",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "column": {
                                "type": "string",
                                "description": "Column name to analyze"
                            },
                            "operation": {
                                "type": "string",
                                "enum": ["mean", "median", "std", "min", "max", "sum", "count"],
                                "description": "Statistical operation to perform"
                            }
                        },
                        "required": ["column", "operation"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "generate_report",
                    "description": "Generate analytical reports",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "report_type": {
                                "type": "string",
                                "enum": ["summary", "trends"],
                                "description": "Type of report to generate"
                            },
                            "filters": {
                                "type": "object",
                                "description": "Optional filters to apply"
                            }
                        },
                        "required": ["report_type"]
                    }
                }
            }
        ]
    
    def run_analysis(self, user_query: str):
        """Run analysis using Grok4 with tool calling"""
        tools = self.get_tools_definition()
        
        messages = [
            {
                "role": "system",
                "content": "You are a data analysis expert. Use the available tools to analyze sales data and provide insights. The database contains columns: date, revenue, units_sold, region, product_category."
            },
            {
                "role": "user",
                "content": user_query
            }
        ]
        
        response = self.client.chat.completions.create(
            model="grok-4",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        # Handle tool calls
        if response.choices[0].message.tool_calls:
            messages.append(response.choices[0].message)
            
            for tool_call in response.choices[0].message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                # Execute the function
                if function_name == "query_database":
                    result = self.query_database(**function_args)
                elif function_name == "calculate_statistics":
                    result = self.calculate_statistics(**function_args)
                elif function_name == "generate_report":
                    result = self.generate_report(**function_args)
                else:
                    result = {"error": f"Unknown function: {function_name}"}
                
                messages.append({
                    "role": "tool",
                    "content": json.dumps(result),
                    "tool_call_id": tool_call.id
                })
            
            # Get final response
            final_response = self.client.chat.completions.create(
                model="grok-4",
                messages=messages,
                tools=tools
            )
            
            return final_response.choices[0].message.content
        else:
            return response.choices[0].message.content

def main():
    agent = DataAnalysisAgent()
    
    print("Grok4 Data Analysis Agent")
    print("=" * 50)
    
    sample_queries = [
        "What is the total revenue for the year?",
        "Which region has the highest sales?",
        "Show me monthly revenue trends",
        "Calculate the average daily revenue",
        "Generate a summary report for Electronics category"
    ]
    
    print("Sample queries:")
    for i, query in enumerate(sample_queries, 1):
        print(f"{i}. {query}")
    
    print("\nEnter your analysis request (or 'quit' to exit):")
    
    while True:
        user_input = input("\nQuery: ")
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        
        try:
            result = agent.run_analysis(user_input)
            print(f"\nAnalysis Result:\n{result}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
