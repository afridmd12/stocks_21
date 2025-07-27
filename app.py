from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    chart_html = ""
    tickers = []

    if request.method == "POST":
        file = request.files["file"]
        if file:
            df = pd.read_csv(file)
            df['Date'] = pd.to_datetime(df['Date'])
            tickers = df['Ticker'].unique().tolist()

            ticker = request.form.get("ticker", tickers[0])
            subset = df[df['Ticker'] == ticker]
            fig = px.line(subset, x='Date', y='Close', title=f'{ticker} Closing Prices')
            chart_html = pio.to_html(fig, full_html=False)

    return render_template("index.html", chart_html=chart_html, tickers=tickers)

if __name__ == "__main__":
    app.run(debug=True, port=3001)
