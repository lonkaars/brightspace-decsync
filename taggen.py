import re

def tag_gen(input_str):
  input_str = input_str.lower()
  input_str = re.sub(r'aii', '', input_str)
  input_str = re.sub(r'20\d{2}-\d{2}', '', input_str)
  input_str = re.sub(r'[pb]\d+', '', input_str)
  input_str = re.sub(r'\d', '', input_str)
  input_str = re.sub(r'blok', '', input_str)
  input_str = re.sub(r'programmeren c', 'programmeren', input_str)
  input_str = re.sub(r'stylofoon', '', input_str)
  input_str = re.sub(r'[-]', '', input_str)
  input_str = re.sub(r'\s+', ' ', input_str)
  return input_str.strip()
  
