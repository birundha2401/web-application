import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap

os.makedirs("assets", exist_ok=True)
os.makedirs("data", exist_ok=True)

# ----------------- EXPERIMENT 5: TABLEAU DATASET & VISUALS -----------------
print("Creating Exp 5: Tableau Dataset and Visuals")
regions = ['North', 'South', 'East', 'West', 'Central']
categories = ['Technology', 'Office Supplies', 'Furniture']
ship_modes = ['Standard Class', 'Second Class', 'First Class', 'Same Day']

np.random.seed(55)
n_orders = 1000
sales = np.random.exponential(scale=250, size=n_orders) + 20
discounts = np.random.choice([0.0, 0.1, 0.2, 0.3, 0.4, 0.5], size=n_orders, p=[0.4, 0.2, 0.15, 0.1, 0.1, 0.05])
profits = sales * (0.35 - discounts) + np.random.normal(0, 15, size=n_orders)

tableau_df = pd.DataFrame({
    'Order_ID': [f'CA-2024-{10000+i}' for i in range(n_orders)],
    'Region': np.random.choice(regions, n_orders),
    'Category': np.random.choice(categories, n_orders),
    'Sales': np.round(sales, 2),
    'Discount': discounts,
    'Profit': np.round(profits, 2),
    'Ship_Mode': np.random.choice(ship_modes, n_orders),
    'High_Profit_Margin': np.where(profits > 50, 'High Profit', 'Standard/Loss')
})
tableau_df.to_csv("data/e_commerce_orders.csv", index=False)

