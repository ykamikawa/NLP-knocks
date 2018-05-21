# 暗号文

def cipher(target):
    """
    文字列の暗号化
    ・英小文字->(219 - 文字コード)
    ・その他->そのまま
    """
    result = "".join([chr(219 - ord(c)) if c.islower() else c for c in target])
    return result

# テスト
# 対象文字列の入力
target = input("文字列を入力してください\n")

# 暗号化
result = cipher(target)
print("暗号化: ", result)

# 復号化
result2 = cipher(result)
print("復号化: ", result2)

assert target == result2, "暗号化,復号化に失敗しました"
