from flask import Flask, render_template
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# Your data preparation function
def prepare_data():
    # Sample data
    data = {
        "Product/Platform/Ops Team": [
            "Analysis Platform", "Analysis Platform", "Analysis Platform", "Analysis Platform",
            "Data Platform", "Data Platform", "Data Platform", "Data Platform"
        ],
        "Contribution Area": [
            "Management", "Overhead", "Oya Platform new feature dev", "Oya Platform tech debt",
            "3rd party data quality + infra", "Data Platform management", "Data Platform tech debt", "New country data onboarding"
        ],
        "monthly_spend": [
            2440.0, 7050.15, 15302.5, 9897.97,
            32772.5785, 8656.665, 11154.1035, 3198.333
        ]
    }
    
    df = pd.DataFrame(data)
    return df

# Plotly figure creation function
def create_plot():
    df = prepare_data()
    grouped_data = df.groupby(['Product/Platform/Ops Team', 'Contribution Area']).sum().reset_index()
    fig = px.bar(grouped_data, x='Product/Platform/Ops Team', y='monthly_spend',
                 color='Contribution Area', title='Monthly Spend Breakdown by Product/Platform/Ops Team',
                 labels={'monthly_spend': 'Monthly Spend', 'Product/Platform/Ops Team': 'Product/Platform/Ops Team'},
                 text='monthly_spend')
    fig.update_layout(xaxis_title='Product/Platform/Ops Team', yaxis_title='Monthly Spend',
                      barmode='stack', xaxis={'categoryorder':'total descending'},
                      legend_title='Contribution Area')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='inside')
    return fig

@app.route('/')
def index():
    fig = create_plot()
    div = pio.to_html(fig, full_html=False)
    return render_template("index.html", plot_div=div)

if __name__ == '__main__':
    app.run(debug=True)
