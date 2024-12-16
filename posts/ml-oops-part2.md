---
title: "ML (O)Ops! Keeping Track of Changes (Part 2)"
date: "March 22 2021"
authors: ["Atul Dhingra", "Gaurav Sood"]
tags: ["Machine Learning", "MLOps", "Edge Computing", "Model Deployment"]
image: "images/ml-oops-part2.jpg"
excerpt: "The first part of the series, “Improving and Deploying On-Device Models With Confidence,” is posted [here](empty)"
---

# ML (O)Ops! Keeping Track of Changes (Part 2)

*By Atul Dhingra and Gaurav Sood*

The first part of the series, “Improving and Deploying On-Device Models With Confidence,” is posted [here](empty)

One way to automate classification is to compare new instances to a known list and plug in the majority class of the exact match. For such instance-based learning, you often don’t need to version data; you just need a hash table. When you are not relying on an exact match—most machine learning—you often need to version data to reproduce the behavior.

Reproducibility is the bedrock of mature software engineering. It is fundamental because it allows you to diagnose issues. You can reproduce the behavior of a ‘version.’ With that power, you can correlate changes in inputs with changes in outputs. Systems that enable reproducibility, like version control, have another vital purpose—reducing risk stemming from changes and allow regression testing in systems that depend on data, such as ML. They reduce it by allowing for changes to be rolled back. 

To reproduce outputs from machine learning models, we need to do more than store data. We also need to store hyper-parameters, details about the OS, programming language, and packages, among other things. But given the primary value of reproducibility is instrumental—diagnosis—we not just want the ability to reproduce but also the ability to understand changes and correlate them. Current solutions miss the mark.

##Current Solutions and Problems
One way to version data is to treat it as a binary blob. Store all the data you learned a model on to a server and store a reference to the data in your repository. If the data changes, store the new version and create a new pointer. One downside of using a <code>git lfs</code> like mechanism is that your storage blows up. Another is that build times can be large if the local cache is small or more generally if access costs are large. Yet another problem is the lack of a neat interface that allows you to track more than source data. 

DVC purports to solve all three problems. It solves the first by providing a way to not treat the data as a blob. For instance, in a computer vision workflow, the source data is image files with some elementary tags—labels, assignments to train and test, etc. The differences between data versions are 1) changes in images (additions mostly) and 2) changes in mapping to labels and assignments. DVC allows you to store the differences in corpora of images as a list of additional hashes to files. DVC is silent on the second point—efficient storage of changes in mappings. We come to it later. DVC purports to solve the second problem by allowing you to save to local cloud storage. But it can still be time-consuming to download data from the cloud storage buckets. The reason is as follows. Each time you want to work on an experiment, you need to clone the entire cache to check out the appropriate files. And if not handled properly, the cloning time often significantly exceeds typical training times. Worse, it locks you into a cloud provider for any optimizations you may want to alleviate these time-bound cache downloads. DVC purports to solve the last problem by using yaml, tags, etc. But anarchy prevails. 

## Future Solutions
### Interpretable Changes

One of the big problems with data versioning is that the diffs are not human-readable, much less comprehensible. The diffs are usually very long, and the changes in the diff are hashes, which means that to review an MR/PR/Diff, the reviewer has to check out the change and pull the data with the updated hashes. The process can be easily improved by adding an extra layer that auto-summarizes the changes into a human-readable form. We can, of course, easily do more. We can provide ways to understand how changes to inputs correlate with changes in outputs.

### Diff. Tables

The standard method of understanding data as a blob seems uniquely bad. For conventional rectangular databases, changes can be understood as changes in functional transformations of core data lake tables. For instance, say we store the label assignments of images in a table. And say we revise the labels of 100 images. (The core data lake tables are immutable, so the changes are executed in the downstream tables.) One conventional way of storing the changes is to use a separate table for recording changes. Another is to write an update statement that is run whenever “the v2” table is generated. This means the differences across data are now tied to a data transformation computation graph. When data transformation is inexpensive, we can delay running the transformations till the table is requested. In other cases, we can cache the tables.