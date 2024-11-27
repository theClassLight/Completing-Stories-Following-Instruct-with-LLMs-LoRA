### 解析指南

#### 背景
这份指南主要介绍了如何在本地部署LLM（例如千问）和Graphrag，并解决其中的一些常见问题。由于本地部署相比使用OpenAI的服务更加复杂，因此需要用户已经熟悉LLM生态和常用操作。

#### 主要步骤

1. **克隆Graphrag**
   - **原因**：Graphrag对中文支持不佳，且对开源大模型的支持也不够好。建议从GitHub安装以获取最新更新。
   - **命令**：`pip install git+ https://github.com/microsoft/graphrag.git`

2. **启动LLM和Embedding模型**
   - **OLLAMA**：使用OLLAMA启动LLM。
   - **LM Studio**：使用LM Studio启动Embedding模型。
   - **Hack OpenAI Embeddings**：修改 `openai_embeddings_llm.py` 文件以适应本地环境。

3. **初始化Graphrag**
   - **命令**：`python -m graphrag.index --init --root .`
   - **作用**：初始化Graphrag索引。

4. **修改配置文件（yaml）**
   - **LLM Model**：将 `llm model` 改为你的模型。
   - **LLM API Base**：将 `llm api_base` 改为 `http://localhost:11434/v1`（OLLAMA的端口）。
   - **LLM Request Timeout**：建议将 `llm request_timeout` 从180改为3600，以避免超时错误。
   - **Embedding Model**：将 `embedding model` 改为你的模型。
   - **Embedding API Base**：将 `embedding api_base` 改为 `http://localhost:1234/v1`（LM Studio的端口）。

5. **调整Prompt Template**
   - **原因**：Graphrag默认的Prompt Template对中文支持不好。
   - **命令**：`python -m graphrag.prompt_tune --root . --language Chinese --output prompts_zh --no-entity-types`
   - **注意**：一定要加上 `--no-entity-types` 参数，其他参数可能会导致错误。
   - **手动修改**：生成的模板可能需要手动调整，确保中文输出格式与英文模板一致。

6. **修改YAML文件中的Prompt路径**
   - **命令**：
     ```yaml
     GRAPHRAG_ENTITY_EXTRACTION_PROMPT_FILE = "prompts_zh/entity_extraction.txt"
     GRAPHRAG_COMMUNITY_REPORT_PROMPT_FILE = "prompts_zh/community_report.txt"
     GRAPHRAG_SUMMARIZE_DESCRIPTIONS_PROMPT_FILE = "prompts_zh/summarize_descriptions.txt"
     ```


7. **建立Index和测试**
   - **命令**：按照正常流程建立索引并进行问询测试。

8. **Hack OpenAI Embeddings（不推荐）**
   - **原因**：如果后续Graphrag更新，可能会覆盖你的修改。
   - **修改内容**：
     - **原代码**：
       ```python
       embedding = await self.client.embeddings.create(
           input=input,
           **args,
       )
       return [d.embedding for d in embedding.data]
       ```

     - **新代码**：
       ```python
       embedding_list = []
       for inp in input:
           embedding = ollama.embeddings(model=你的model, prompt=inp)
           embedding_list.append(embedding["embedding"])
       return embedding_list
       ```


### 总结
这份指南详细介绍了如何在本地部署LLM和Graphrag，并解决了一些常见的配置问题。通过这些步骤，你可以确保在本地环境中顺利运行Graphrag，并针对中文内容进行优化。