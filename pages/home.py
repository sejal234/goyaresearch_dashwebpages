import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div(children=[
    html.H2(children='What is this?'),

    html.P(children='''
        Welcome! We scraped, cleaned, and analyzed Twitter data on the Goya Boycott. 
        This website shows the different visualizations we designed to help us understand the conversation,
        including user sentiment and how the dialogue changed over time. Use the above links to 
        navigate through different tools we designed and replicate them for your own project!
    '''),

    html.H2(children='What is the Goya Boycott?'),

    html.P(children='''
        [describe the boycott]
    '''),

    html.H2(children='''I have a subject I'd like to analyze Twitter data on. How could I get started?'''),

    html.P(children='''
        That's so exciting! First, you want to scrape the data using a Tweepy API account. 
        Check out the page (link the page) to learn how used 24 keywords to scrape tweets related to the Goya Boycott.
        
        Then, you want to clean the dataset and identify variables of interest. Check out (link to the page) to see our code! We removed duplicates, identify the hashtags
        and political actors mentioned in each tweet, extract location information, and perform sentiment analysis. 

        Once your dataset is clean, you are ready to create your own visualizations! Click through the pages to see how we
        compared tweet sentiment to the actor and hashtag they mentioned, used scatterplots to find correlation in the data,
        depict the data over time, and mapped the conversation throughout the world. (put links for all of these)
    '''),

])