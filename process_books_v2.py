import os
import re
import datetime

DIRECTORY = "/Users/wzb/obsidian"

FILE_MAP = {
    "Aspects_in_Astrology_Chinese.md": "占星相位研究_Aspects_in_Astrology.md",
    "Astrological_Neptune_Chinese.md": "占星海王星_Astrological_Neptune.md",
    "Astrology_Karma_Transformation_Chinese.md": "占星业力与转化_Astrology_Karma_Transformation.md",
    "Astrology_Psychology_Elements_Chinese.md": "占星心理学与四元素_Astrology_Psychology_Elements.md",
    "Chiron_and_the_Healing_Journey_Chinese.md": "凯龙星与疗愈之旅_Chiron_and_the_Healing_Journey.md",
    "Cosmos_and_Psyche_Chinese.md": "宇宙与心灵_Cosmos_and_Psyche.md",
    "Development_Personality_Chinese.md": "人格发展_Development_Personality.md",
    "Dynamics_of_the_Unconscious_Chinese.md": "无意识的动力_Dynamics_of_the_Unconscious.md",
    "Gods_of_Change_Chinese.md": "变革之神_Gods_of_Change.md",
    "Jung_and_Astrology_Chinese.md": "荣格与占星学_Jung_and_Astrology.md",
    "Pluto_Evolutionary_Journey_Chinese.md": "冥王星进化之旅_Pluto_Evolutionary_Journey.md",
    "Psychological_Astrology_Chinese.md": "心理占星学_Psychological_Astrology.md",
    "Relating_Analysis_Chinese.md": "人际关系占星_Relating_Analysis.md",
    "Retrograde_Planets_Chinese.md": "逆行行星_Retrograde_Planets.md",
    "Saturn_Analysis_Chinese.md": "土星研究_Saturn_Analysis.md",
    "The_Dark_of_the_Soul_Chinese.md": "灵魂的暗夜_The_Dark_of_the_Soul.md",
    "The_Inner_Planets_Chinese.md": "内行星_The_Inner_Planets.md",
    "The_Inner_Sky_Chinese.md": "内在的天空_The_Inner_Sky.md",
    "The_Luminaries_Chinese.md": "发光体_The_Luminaries.md",
    "The_Twelve_Houses_Chinese.md": "十二宫位_The_Twelve_Houses.md"
}

def optimize_content(content, filename):
    author_match = re.search(r'作者[:：]\s*(.*)', content)
    author = author_match.group(1).strip() if author_match else "Unknown"
    
    title = filename.replace('.md', '')
    
    frontmatter = f"""---
title: {title}
author: {author}
date: {datetime.date.today()}
icon: 🔮
tags:
  - 占星
  - 经典解读
  - 读书笔记
---

"""
    
    lines = content.split('\n')
    new_lines = []
    
    if lines and lines[0].strip() == '---':
        try:
            end_idx = lines.index('---', 1)
            lines = lines[end_idx+1:]
        except ValueError:
            pass

    for line in lines:
        stripped = line.strip()
        
        if '═══' in line or '───' in line:
            new_lines.append('---')
            continue
            
        if re.match(r'^[一二三四五六七八九十]+、', stripped):
            line = f"## {stripped}"
        
        elif re.match(r'^\d+\.\d+\s', stripped):
            line = f"### {stripped}"
            
        line = re.sub(r'《([^》]+)》', r'[[\1]]', line)
        
        new_lines.append(line)

    return frontmatter + '\n'.join(new_lines)

def main():
    for old_name, new_name in FILE_MAP.items():
        old_path = os.path.join(DIRECTORY, old_name)
        new_path = os.path.join(DIRECTORY, new_name)
        
        if not os.path.exists(old_path):
            print(f"Skipping {old_name}: File not found.")
            continue
            
        print(f"Processing {old_name} -> {new_name}")
        
        with open(old_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        optimized_content = optimize_content(content, new_name)
        
        with open(new_path, 'w', encoding='utf-8') as f:
            f.write(optimized_content)
            
        if old_name != new_name:
            os.remove(old_path)

if __name__ == "__main__":
    main()
