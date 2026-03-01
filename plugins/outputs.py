from typing import Any, List, Tuple
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# ═══════════════════════════════════════════════════════════════════════ #
#  ConsoleWriter (Standard Text Output)                                   #
# ═══════════════════════════════════════════════════════════════════════ #
class ConsoleWriter:
    TITLES = {
        "top10": "🏆 Top 10 Countries by GDP (Selected Continent & Year)",
        "bottom10": "📉 Bottom 10 Countries by GDP (Selected Continent & Year)",
        "gdp_growth_rate": "📈 GDP Growth Rate per Country (Selected Continent & Date Range)",
        "avg_gdp_continent": "🌍 Average GDP by Continent (Selected Date Range)",
        "global_gdp_trend": "🌐 Total Global GDP Trend (Selected Date Range)",
        "fastest_growing": "🚀 Fastest Growing Continent (Selected Date Range)",
        "consistent_decline": "⚠️ Countries with Consistent GDP Decline (Last X Years)",
        "continent_contribution": "🥧 Continent Contribution to Global GDP (Selected Date Range)",
    }

    def write(self, report_type: str, data: Any) -> None:
        title = self.TITLES.get(report_type, report_type.upper())
        print("\n" + "=" * 70)
        print(f"{title}")
        print("=" * 70)
        self.render(report_type, data)

    def render(self, report_type: str, data: Any) -> None:
        if not data:
            print("No data available.")
            return

        if report_type in ("top10", "bottom10", "gdp_growth_rate", "avg_gdp_continent", "global_gdp_trend", "continent_contribution"):
            for label, value in data:
                if report_type == "gdp_growth_rate":
                    print(f"{label:<35} {value:>10.2f}%")
                elif report_type == "continent_contribution":
                    print(f"{label:<25} {value:>8.2f}%")
                elif report_type == "global_gdp_trend":
                    print(f"Year {label}: ${value:,.2f}")
                else:
                    print(f"{label:<35} ${value:,.2f}")
        elif report_type == "fastest_growing":
            continent, rate = data
            print(f"{continent} -> {rate:.2f}% growth")
        elif report_type == "consistent_decline":
            for country in data:
                print(f"~ {country}")


# ═══════════════════════════════════════════════════════════════════════ #
#  GraphicsChartWriter (Matplotlib to Window/File)                       #
# ═══════════════════════════════════════════════════════════════════════ #
class GraphicsChartWriter:
    def write(self, report_type: str, data: Any) -> None:
        if not data: return
        fig, ax = self.create_figure(report_type, data)
        if fig:
            plt.show()

    def create_figure(self, report_type: str, data: Any):
        """Helper to build figures for both GraphicsWriter and StreamlitDashboard."""
        
        if not data:
            return None, None

        if report_type in ("top10", "bottom10"):
            labels, values = zip(*data)
            fig, ax = plt.subplots(figsize=(10, 6))
            color = "#2ecc71" if report_type == "top10" else "#e74c3c"
            ax.barh(labels, values, color=color)
            ax.xaxis.set_major_formatter(mtick.StrMethodFormatter("${x:,.0f}"))
            ax.set_xlabel("GDP (USD)")
            ax.set_title("Top 10 Countries by GDP" if report_type == "top10" else "Bottom 10 Countries by GDP")

        elif report_type == "gdp_growth_rate":
            labels, values = zip(*data)
            fig, ax = plt.subplots(figsize=(14, 6))
            colors = ["#27ae60" if v >= 0 else "#c0392b" for v in values]
            ax.bar(labels, values, color=colors)
            ax.set_ylabel("Growth Rate (%)")
            ax.set_title("GDP Growth Rate per Country")
            plt.xticks(rotation=90)

        elif report_type == "avg_gdp_continent":
            labels, values = zip(*data)
            fig, ax = plt.subplots(figsize=(10, 6))
            colors = ["#3498db", "#e67e22", "#9b59b6", "#1abc9c", "#e74c3c", "#f1c40f", "#34495e"]
            ax.bar(labels, values, color=colors[:len(labels)])
            ax.set_ylabel("Average GDP (USD)")
            ax.set_title("Average GDP by Continent")
            ax.yaxis.set_major_formatter(mtick.StrMethodFormatter("${x:,.0f}"))

        elif report_type == "global_gdp_trend":
            years, values = zip(*data)
            fig, ax = plt.subplots(figsize=(12, 5))
            ax.plot(years, values, marker="o", color="#2980b9")
            ax.set_xlabel("Year")
            ax.set_ylabel("Total Global GDP (USD)")
            ax.set_title("Total Global GDP Trend")
            ax.yaxis.set_major_formatter(mtick.StrMethodFormatter("${x:,.0f}"))

        elif report_type == "fastest_growing":
            continent, rate = data
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.bar([continent], [rate], color="#e67e22")
            ax.set_ylabel("Growth Rate (%)")
            ax.set_title("Fastest Growing Continent")

        elif report_type == "consistent_decline":
            if not data:
                return None, None
            fig, ax = plt.subplots(figsize=(8, max(4, len(data) * 0.5)))
            ax.barh(data, [1] * len(data), color="#c0392b")
            ax.set_xticks([])
            ax.set_title("Countries with Consistent GDP Decline")

        elif report_type == "continent_contribution":
            labels, values = zip(*data)
            total = sum(values)
            percentages = [round((v / total) * 100, 1) for v in values]
            fig, ax = plt.subplots(figsize=(9, 7))
            wedges, _ = ax.pie(values, startangle=90)
            legend_labels = [f"{label}: {pct}%" for label, pct in zip(labels, percentages)]
            ax.legend(wedges, legend_labels, title="Continents", loc="center left", bbox_to_anchor=(1, 0.5))
            ax.set_title("Continent Contribution to Global GDP")

        else:
            return None, None

        plt.tight_layout()
        return fig, ax


# ═══════════════════════════════════════════════════════════════════════ #
#  StreamlitDashboard (THE UI PLUGIN - Combining Tables & Graphics)       #
# ═══════════════════════════════════════════════════════════════════════ #
class StreamlitDashboard:
    def __init__(self):
        try:
            import streamlit as st
            import pandas as pd
            self.st, self.pd, self.ok = st, pd, True
            # We reuse the logic from GraphicsChartWriter
            self.graph_maker = GraphicsChartWriter()
        except ImportError:
            self.ok = False

    def write(self, report_type: str, data: Any) -> None:
        if not self.ok: return
        st = self.st
        
        # Dashboard Header
        st.title("🌍 GDP Global Analytics Dashboard")
        st.markdown("---")

        # Create a container for each report
        with st.container():
            st.subheader(f"📊 {report_type.replace('_', ' ').upper()}")
            
            col1, col2 = st.columns([1, 1.2]) # Table on left, Graph on right

            with col1:
                st.write("**Data Summary**")
                if isinstance(data, list) and len(data) > 0 and isinstance(data[0], (list, tuple)):
                    df = self.pd.DataFrame(data, columns=["Category", "Value"])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info(f"Result: {data}")

            with col2:
                st.write("**Visual Representation**")
                # Call our shared Matplotlib logic
                fig, ax = self.graph_maker.create_figure(report_type, data)
                if fig:
                    st.pyplot(fig)
                else:
                    st.write("Visual not applicable for this report type.")
        
        st.write("") # Padding