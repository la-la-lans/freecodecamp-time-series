import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('/workspace/boilerplate-page-view-time-series-visualizer/fcc-forum-pageviews.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025))&(df['value'] <= df['value'].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(20,8))
    df.plot(kind = 'line', ax = ax)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar.index = pd.to_datetime(df_bar.index)
    df_bar['month'] = df_bar.index.month
    df_bar['year'] = df_bar.index.year
    df_bar = df_bar.groupby(['year', 'month'], sort=False)['value'].mean().astype(int)
    df_bar = df_bar.reset_index()
    df_bar = df_bar.pivot(index='year', columns='month', values='value')

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(10, 6))  
    df_bar.plot(kind='bar', ax=ax)
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 
                   'July', 'August', 'September', 'October', 'November', 'December']
    
    ax.legend(title='Month', labels=month_names, loc='upper left', frameon=False)

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)

    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    fig, axes = plt.subplots(1,2)
    fig.set_figwidth(20)
    fig.set_figheight(10)
    sns.boxplot(data=df_box, x = 'year', y = 'value', hue = 'year' ,ax=axes[0])
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')
    axes[0].set_title('Year-wise Box Plot (Trend)')
    sns.boxplot(data=df_box, x = 'month', y = 'value', hue ='month', order = month_order, ax= axes[1])
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')
    axes[1].set_title('Month-wise Box Plot (Seasonality)')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
