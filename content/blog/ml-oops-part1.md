---
title: "ML (O)Ops! Improving and Deploying On-Device Models With Confidence (Part 1)"
date: 2021-02-21
authors: ["Atul Dhingra", "Gaurav Sood"]
tags: ["Machine Learning", "MLOps", "Edge Computing", "Model Deployment"]
series: ["ML (O)Ops"]
series_order: 1
description: "Part 1 of a multi-part series exploring the challenges and solutions in deploying ML models on edge devices."
aliases: ["/posts/ml-oops-part1/"]
---
**With Gaurav Sood**

It is well known that ML Engineers today spend most of their time doing things that do not have a lot to do with machine learning. They spend time working on technically unsophisticated but important things like deployment of models, keeping track of experiments, etc.—operations. Atul and I dive into the reasons behind the status quo and propose solutions, starting with issues to do with on-device deployments. 

## Performance on Device

The deployment of on-device models is complicated by the fact that the infrastructure used for training is different from what is used for production. This leads to many tedious rollbacks. 

The underlying problem is missing data. We are missing data on the latency in prediction, which is a function of i/o latency and the time taken to compute. One way to impute the missing data is to build a model that predicts latency based on various features of the deployed model. Given many companies have gone through thousands of deployments and rollbacks, there is rich data to learn from. Another is to directly measure the time with 'shadow deployments—performance on redundant chips colocated with the production chip and getting exactly the same data at about the same time (a small lag in passing on the data to the redundant chips is just fine as we can start the clock at a different time).  

Predicting latency given a model and deployment architecture solves the problem of deploying reliably. It doesn't solve the problem of how to improve the performance of the system given a model. To improve the production performance of ML systems, companies need to analyze the data, e.g., compute the correlation between load on the edge server and latency, and generate additional data by experimenting with various easily modifiable parts of the system, e.g., increasing capacity of the edge server, etc. (If you are a cloud service provider like AWS, you can learn from all the combinations of infrastructure that exist to predict latency for various architectures given a model and propose solutions to the customer.)

There is plausibly also a need for a service that helps companies decide which chip is optimal for deployment. One solution to the problem is [MLPerf.org](https://mlcommons.org/benchmarks/) as a service— a service that provides data on the latency of a model on different chips. 