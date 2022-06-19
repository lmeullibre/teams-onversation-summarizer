# teams-conversation-summarizer
 
 The code contains a Python function exposed as a rest api. The endpoint expects a list of all meeting entries that are parsed from a meeting transcript (Text and person who spoke it) and uses this information to summarize the entire dialogue and find most important keywords based on the summary.
 For summarization bart-large-cnn model is used due to lacking of data. While for topic extraction we use KEYBert model.


Example api response :

