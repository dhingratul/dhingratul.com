---
title: "ML (O)Ops: What Data to Collect? (Part 3)"
date: 2021-06-16
authors: ["Atul Dhingra", "Gaurav Sood"]
tags: ["Machine Learning", "MLOps", "Data Collection", "Monitoring"]
series: ["ML (O)Ops"]
series_order: 3
description: "Part 3 of our series on ML Operations, focusing on what data to collect for effective ML system monitoring."
---
**With Gaurav Sood**

The first part of the series, "Improving and Deploying On-Device Models With Confidence," is posted [here](/posts/ml-oops-part1). The second part, "Keeping Track of Changes," is posted [here](/posts/ml-oops-part2).

## Introduction

In the previous parts of this series, we discussed deployment challenges and change tracking in ML systems. Now, let's focus on a crucial aspect of MLOps: what data to collect for effective monitoring and improvement of ML systems.

## Types of Data to Collect

### 1. Model Performance Metrics
- Accuracy, precision, recall
- Latency and throughput
- Resource utilization
- Error rates and types

### 2. Input Data Statistics
- Distribution of features
- Data quality metrics
- Missing value patterns
- Data drift indicators

### 3. System Health Metrics
- CPU/GPU utilization
- Memory usage
- Network bandwidth
- Storage metrics

### 4. Operational Metrics
- Request volumes
- Queue lengths
- Cache hit rates
- Error logs

## Data Collection Strategies

### 1. Real-time Monitoring
- Stream processing for immediate insights
- Live dashboards
- Alerting systems
- Anomaly detection

### 2. Batch Processing
- Daily aggregations
- Trend analysis
- Performance reports
- Resource optimization

### 3. Sampling Techniques
- Random sampling
- Stratified sampling
- Error-focused sampling
- Edge case collection

## Best Practices

1. **Data Storage**
   - Use appropriate storage solutions
   - Implement data retention policies
   - Ensure data security
   - Enable easy access

2. **Data Processing**
   - Process data in real-time where needed
   - Batch process for deeper analysis
   - Maintain data quality
   - Handle missing data

3. **Visualization**
   - Create clear dashboards
   - Enable drill-down capabilities
   - Show trends and patterns
   - Highlight anomalies

4. **Action Items**
   - Set up automated alerts
   - Define action thresholds
   - Create response procedures
   - Enable quick debugging

## Conclusion

Collecting the right data is crucial for:
- Maintaining system health
- Improving model performance
- Quick problem resolution
- Continuous improvement

The key is to find the right balance between collecting enough data for effective monitoring and not being overwhelmed by data volume. Start with the essential metrics and gradually expand based on your specific needs. 