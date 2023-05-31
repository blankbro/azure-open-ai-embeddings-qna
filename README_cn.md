# 用 Azure OpenAI 构建的一个问答系统

[Question Answering Over Documents](https://docs.langchain.com/docs/use-cases/qa-docs)

[火爆工具chatpdf原理解析](https://zhuanlan.zhihu.com/p/613489282)

# 资源说明

BLOB_ACCOUNT（存储账号）：主要用来存储知识库的源文件和文本文件（文本从pdf提取）

FORM_RECOGNIZER（表单识别器）：扫描PDF，提取文本

Redis：向量数据库

OPENAI_ENGINE（文本模型）：用于生成文本

OPENAI_EMBEDDINGS_ENGINE（向量模型）：用于生成向量

TRANSLATE：翻译工具

# 服务器部署命令

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