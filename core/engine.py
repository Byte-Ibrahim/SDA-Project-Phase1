from typing import List, Any, Dict
from functools import reduce
from core.contracts import DataSink


class TransformationEngine:
    """
    Core Engine.  Knows NOTHING about file formats or output destinations.
    It only knows about a DataSink it received at runtime.
    """


    def __init__(self, sink: DataSink, config: dict):
        self.sink = sink
        self.config = config

    #  Entry-point called by Input plugins (satisfies PipelineService)    #
 
    def execute(self, raw_data: List[Any]) -> None:
        cfg = self.config.get("filters", {})
        continent   = cfg.get("continent", "")
        year_start  = int(cfg.get("year_start", 0))
        year_end    = int(cfg.get("year_end", 9999))
        decline_yrs = int(cfg.get("decline_years", 5))


        continents = list(map(str.strip, continent.split("&"))) if continent else []

        filtered = list(filter(
            lambda r: (r["continent"] in continents or not continents)
                      and year_start <= r["year"] <= year_end
                      and r["gdp"] is not None,
            raw_data
        ))

        year = int(cfg.get("year", year_end))
        self.sink.write("top10",    self.top10(raw_data, continents, year if year != 0 else year_end ))
        self.sink.write("bottom10", self.bottom10(raw_data, continents, year if year != 0 else year_end))
        self.sink.write("gdp_growth_rate", self.gdp_growth_rate(filtered, continents, year_start, year_end))
        self.sink.write("avg_gdp_continent", self.avg_gdp_by_continent(raw_data, year_start, year_end))
        self.sink.write("global_gdp_trend",  self.global_gdp_trend(raw_data, year_start, year_end))
        self.sink.write("fastest_growing",   self.fastest_growing_continent(raw_data, year_start, year_end))
        self.sink.write("consistent_decline", self.consistent_decline(raw_data, continents, year_end, decline_yrs))
        self.sink.write("continent_contribution", self.continent_contribution(raw_data, year_start, year_end))



    def gdp_by_country_year(self, data, continents, year):
        """Return {country: gdp} for a specific year filtered by continents."""
        year_data = filter(
            lambda r: r["year"] == year
                      and (r["continent"] in continents or not continents)
                      and r["gdp"] is not None,
            data
        )
        return dict(map(lambda r: (r["country"], r["gdp"]), year_data))

    def top10(self, data, continents, year):
        gdp_map = self.gdp_by_country_year(data, continents, year)
        sorted_countries = sorted(gdp_map.items(), key=lambda x: x[1], reverse=True)
        return sorted_countries[:10]

    def bottom10(self, data, continents, year):
        gdp_map = self.gdp_by_country_year(data, continents, year)
        sorted_countries = sorted(gdp_map.items(), key=lambda x: x[1])
        return sorted_countries[:10]

    def gdp_growth_rate(self, filtered, continents, year_start, year_end):

        start_map = self.gdp_by_country_year(filtered, continents, year_start)
        end_map   = self.gdp_by_country_year(filtered, continents, year_end)

        common = set(start_map.keys()) & set(end_map.keys())

        growth = list(map(
            lambda country: (
                country,
                round(((end_map[country] - start_map[country]) / start_map[country]) * 100, 2)
                if start_map[country] != 0 else 0.0
            ),
            common
        ))
        return sorted(growth, key=lambda x: x[1], reverse=True)

    def avg_gdp_by_continent(self, data, year_start, year_end):
        
        in_range = list(filter(
            lambda r: year_start <= r["year"] <= year_end and r["gdp"] is not None,
            data
        ))
        continents = sorted(set(map(lambda r: r["continent"], in_range)))

        def avg_for_cont(cont):
            vals = list(map(lambda r: r["gdp"],
                            filter(lambda r: r["continent"] == cont, in_range)))
            return (cont, round(reduce(lambda a, b: a + b, vals) / len(vals), 2) if vals else 0)

        return list(map(avg_for_cont, continents))

    def global_gdp_trend(self, data, year_start, year_end):
    
        in_range = list(filter(
            lambda r: year_start <= r["year"] <= year_end and r["gdp"] is not None,
            data
        ))
        years = sorted(set(map(lambda r: r["year"], in_range)))

        def total_for_year(yr):
            vals = list(map(lambda r: r["gdp"],
                            filter(lambda r: r["year"] == yr, in_range)))
            return (yr, round(reduce(lambda a, b: a + b, vals, 0), 2))

        return list(map(total_for_year, years))

    def fastest_growing_continent(self, data, year_start, year_end):
        
        def total_gdp(cont, year):
            vals = list(map(lambda r: r["gdp"],
                            filter(lambda r: r["continent"] == cont
                                            and r["year"] == year
                                            and r["gdp"] is not None, data)))
            return reduce(lambda a, b: a + b, vals, 0)

        continents = sorted(set(map(lambda r: r["continent"],
                                    filter(lambda r: r["gdp"] is not None, data))))

        growth = list(map(
            lambda cont: (
                cont,
                round(((total_gdp(cont, year_end) - total_gdp(cont, year_start))
                       / total_gdp(cont, year_start)) * 100, 2)
                if total_gdp(cont, year_start) != 0 else 0.0
            ),
            continents
        ))
        return max(growth, key=lambda x: x[1])

    def consistent_decline(self, data, continents, year_end, n_years):
        
        years = list(range(year_end - n_years + 1, year_end + 1))

        def get_gdp(country, year):
            rows = list(filter(lambda r: r["country"] == country
                                        and r["year"] == year
                                        and r["gdp"] is not None, data))
            return rows[0]["gdp"] if rows else None

        countries = sorted(set(map(lambda r: r["country"],
                                   filter(lambda r: (r["continent"] in continents or not continents)
                                                    and r["gdp"] is not None, data))))

        def is_declining(country):
            gdps = list(map(lambda y: get_gdp(country, y), years))
            if None in gdps:
                return False
            return all(gdps[i] > gdps[i + 1] for i in range(len(gdps) - 1))

        return list(filter(is_declining, countries))

    def continent_contribution(self, data, year_start, year_end):
        
        in_range = list(filter(
            lambda r: year_start <= r["year"] <= year_end and r["gdp"] is not None,
            data
        ))
        total_global = reduce(lambda a, b: a + b,
                              map(lambda r: r["gdp"], in_range), 0)

        continents = sorted(set(map(lambda r: r["continent"], in_range)))

        def contribution(cont):
            cont_gdp = reduce(lambda a, b: a + b,
                              map(lambda r: r["gdp"],
                                  filter(lambda r: r["continent"] == cont, in_range)), 0)
            pct = round((cont_gdp / total_global) * 100, 2) if total_global else 0
            return (cont, pct)

        return list(map(contribution, continents))
