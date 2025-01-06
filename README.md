
# **Real-Time Anomaly Detection On NVDIA stock**

This project demonstrates how to build a modern anomaly detection pipeline with real-time data streaming, machine learning, and containerized deployment. The pipeline includes data ingestion, transformation, anomaly detection of NVDIA stock from 11/26/2024 to 12/26/2024 using Isolation Forests, and deployment using state-of-the-art tools like **Quix Streams**, **Redpanda**, and **Docker**.

---

## **Project Features**

- a complete anomaly detection pipeline  
- Fetching stock market data via HTTP  
- stock data producer using Quix Streams  
- Sn anomaly detection system with Isolation Forests  
- Real-time data transformation and processing with Quix Streams  
- Docker for streamlined deployment  

---

## **Pipeline Overview**

1. **Data Collection**  
   - Historical price data of NVDIA Obtained from [Data Bento](https://databento.com/)
   - Converts the data into JSON format and publishes it to a Kafka topic.  

2. **Data Transformation & Anomaly Detection**  
   - Applies the following rules for anomaly detection:  
     - **High Volume Anomalies**: Flags trades with unusually high volumes.  
     - **Isolation Forest Anomalies**: Uses Isolation Forests to identify price-based anomalies.  
   - Combines detected anomalies into a unified output.

3. **Real-Time Streaming**  
   - Processes and filters data streams using Quix Streams.  
   - Publishes only anomalous data to the output topic for further analysis or visualization.

4. **Deployment**  
   - Uses Docker to containerize and deploy the project, ensuring seamless integration across environments.

---

## **Requirements**

### **Software**
- Python 3.9+
- Quix Streams SDK  
- Kafka (Redpanda recommended)  
- Docker  

### **Python Packages**  
Install dependencies using:  
```bash
pip install -r requirements.txt
```



## **Setup Instructions**

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/inagib21/StockAnomlyDetection

2. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

3. **Prepare Datasets**  
   - Place stock market datasets in the `nasdaq/` folder.  

4. **Run the Producer**  
   Start the stock data producer to publish data to Kafka:  
   ```bash
   python producer.py
   ```

5. **Run the Consumer**  
   Start the anomaly detection pipeline:  
   ```bash
   python pipeline.py
   ```

6. **Containerization (Optional)**  
   Build and deploy the project using Docker:  
   ```bash
   docker build -t anomaly-detection-pipeline .
   docker run -d --env-file .env anomaly-detection-pipeline
   ```

---


## **How It Works**

### **Anomaly Detection Logic**  
1. **High Volume Rule**:  
   Flags anomalies based on a threshold trade volume for each stock symbol.  

2. **Isolation Forest**:  
   - Normalizes price data and trains the Isolation Forest model every 1000 data points.  
   - Scores and flags prices with negative anomaly scores.  

3. **Anomaly Combination**:  
   Merges detected anomalies into a unified output field for each trade.  


---

## **References**

- [Quix Streams Documentation](https://quix.io/docs/)  
- [Redpanda](https://redpanda.com/)  
- [Scikit-learn Isolation Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)  

---
