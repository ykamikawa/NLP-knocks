# テンプレートによる文字生成
from string import Template

def format_string(x, y, z):
    s = Template("$hour時の$targetは$value")
    return s.substitute(hour=x, target=y, value=z)

# テスト
x = 12
y = "気温"
z = 22.4
print(format_string(x, y, z))
