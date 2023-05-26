from typing import (Any, List, )

from langchain.text_splitter import TokenTextSplitter


class MyTokenTextSplitter(TokenTextSplitter):

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    def split_text(self, text: str) -> List[str]:
        """Split incoming text and return chunks."""
        splits = self.split_text_of_openai(text, self._chunk_size)
        return splits

    def split_text_of_openai(self, text, n):
        # https://github.com/openai/openai-cookbook/blob/main/examples/Entity_extraction_for_long_documents.ipynb
        # Split a text into smaller chunks of size n, preferably ending at the end of a sentence
        def create_chunks(text, n, tokenizer):
            tokens = tokenizer.encode(text)
            """Yield successive n-sized chunks from text."""
            i = 0
            while i < len(tokens):
                # Find the nearest end of sentence within a range of 0.5 * n and 1.5 * n tokens
                j = min(i + int(1.5 * n), len(tokens))
                while j > i + int(0.5 * n):
                    # Decode the tokens and check for full stop or newline
                    chunk = tokenizer.decode(tokens[i:j])
                    if chunk.endswith(".") or chunk.endswith("\n") or chunk.endswith("。"):
                        break
                    j -= 1
                # If no end of sentence found, use n tokens as the chunk size
                if j == i + int(0.5 * n):
                    j = min(i + n, len(tokens))
                yield tokens[i:j]
                i = j

        chunks = create_chunks(text, n, self._tokenizer)
        text_chunks = [self._tokenizer.decode(chunk) for chunk in chunks]
        return text_chunks


def test(text_splitter: MyTokenTextSplitter):
    text1 = "This is a short text. It doesn't need to be split."
    result1 = text_splitter.split_text(text1)
    print(f"Test case 1 result: {result1}")
    print("len(result1):", len(result1))


if __name__ == "__main__":
    text_splitter: MyTokenTextSplitter = MyTokenTextSplitter(chunk_size=500, chunk_overlap=100)
    test(text_splitter)
