import dash
from dash import html, dcc

dash.register_page(__name__, path='/', order = 1)

layout = html.Div(children=[
    html.H2(children='What is this?'),

    html.P(children='''
        Welcome! We scraped, cleaned, and analyzed Twitter data on the Goya Boycott. 
        This website shows the different visualizations we designed to help us understand the conversation,
        including user sentiment and how the dialogue changed over time. Use the above links to 
        navigate through different tools we designed and replicate them for your own project!
    '''),

    html.Br(),

    # html.H2(children='What is the Goya Boycott?'),

    # html.P(children='''
    #     [describe the boycott]
    # '''),

    # html.Br(),

    html.H2(children='''I have a subject I'd like to analyze Twitter data on. How could I get started?'''),

     dcc.Markdown('''
        That's so exciting! First, you want to scrape the data using a Tweepy API account. 
        Check out the [scraping tutorial](/scrape_twitter_data) to learn how we used 24 keywords to scrape tweets related to the Goya Boycott.
    '''),

    html.Br(),

        dcc.Markdown('''
        Then, you want to clean the dataset and identify variables of interest. Check out the [cleaning tutorial](/clean_twitter_data) to see our code! We removed duplicates, identify the hashtags
        and political actors mentioned in each tweet, extract location information, and perform sentiment analysis. 
    '''),

    html.Br(),

        dcc.Markdown('''
        Once your dataset is clean, you are ready to create your own visualizations! Click through the pages to see how we
        compared tweet sentiment to the [actor](/actor_barchart) and [hashtag](/hashtag_barchart) they mentioned, 
               used [scatterplots](/scatter) to find correlation in the data,
        depict the data [over time](/timeseries), and [mapped](/map) the conversation throughout the world. 
    '''),

    html.Br(),

    dcc.Markdown(''' Note that the plot tutorials are to make plots on dash virtual environments. You can learn more about dash plotly [here](https://dash.plotly.com/). This site
                 offers valuable insight into how to generate plots  on your computer's virtual environment. View the requirements.txt file to see what packages are used in this tutorial.
                 For each plot in this site, you essentially code a script following the instructions, run the script in your terminal, and use the link your terminal output provides (it will likely be
                the message "Dash is running on http://0.0.0.0:8050/") to view your plot. We do it this way because these plots involve [callbacks](https://dash.plotly.com/basic-callbacks), a tool that lets the user
                 interact with the plot and change the input/output data. You can, however, just use the actual graph code to generate the plotly plots themselves without callbacks
                 in each plot.
'''),

html.Br(),

    dcc.Markdown('''Please reach out to sg120@rice.edu with any questions you may have!''')

])