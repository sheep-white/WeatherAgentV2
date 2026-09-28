# 第3步练习：Python 最基础的 4 个语法点

# 1) 变量：用 = 把值"装进"一个名字里，不需要声明类型
city = "佛山"
temp = 28

# 2) 函数：def 定义一段可重复使用的代码块
def make_greeting(name):
    # f-string：字符串前面加 f，里面就能用 {变量} 直接嵌值
    return f"{name}天气助手已启动！"

# 3) print：把内容显示到屏幕（终端）
print("=" * 30)
print(make_greeting(city))
print(f"当前设定温度：{temp}°C，类型是 {type(temp).__name__}")
print("=" * 30)
