import requests
from pathlib import Path
import re
import json
import yaml
import os
import sys

def get_redirect_url(url):
    max_redirects = 10  # Set a limit to avoid infinite loops
    response = requests.get(url, allow_redirects=True, timeout=5, headers={'User-Agent': 'your_user_agent'})  # Set timeout and user-agent

    if response.history or 200 <= response.status_code < 300:
        return response.url
    else:

        raise Exception(f"Error fetching URL: {response.status_code}")

def remove_content_between_dashes(markdown_file):

    with open(markdown_file, 'r') as f:
        content = f.read()

    if '---' in content:
        sep = '-'
    else:
        sep = '{'

  # 使用正则表达式匹配 --- 之间的内容
    if sep == '-':
        pattern = r'^---(.*?)---\n'
    else:
        pattern = r'^{(.*?)}\n'

    match = re.match(pattern, content, flags=re.DOTALL)

    if match:
        header = match.group(1)
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    else:
        header = ''

    return content, header, sep

def send_req(body):
    domain = os.environ.get('DOMAIN')
    api_key = os.environ.get('API_KEY')
    try:
        response = requests.post(
            url=f"{domain}/api/posts",
            params={
                "api_key": api_key,
            },
            headers={
                "Content-Type": "application/json; charset=utf-8",
            },
            data=json.dumps({
                "post": body
            })
        )
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        # print('Response HTTP Response Body: {content}'.format(
        #     content=response.content))
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def publish_all():
    md_files = []
    for file in Path("../content/posts/").rglob("*.md"):
        md_files.append(str(file))

    for md_file in md_files:
        print(md_file)
        publish_one(md_file)

def publish_one(md_file):
    content, header, sep = remove_content_between_dashes(md_file)
    if sep == '-':
        header_obj = yaml.safe_load(header.strip())
    else:
        header_obj = json.loads("{" + header + "}")            
    if header_obj and 'title' in header_obj:
        title = header_obj['title']
        image = get_redirect_url("https://source.unsplash.com/random/?computer&1")
        send_req({'title': title, 'content': content, 'image_url': image}) 
    

if __name__ == "__main__":
    if not os.environ.get('DOMAIN'):
        exit('DOMAIN must be existed')
    if not os.environ.get('API_KEY'):
        exit('API_KEY must be existed')
    if len(sys.argv) < 2:
        print("USAGE: DOMAIN=XXX API_KEY=YYYY python publish.py all/md_file_path")    
        exit(1)

    file_path = sys.argv[-1]
    if file_path == 'all':
        print('Importing all')
        publish_all()
    else:
        print(f"Importing {file_path}")
        publish_one(file_path)
