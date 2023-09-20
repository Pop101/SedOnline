from flask import Flask, render_template, make_response, request
from waitress import serve
import requests, yaml, re

app = Flask(__name__)
config = yaml.load(open('config.yml'), Loader=yaml.FullLoader)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<int:linestart>/<int:linened>/<string:pattern>/<string:replacement>/<path:input>')
def replace_detailed(linestart, linened, pattern, replacement, input):
    return run_replacement(pattern, replacement, input, start=linestart, end=linened)

@app.route('/<string:pattern>/<string:replacement>/<path:input>')
def replace(pattern, replacement, input):
    print(pattern, replacement, input)
    return run_replacement(pattern, replacement, input)

@app.route('/<string:pattern>/<path:replacement>', methods=['POST'])
def replace_files(pattern, replacement):
    all_responses = list()
    
    for file in request.files:
        file = request.files[file]
        
        # Read a maximum of config['Max Filesize'] bytes from the file
        contents = str()
        with file.stream as f:
            contents = f.read(config['Max Filesize'])
        
        all_responses.append(run_replacement(pattern, replacement, contents))
    
    # Ignore all other files
    # TODO: Add a way to handle multiple files
    if len(all_responses):
        return all_responses[0]
    else:
        return make_response(('No files were uploaded', '400', config.get('Default Headers', {})))
            

def run_replacement(pattern, replacement, strin, start=0, end=-1):
    # If the input is a url, fetch it
    response_info = {
        'status': '200',
        'headers': config.get('Default Headers', {})
    }
    
    # Ensure that unescaped \n and \r from either the pattern or replacement are treated as newlines
    pattern = pattern.replace('\\n', '\n').replace('\\r', '\r')
    replacement = replacement.replace('\\n', '\n').replace('\\r', '\r')
    
    if strin.startswith('http'):
        request = requests.get(strin)
        strin = request.text
        response_info['Status'] = request.status_code
        response_info['Headers'] = request.headers
        response_info['URL'] = request.url
    
    # Perform the replacement
    if end <= -1 or end > len(strin) or end < start:
        end = len(strin)
    if start < 0 or start > len(strin) or start > end:
        start = 0
    
    before, strin, after = strin[:start], strin[start:end], strin[end:]
    strin = re.sub(pattern, replacement, strin)
    strin = before + strin + after
    
    return make_response((strin, response_info['status'], response_info['headers']))
    


if __name__ == '__main__':
    print(f"Starting Server on Port {config['Port']}")
    if config['Development']:
        app.run(debug=config['Development'], port=config['Port'])
    else:
        serve(app, port=config['Port'])