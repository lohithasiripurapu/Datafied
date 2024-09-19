from flask import request, render_template, redirect, url_for, session
import os
import pandas as pd
from app.services.cleaning_service import clean_data
from app.services.analytics_service import (total_sales, highest_selling_sku, max_sku_sales,
                                             highest_selling_sku_category, category_sales_by_sales,
                                             category_sales_by_units_sold, all_top_sku)

def init_routes(app):
    """Initialize all routes."""
    
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    if not os.path.exists(app.config['PROCESSED_FOLDER']):
        os.makedirs(app.config['PROCESSED_FOLDER'])

    if not os.path.exists('static/images'):
        os.makedirs('static/images')

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            if 'file' not in request.files:
                return 'No file part'
            file = request.files['file']
            if file.filename == '':
                return 'No file selected'
            if file:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
                file.save(filepath)
                
                cleaned_filepath = clean_data(filepath, app.config['PROCESSED_FOLDER'])
                cleaned_df = pd.read_csv(cleaned_filepath)
                cleaned_df['Total_Sales'] = cleaned_df['Quantity_Ordered'] * cleaned_df['Price_Per_Unit']
                
                category_sales = category_sales_by_units_sold(cleaned_df)
                
                category_metrics = []
                for category in category_sales.index:
                    category_metrics.append((category,
                        float(category_sales_by_sales(cleaned_df)[category]),  # Convert to float
                        float(category_sales[category]),  # Convert to float
                        all_top_sku(cleaned_df)[category]
                    ))
                
                category_metrics = sorted(category_metrics, key=lambda x: x[1], reverse=True)
                
                # Store data in session or temporary storage
                session['total_sales'] = float(total_sales(cleaned_df))  # Convert to float
                session['max_sku_sales'] = float(max_sku_sales(cleaned_df))  # Convert to float
                session['high_selling_sku'] = highest_selling_sku(cleaned_df)
                session['high_selling_sku_category'] = highest_selling_sku_category(cleaned_df)
                session['category_metrics'] = category_metrics

                return redirect(url_for('index'))
        
        # Retrieve data from session
        total_sales_data = session.get('total_sales', None)
        max_sku_sales_data = session.get('max_sku_sales', None)
        high_selling_sku = session.get('high_selling_sku', None)
        high_selling_sku_category = session.get('high_selling_sku_category', None)
        category_metrics = session.get('category_metrics', None)

        return render_template('index.html',
                            total_sales=total_sales_data,
                            max_sku_sales=max_sku_sales_data,
                            high_selling_sku=high_selling_sku,
                            high_selling_sku_category=high_selling_sku_category,
                            category_metrics=category_metrics)