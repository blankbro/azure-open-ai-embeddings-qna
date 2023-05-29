from typing import Any, Dict, Union, List

from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentFinish, AgentAction, LLMResult


class CustomHandler(BaseCallbackHandler):

    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any) -> Any:
        print("on_llm_start")

    def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        print("on_llm_new_token")

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        print("on_llm_end")

    def on_llm_error(self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any) -> Any:
        print("on_llm_error")

    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any) -> Any:
        print("on_chain_start")

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> Any:
        print("on_chain_end")

    def on_chain_error(self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any) -> Any:
        print("on_chain_error")

    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs: Any) -> Any:
        print("on_tool_start")

    def on_tool_end(self, output: str, **kwargs: Any) -> Any:
        print("on_tool_end")

    def on_tool_error(self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any) -> Any:
        print("on_tool_error")

    def on_text(self, text: str, **kwargs: Any) -> Any:
        print("on_text")

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        print("on_agent_action")

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> Any:
        print("on_agent_finish")
