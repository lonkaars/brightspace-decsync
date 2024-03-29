import re

def tag_gen(input_str):
  input_str = input_str.lower()
  input_str = re.sub(r'studieloopbaanbegeleiding.*', 'studieloopbaanbegeleiding', input_str)
  input_str = re.sub(r'aii', '', input_str)
  input_str = re.sub(r'atd', '', input_str)
  input_str = re.sub(r'et\/ti', '', input_str)
  input_str = re.sub(r'20\d{2}-\d{2}', '', input_str)
  input_str = re.sub(r'[pb]\d+', '', input_str)
  input_str = re.sub(r'\d', '', input_str)
  input_str = re.sub(r'blok', '', input_str)
  input_str = re.sub(r'programmeren c', 'programmeren', input_str)
  input_str = re.sub(r'stylofoon', '', input_str)
  input_str = re.sub(r'[-]', '', input_str)
  input_str = re.sub(r'\s+', ' ', input_str)
  input_str = re.sub(r' \(c\+\+\)', '', input_str)
  return input_str.strip()
  
def title_filter(input_str):
  input_str = input_str.lower()
  input_str = re.sub(r'- due', '', input_str)
  input_str = re.sub(r'- available', '', input_str)
  input_str = re.sub(r'- availability ends', '', input_str)
  return input_str.strip()
