from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

BACKEND_URL = "http://localhost:8000"

html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>FastAPI Frontend</title>
    <script>
        async function search() {{
            let query = document.getElementById("query").value;
            if (!query) {{
                document.getElementById("output").innerText = "Please enter a search term.";
                return;
            }}
            try {{
                let response = await fetch(`{BACKEND_URL}/get?query=${{encodeURIComponent(query)}}`);
                if (!response.ok) throw new Error("Failed to fetch data");

                let data = await response.json();
                document.getElementById("output").innerHTML = data.text ? `<p>${{data.text}}</p>` : data.message;
            }} catch (error) {{
                console.error("Error:", error);
                document.getElementById("output").innerText = "Error fetching data.";
            }}
        }}

        async function insert() {{
            try {{
                let response = await fetch("{BACKEND_URL}/insert", {{ method: "POST" }});
                if (!response.ok) throw new Error("Failed to insert data");

                let data = await response.json();
                document.getElementById("output").innerText = data.message;
            }} catch (error) {{
                console.error("Error:", error);
                document.getElementById("output").innerText = "Error inserting data.";
            }}
        }}
    </script>
</head>
<body>
    <h2>Search in Elasticsearch</h2>
    <input type="text" id="query" placeholder="Enter text">
    <button onclick="search()">Get</button>
    <button onclick="insert()">Insert</button>
    <div id="output"></div>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return html_content
