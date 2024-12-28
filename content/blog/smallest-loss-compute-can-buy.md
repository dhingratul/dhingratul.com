---
title: "The Smallest Loss Compute Can Buy"
date: 2023-08-15
authors: ["Atul Dhingra", "Gaurav Sood", "Chris Alexiuk"]
tags: ["Machine Learning", "MLOps", "Edge Computing", "Model Deployment"]
series: ["The Smallest Loss Compute Can Buy"]
series_order: 0
description: "The best way to spend the compute budget"
---
**With [Gaurav Sood](https://gojiberries.io/2023/08/15/smallest-loss-that-compute-can-buy/), [Chris Alexiuk](https://www.linkedin.com/in/csalexiuk/)**

The most expensive portion of model training today is GPU time. Given that, it is useful to ask what is the best way to spend the compute budget. More formally, the optimization problem is: minimize test loss given a FLOPs budget. To achieve the smallest loss, there are many different levers that we can pull, including, 

1. Amount of data. 
2. Number of parameters. There is an implicit trade-off between this and the previous point given a particular amount of compute. 
3. Optimization hyperparameters. For e.g., Learning rate, learning rate schedule, batch size, optimizer, etc. 
4. Model architecture
   1. Width-to-depth ratio.
   2. Deeper aspects of model architecture. For e.g., [RETRO](https://arxiv.org/abs/2112.04426), MoE models like [switch transformers](https://arxiv.org/abs/2101.03961), [MoE with expert choice](https://ai.googleblog.com/2022/11/mixture-of-experts-with-expert-choice.html), etc.
5. Precision in which the parameters and hyperparameters are stored.
6. Data quality. As some of the recent work [shows](https://arxiv.org/abs/2306.11644), data quality matters a lot.

We could reformulate the optimization problem to make it more general. For instance, rather than use FLOPs or GPU time, we may want to use dollars. This opens up opportunities to think about how to purchase GPU time most cheaply, e.g., using spot GPUs. We can abstract out the optimization problem further. If we knew the ROI of the prediction task, we could ask what is the profit-maximizing loss given a constraint on latency. Inference ROI is a function of ~ accuracy (or another performance metric of choice) and the compute cost of inference.

### What Do We Know?

[Kaplan et al. (2020)](https://arxiv.org/abs/2001.08361) and [Hoffman et al. (2022)](https://arxiv.org/abs/2203.15556) study a limited version of the problem for autoregressive modeling of language using dense (compared to Mixture-of-Experts models) transformer models. The papers primarily look at #1 and #2 though Hoffman et al. (2022) also study the impact of learning rate schedule and Kaplan et al. (2020) provide limited analysis of width-to-depth ratio and batch size (see [separate paper](https://arxiv.org/abs/1812.06162) featuring Kaplan).

Kaplan et al. uncover a chock-full of compelling empirical patterns including: 

1. Power Laws. “The loss scales as a power-law with model size, dataset size, and the amount of compute used for training.”
2. Future test loss is predictable. “By extrapolating the early part of a training curve, we can roughly predict the loss that would be achieved if we trained for much longer.” 
3. Models generalize. “When we evaluate models on text with a different distribution than they were trained on, the results are strongly correlated to those on the training validation set with a roughly constant offset in the loss.”
4. Don’t train till convergence. “[W]e attain optimal performance by training very large models and stopping significantly short of convergence.” This is a great left field find. You get the same test loss with a larger model that is not trained to convergence as with a smaller model trained till convergence except it turns out that former is compute optimal.

Hoffman et al. assume #1, replicate #2 and #4, and have nothing to say about #3. One place where the papers differ is around the specifics of the claim about large models’ sample efficiency with implications for #4. Both agree that models shouldn’t be trained till convergence but whereas Kaplan et al. conclude that “[g]iven a 10x increase computational budget, … the size of the model should increase 5.5x while the number of training tokens should only increase 1.8x” (Hoffman et al.), Hoffman et al. find that “model size and the number of training tokens should be scaled in equal proportions.” Because of this mismatch Hoffman et al. find that most commercial models (which are trained in line with Kaplan et al.’s guidance) are undertrained. They drive home the point by showing that a 4x smaller model (Chinchilla) with 4x the data outperforms (this bit is somewhat inconsistent with their prediction) the larger model (Gopher) (both use the same compute). They argue that Chinchilla is optimal given that inference (and fine-tuning costs) for smaller models are lower.

All of this means that there is still much to be discovered. But the discovery of patterns like the power law leaves us optimistic about the discovery of other interesting patterns.