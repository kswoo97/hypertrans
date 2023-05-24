# Official code and datasets of How Transitive Are Real-World Group Interactions? - Measurement and Reproduction

## Publication

How Transitive Are Real-World Group Interactions? - Measurement and Reproduction.
Sunwoo Kim, Fanchen Bu, Minyoung Choe, Jaemin Yoo, and Kijung Shin.
KDD 2023 [to appear]

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

***We also provide generated hypergraphs by THera***

## Implementation
Codes are in src folder.

### Overview

In this repo, there are three main codes: HyperTrans.jar, THera.jar, and Observation.py.
- /src/HyperTrans.jar: It receives any hypergraph dataset (same format as explained in dataset section), and computes hyperwedge with resulting transitivity by using HyperTrans and Fast-HyperTrans (see Section 3 of the main paper).
- /src/THera.jar: It receives real-world hypergraph dataset (same format as explained in dataset section), and generates a synthetic hypergraph by using THera (see Section 5 of the main paper).
- /src/Observation.py: It receives hypergraph dataset and resulting transitivity, and reproduces observations of hypergraphs (see Section 4 and 5 of the main paper).

### Execution

#### HyperTrans.jar
##### Input
````
java -jar HyperTrans.jar [data path]
````
Note that data path is a path of input hypergraph. 

##### Output
It returns dataname_output.txt file with hyperwedge and the corresponding transitivity.
For example, with "email_enron_HE.txt" file, it creates "email_enron_HE_output.txt", which looks like
````
0,3,0.1525
1,5,0.5815
````
This implies
- hyperedge index 0 and 3 is hyperwedge and the corresponding hyperwedge transitivity is 0.1525
- hyperedge index 1 and 5 is hyperwedge and the corresponding hyperwedge transitivity is 0.5815

#### THera.jar
##### Input
````
java -jar HyperTrans.jar [data path] [C] [p] [alpha]
````
- Data path is a path to the original real-world hypergraph.
- C is a size of each community.
- p is a ratio of intra-community hyperedge.
- alpha is a base of hierarchical hyperedge generation scalar.

##### Output
It returns dataname_output.txt file with hyperwedge and the corresponding transitivity.
For example, with "email_enron_HE.txt" file and C = 10, p = 0.6, alpha = 3.0, it creates "email_enron_HE_10_0.6_3.0_THera.txt", which looks like
````
0,1,2
0,2,3,4
````
This implies
- First hyperedge consist of node index 0, 1, and 2.
- Second hyperedge consist of node index 0, 2, 3, and 4.
Note that this format is identical to the original hypergraph

#### Observation.py
##### Input
````
python [-obs: observation type] [-obs_detail: type of hypergraph] [-real_data_name: file path to real-world hypergraph] [-gen_data_name: file path to generated hypergraph] [-real_result_name: file path to the real-world transitivity results] [-gen_result_name: file path to the generated transitivity results]
````
- obs indicates whether observation 1, 2, 3, or 4.
- obs_detail indicates whether to check observation of real-world or generated .
- real_data_name indicates file path to the real-world hypergraph.
- gen_data_name indicates file path to the generated hypergraph.
- real_result_name indicates file path to the resulting hypergraph transitivity of real-world hypergraph.
- gen_result_name indicates file path to the resulting hypergraph transitivity of generated hypergraph.

##### Output
It reproduces result of real-world hypergraphs.

## Reference

[1]: Austin R. Benson, Rediet Abebe, Michael T. Schaub, Ali Jadbabaie, and Jon Kleinberg. Simplicial closure and higher-order link prediction. Proceedings of the National Academy of Sciences (PNAS), 2018.

[2]: Sunwoo Kim, Minyoung Choe, Jaemin Yoo, and Kijung Shin. Reciprocity in Directed Hypergraphs: Measures, Findings, and Generators. IEEE International Conference On Data Mining (ICDM), 2022.
