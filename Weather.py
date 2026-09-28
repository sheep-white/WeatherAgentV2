# ========== 第一阶段：导入需要的工具和模块 ==========
from langchain_core.tools import tool          # 导入 @tool 装饰器：把普通函数变成大模型能调用的工具
from dotenv import load_dotenv                 # 导入加载 .env 文件的函数
from langchain_openai.chat_models import ChatOpenAI  # 导入大模型类（OpenAI 兼容接口，这里实际接的是通义千问）
import os                                       # 导入系统标准库，用来读取环境变量
from langchain_core.messages import HumanMessage, ToolMessage  # 导入三种消息类型（用户/模型/工具）
import requests

# ========== 第二阶段：加载密钥，定义天气工具 ==========
load_dotenv()                                   # 把 .env 文件里的配置加载进系统环境变量

@tool                                           # 装饰器：把下面的函数包装成 LangChain 工具对象
def get_weather(city):                          # 定义工具函数，city 是调用时传入的城市名
    """获取城市天气"""                            # docstring：工具说明书，会被大模型看到，用来判断何时调用
    try:
        response=requests.get(
            "https://restapi.amap.com/v3/weather/weatherInfo",
            params={
                "key":amap_key,
                "city":city,
                "extensions":"base",
            }
        )          
        
        data=response.json()
        
        if data.get("status")!="1":   # 目前返回模拟数据（f-string 把城市名嵌进字符串）
            return f"查询{city}天气失败"

        live = data["lives"][0]

        return ( 
            f" {live[ 'city' ]} 当前 {live[ 'weather' ]}" 
            f"气温 {live[ 'temperature' ]} ℃，" 
            f"湿度 {live[ 'humidity' ]} %" 
            f" {live[ 'winddirection' ]} 风 {live[ 'windpower' ]} 级，" 
            f"数据更新时间 {live[ 'reporttime' ]} " ) 
            
    except requests.exceptions.RequestException:
        return f"网络请求失败，暂时无法查询 {city} 的天气，请稍后再试"

        

# ========== 第三阶段：从环境变量取出配置 ==========
api_key = os.getenv("OPENAI_API_KEY")           # 读取 API 密钥
base_url = os.getenv("OPENAI_API_BASE")         # 读取接口地址（阿里云百炼的兼容地址）
model = os.getenv("OPENAI_MODEL")               # 读取模型名（qwen-plus）
amap_key = os.getenv("AMAP_KEY")                 # 读取高德地图密钥（用于天气查询）

# ========== 第四阶段：创建大模型，并把工具绑定给它 ==========
llm = ChatOpenAI(                               # 实例化大模型对象
    api_key=api_key,                            # 传入密钥（左边是固定参数名，右边是你的变量）
    base_url=base_url,                          # 传入接口地址，告诉请求别发去 openai 官方
    model=model,                                # 传入要用的模型名
)

llm_with_tools = llm.bind_tools([get_weather])  # 把工具装进列表绑定给模型，返回一个"知道有哪些工具"的新模型

if __name__ == "__main__":
    
    messages = []

    while True:
        user_input = input("你:")
        if user_input in ("退出","exit","quit"):
            print("再见！")
            break

        messages.append(HumanMessage(content=user_input))

        while True:
            response = llm_with_tools.invoke(messages)
            
            if not response.tool_calls:
                print("助手:",response.content)
                messages.append(response)
                break
            
            messages.append(response)

            for tool_call in response.tool_calls:
                tool_result = get_weather.invoke(tool_call["args"])
                messages.append(
                    ToolMessage(
                        content=tool_result,
                        tool_call_id=tool_call["id"]
                    )
                )