# Chart 1: Total Sales by Region (Tableau Style Bar)
plt.figure(figsize=(6.5, 3.8))
reg_sales = tableau_df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
plt.barh(reg_sales.index, reg_sales.values, color='#4e79a7', edgecolor='#2c4969')
plt.title("Total Sales by Region", fontsize=11, fontweight='bold', pad=10)
plt.xlabel("Sum of Sales ($)")
plt.ylabel("Region")
plt.grid(axis='x', linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig("assets/exp5_tableau_chart1.png", dpi=200)
plt.close()

# Chart 2: Profit vs Discount Trend Line
plt.figure(figsize=(6.5, 3.8))
disc_profit = tableau_df.groupby('Discount')['Profit'].mean().reset_index()
plt.plot(disc_profit['Discount'], disc_profit['Profit'], marker='o', color='#f28e2b', linewidth=2.5)
plt.title("Average Profit vs Discount Trend", fontsize=11, fontweight='bold', pad=10)
plt.xlabel("Discount Rate")
plt.ylabel("Average Profit ($)")
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig("assets/exp5_tableau_chart2.png", dpi=200)
plt.close()

# Chart 3: Discount vs Profit Scatter Plot
plt.figure(figsize=(6.5, 3.8))
plt.scatter(tableau_df['Discount'], tableau_df['Profit'], alpha=0.5, c='#e15759', edgecolors='none', s=35)
plt.axhline(0, color='gray', linestyle='--', linewidth=1)
plt.title("Discount vs Profit Analysis", fontsize=11, fontweight='bold', pad=10)
plt.xlabel("Discount")
plt.ylabel("Profit ($)")
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig("assets/exp5_tableau_chart3.png", dpi=200)
plt.close()

# Chart 4: Count by Profit Margin Category
plt.figure(figsize=(6.5, 3.8))
margin_counts = tableau_df['High_Profit_Margin'].value_counts()
plt.bar(margin_counts.index, margin_counts.values, color=['#59a14f', '#edc948'], edgecolor='#333333', width=0.5)
plt.title("Number of Records by Profit Margin", fontsize=11, fontweight='bold', pad=10)
plt.xlabel("Profit Margin Classification")
plt.ylabel("Number of Records")
for i, v in enumerate(margin_counts.values):
    plt.text(i, v + 15, str(v), ha='center', fontweight='bold', fontsize=9)
plt.grid(axis='y', linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig("assets/exp5_tableau_chart4.png", dpi=200)
plt.close()

# Chart 5: Sales Distribution Bins
plt.figure(figsize=(6.5, 3.8))
plt.hist(tableau_df['Sales'], bins=20, color='#76b7b2', edgecolor='#2c5c57')
plt.title("Sales Distribution (Frequency)", fontsize=11, fontweight='bold', pad=10)
plt.xlabel("Sales Amount ($)")
plt.ylabel("Count of Records")
plt.grid(True, linestyle=':', alpha=0.6)
plt.tight_layout()
plt.savefig("assets/exp5_tableau_chart5.png", dpi=200)
plt.close()

# Chart 6: Tableau Dashboard Composite View
fig, axs = plt.subplots(2, 2, figsize=(8.5, 5.5))
fig.suptitle("E-Commerce Performance Dashboard - Tableau Overview", fontsize=13, fontweight='bold', y=0.98)
# Top-left: Bar
axs[0, 0].barh(reg_sales.index, reg_sales.values, color='#4e79a7')
axs[0, 0].set_title("Total Sales by Region", fontsize=9, fontweight='bold')
axs[0, 0].grid(axis='x', linestyle=':', alpha=0.5)
# Top-right: Trend
axs[0, 1].plot(disc_profit['Discount'], disc_profit['Profit'], marker='s', color='#f28e2b')
axs[0, 1].set_title("Avg Profit vs Discount", fontsize=9, fontweight='bold')
axs[0, 1].grid(True, linestyle=':', alpha=0.5)
# Bottom-left: Margin counts
axs[1, 0].bar(margin_counts.index, margin_counts.values, color=['#59a14f', '#edc948'], width=0.45)
axs[1, 0].set_title("Order Count by Margin Status", fontsize=9, fontweight='bold')
axs[1, 0].grid(axis='y', linestyle=':', alpha=0.5)
# Bottom-right: Scatter
axs[1, 1].scatter(tableau_df['Discount'][:200], tableau_df['Profit'][:200], color='#e15759', alpha=0.6, s=25)
axs[1, 1].set_title("Discount vs Profit Sample", fontsize=9, fontweight='bold')
axs[1, 1].grid(True, linestyle=':', alpha=0.5)
plt.tight_layout()
plt.savefig("assets/exp5_tableau_dashboard.png", dpi=200)
plt.close()

# ----------------- EXPERIMENT 6: POWER BI DATASET & VISUALS -----------------
print("Creating Exp 6: Power BI Dataset and Visuals")
countries = ['Norway', 'Denmark', 'Germany', 'United Kingdom', 'Canada', 
             'France', 'Australia', 'Japan', 'United States', 'India', 'Brazil', 'South Africa']
np.random.seed(88)
renewable_share = [71.5, 68.2, 52.4, 46.8, 65.1, 28.4, 32.5, 22.1, 24.8, 21.4, 83.2, 11.5]
co2_per_capita = [6.7, 4.9, 8.1, 4.8, 14.2, 4.2, 15.1, 8.5, 14.8, 1.9, 2.1, 7.3]
energy_transition_idx = [82.4, 79.1, 71.5, 69.8, 70.2, 65.4, 62.1, 59.8, 61.3, 53.2, 66.5, 45.1]
grid_reliability = [98.5, 99.1, 97.4, 96.8, 97.9, 98.2, 95.4, 99.4, 96.1, 89.2, 91.5, 78.4]

powerbi_df = pd.DataFrame({
    'Country': countries,
    'Renewable_Share_Pct': renewable_share,
    'CO2_Emissions_Per_Capita': co2_per_capita,
    'Energy_Transition_Index': energy_transition_idx,
    'Grid_Reliability_Score': grid_reliability
})
powerbi_df.to_csv("data/energy_transition_2024.csv", index=False)

# Render Power BI Visuals Composite & Individual
fig = plt.figure(figsize=(9, 6), facecolor='#f3f2f1')
# Card 1: Metric KPI Card
ax1 = plt.subplot2grid((3, 3), (0, 0), facecolor='white')
ax1.text(0.5, 0.6, f"{np.mean(renewable_share):.1f}%", fontsize=22, fontweight='bold', ha='center', va='center', color='#0078d4')
ax1.text(0.5, 0.25, "Average Renewable Share", fontsize=8.5, ha='center', va='center', color='#605e5c')
ax1.axis('off')

# Card 2: Avg Transition Index KPI Card
ax2 = plt.subplot2grid((3, 3), (0, 1), facecolor='white')
ax2.text(0.5, 0.6, f"{np.mean(energy_transition_idx):.1f}", fontsize=22, fontweight='bold', ha='center', va='center', color='#107c41')
ax2.text(0.5, 0.25, "Avg Energy Transition Index", fontsize=8.5, ha='center', va='center', color='#605e5c')
ax2.axis('off')

# Slicer Box representation
ax_s = plt.subplot2grid((3, 3), (0, 2), facecolor='white')
ax_s.text(0.5, 0.75, "Country Slicer (All Selected)", fontsize=8.5, fontweight='bold', ha='center', va='center', color='#323130')
ax_s.text(0.5, 0.4, "12 Countries Evaluated\nYear: 2024", fontsize=8, ha='center', va='center', color='#605e5c')
ax_s.axis('off')

# Bar Chart: Renewable Share by Country
ax3 = plt.subplot2grid((3, 3), (1, 0), colspan=2, facecolor='white')
sorted_df = powerbi_df.sort_values('Renewable_Share_Pct', ascending=True)
ax3.barh(sorted_df['Country'], sorted_df['Renewable_Share_Pct'], color='#0078d4')
ax3.set_title("Renewable Energy Share (%) by Country", fontsize=9, fontweight='bold')
ax3.grid(axis='x', linestyle=':', alpha=0.5)
ax3.tick_params(labelsize=7.5)

# Column Chart: CO2 Emissions Per Capita
ax4 = plt.subplot2grid((3, 3), (1, 2), facecolor='white')
ax4.bar(range(len(countries)), co2_per_capita, color='#d83b01')
ax4.set_title("CO2 / Capita", fontsize=9, fontweight='bold')
ax4.set_xticks(range(len(countries)))
ax4.set_xticklabels([c[:3] for c in countries], rotation=90, fontsize=7)
ax4.grid(axis='y', linestyle=':', alpha=0.5)

# Scatter: Renewable Share vs CO2 Emissions
ax5 = plt.subplot2grid((3, 3), (2, 0), colspan=2, facecolor='white')
ax5.scatter(powerbi_df['Renewable_Share_Pct'], powerbi_df['CO2_Emissions_Per_Capita'], color='#5c2d91', s=50)
for i, c in enumerate(countries):
    ax5.annotate(c, (powerbi_df['Renewable_Share_Pct'][i]+1, powerbi_df['CO2_Emissions_Per_Capita'][i]), fontsize=6.5)
ax5.set_title("Renewable Share (%) vs CO2 Emissions Per Capita", fontsize=9, fontweight='bold')
ax5.set_xlabel("Renewable Share (%)", fontsize=7.5)
ax5.set_ylabel("CO2 / Capita (Tons)", fontsize=7.5)
ax5.grid(True, linestyle=':', alpha=0.5)

# Column Chart: Energy Transition Index
ax6 = plt.subplot2grid((3, 3), (2, 2), facecolor='white')
ax6.bar(range(len(countries)), energy_transition_idx, color='#107c41')
ax6.set_title("Transition Index", fontsize=9, fontweight='bold')
ax6.set_xticks(range(len(countries)))
ax6.set_xticklabels([c[:3] for c in countries], rotation=90, fontsize=7)
ax6.grid(axis='y', linestyle=':', alpha=0.5)

plt.tight_layout()
plt.savefig("assets/exp6_powerbi_dashboard.png", dpi=200)
plt.close()

# ----------------- EXPERIMENT 7: GEOSPATIAL EDA USING FOLIUM -----------------
print("Creating Exp 7: Folium Dataset and Maps")
# Dataset: Significant World Volcanoes / Seismicity
volcano_data = [
    {"name": "Eyjafjallajökull", "country": "Iceland", "latitude": 63.63, "longitude": -19.62, "elevation": 1666, "vei": 4},
    {"name": "Mount Fuji", "country": "Japan", "latitude": 35.36, "longitude": 138.73, "elevation": 3776, "vei": 5},
    {"name": "Mount Vesuvius", "country": "Italy", "latitude": 40.82, "longitude": 14.43, "elevation": 1281, "vei": 5},
    {"name": "Krakatoa", "country": "Indonesia", "latitude": -6.10, "longitude": 105.42, "elevation": 813, "vei": 6},
    {"name": "Mount St. Helens", "country": "United States", "latitude": 46.20, "longitude": -122.19, "elevation": 2549, "vei": 5},
    {"name": "Mount Pinatubo", "country": "Philippines", "latitude": 15.13, "longitude": 120.35, "elevation": 1486, "vei": 6},
    {"name": "Cotopaxi", "country": "Ecuador", "latitude": -0.68, "longitude": -78.44, "elevation": 5897, "vei": 4},
    {"name": "Mauna Loa", "country": "United States", "latitude": 19.47, "longitude": -155.61, "elevation": 4169, "vei": 3},
    {"name": "Mount Etna", "country": "Italy", "latitude": 37.75, "longitude": 14.99, "elevation": 3357, "vei": 3},
    {"name": "Popocatépetl", "country": "Mexico", "latitude": 19.02, "longitude": -98.62, "elevation": 5426, "vei": 4},
    {"name": "Tambora", "country": "Indonesia", "latitude": -8.25, "longitude": 118.00, "elevation": 2850, "vei": 7},
    {"name": "Mount Merapi", "country": "Indonesia", "latitude": -7.54, "longitude": 110.44, "elevation": 2930, "vei": 4},
    {"name": "Kilauea", "country": "United States", "latitude": 19.42, "longitude": -155.29, "elevation": 1247, "vei": 3},
    {"name": "Sakurajima", "country": "Japan", "latitude": 31.59, "longitude": 130.66, "elevation": 1117, "vei": 4},
    {"name": "Santorini", "country": "Greece", "latitude": 36.40, "longitude": 25.40, "elevation": 367, "vei": 7}
]
volcano_df = pd.DataFrame(volcano_data)
volcano_df.to_csv("data/world_volcanoes.csv", index=False)

# Map 1: Circle Marker Map
v_map = folium.Map(location=[20, 10], zoom_start=2)
for _, r in volcano_df.iterrows():
    folium.CircleMarker(
        location=[r['latitude'], r['longitude']],
        radius=6,
        popup=f"<b>{r['name']}</b><br>Elevation: {r['elevation']} m<br>Country: {r['country']}",
        tooltip=r['name'],
        color='blue',
        fill=True,
        fill_opacity=0.7
    ).add_to(v_map)
v_map.save("data/volcano_marker_map.html")

# Map 2: Bubble / Hotspot Map
bubble_map = folium.Map(location=[20, 10], zoom_start=2)
for _, r in volcano_df.iterrows():
    folium.CircleMarker(
        location=[r['latitude'], r['longitude']],
        radius=r['vei'] * 3,
        popup=f"<b>{r['name']}</b><br>VEI: {r['vei']}",
        tooltip=f"{r['name']} (VEI: {r['vei']})",
        color='crimson',
        fill=True,
        fill_color='red',
        fill_opacity=0.6
    ).add_to(bubble_map)
bubble_map.save("data/volcano_bubble_map.html")

# Map 3: Heatmap
heat_map = folium.Map(location=[20, 10], zoom_start=2)
heat_data = [[r['latitude'], r['longitude'], r['vei']] for _, r in volcano_df.iterrows()]
HeatMap(heat_data, radius=18, blur=12, min_opacity=0.4).add_to(heat_map)
heat_map.save("data/volcano_heatmap.html")

# Map 4: Country Distribution
country_counts = volcano_df['country'].value_counts().reset_index()
country_counts.columns = ['country', 'volcano_count']
country_counts.to_csv("data/volcano_country_counts.csv", index=False)

# Generate visual previews of maps for the PDF
# Marker Map preview
fig, ax = plt.subplots(figsize=(8, 4.2), facecolor='#e6f2ff')
ax.set_facecolor('#dbeef3')
# Draw rough world boundaries / dots for representation
ax.scatter(volcano_df['longitude'], volcano_df['latitude'], color='#1f77b4', s=60, edgecolors='black', zorder=5)
for _, r in volcano_df.iterrows():
    ax.annotate(r['name'], (r['longitude']+2, r['latitude']), fontsize=7, color='#003366')
ax.set_xlim(-180, 180)
ax.set_ylim(-60, 80)
ax.set_title("Folium Interactive Circle Marker Map: Global Active Volcanoes", fontsize=10, fontweight='bold')
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.grid(True, linestyle=':', alpha=0.5)
plt.tight_layout()
plt.savefig("assets/exp7_marker_map.png", dpi=200)
plt.close()

# Bubble Map preview
fig, ax = plt.subplots(figsize=(8, 4.2), facecolor='#fceeed')
ax.set_facecolor('#fff5f5')
sizes = volcano_df['vei'] ** 3 * 2.5
ax.scatter(volcano_df['longitude'], volcano_df['latitude'], s=sizes, color='#d62728', alpha=0.6, edgecolors='#7f0000', zorder=5)
for _, r in volcano_df.iterrows():
    ax.annotate(f"{r['name']} (VEI {r['vei']})", (r['longitude']+2, r['latitude']), fontsize=6.8, color='#800000')
ax.set_xlim(-180, 180)
ax.set_ylim(-60, 80)
ax.set_title("Folium Bubble Map: Volcanic Explosivity Index (VEI Magnitude)", fontsize=10, fontweight='bold')
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.grid(True, linestyle=':', alpha=0.5)
plt.tight_layout()
plt.savefig("assets/exp7_bubble_map.png", dpi=200)
plt.close()

# Heatmap preview
fig, ax = plt.subplots(figsize=(8, 4.2), facecolor='#fcf8e3')
ax.set_facecolor('#faf8f0')
sns.kdeplot(x=volcano_df['longitude'], y=volcano_df['latitude'], cmap="YlOrRd", fill=True, alpha=0.7, bw_adjust=0.5, ax=ax)
ax.scatter(volcano_df['longitude'], volcano_df['latitude'], color='black', s=15, alpha=0.6)
ax.set_xlim(-180, 180)
ax.set_ylim(-60, 80)
ax.set_title("Folium Volcanic Heatmap: Density and Activity Concentration", fontsize=10, fontweight='bold')
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.grid(True, linestyle=':', alpha=0.5)
plt.tight_layout()
plt.savefig("assets/exp7_heatmap.png", dpi=200)
plt.close()

# Choropleth / Regional Count preview
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.bar(country_counts['country'], country_counts['volcano_count'], color='#e67e22', edgecolor='black')
ax.set_title("Choropleth Distribution: Active Volcanoes by Country", fontsize=10, fontweight='bold')
ax.set_xlabel("Country")
ax.set_ylabel("Count of Volcanoes")
ax.tick_params(axis='x', rotation=30, labelsize=8)
ax.grid(axis='y', linestyle=':', alpha=0.5)
plt.tight_layout()
plt.savefig("assets/exp7_choropleth_bar.png", dpi=200)
plt.close()

# ----------------- EXPERIMENT 8: D3.JS DATASET & VISUALS -----------------
print("Creating Exp 8: D3.js Dataset, HTML and Visuals")
d3_df = pd.DataFrame({
    'Category': ['Cloud Computing', 'Data Analytics', 'Cybersecurity', 'Web Systems', 'Artificial Intelligence'],
    'Project_Count': [48, 62, 35, 74, 91]
})
d3_df.to_csv("data/d3_projects_data.csv", index=False)

# Create index.html for Exp 8
html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>D3.js Projects Visualization Bar Chart</title>
    <!-- D3.js Version 7 -->
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: #fafafa;
        }
        h1 {
            color: #2c3e50;
            margin-top: 30px;
            margin-bottom: 20px;
        }
        .bar {
            fill: #3498db;
            transition: fill 0.2s ease;
        }
        .bar:hover {
            fill: #e67e22;
        }
        .value {
            font-size: 13px;
            font-weight: bold;
            fill: #2c3e50;
        }
        .axis-label {
            font-size: 14px;
            font-weight: bold;
            fill: #34495e;
        }
        .axis text {
            font-size: 12px;
        }
    </style>
</head>
<body>
    <h1>Technology Domains - Number of Completed Projects</h1>
    <svg width="720" height="480"></svg>
    <script>
        const svg = d3.select("svg");
        const width = 720;
        const height = 480;
        const margin = { top: 40, right: 30, bottom: 80, left: 70 };

        d3.csv("data/d3_projects_data.csv").then(function(data) {
            data.forEach(function(d) {
                d.Project_Count = +d.Project_Count;
            });

            const x = d3.scaleBand()
                .domain(data.map(d => d.Category))
                .range([margin.left, width - margin.right])
                .padding(0.35);

            const y = d3.scaleLinear()
                .domain([0, d3.max(data, d => d.Project_Count) * 1.15])
                .nice()
                .range([height - margin.bottom, margin.top]);

            svg.append("g")
                .attr("class", "axis")
                .attr("transform", `translate(0, ${height - margin.bottom})`)
                .call(d3.axisBottom(x))
                .selectAll("text")
                .style("text-anchor", "middle");

            svg.append("g")
                .attr("class", "axis")
                .attr("transform", `translate(${margin.left}, 0)`)
                .call(d3.axisLeft(y));

            svg.selectAll(".bar")
                .data(data)
                .enter()
                .append("rect")
                .attr("class", "bar")
                .attr("x", d => x(d.Category))
                .attr("y", d => y(d.Project_Count))
                .attr("width", x.bandwidth())
                .attr("height", d => (height - margin.bottom) - y(d.Project_Count));

            svg.selectAll(".value")
                .data(data)
                .enter()
                .append("text")
                .attr("class", "value")
                .attr("x", d => x(d.Category) + x.bandwidth() / 2)
                .attr("y", d => y(d.Project_Count) - 8)
                .attr("text-anchor", "middle")
                .text(d => d.Project_Count);

            svg.append("text")
                .attr("class", "axis-label")
                .attr("x", width / 2)
                .attr("y", height - 20)
                .attr("text-anchor", "middle")
                .text("Technology Category");

            svg.append("text")
                .attr("class", "axis-label")
                .attr("transform", "rotate(-90)")
                .attr("x", -(height / 2))
                .attr("y", 25)
                .attr("text-anchor", "middle")
                .text("Number of Projects");
        }).catch(function(err) {
            console.error("Error loading CSV:", err);
        });
    </script>
</body>
</html>
"""
with open("data/index.html", "w") as f:
    f.write(html_content)

# Render actual high quality chart output image for Exp 8
plt.figure(figsize=(7.5, 4.5))
bars = plt.bar(d3_df['Category'], d3_df['Project_Count'], color='#3498db', width=0.55, edgecolor='#2980b9')
plt.title("Students per Department / Technology Projects Completed", fontsize=12, fontweight='bold', pad=15)
plt.xlabel("Technology Category", fontsize=10, fontweight='bold', labelpad=10)
plt.ylabel("Number of Projects", fontsize=10, fontweight='bold')
plt.ylim(0, 105)
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 2, int(yval), ha='center', va='bottom', fontweight='bold', fontsize=10)
plt.grid(axis='y', linestyle=':', alpha=0.5)
plt.tight_layout()
plt.savefig("assets/exp8_d3_barchart_output.png", dpi=200)
plt.close()

print("Experiments 5 through 8 assets generated successfully!")
