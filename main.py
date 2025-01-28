import base64
from io import BytesIO
from flask import Flask, render_template, jsonify
import matplotlib.pyplot as plt
from matplotlib import rcParams
from notion_client import Client
import pandas as pd
from datetime import datetime
import os
import dotenv

# Flask app initialization
app = Flask(__name__)

# Configure font to use Provicali
rcParams['font.family'] = 'Provicali'

# Notion API Configuration
dotenv.load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("DATABASE_ID")
notion = Client(auth=NOTION_API_KEY)


# Fetch data from Notion
def fetch_data_from_notion():
    response = notion.databases.query(database_id=DATABASE_ID)
    results = response.get("results", [])
    rows = []
    for item in results:
        props = item["properties"]
        rows.append({
            "Name": props["Name"]["title"][0]["plain_text"] if props["Name"]["title"] else None,
            "Status": props["Status"]["status"]["name"] if props["Status"]["status"] else None,
            "Upload Due Date": props["Upload Due Date"]["date"]["start"] if props["Upload Due Date"]["date"] else None,
        })
    return pd.DataFrame(rows)


# Calculate the monthly quota
def calculate_monthly_quota(df):
    current_month = datetime.now().month
    current_year = datetime.now().year

    # Filter for uploaded videos in the current month and year
    monthly_data = df[
        (pd.to_datetime(df["Upload Due Date"]).dt.month == current_month) &
        (pd.to_datetime(df["Upload Due Date"]).dt.year == current_year) &
        (df["Status"] == "Uploaded")
    ]

    return monthly_data.shape[0]


# Generate the donut chart as a base64 string
def generate_chart_as_base64(videos_published, monthly_target):
    remaining_videos = max(0, monthly_target - videos_published)

    # Data for the chart
    data = [videos_published, remaining_videos]
    labels = ["Uploaded", "Remaining"]
    colors = ["#2d9963", "#2f2f2f"]  # Green and grey

    # Create the chart
    fig, ax = plt.subplots(figsize=(6, 6), dpi=200)
    wedges, texts, autotexts = ax.pie(
        data,
        labels=labels,
        colors=colors,
        startangle=90,
        autopct="",
        wedgeprops={"width": 0.3},
    )

    # Add center text
    plt.text(0, 0, f"{videos_published}/{monthly_target}", ha="center", va="center",
             fontsize=24, fontweight="bold", color="#d4d4d4")

    # Customize label colors
    for text in texts:
        text.set_color("#d4d4d4")
        text.set_fontfamily("Provicali")

    # Customize legend
    ax.legend(
        loc="lower center",
        labels=[f"{label} ({value})" for label, value in zip(labels, data)],
        frameon=False,
        fontsize=12,
        bbox_to_anchor=(0.5, -0.1),
        ncol=2,
        prop={"family": "Provicali", "size": 12, "weight": "bold"}
    )

    # Set legend text color
    plt.title("Monthly Quota Progress", fontsize=16, weight="bold", color="#d4d4d4")
    plt.tight_layout()

    # Convert the plot to a base64 string
    buffer = BytesIO()
    plt.savefig(buffer, format="png", transparent=True)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    buffer.close()
    plt.close(fig)

    return image_base64


# Flask route for chart rendering
@app.route("/")
def interactive_chart():
    df = fetch_data_from_notion()
    videos_published = calculate_monthly_quota(df)
    monthly_target = 5
    chart_base64 = generate_chart_as_base64(videos_published, monthly_target)
    return render_template(
        "chart.html",
        videos_published=videos_published,
        monthly_target=monthly_target,
        chart_base64=chart_base64,
    )


# Flask route for JSON data (API endpoint)
@app.route("/api/interactive-chart")
def chart_data():
    df = fetch_data_from_notion()
    videos_published = calculate_monthly_quota(df)
    monthly_target = 5
    return jsonify({
        "videos_published": videos_published,
        "monthly_target": monthly_target,
        "chart_base64": generate_chart_as_base64(videos_published, monthly_target)
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
