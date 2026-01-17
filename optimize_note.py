import re
import os
import datetime

def optimize_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(filepath).replace('.md', '')
    
    # 1. Extract Author
    author_match = re.search(r'作者[:：]\s*(.*)', content)
    author = author_match.group(1).strip() if author_match else "Unknown"
    
    # 2. Add Frontmatter
    frontmatter = f"""---
title: {filename}
author: {author}
date: {datetime.date.today()}
tags:
  - 占星
  - 经典解读
  - 读书笔记
---

"""

    # 3. Process Content
    lines = content.split('\n')
    new_lines = []
    
    in_code_block = False
    
    for line in lines:
        original_line = line
        stripped = line.strip()
        
        # Skip original ASCII art headers if we are adding frontmatter
        if '═══' in line:
            new_lines.append('---')
            continue
            
        # Headers transformation
        # Level 2: 一、 二、 ...
        if re.match(r'^[一二三四五六七八九十]+、', stripped):
            line = '## ' + stripped
        
        # Level 3: 1.1, 1.2 ...
        elif re.match(r'^\d+\.\d+\s', stripped):
            # Keep indentation? usually markdown headers should be top level or standard indent
            # But the original file has heavy indentation. Let's strip standard indentation for headers.
            line = '### ' + stripped
            
        # Book Links: 《Title》 -> [[Title]]
        # Use a callback to avoid replacing if it's already a link (simplistic approach)
        line = re.sub(r'《([^》]+)》', r'[[\1]]', line)
        
        # Callouts for specific keywords
        if '核心思想' in line and not line.startswith('>'):
            new_lines.append('> [!abstract] ' + line.strip())
            continue # Skip adding the line again if we transformed it entirely? 
                     # Actually the line might contain the content.
                     # If it's a header-like line: "1.4 一句话核心思想", we make it a callout header.
                     # Let's keep it simple: Just wrap the content if it follows. 
                     # Complex parsing is hard with line-by-line. 
                     # Let's just do simple replacements for now.
        
        new_lines.append(line)

    # Reassemble
    new_content = frontmatter + '\n'.join(new_lines)
    
    # Post-processing for Callouts (Multi-line regex is better here)
    # Convert "一句话核心思想" section content to callout
    # Pattern: Header -> Content -> Separator
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

# Target file
target = "/Users/wzb/obsidian/知识库/占星知识库/经典解读/占星相位研究.md"
optimize_file(target)
