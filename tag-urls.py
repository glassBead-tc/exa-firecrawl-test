#!/usr/bin/env python3

import json
import re
from urllib.parse import urlparse

def categorize_url(url):
    """Categorize URLs by their content type based on domain and path patterns."""
    
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()
    
    # GitHub categorization
    if 'github.com' in domain:
        if '/blob/' in path or '/tree/' in path:
            if path.endswith('.md'):
                return 'github_markdown'
            elif path.endswith(('.ts', '.js', '.tsx', '.jsx', '.py', '.java')):
                return 'github_code'
            else:
                return 'github_file'
        elif '/releases/' in path or '/tag/' in path:
            return 'github_release'
        elif '/commits/' in path:
            return 'github_commits'
        elif '/wiki/' in path:
            return 'github_wiki'
        else:
            return 'github_repo'
    
    # NPM packages
    elif 'npmjs.com' in domain:
        return 'npm_package'
    
    # Documentation sites
    elif any(doc_domain in domain for doc_domain in [
        'docs.', '.dev/docs', 'typescriptlang.org/docs', 
        'storybook.js.org/docs', 'lit.dev/docs', 'formik.org/docs',
        'readthedocs.io', 'angular.dev', 'nextjs.org/docs',
        'remix.run/docs', 'solidjs.com/docs', 'aurelia.io/docs'
    ]):
        return 'documentation'
    
    # Framework/library sites
    elif any(framework in domain for framework in [
        'tanstack.com', 'mui.com', 'chakra-ui.com', 'ant.design',
        'fluent2.microsoft.design', 'react-hook-form.com', 'inversify.io',
        'axios-http.com', 'rxjs.dev', 'reactrouter.com', 'swr.vercel.app',
        'apollographql.com', 'typegraphql.com', 'discord.js.org',
        'web3js.readthedocs.io', 'definitelytyped.org'
    ]):
        return 'framework_docs'
    
    # Chinese mirror sites
    elif '.bootcss.com' in domain:
        return 'mirror_site'
    
    # Default
    else:
        return 'website'

def add_github_raw_url(url):
    """Convert GitHub blob URLs to raw URLs for better crawling."""
    if 'github.com' in url and '/blob/' in url:
        return url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
    return None

def process_urls():
    """Process urls-list.md and create a tagged version with metadata."""
    
    urls_data = []
    
    with open('urls-list.md', 'r') as f:
        lines = f.readlines()
    
    for line in lines:
        match = re.match(r'{id:\s*(\d+),\s*url:\s*"([^"]+)"}', line.strip())
        if match:
            id_num = int(match.group(1))
            url = match.group(2)
            
            content_type = categorize_url(url)
            raw_url = add_github_raw_url(url)
            
            url_entry = {
                'id': id_num,
                'url': url,
                'content_type': content_type,
                'requires_raw': raw_url is not None,
                'raw_url': raw_url
            }
            
            urls_data.append(url_entry)
    
    # Save as JSON for easy processing
    with open('urls-tagged.json', 'w') as f:
        json.dump(urls_data, f, indent=2)
    
    # Also save as CSV for easy viewing
    with open('urls-tagged.csv', 'w') as f:
        f.write('id,url,content_type,requires_raw,raw_url\n')
        for entry in urls_data:
            raw = entry['raw_url'] if entry['raw_url'] else ''
            f.write(f"{entry['id']},\"{entry['url']}\",{entry['content_type']},{entry['requires_raw']},\"{raw}\"\n")
    
    # Print summary statistics
    print("URL Categorization Summary:")
    print("==========================")
    
    type_counts = {}
    for entry in urls_data:
        ct = entry['content_type']
        type_counts[ct] = type_counts.get(ct, 0) + 1
    
    for content_type, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"{content_type}: {count}")
    
    github_count = sum(1 for e in urls_data if e['requires_raw'])
    print(f"\nGitHub URLs requiring raw conversion: {github_count}")
    
    return urls_data

if __name__ == "__main__":
    process_urls()