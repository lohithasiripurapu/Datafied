import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def total_sales(df):
    df['Total_sales'] = df['Quantity_Ordered'] * df['Price_Per_Unit']
        
    return df['Total_sales'].sum()//1

def highest_selling_sku(df):
    sku_sales = df.groupby('SKU')['Quantity_Ordered'].sum()

    return sku_sales.idxmax()

def max_sku_sales(df):
    sku_sales = df.groupby('SKU')['Quantity_Ordered'].sum()
    return sku_sales.max()

def highest_selling_sku_category(df):
    sku =  highest_selling_sku(df)
    return df[df['SKU'] == sku]['Category'].iloc[0]
    
#most money generated category
def category_sales_by_sales(df):
    df['Total_sales'] = df['Quantity_Ordered'] * df['Price_Per_Unit']
    return df.groupby('Category')['Total_sales'].sum()
            
    # sorted_category_sales_by_quantity = category_sales_by_quantity.sort_values(ascending=False)
            
    # sorted_category_sales_by_quantity = list(sorted_category_sales_by_quantity.items())
    
    # return sorted_category_sales_by_quantity

# Highest no of products sold per category
def category_sales_by_units_sold(df):

    # Get total number of products sold per category
    return df.groupby('Category')['Quantity_Ordered'].sum()

    # sorted_category_sales_by_units_sold = category_sales_by_units_sold.sort_values(ascending=False)
            
    # return list(sorted_category_sales_by_units_sold.items())
    
def all_top_sku(df):
    top_sku_per_category = df.groupby('Category').apply(
        lambda x: x.loc[x['Total_Sales'].idxmax(), 'SKU'])
    return top_sku_per_category
    
    

def generate_bar_graph(df, column, output_path):
    """
    Generates a bar graph for a given column in the DataFrame and saves it to output_path.
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' does not exist in the DataFrame.")
    
    # if pd.api.types.is_numeric_dtype(df[column]):
    #     sns.histplot(data=df, x=column, bins=10, kde=True, color='blue')  # Use histplot for numeric data
    # else:
    #     sns.countplot(data=df, x=column, palette='viridis', hue=column, legend=False)  # Use countplot for categorical data
    
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x=column, palette='viridis')
    plt.title(f'Frequency of {column}')
    plt.xticks(rotation=45)
    plt.tight_layout()


    # Save the plot as a PNG image
    plt.savefig(output_path)
    plt.close()
    
    
