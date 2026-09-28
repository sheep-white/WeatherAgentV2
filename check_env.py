import os
from dotenv import load_dotenv

load_dotenv()

for name in ["OPENAI_API_KEY","OPENAI_API_BASE","OPENAI_MODEL"]:
    value = os.getenv(name)
    if value:
        print(f"{name}:已设置（长度{len(value)}字符）")
    else:
        print(f"{name}缺失请检查env")    