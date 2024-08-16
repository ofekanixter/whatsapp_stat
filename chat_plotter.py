import os
from collections import Counter
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

WIDTH=1400
HEIGHT=900
TICK_SIZE = 16
TITLE_SIZE = 22
AXIS_SIZE = 20
BAD_WORDS=[
    ("זונה","הזונה","זונות","הזונות","בנזונה","זנות"),
    ("סתום","טיפש","אידיוט","מפגר","דבע"),
    ("זין","זיןן"),
    ("מזדיין","מדיינת","זדיין","זיין","זיינתי","זיינו","הזדיינתי","תזדיינו","להזדיין"),
    ("שרמוטה","שרמוטות"),]
GOOD_WORDS = [
    ("אוהב","מאוהב","אהבתי","אהבה","לאהוב","אהבה"),
    ("תודה","תודות","להודות","מודה"),
    ("שמח","שמחתי","לשמוח","לחייך","חיוך"),
    ("טוב","טובה","לטובה","טובב","יופי"),
]
class ChatStatsPlotter:
    def __init__(self,chat_data , plot_folder = "whatsapp_stat/plots"):
        self.hour_dict = chat_data.hour_dict
        self.month_dict =chat_data.month_dict
        self.year_dict = chat_data.year_dict
        self.date_dict = chat_data.date_dict
        self.name_dict = chat_data.name_dict
        self.person_word_count_dict = chat_data.person_word_count_dict  # Add this line
        self.plots_folder = plot_folder + "/"+ chat_data.chat_name
        self.two_word_dict = chat_data.two_word_dict
        self.three_word_dict = chat_data.three_word_dict
        self.person_next_message = chat_data.person_next_message
        os.makedirs(self.plots_folder, exist_ok=True)  # Ensure the plots folder exists

    def plot_all(self):
        self.plot_next_message_distribution()
        self.plot_word_distribution(BAD_WORDS , title="Curses Words")
        self.plot_word_distribution( GOOD_WORDS, title="Good Words")
        self.plot_name_distribution()
        self.plot_year_distribution()
        self.plot_month_distribution()
        self.plot_date_distribution()
        self.plot_hour_distribution()
        self.plot_top_25_words_by_person()
        self.plot_top_25_words_overall()
        self.plot_top_30_dates()
        self.plot_top_25_three_word_phrases()
        self.plot_top_25_two_word_phrases()

    def plot_next_message_distribution(self):
        for person, next_dict in self.person_next_message.items():
            plot_data = [{'next_person': next_person, 'count': count} for next_person, count in next_dict.items()]
            plot_data.sort(key=lambda x: x["count"], reverse=True)
            df = pd.DataFrame(plot_data)
            
            fig = go.Figure()
            
            # Use a gradient color for the bars
            fig.add_trace(go.Bar(
                x=df['next_person'],
                y=df['count'],
                marker_color=df['count'],
                marker_colorscale='Blues',
                text=df['count'],
                textposition='outside',
                texttemplate='%{text:.0f}',  # Format text to show integer values
                showlegend=False
            ))
            
            fig.update_layout(
                title=f'Who Sent the Message After {person}',
                xaxis_title='Next Person',
                yaxis_title='Message Count',
                xaxis_tickangle=-45,
                xaxis_title_font=dict(size=AXIS_SIZE, family='Arial', color='RebeccaPurple'),
                yaxis_title_font=dict(size=AXIS_SIZE, family='Arial', color='RebeccaPurple'),
                title_font=dict(size=TITLE_SIZE, family='Arial', color='RebeccaPurple'),
                autosize=True,
                margin=dict(l=100, r=50, t=100, b=100),  # Adjust margins for better spacing
                plot_bgcolor='rgba(243, 243, 243, 0.5)',  # Light background color
                paper_bgcolor='rgba(255, 255, 255, 0.9)',  # Slightly off-white plot background
                xaxis=dict(
                    tickangle=-45,
                    tickfont=dict(size=TICK_SIZE, color='black')
                ),
                yaxis=dict(
                    tickfont=dict(size=TICK_SIZE, color='black')
                ),
                font=dict(family='Arial', size=TICK_SIZE, color='black'),  # Adjust margins for better spacing
                width=WIDTH,  # Set the width of the image
                height=HEIGHT  # Set the height of the image)
            )
            
            os.makedirs(f'{self.plots_folder}/next', exist_ok=True)
            fig.write_image(f'{self.plots_folder}/next/{person}_next_message.png')
    
    def plot_word_distribution(self, word_list , title="Words"):
        plot_data = []
        for word_group in word_list:
            person_total_counts = {}
            for word in word_group:
                for person, count in self.person_word_count_dict[word].items():
                    if person != 'count':
                        if person not in person_total_counts:
                            person_total_counts[person] = 0
                        person_total_counts[person] += count

            for person, total_count in person_total_counts.items():
                plot_data.append({"word": word_group[0], "person": person, "count": total_count})

        df = pd.DataFrame(plot_data)

        # Create the bar chart with Plotly Express
        fig = px.bar(df, x='word', y='count', color='person', title=f'Distribution of {title} Across Persons',
                    labels={'count': 'Count', 'word': 'Word'},
                    color_discrete_sequence=px.colors.qualitative.Plotly)

        # Update the layout for better readability and appearance
        fig.update_layout(
            xaxis_title='Word',
            yaxis_title='Count',
            xaxis_tickangle=-45,
            xaxis_title_font=dict(size=AXIS_SIZE, family='Arial', color='DarkSlateGray'),
            yaxis_title_font=dict(size=AXIS_SIZE, family='Arial', color='DarkSlateGray'),
            title_font=dict(size=TITLE_SIZE, family='Arial', color='DarkSlateGray'),
            xaxis=dict(
                tickangle=-45,
                tickfont=dict(size=TICK_SIZE, color='Black'),
                tickmode='array'
            ),
            yaxis=dict(
                tickfont=dict(size=TICK_SIZE, color='Black'),
                showgrid=True,
                gridcolor='LightGray'
            ),
            legend_title_text='Person',
            legend=dict(
                title='Person',
                title_font=dict(size=TITLE_SIZE, family='Arial', color='DarkSlateGray'),
                font=dict(size=TICK_SIZE, color='Black')
            ),
            plot_bgcolor='rgba(243, 243, 243, 0.5)',  # Light background color for the entire chart
            paper_bgcolor='rgba(255, 255, 255, 0.9)',  # Slightly off-white plot background
            margin=dict(l=80, r=20, t=60, b=100),  # Adjust margins for better spacing
            barmode='group',  # Group bars to compare different persons more easily
            width=WIDTH,  # Set the width of the image
            height=HEIGHT  # Set the height of the image)
        )

        fig.update_traces(texttemplate='%{y}', textposition='outside')
        
        fig.write_image(f"{self.plots_folder}/{title}_distribution.png")
    
    def plot_top_30_dates(self):
        # Sort dates by count and select the top 30
        sorted_dates = sorted(self.date_dict.items(), key=lambda x: x[1], reverse=True)[:30]
        dates, counts = zip(*sorted_dates)
        
        # Create a DataFrame
        df = pd.DataFrame({'Date': dates, 'Count': counts})
        
        # Create the bar chart with Plotly Express
        fig = px.bar(df, x='Date', y='Count', title='Top 30 Dates with Most Messages',
                    labels={'Count': 'Number of Messages', 'Date': 'Date'},
                    color='Count', color_continuous_scale='viridis',
                    text='Count')  # Show counts on the bars
        
        # Update layout to treat x-axis as categorical and for better readability
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Number of Messages',
            xaxis_title_font=dict(size=AXIS_SIZE, family='Arial', color='DarkSlateGray'),
            yaxis_title_font=dict(size=AXIS_SIZE, family='Arial', color='DarkSlateGray'),
            title_font=dict(size=TITLE_SIZE, family='Arial', color='DarkSlateGray'),
            xaxis=dict(
                tickangle=-45,  # Rotate x-axis labels for better readability
                tickfont=dict(size=TICK_SIZE, color='Black'),
                type='category'  # Treat x-axis as categorical labels
            ),
            yaxis=dict(
                tickfont=dict(size=TICK_SIZE, color='Black'),
                showgrid=True,
                gridcolor='LightGray'
            ),
            plot_bgcolor='rgba(243, 243, 243, 0.5)',  # Light background color for the entire chart
            paper_bgcolor='rgba(255, 255, 255, 0.9)',  # Slightly off-white plot background
            margin=dict(l=80, r=20, t=60, b=100),  # Adjust margins for better spacing
            width=WIDTH,  # Set the width of the image
            height=HEIGHT  # Set the height of the image
        )
        
        # Adjust the trace to ensure labels are outside the bars
        fig.update_traces(
            texttemplate='%{y}', 
            textposition='outside',  # Place the labels outside the bars
            cliponaxis=False  # Ensure labels are not clipped by the axis
        )
        
        # Save the plot as an image
        fig.write_image(f"{self.plots_folder}/top_30_dates.png")


    def plot_hour_distribution(self):
        hours = list(self.hour_dict.keys())
        counts = list(self.hour_dict.values())
        df = pd.DataFrame({'Hour': hours, 'Count': counts})
        
        fig = px.bar(df, x='Hour', y='Count', title='Messages Distribution by Hour',
                    labels={'Count': 'Number of Messages', 'Hour': 'Hour of the Day'},
                    color='Count', color_continuous_scale='Blues')
        
        fig.update_layout(
            xaxis_title='Hour of the Day',
            yaxis_title='Number of Messages',
            xaxis_title_font=dict(size=AXIS_SIZE),
            yaxis_title_font=dict(size=AXIS_SIZE),
            title_font=dict(size=18)
        )
        
        fig.update_traces(texttemplate='%{y}', textposition='outside')
        
        fig.write_image(os.path.join(self.plots_folder, 'hour_distribution.png'))
    
    def plot_month_distribution(self):
        months = list(self.month_dict.keys())
        counts = list(self.month_dict.values())
        df = pd.DataFrame({'Month': months, 'Count': counts})
    
        fig = px.bar(df, x='Month', y='Count', title='Messages Distribution by Month',
                    labels={'Count': 'Number of Messages', 'Month': 'Month'},
                    color='Count', color_continuous_scale='Greens')
        
        fig.update_layout(
            xaxis_title='Month',
            yaxis_title='Number of Messages',
            xaxis_title_font=dict(size=AXIS_SIZE),
            yaxis_title_font=dict(size=AXIS_SIZE),
            title_font=dict(size=18)
        )
        
        fig.update_traces(texttemplate='%{y}', textposition='outside')
        
        fig.write_image(os.path.join(self.plots_folder, 'month_distribution.png'))
    
    def plot_year_distribution(self):
        years = list(self.year_dict.keys())
        counts = list(self.year_dict.values())

        df = pd.DataFrame({'Year': years, 'Count': counts})
        
        # Create the bar chart with Plotly Express
        fig = px.bar(df, x='Year', y='Count', title='Messages Distribution by Year',
                    labels={'Count': 'Number of Messages', 'Year': 'Year'},
                    color='Count', color_continuous_scale='Reds', 
                    text='Count')
        
        # Update layout for better readability and appearance
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Number of Messages',
            xaxis_title_font=dict(size=AXIS_SIZE, family='Arial', color='DarkSlateGray'),
            yaxis_title_font=dict(size=AXIS_SIZE, family='Arial', color='DarkSlateGray'),
            title_font=dict(size=18, family='Arial', color='DarkSlateGray'),
            xaxis=dict(
                tickangle=-45,  # Rotate x-axis labels
                tickfont=dict(size=TICK_SIZE, color='Black')
            ),
            yaxis=dict(
                tickfont=dict(size=TICK_SIZE, color='Black'),
                showgrid=True,
                gridcolor='LightGray'
            ),
            plot_bgcolor='rgba(243, 243, 243, 0.5)',  # Light background color for the entire chart
            paper_bgcolor='rgba(255, 255, 255, 0.9)',  # Slightly off-white plot background
            margin=dict(l=80, r=20, t=60, b=100),  # Adjust margins for better spacing
            width=WIDTH,  # Set the width of the image
            height=HEIGHT  # Set the height of the image)
        )
        
        # Add data labels
        fig.update_traces(
            texttemplate='%{text}',  # Show the count value on each bar
            textposition='outside',  # Place text outside the bars for visibility
            textfont=dict(size=TICK_SIZE, color='Black')  # Adjust font size and color for text
        )
        
        # Save the plot as an image
        fig.write_image(os.path.join(self.plots_folder, 'year_distribution.png'))
    
    def plot_date_distribution(self):
        dates = list(self.date_dict.keys())
        counts = list(self.date_dict.values())

        df = pd.DataFrame({'Date': dates, 'Count': counts})
        
        # Create the line plot with Plotly Express
        fig = px.line(df, x='Date', y='Count', title='Messages Distribution by Date',
                    labels={'Count': 'Number of Messages', 'Date': 'Date'},
                    markers=True, line_shape='linear', color_discrete_sequence=['orange'])
        
        # Update layout for better readability and appearance
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Number of Messages',
            xaxis_title_font=dict(size=AXIS_SIZE, family='Arial', color='DarkSlateGray'),
            yaxis_title_font=dict(size=AXIS_SIZE, family='Arial', color='DarkSlateGray'),
            title_font=dict(size=18, family='Arial', color='DarkSlateGray'),
            xaxis=dict(
                tickangle=-45,  # Rotate x-axis labels
                tickfont=dict(size=TICK_SIZE, color='Black')
            ),
            yaxis=dict(
                tickfont=dict(size=TICK_SIZE, color='Black'),
                showgrid=True,
                gridcolor='LightGray'
            ),
            plot_bgcolor='rgba(243, 243, 243, 0.5)',  # Light background color for the entire chart
            paper_bgcolor='rgba(255, 255, 255, 0.9)',  # Slightly off-white plot background
            margin=dict(l=80, r=20, t=60, b=100),  # Adjust margins for better spacing
            width=WIDTH,  # Set the width of the image
            height=HEIGHT  # Set the height of the image)
        )
        
        # Save the plot as an image
        fig.write_image(os.path.join(self.plots_folder, 'date_distribution.png'))
    def plot_name_distribution(self):
        names = list(self.name_dict.keys())
        counts = list(self.name_dict.values())

        df = pd.DataFrame({'Person': names, 'Count': counts})
    
        fig = px.bar(df, x='Person', y='Count', title='Messages Distribution by Person',
                    labels={'Count': 'Number of Messages', 'Person': 'Person'},
                    color='Count', color_continuous_scale='Purples', 
                    text='Count')
        
        fig.update_layout(
            xaxis_title='Person',
            yaxis_title='Number of Messages',
            xaxis_title_font=dict(size=AXIS_SIZE, family='Arial', color='DarkSlateGray'),
            yaxis_title_font=dict(size=AXIS_SIZE, family='Arial', color='DarkSlateGray'),
            title_font=dict(size=18, family='Arial', color='DarkSlateGray'),
            xaxis=dict(
                tickangle=-45,
                tickfont=dict(size=TICK_SIZE, color='Black')
            ),
            yaxis=dict(
                tickfont=dict(size=TICK_SIZE, color='Black'),
                showgrid=True,
                gridcolor='LightGray'
            ),
            plot_bgcolor='rgba(243, 243, 243, 0.5)',
            paper_bgcolor='rgba(255, 255, 255, 0.9)',
            margin=dict(l=80, r=20, t=60, b=100),
            width=WIDTH,
            height=HEIGHT
        )
        
        fig.update_traces(
            texttemplate='%{text}',
            textposition='outside',
            textfont=dict(size=TICK_SIZE, color='Black')
        )
        
        fig.write_image(os.path.join(self.plots_folder, 'name_distribution.png'))
    
    def plot_top_25_words_by_person(self):
        """Plot and save the top 25 most common words for each person."""
        for person in self.name_dict.keys():
            word_counts = Counter({word: self.person_word_count_dict[word][person] for word in self.person_word_count_dict if self.person_word_count_dict[word][person] > 0})
            most_common_words = word_counts.most_common(25)
            if most_common_words:
                words, counts = zip(*most_common_words)
                df = pd.DataFrame({'Word': words, 'Count': counts})
                
                fig = px.bar(df, x='Word', y='Count', title=f'Top 25 Most Common Words Used by {person}',
                            labels={'Count': 'Occurrences', 'Word': 'Word'},
                            color='Count', color_continuous_scale='Blues',
                            text='Count')
                
                fig.update_layout(
                    xaxis_title='Word',
                    yaxis_title='Occurrences',
                    xaxis_title_font=dict(size=AXIS_SIZE, family='Arial', color='DarkSlateGray'),
                    yaxis_title_font=dict(size=AXIS_SIZE, family='Arial', color='DarkSlateGray'),
                    title_font=dict(size=18, family='Arial', color='DarkSlateGray'),
                    xaxis=dict(
                        tickangle=-45,
                        tickfont=dict(size=TICK_SIZE, color='Black')
                    ),
                    yaxis=dict(
                        tickfont=dict(size=TICK_SIZE, color='Black'),
                        showgrid=True,
                        gridcolor='LightGray'
                    ),
                    plot_bgcolor='rgba(243, 243, 243, 0.5)',
                    paper_bgcolor='rgba(255, 255, 255, 0.9)',
                    margin=dict(l=80, r=20, t=60, b=100),
                    width=WIDTH,
                    height=HEIGHT
                )
                
                fig.update_traces(
                    texttemplate='%{text}',
                    textposition='outside',
                    textfont=dict(size=TICK_SIZE, color='Black')
                )
            os.makedirs(f'{self.plots_folder}/top25', exist_ok=True)
            fig.write_image(os.path.join(self.plots_folder, 'top25', f'{person}_top_25_words.png'))
                
    def plot_top_25_words_overall(self):
        total_word_counts = Counter()
        for word in self.person_word_count_dict:
            total_word_counts[word] = self.person_word_count_dict[word]['count']
        
        most_common_words = total_word_counts.most_common(25)
        if most_common_words:
            words, counts = zip(*most_common_words)
            df = pd.DataFrame({'Word': words, 'Count': counts})
            
            fig = px.bar(df, x='Word', y='Count', title='Top 25 Most Common Words Overall',
                        labels={'Count': 'Occurrences', 'Word': 'Word'},
                        color='Count', color_continuous_scale='Reds',
                        text='Count')
            
            fig.update_layout(
                xaxis_title='Word',
                yaxis_title='Occurrences',
                xaxis_title_font=dict(size=AXIS_SIZE, family='Arial', color='DarkSlateGray'),
                yaxis_title_font=dict(size=AXIS_SIZE, family='Arial', color='DarkSlateGray'),
                title_font=dict(size=18, family='Arial', color='DarkSlateGray'),
                xaxis=dict(
                    tickangle=-45,
                    tickfont=dict(size=TICK_SIZE, color='Black')
                ),
                yaxis=dict(
                    tickfont=dict(size=TICK_SIZE, color='Black'),
                    showgrid=True,
                    gridcolor='LightGray'
                ),
                plot_bgcolor='rgba(243, 243, 243, 0.5)',
                paper_bgcolor='rgba(255, 255, 255, 0.9)',
                margin=dict(l=80, r=20, t=60, b=100),
                width=WIDTH,
                height=HEIGHT
            )
            
            fig.update_traces(
                texttemplate='%{text}',
                textposition='outside',
                textfont=dict(size=TICK_SIZE, color='Black')
            )
            
            fig.write_image(os.path.join(self.plots_folder, 'top_25_words_overall.png'))
    
    def plot_top_25_two_word_phrases(self):
        sorted_phrases = sorted(self.two_word_dict.items(), key=lambda x: x[1]['count'], reverse=True)[:25]
        phrases, counts = zip(*[(phrase, data['count']) for phrase, data in sorted_phrases])

        df = pd.DataFrame({'Phrase': phrases, 'Count': counts})
        
        fig = px.bar(df, y='Count', x='Phrase', title='Top 25 Two-Word Phrases',
                    labels={'Count': 'Number of Occurrences', 'Phrase': '2-Word Phrase'},
                    color='Count', color_continuous_scale='viridis',
                    text='Count')
        
        fig.update_layout(
            yaxis_title='Number of Occurrences',
            xaxis_title='2-Word Phrase',
            xaxis_title_font=dict(size=AXIS_SIZE, family='Arial', color='DarkSlateGray'),
            yaxis_title_font=dict(size=AXIS_SIZE, family='Arial', color='DarkSlateGray'),
            title_font=dict(size=18, family='Arial', color='DarkSlateGray'),
            xaxis=dict(
                tickangle=-45,
                tickfont=dict(size=TICK_SIZE, color='Black')
            ),
            yaxis=dict(
                tickfont=dict(size=TICK_SIZE, color='Black'),
                showgrid=True,
                gridcolor='LightGray'
            ),
            plot_bgcolor='rgba(243, 243, 243, 0.5)',
            paper_bgcolor='rgba(255, 255, 255, 0.9)',
            margin=dict(l=80, r=20, t=60, b=100),
            width=WIDTH,
            height=HEIGHT
        )
        
        fig.update_traces(
            texttemplate='%{text}',
            textposition='outside',
            textfont=dict(size=TICK_SIZE, color='Black')
        )
        
        fig.write_image(os.path.join(self.plots_folder, 'top_25_two_word_phrases.png'))
    def plot_top_25_three_word_phrases(self):
        sorted_phrases = sorted(self.three_word_dict.items(), key=lambda x: x[1]['count'], reverse=True)[:25]
        phrases, counts = zip(*[(phrase, data['count']) for phrase, data in sorted_phrases])

        df = pd.DataFrame({'Phrase': phrases, 'Count': counts})
        
        fig = px.bar(df, y='Count', x='Phrase', title='Top 25 Three-Word Phrases',
                    labels={'Count': 'Number of Occurrences', 'Phrase': '3-Word Phrase'},
                    color='Count', color_continuous_scale='plasma',
                    text='Count')
        
        # Update layout to adjust axis titles, font, and background colors
        fig.update_layout(
            xaxis_title='3-Word Phrase',
            yaxis_title='Number of Occurrences',
            xaxis_title_font=dict(size=AXIS_SIZE, family='Arial', color='DarkSlateGray'),
            yaxis_title_font=dict(size=AXIS_SIZE, family='Arial', color='DarkSlateGray'),
            title_font=dict(size=18, family='Arial', color='DarkSlateGray'),
            xaxis=dict(
                tickangle=-45,  # Rotate x-axis labels for better readability
                tickfont=dict(size=TICK_SIZE, color='Black')
            ),
            yaxis=dict(
                tickfont=dict(size=TICK_SIZE, color='Black'),
                showgrid=True,
                gridcolor='LightGray'
            ),
            plot_bgcolor='rgba(243, 243, 243, 0.5)',
            paper_bgcolor='rgba(255, 255, 255, 0.9)',
            margin=dict(l=80, r=20, t=60, b=150),  # Adjust bottom margin for rotated labels
            width=WIDTH,
            height=HEIGHT
        )

        # Update traces for the text position
        fig.update_traces(
            texttemplate='%{text}',
            textposition='outside',
            textfont=dict(size=TICK_SIZE, color='Black')
        )

        # Save the plot as an image
        fig.write_image(os.path.join(self.plots_folder, 'top_25_three_word_phrases.png'))