"""
Dynamic dashboard visualizations using Python libraries.
Supports Plotly, Panel, Voila, and other dynamic visualization frameworks.
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import panel as pn
import streamlit as st
from typing import Optional, Dict, Any, List, Callable
from pathlib import Path


class PlotlyDashboard:
    """
    I am a class for creating interactive Plotly dashboards.
    I provide methods to add various charts and export them to HTML.
    """

    def __init__(self, title: str = "Dashboard"):
        """
        I initialize the Plotly dashboard with a title.

        Args:
            title: Dashboard title.
        """
        self.title = title
        self.figures = []

    def add_line_chart(
        self, df: pd.DataFrame, x_col: str, y_cols: List[str], name: Optional[str] = None
    ) -> None:
        """
        I add a line chart to the dashboard.

        Args:
            df: Data for the chart.
            x_col: Column for x-axis.
            y_cols: Columns for y-axis.
            name: Chart name.
        """
        fig = px.line(df, x=x_col, y=y_cols, title=name or self.title)
        self.figures.append(fig)

    def add_bar_chart(self, df: pd.DataFrame, x_col: str, y_col: str, name: Optional[str] = None) -> None:
        """
        I add a bar chart to the dashboard.

        Args:
            df: Data for the chart.
            x_col: Column for x-axis.
            y_col: Column for y-axis.
            name: Chart name.
        """
        fig = px.bar(df, x=x_col, y=y_col, title=name or self.title)
        self.figures.append(fig)

    def add_scatter_plot(
        self,
        df: pd.DataFrame,
        x_col: str,
        y_col: str,
        size_col: Optional[str] = None,
        color_col: Optional[str] = None,
        name: Optional[str] = None,
    ) -> None:
        """
        I add a scatter plot to the dashboard.

        Args:
            df: Data for the chart.
            x_col: Column for x-axis.
            y_col: Column for y-axis.
            size_col: Optional column for marker size.
            color_col: Optional column for marker color.
            name: Chart name.
        """
        fig = px.scatter(df, x=x_col, y=y_col, size=size_col, color=color_col, title=name or self.title)
        self.figures.append(fig)

    def add_heatmap(self, data: pd.DataFrame, name: Optional[str] = None) -> None:
        """
        I add a heatmap to the dashboard.

        Args:
            data: Data for heatmap.
            name: Chart name.
        """
        fig = px.imshow(data, title=name or self.title)
        self.figures.append(fig)

    def add_table(self, data: pd.DataFrame, name: Optional[str] = None) -> None:
        """
        I add a data table to the dashboard.

        Args:
            data: Data to display.
            name: Table name.
        """
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(data.columns), fill_color='paleturquoise', align='left'),
            cells=dict(values=[data[col] for col in data.columns], fill_color='lavender', align='left')
        )])
        fig.update_layout(title=name or self.title)
        self.figures.append(fig)

    def render(self) -> Any:
        """
        I render all figures in the dashboard.

        Returns:
            List: List of plotly figures.
        """
        return self.figures

    def save_html(self, output_path: str) -> None:
        """
        I save the dashboard as an HTML file.

        Args:
            output_path: Path to save HTML file.
        """
        with open(output_path, "w") as f:
            f.write(f"<html><head><title>{self.title}</title></head><body>")
            f.write(f"<h1>{self.title}</h1>")
            for fig in self.figures:
                f.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))
            f.write("</body></html>")


class PanelDashboard:
    """
    I am a class for creating dynamic dashboards using Panel.
    I support interactive widgets and real-time updates.
    """

    def __init__(self, title: str = "Interactive Dashboard"):
        """
        I initialize the Panel dashboard with a title.

        Args:
            title: Dashboard title.
        """
        self.title = title
        self.layout = pn.Column(f"# {self.title}")
        self.widgets = {}

    def add_widget(
        self, widget_type: str, name: str, options: Optional[List] = None, **kwargs
    ) -> Any:
        """
        I add an interactive widget to the dashboard.

        Args:
            widget_type: Type of widget ('select', 'slider', 'checkbox', etc.).
            name: Widget name.
            options: Widget options.

        Returns:
            Widget instance.
        """
        if widget_type == "select":
            widget = pn.widgets.Select(name=name, options=options or [], **kwargs)
        elif widget_type == "slider":
            widget = pn.widgets.FloatSlider(name=name, **kwargs)
        elif widget_type == "checkbox":
            widget = pn.widgets.Checkbox(name=name, **kwargs)
        else:
             widget = pn.widgets.StaticText(name=name, value="Unsupported widget")
        
        self.widgets[name] = widget
        self.layout.append(widget)
        return widget

    def add_plot(self, plot_function: Callable, params: Optional[Dict] = None) -> None:
        """
        I add a plot that responds to widget changes.

        Args:
            plot_function: Function that generates the plot.
            params: Parameters mapping to widgets.
        """
        interactive_plot = pn.bind(plot_function, **(params or {}))
        self.layout.append(interactive_plot)

    def add_data_table(self, data: pd.DataFrame, name: Optional[str] = None) -> None:
        """
        I add an interactive data table to the dashboard.

        Args:
            data: Data to display.
            name: Table name.
        """
        if name: self.layout.append(f"### {name}")
        self.layout.append(pn.widgets.Tabulator(data, pagination='remote', page_size=10))

    def add_metric_card(
        self, value: Any, label: str, color: Optional[str] = None
    ) -> None:
        """
        I add a metric card display to the dashboard.

        Args:
            value: Metric value.
            label: Metric label.
            color: Optional card color.
        """
        card = pn.indicators.Number(
            name=label, value=value, format='{value}', 
            colors=[(100, color or 'green')]
        )
        self.layout.append(card)

    def serve(self, port: int = 5006, show: bool = True) -> Any:
        """
        I serve the Panel dashboard on a local port.

        Args:
            port: Port number.
            show: Whether to open browser automatically.

        Returns:
            Server instance.
        """
        return self.layout.show(port=port, title=self.title)

    def save(self, output_path: str) -> None:
        """
        I save the Panel dashboard as an HTML file.

        Args:
            output_path: Path to save dashboard.
        """
        self.layout.save(output_path, title=self.title)


class StreamlitDashboard:
    """
    I am a class for creating dashboards using Streamlit.
    """

    def __init__(self, title: str = "Dashboard"):
        """
        I initialize the Streamlit dashboard with a title.

        Args:
            title: Dashboard title.
        """
        self.title = title
        st.set_page_config(page_title=self.title)
        st.title(self.title)

    def add_metric(self, label: str, value: Any, delta: Optional[Any] = None) -> None:
        """
        I add a metric display to the Streamlit dashboard.

        Args:
            label: Metric label.
            value: Metric value.
            delta: Optional change value.
        """
        st.metric(label=label, value=value, delta=delta)

    def add_chart(self, chart_type: str, data: pd.DataFrame, **kwargs) -> None:
        """
        I add a chart to the Streamlit dashboard.

        Args:
            chart_type: Type of chart ('line', 'bar', 'scatter').
            data: Data for the chart.
            **kwargs: Additional chart parameters.
        """
        if chart_type == "line":
            st.line_chart(data, **kwargs)
        elif chart_type == "bar":
            st.bar_chart(data, **kwargs)
        elif chart_type == "scatter":
            st.scatter_chart(data, **kwargs)
        elif chart_type == "plotly":
             st.plotly_chart(kwargs.get("figure"), use_container_width=True)

    def add_dataframe(self, data: pd.DataFrame, page_size: int = 10) -> None:
        """
        I add an interactive dataframe to the Streamlit dashboard.

        Args:
            data: Data to display.
            page_size: Rows per page (not directly supported by st.dataframe but good for logic).
        """
        st.dataframe(data, use_container_width=True)

    def add_filter(self, column: str, data: pd.DataFrame) -> Any:
        """
        I add a filter widget to the Streamlit sidebar.

        Args:
            column: Column to filter on.
            data: Data for filter options.

        Returns:
            Selected filter value.
        """
        options = ["All"] + list(data[column].unique())
        selected = st.sidebar.selectbox(f"Filter by {column}", options)
        return selected

    def run(self) -> None:
        """
        I run the Streamlit dashboard.
        """
        # Streamlit script is executed from top to bottom
        pass
