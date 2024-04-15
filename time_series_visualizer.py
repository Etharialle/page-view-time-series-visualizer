import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col='date', parse_dates=True)


# Clean data
df = df[
  (df["value"] >= df["value"].quantile(0.025)) &
  (df["value"] <= df["value"].quantile(0.975))]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(32, 10), dpi=100)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    sns.lineplot(data=df, legend=False, palette=['r'])

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year'] = df.index.year
    df_bar['Months'] = df.index.month
    
    df_bar = df_bar.groupby(['year', 'Months']).mean().reset_index()
    missing_data = {
        "year": [2016, 2016, 2016, 2016],
        "Months": ['January', 'February', 'March', 'April'],
        "value": [0, 0, 0, 0]
    }
    df_bar = pd.concat([pd.DataFrame(missing_data), df_bar])
    df_bar = df_bar.reset_index()

    month_legend = {
        1: 'January',
        2: 'February',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December'}
    df_bar.replace({'Months': month_legend}, inplace=True)

    # Draw bar plot
    #sns.barplot(x='year', y='value', data=df_bar, hue='Months',palette= 'bright')
    fig = sns.catplot(data=df_bar, x='year', y='value', hue='Months', kind='bar', palette='bright', legend=False)
    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(loc = 'upper left', title = 'Months', labels=month_legend.values())
    plt.show
    fig = fig.fig
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
    fig, axes = plt.subplots(1, 2, figsize=(32, 10), dpi=100)
    
    sns.boxplot(data=df_box, x="year", y="value", hue='year', palette=sns.color_palette('husl', n_colors=4), ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sns.boxplot(data=df_box, x="month", y="value", hue='month', palette=sns.color_palette(n_colors=12), order=month_order, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
