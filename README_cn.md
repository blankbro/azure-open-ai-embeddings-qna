一个简单的web应用程序，用于支持OpenAI的文档搜索。这个repo使用Azure OpenAI服务从文档中创建嵌入向量。为了回答用户的问题，它检索最相关的文档，然后使用GPT-3提取问题的匹配答案。 

如果你对ChatPDF不了解，推荐阅读[这个](https://zhuanlan.zhihu.com/p/613489282)。

Azure 资源

- BLOB_ACCOUNT
- 表单识别器
- 向量数据库
- GPT模型

Python 应用

- Web应用


# WebApp（交互页面）

现成的 Docker 镜像：fruocco/oai-embeddings

对应的 Docker File：WebApp.Dockerfile、WebApp.Dockerfile.dockerignore

源代码（code 文件夹包含了两个项目的代码，下面列出来的是 WebApp 项目相关的源码）：

```
code
├── OpenAI_Queries.py
├── embeddings_text.csv
├── images
│         └── microsoft.png
├── pages
│         ├── 00_Chat.py
│         ├── 01_Add_Document.py
│         ├── 03_Document_Viewer.py
│         ├── 04_Index_Management.py
│         ├── 10_Sandbox.py
│         ├── 10_Utils - Document_Summary.py
│         ├── 11_Utils - Conversation_Data_Extraction.py
│         └── 12_Utils - Prompt Exploration.py
├── requirements.txt
└── utilities
    ├── __init__.py
    ├── azureblobstorage.py
    ├── customprompt.py
    ├── formrecognizer.py
    ├── helper.py
    ├── redis.py
    └── translator.py
```

通过 Mac 系统创建 venv 环境后，需要通过 "source .venv/bin/activate" 激活 venv 环境。 退出当前 venv 环境，直接执行 deactivate 即可。

# BatchProcess（干嘛用的？）

现成的 Docker 镜像：fruocco/oai-batch

对应的 Docker File：BatchProcess.Dockerfile、BatchProcess.Dockerfile.dockerignore

源代码（code 文件夹包含了两个项目的代码，下面列出来的是 BatchProcess 项目相关的源码）：

```
code
├── ApiQnA
│   ├── __init__.py
│   └── function.json
├── BatchPushResults
│   ├── __init__.py
│   └── function.json
├── BatchStartProcessing
│   ├── __init__.py
│   └── function.json
├── embeddings_text.csv
├── requirements.txt
└── utilities
    ├── __init__.py
    ├── azureblobstorage.py
    ├── customprompt.py
    ├── formrecognizer.py
    ├── helper.py
    ├── redis.py
    └── translator.py
```

# 服务器部署命令备忘

```
# ====== 自测
# 删除旧镜像
docker image rm -f azure-open-ai-embeddings-qna

# 打包新镜像
git pull
docker build . -f WebApp.Dockerfile -t azure-open-ai-embeddings-qna

# 停止旧应用
docker rm -f webapp

# 启动新应用
docker run -d --env-file .env -p 8081:80 --name webapp azure-open-ai-embeddings-qna 

# 清除未被使用的镜像及其数据
docker image prune -a 

# ====== 用户部署
# 删除旧镜像
docker image rm -f azure-open-ai-embeddings-qna:user

# 打包新镜像
git pull
docker build . -f WebApp-User.Dockerfile -t azure-open-ai-embeddings-qna:user

# 停止旧应用
docker rm -f webapp-user

# 启动新应用
docker run -d --env-file .env -p 8080:80 --name webapp-user azure-open-ai-embeddings-qna:user

# 清除未被使用的镜像及其数据
docker image prune -a 
```