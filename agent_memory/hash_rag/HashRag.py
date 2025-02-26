import json
import pprint
import faiss
import numpy as np
from docx import Document as DOC
from agent_memory.data_classes.graph_dataclasses import *
from loguru import logger

class HashRag:
    def __init__(self, ai_driver, data_for_rag = None):
        self.ai_driver = ai_driver
        self.vector_store = None
        self.data_for_rag = data_for_rag
        self.mapping = {}
        self.markdown_store = {}
        self.dataclass_list = []
        return

    def chunking_strategy(self):
        obj = self.data_for_rag.split('.')
        return obj

    def markdown_chunking_strategy(self):

        return

    def tester(self):
        step_uuid = self.data_for_rag.step_uuid
        if self.data_for_rag.has_markdown:
            self.markdown_store[step_uuid] = self.data_for_rag.function_output
            self.data_for_rag.function_output = step_uuid
        chunks = self._chuncking_strategy_function_output(step_data=self.data_for_rag)
        dataclass_list = []
        embeddings, cost = self.ai_driver.embeddings(prompt=chunks)
        index = step_uuid
        self._create_mapping(str(index), chunks)

        self.dataclass_list.append(HashRagBaseModel(
            index=index,
            data_object=DataInformation(
                parent_location='',
                datatype=str(type(list)),
                is_stored_locally=True,
                data=chunks,
                data_location=""
            ),
            vector_embeddings=embeddings
        ))

        self.create_faiss_index()


    def _chuncking_strategy_function_output(self, step_data):
        """No strategy built yet, just for testing"""
        return str(step_data)

    def _create_mapping(self, index, data):
        self.mapping[index] = data
        return

    def create_faiss_index(self):
        """
        Creates a FAISS index from the stored embeddings
        """
        if not self.dataclass_list:
            logger.warning("No data loaded to create index")
            return

        # Convert embeddings to numpy array
        embeddings = np.array([item.vector_embeddings for item in self.dataclass_list])
        dimension = len(embeddings[0])

        # Initialize FAISS index
        self.vector_store = faiss.IndexFlatL2(dimension)
        self.vector_store.add(embeddings.astype('float32'))

        logger.info(f"Created FAISS index with {len(embeddings)} vectors")

    def search(self, query: str, k: int = 5) -> List[str]:
        """
        Search for similar chunks using the query
        """
        if not self.vector_store:
            logger.error("No vector store initialized")
            return []

        # Get query embedding
        query_embedding, _ = self.ai_driver.embeddings(prompt=query)
        query_embedding = np.array([query_embedding]).astype('float32')

        # Search in FAISS
        distances, indices = self.vector_store.search(query_embedding, k)

        # Return the original text chunks
        results = {}
        for idx in indices[0]:
            results[self.dataclass_list[idx].index] = self.mapping[str(self.dataclass_list[idx].index)]

        return results


    """----------------REF CODE------------------"""

    def _load_mapping(self):
        with open('mapping.json', 'r') as json_file:
            self.mapping = json.loads(json_file.read())

    def _load_dataclasses(self):
        with open('test.txt', 'r') as files:
            data_list = (files.readlines())
        for item in data_list:
            tmp = item.strip()
            tmp = json.loads(tmp)
            self.dataclass_list.append(HashRagBaseModel(
                index=tmp.get('index'),
                data_object=DataInformation(
                    parent_location=tmp['data_object'].get('parent_location', ''),
                    datatype=tmp['data_object'].get('datatype'),
                    is_stored_locally=tmp['data_object'].get('is_stored_locally'),
                    data=tmp['data_object'].get('data'),
                    data_location=tmp['data_object'].get('data_location')
                ),
                vector_embeddings=tmp.get('vector_embeddings')
            ))

    def process_doc(self):
        test = self.chunking_strategy()
        dataclass_list = []
        for item in test:
            embeddings, cost = self.ai_driver.embeddings(prompt=item)
            index = str(uuid.uuid4())
            self._create_mapping(str(index), item)

            dataclass_list.append(HashRagBaseModel(
                index = index,
                data_object = DataInformation(
                    parent_location = '',
                    datatype = str(type(item)),
                    is_stored_locally = True,
                    data = item,
                    data_location = ""
                ),
                vector_embeddings = embeddings
            ))


        with open('test.txt', 'a') as f:
            for item in dataclass_list:
                f.write(item.model_dump_json() +  '\n')

    def write_mapping_to_json(self, filename="mapping.json"):
        with open(filename, 'w') as f:
            json.dump(self.mapping, f, indent=4)


if __name__ == '__main__':
    logger.remove()
    run = HashRag(ai_driver=None)


