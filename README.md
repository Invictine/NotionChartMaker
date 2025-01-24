# NotionChartMaker

Just a silly little program I made to pull my notion data and turn it into interactive charts so I can track my long-term goals better. 

##ChatGPT generated from here

NotionChartMaker is a Flask-based application that visualizes progress metrics from a Notion database in real time. The project dynamically generates a donut chart that updates periodically, displaying the current status of monthly goals or quotas
# NotionChartMaker

## Overview
**NotionChartMaker** is a Python web application that generates real-time, interactive visualizations for tracking progress from a Notion database. It is designed for professionals, students, or anyone who uses Notion for managing tasks or setting goals. The project leverages Flask for serving the web page and Matplotlib for creating dynamic donut charts.

## Features
- **Real-Time Updates**: Automatically refreshes every 5 seconds to display the latest data.
- **Interactive Visualization**: Displays progress as a visually appealing donut chart.
- **Notion Integration**: Fetches data directly from your Notion database.
- **Custom Font Support**: Styled with the **Provicali** font for a unique aesthetic.
- **Lightweight Deployment**: Built with Flask, deployable using Docker or any cloud service.

## Technologies Used
- **Python**: Core programming language.
- **Flask**: Backend framework for web server functionality.
- **Matplotlib**: Library for data visualization.
- **Notion API**: Fetches task and progress data.
- **Docker**: Containerization for easy deployment.
- **HTML/CSS**: Frontend design.

## Installation and Setup
### Prerequisites
- Python 3.10 or higher
- Docker (optional, for containerized deployment)
- Notion API Key

### Steps to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/NotionChartMaker.git
   cd NotionChartMaker
