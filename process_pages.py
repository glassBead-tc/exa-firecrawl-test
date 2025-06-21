import os
import re
import json

def process_page(page_id):
    input_md_path = f"benchmark/pages/exa/{page_id}.md"
    output_md_dir = "output/markdown"
    output_json_dir = "output/json"

    os.makedirs(output_md_dir, exist_ok=True)
    os.makedirs(output_json_dir, exist_ok=True)

    try:
        with open(input_md_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract front matter
        front_matter_match = re.match(r'---\n(.*?)\n---', content, re.DOTALL)
        front_matter = {}
        if front_matter_match:
            front_matter_str = front_matter_match.group(1)
            for line in front_matter_str.split('\n'):
                if ': ' in line:
                    key, value = line.split(': ', 1)
                    front_matter[key.strip()] = value.strip().replace('"', '') # Remove quotes

        # Extract title (first line after front matter)
        cleaned_content = content
        if front_matter_match:
            cleaned_content = content[front_matter_match.end():].strip()
        
        title = ""
        if cleaned_content:
            first_line_match = re.match(r'^(.*?)\n', cleaned_content)
            if first_line_match:
                title = first_line_match.group(1).strip()
            # Handle cases where the content after front matter might be just one line without a newline
            elif cleaned_content: 
                title = cleaned_content.split('\n')[0].strip()


        # Define output paths
        output_md_path = os.path.join(output_md_dir, f"{page_id}.md")
        output_json_path = os.path.join(output_json_dir, f"{page_id}.json")

        # Create JSON summary
        summary = {
            "id": page_id,
            "source_url": front_matter.get("source_url"),
            "retrieved_at": front_matter.get("retrieved_at"),
            "mcp_server": front_matter.get("mcp_server"),
            "title": title,
            "markdown_filepath": output_md_path,
            "json_filepath": output_json_path
        }

        # Write Markdown file
        with open(output_md_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Write JSON summary file (one line)
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, separators=(',', ':')) # ensures one line

        print(f"Processed ID {page_id}")

    except FileNotFoundError:
        print(f"Error: File not found for ID {page_id}: {input_md_path}")
    except Exception as e:
        print(f"Error processing ID {page_id}: {e}")

# Process IDs from 1 to 50
for i in range(1, 51):
    process_page(i)