import requests
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt

def get_india_economic_data():
    """Get India's economic data from World Bank API"""
    
    # Working indicators for India
    indicators = {
        'NY.GDP.MKTP.CD': 'GDP_USD_billions',
        'NY.GDP.PCAP.PP.KD': 'GDP_per_capita_PPP',
        'NY.GDP.MKTP.KD.ZG': 'GDP_growth_percent',
        'SP.POP.TOTL': 'Population_millions',
        'NV.AGR.TOTL.ZS': 'agriculture value added(%GDP)',
        'NV.IND.TOTL.ZS': 'Industry value added(% GDP)',
        'NV.SRV.TOTL.ZS':'service_value_added(% GDP)'
    }
    
    result = {}
    
    for code, name in indicators.items():
        url = f"http://api.worldbank.org/v2/country/IND/indicator/{code}"
        params = {'format': 'json', 'per_page': 100}
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if len(data) > 1 and data[1]:
                years = {}
                for item in data[1]:
                    if item['value']:
                        year = int(item['date'])
                        value = float(item['value'])
                        years[year] = value
                
                # Convert billions for GDP
                if name == 'GDP_USD_billions':
                    years = {k: v/1e9 for k, v in years.items()}
                # Convert to millions for population
                elif name == 'Population_millions':
                    years = {k: v/1e6 for k, v in years.items()}
                
                result[name] = years
    
    # Create DataFrame
    df = pd.DataFrame(result).sort_index()
    return df

# Fetch the data
print("Fetching India data from World Bank...")
india_df = get_india_economic_data()

print("\n" + "="*60)
print("INDIA ECONOMIC DATA (2015-2023)")
print("="*60)
print(india_df.tail(10))


# Create a simple chart
fig, axes = plt.subplots(3, 3, figsize=(12, 8))

# GDP Chart
axes[0, 0].plot(india_df.index, india_df['GDP_USD_billions'], 'b-', linewidth=2)
axes[0, 0].set_title('India GDP (Current US$ Billions)')
axes[0, 0].set_xlabel('Year')
axes[0, 0].set_ylabel('Billions USD')
axes[0, 0].grid(True, alpha=0.3)

# GDP Growth Chart
axes[0, 1].plot(india_df.index, india_df['GDP_growth_percent'], 'g-', linewidth=2)
axes[0, 1].axhline(y=0, color='black', linestyle='-', linewidth=0.5)
axes[0, 1].set_title('India GDP Growth Rate (%)')
axes[0, 1].set_xlabel('Year')
axes[0, 1].set_ylabel('Growth %')
axes[0, 1].grid(True, alpha=0.3)

# GDP per Capita Chart
axes[1, 0].plot(india_df.index, india_df['GDP_per_capita_PPP'], 'purple', linewidth=2)
axes[1, 0].set_title('India GDP per Capita (PPP, Constant 2017 $)')
axes[1, 0].set_xlabel('Year')
axes[1, 0].set_ylabel('USD (PPP)')
axes[1, 0].grid(True, alpha=0.3)

# Population Chart
axes[1, 1].plot(india_df.index, india_df['Population_millions'], 'orange', linewidth=2)
axes[1, 1].set_title('India Population (Millions)')
axes[1, 1].set_xlabel('Year')
axes[1, 1].set_ylabel('Population (Millions)')
axes[1, 1].grid(True, alpha=0.3)

# agriculture vs gdp growth
axes[0, 2].scatter(india_df['GDP_growth_percent'], india_df['agriculture value added(%GDP)'], color = 'red')
axes[0, 2].set_title('agr vs gdp growth')
axes[0, 2].set_xlabel('gdp growth percentage')
axes[0, 2].set_ylabel('agriculture value added')
axes[0, 2].grid(True, alpha=0.3)

#industry vs gdp growth
axes[1, 2].scatter(india_df['GDP_growth_percent'], india_df['Industry value added(% GDP)'], color = 'pink')
axes[1, 2].set_title('industry vs gdp growth')
axes[1, 2].set_xlabel('gdp growth percentage')
axes[1, 2].set_ylabel('Industry value added(% GDP)')
axes[1, 2].grid(True, alpha=0.3)

# service_value_added(% GDP) vs gdp growth
axes[2, 2].scatter(india_df['GDP_growth_percent'], india_df['service_value_added(% GDP)'], color = 'yellow')
axes[2, 2].set_title('service industry vs gdp growth')
axes[2, 2].set_xlabel('gdp growth percentage')
axes[2, 2].set_ylabel('service (% GDP)')
axes[2, 2].grid(True, alpha=0.3)

axes[2,0].remove()
axes[2,1].remove()

#correlation analysis of gdp with industry agr serv
correlations = {
    'Agriculture': india_df['agriculture value added(%GDP)'].corr(india_df['GDP_growth_percent']),
    'Industry': india_df['Industry value added(% GDP)'].corr(india_df['GDP_growth_percent']),
    'Services': india_df['service_value_added(% GDP)'].corr(india_df['GDP_growth_percent'])
}

print("Correlation with GDP Growth:")
for sector, corr in correlations.items():
    print(f"  {sector}: {corr:.3f}")



plt.tight_layout()
plt.savefig('india_economic_charts.png', dpi=150)
plt.show()

print("\n✓ Charts saved to 'india_economic_charts.png'")
print("✓ Data saved in 'india_df' variable")
