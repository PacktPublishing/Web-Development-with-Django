from plotly.offline import plot
import plotly.graph_objs as graphs


def generate_scatter_plot(x_axis, y_axis):
    """Generate a scatter plot for the provided x and y-axis values."""
    figure = graphs.Figure()
    scatter = graphs.Scatter(x=x_axis, y=y_axis)
    figure.add_trace(scatter)
    return plot(figure, output_type='div')

def generate_html(plot_html):
    """Generate an HTML page for the provided plot."""
    html_content = "<html><head><title>Plot Demo</title></head><body>{}</body></html>".format(plot_html)
    try:
        with open('plot_demo.html', 'w') as plot_file:
            plot_file.write(html_content)
    except (IOError, OSError) as file_io_error:
        print("Unable to generate plot file. Exception: {}".format(file_io_error))

if __name__ == '__main__':
    x = [1,2,3,4,5]
    y = [3,8,7,9,2]
    plot_html = generate_scatter_plot(x, y)
    generate_html(plot_html)
