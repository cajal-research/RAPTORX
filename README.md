# RAPTORX: Self-Improving Tree for Recursive Abstractive Processing for Tree-Organized Retrieval

**RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval)** introduces a novel approach to retrieval-augmented language models by constructing a recursive tree structure from documents, enabling efficient and context-aware information retrieval across large texts. It addresses common limitations in traditional language models. For detailed methodologies and implementations, refer to the original paper and Github Repo:

- [RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval](https://arxiv.org/abs/2401.18059)
- [GitHub Repository](https://github.com/parthsarthi03/raptor)


**RAPTORX** builds on the RAPTOR framework by introducing adaptive learning to continually improve the tree structure. This is achieved by updating node embeddings when mistakes are made, ensuring the correct path is taken in future traversals. Since the knowledge base is fixed, after building the initial tree, one can generate synthetic queries and self-correct the tree. Also, the tree can be continually improved during its lifetime with human feedback.

## Motivation
Despite the original paper demonstrating that the collapsed tree retrieval performs better than tree traversal, we hypothesize that self-correcting the tree will lead to improved performance in tree traversal.

If tree traversal underperforms, it must indicate that the tree is not sufficiently optimized. The concept of recursively accessing "more evidence" hierarchically is compelling. Essentially, at each step, the system searches for the node that maximizes the expected information gain, which is equivalent to maximizing the Shannon entropy, effectively denoising the query -similar to how humans iteratively ask questions that maximize entropy to acquire more evidence until the precise query is understood.

In this approach, there is a single path for a particular answer, which aligns with the expectations of a retrieval system. The key is to have a highly optimized tree that self-corrects and adjusts to always guide the path towards the correct answer.


## Tasks

- [ ] **Replicate Results and Set Up Evaluation Environment**
  - Replicate the results from the original RAPTOR paper.
  - Create a robust environment for ongoing evaluations.

- [ ] **Implement Algorithm for Node Updates**
  - Updating embeddings directly (more efficient).
  - Updating summaries (less efficient, more explainable).

- [ ] **Integrate Automated Self-Correction**
  - Implement the self-correction mechanism using synthetic data.

- [ ] **Incorporate Human Feedback for Continuous Improvement**
  - Develop a system to incorporate human feedback into the tree structure for ongoing optimization.

- [ ] **Optimize Tree Traversal Algorithms**

- [ ] **Evaluate and Adjust Model Parameters**
  
- [ ] **Explore a similar method with a collapsed tree** 
