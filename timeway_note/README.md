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
├── BatchPushResults
│         ├── __init__.py
│         └── function.json
├── BatchStartProcessing
│         ├── __init__.py
│         └── function.json
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