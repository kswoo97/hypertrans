# Official code and datasets of How Transitive Are Real-World Group Interactions? - Measurement and Reproduction

## Description

- This is an official code and datasets for How Transitive Are Real-World Group Interactions? - Measurement and Reproduction.
- FastHyperTrans and THera are implemented with JAVA
- Experimental results (Tables, Figures) are implemented with Python

## Dataset

### Overview and Source

We used 12 real-world hypergraph datasets. Details and source of each datasets are as follows.
1. Email (Enron, EU) [1]
2. NDC (Substances, Classes) [1]
3. Contact (High, Primary) [1]
4. Co-Authorship (DBLP, MAG-Geology, -History) [1]
5. Q&A (Ubuntu, Server, Math) [1, 2]

Since file sizes are greater than 25MB, we uploaded datasets in the following URL: 
https://www.dropbox.com/sh/in4x4vly764su8g/AAAZZ3J81jY2dc7YaxmCmJVaa?dl=0

### Example

Each line of data indicates each hyperedge.
Comma-seperated numbers are all node.
Shape of each dataset is as follows:

````
0,1,2
1,3,4,5
````
where the first hyperedge consists of node index 0, 1, and 2, and the second hyperedge consists of node index 1, 3, 4, and 5.



## Reference

[1]: Austin R. Benson, Rediet Abebe, Michael T. Schaub, Ali Jadbabaie, and Jon Kleinberg. Simplicial closure and higher-order link prediction. Proceedings of the National Academy of Sciences (PNAS), 2018.

[2]: Sunwoo Kim, Minyoung Choe, Jaemin Yoo, and Kijung Shin. Reciprocity in Directed Hypergraphs: Measures, Findings, and Generators. IEEE International Conference On Data Mining (ICDM), 2022.
