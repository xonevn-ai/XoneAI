from flask import Flask
import markdown

app = Flask(__name__)

def basic():
    from xoneai import XoneAI
    xoneai = XoneAI(agent_file="agents.yaml")
    return xoneai.run()

@app.route('/')
def home():
    output = basic()
    html_output = markdown.markdown(output)
    return f'<html><body>{html_output}</body></html>'

if __name__ == "__main__":
    app.run(debug=True)
