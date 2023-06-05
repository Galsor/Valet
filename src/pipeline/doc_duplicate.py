from haystack import BaseComponent, Document
from typing import List, Optional, Dict, Tuple

from src.utils.formatter import reverse_formatting

class DuplicateDocQueryNode(BaseComponent):
    outgoing_edges = 1

    def run(self, query: Optional[str]= None, documents: Optional[List[Document]] = None, **kwargs) -> Tuple[Dict, str]:
        output_dict = {"query": query, **kwargs}
        filtered_docs = [doc for doc in documents if not self.doc_is_query(query, doc)]
        if len(filtered_docs) != len(documents):
            print(f"/!\ Removed {len(documents) - len(filtered_docs)} duplicate documents")
        output_dict["documents"] = filtered_docs
        return output_dict, "output_1"
    
    def run_batch(self, queries: List[str], documents: Optional[List[List[Document]]] = None, **kwargs) -> Tuple[Dict, str]:
        output_dict = {"queries": queries, **kwargs}
        filtered_docs = [[doc for doc in docs if not self.doc_is_query(query, doc)] for query, docs in zip(queries, documents)]
        output_dict["documents"] = filtered_docs
        return output_dict, "output_1"
    
    def doc_is_query(self, query: str, doc: Document) -> bool:
        print("_"*80)
        print(query, doc.content)
        return query == reverse_formatting(doc.content).get("message")
