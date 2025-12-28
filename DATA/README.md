## About Dataset

### Context
This dataset is the **Sentiment140 dataset**, which contains 1,600,000 tweets
extracted using the Twitter API. The tweets have been annotated for sentiment
analysis based on the presence of positive and negative emoticons.

Sentiment labels are assigned as:
- `0` → Negative sentiment
- `4` → Positive sentiment

This dataset is widely used for sentiment analysis and natural language
processing tasks.

---

### Dataset Source
- Platform: Kaggle
- Dataset Name: Sentiment140
- Link: https://www.kaggle.com/datasets/kazanova/sentiment140

---

### Content
The original dataset contains the following 6 fields:

1. **target**  
   The polarity of the tweet  
   - `0` = Negative  
   - `4` = Positive  

2. **ids**  
   The unique ID of the tweet  
   (example: `2087`)

3. **date**  
   The date and time when the tweet was posted  
   (example: `Sat May 16 23:58:44 UTC 2009`)

4. **flag**  
   The query used to collect the tweet  
   If there is no query, the value is `NO_QUERY`

5. **user**  
   The username of the person who posted the tweet  
   (example: `robotickilldozr`)

6. **text**  
   The actual content of the tweet  
   (example: `Lyx is cool`)

---

### Note
The full Sentiment140 dataset is not included in this repository.
Users are expected to download the dataset directly from Kaggle using the link above.
