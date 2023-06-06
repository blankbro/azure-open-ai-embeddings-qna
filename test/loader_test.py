from langchain.document_loaders import UnstructuredURLLoader
from langchain.document_loaders import SeleniumURLLoader
from langchain.document_loaders import PlaywrightURLLoader


def testUnstructuredURLLoader():
    urls = [
        "",
    ]
    loader = UnstructuredURLLoader(urls=urls, headers={"Cookie": ""})
    data = loader.load()
    print(data)

def testSeleniumURLLoader():
    urls = [
        "",
    ]
    loader = SeleniumURLLoader(urls=urls)
    data = loader.load()
    print(data)

if __name__ == "__main__":
    testUnstructuredURLLoader()
