# zhihu_hotlist

### 获取登录token的方式
如果提示需要手机登录，则电脑上打开知乎网页，按F12然后在调试窗口的console页中输入下方代码并回车，返回 undefined 即为成功。

window.addEventListener("beforeunload", function() { debugger; }, false)

接着打开调试窗口的network页，点击clear按钮清除所有记录。

接着在网页上用手机登录，登录后会触发调试窗口暂停，在 network 页中找到 sign_in 条目，
选中后从 response 中把内容复制出来，粘贴到 config.json 的 token_json 中覆盖原条目。

这个请求的body是加密的，暂时没找到自动发请求的方法，得手动复制。


```python

from zhihu_oauth import ZhihuClient, Answer
from zhihu_oauth.oauth.token import ZhihuToken

ZhihuToken.from_dict(zhihu_config['token_json']).save(zhihu_config['token_file'])

client = ZhihuClient()

if os.path.isfile(zhihu_config['token_file']):
    client.load_token(zhihu_config['token_file'])


# token_json 长这样

{
      "user_id": 1111111111111111111,
      "uid": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "access_token": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "lock_in": 1800,
      "expires_in": 15000000,
      "token_type": "bearer",
      "cookie": {
        "q_c0": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
        "z_c0": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
      },
      "unlock_ticket": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
      "refresh_token": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
}