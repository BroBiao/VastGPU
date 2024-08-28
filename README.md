# VastGPU

监控vast.ai的GPU供应，寻找符合条件的GPU并自动下单。

## 使用方式

- 安装vast.ai的cli并设置API Key   
 `pip install --upgrade vastai;`   
 `vastai set api-key your-api-key`

- 创建`.env`文件并设置Telegram Bot   
 `echo "BOT_TOKEN=your-telegram-bot-token" > .env`   
 `echo "CHAT_ID=telgram-chat-id" >> .env`   
 (配置Telegram Bot是为了在下单后通过Telegram发送通知)

- 修改搜索和筛选条件   
 主要是代码中的`search_command`, `create_command`和`for`循环中的`cond1/2/3`，根据需要自行修改。

- 加入corntab定时执行   
 每5分钟检查一次：   
 `*/5 * * * * /usr/bin/python3 /root/VastGPU/check.py >> /root/VastGPU/check.py.log 2>&1`