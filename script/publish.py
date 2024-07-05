import requests
from pathlib import Path
import re
import json
import yaml
import os
import sys
import random

def get_an_image():
    images = ['https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
     'https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
     'https://images.unsplash.com/photo-1461749280684-dccba630e2f6?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
     'https://images.unsplash.com/photo-1486312338219-ce68d2c6f44d?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
     'https://images.unsplash.com/photo-1531297484001-80022131f5a1?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
     'https://images.unsplash.com/photo-1487058792275-0ad4aaf24ca7?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
     'https://images.unsplash.com/photo-1519389950473-47ba0277781c?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
     'https://images.unsplash.com/photo-1460925895917-afdab827c52f?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
     'https://images.unsplash.com/photo-1483058712412-4245e9b90334?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
     'https://images.unsplash.com/photo-1487017159836-4e23ece2e4cf?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
     'https://images.unsplash.com/photo-1573164713988-8665fc963095?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
     'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
     'https://images.unsplash.com/photo-1499750310107-5fef28a66643?q=80&w=1000&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'
     ]
    return random.sample(images, 1)[0]


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
        # image = get_redirect_url("https://source.unsplash.com/random/?computer&1")
        image = get_an_image()
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
