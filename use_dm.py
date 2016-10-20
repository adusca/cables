import json
import scipy.sparse as sparse
import scipy.sparse.linalg as linalg

# from document_matrix import DocumentMatrix

# filename = "document_matrix.json"
# dm = DocumentMatrix(25128, filename)
# dm.process_all_documents()

with open("document_matrix.json", "r") as f:
    matrix = json.load(f)


size = 200*1000
A = sparse.dok_matrix((len(matrix), size))

for document in matrix:
    for term in matrix[document]:
        A[int(document), int(term) - size] = matrix[document][term]

u, s, vt = linalg.svds(A, 100)
