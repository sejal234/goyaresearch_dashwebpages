Welcome! This repository contains a dash app that explains how to scrape Twitter data about a given topic, clean said Twitter data, and create interactive visualizations that help you understand more about the data. We focus our project on the Goya Boycott, a Twitter movement where users called for a boycott of Goya Foods after its CEO praised former President Donald Trump. We scraped all tweets about the topic, regardless if they represent users that speak out in favor of, against, or neutrally about the Goya Boycott. The visualizations we created help us understand how conversation about Goya changes over time, geography, subtopic and the sentiment around certain political actors and hashtags.

Please view [this slidedeck](https://docs.google.com/presentation/d/1imkouj9y-ilDMjUyWbEC14dMZMerQuxy79XtIom7akI/edit?usp=sharing) to see the visualizations, an in-depth view into the webpage, and an explanation on how to open the dash app on your computer. I have outlined rough steps below:

Step 1. Download my repo! Create a folder (local directory) in your computer where you'd like to download these files and in terminal, cd into that local directory and paste "git clone https://github.com/sejal234/goyaresearch_dashwebpages/"

Step 2. Create a virtual environment, initialize it, and then install all the requirements. We use python, but you can use python3 if that is the python version in your computer. Use the following code:

cd goyaresearch_dashwebpages
python -m venv venv 
source venv/bin/activate
pip install -r requirements.txt

Step 3. You should now be able to run the webpage with the line "python app.py". The terminal will output a browser link - open it to run the dash app!
