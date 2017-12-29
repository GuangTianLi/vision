import csv
import logging
import os
import pandas as pd
import pygal

from vision.datareportcenter import DataReportCenter

logger = logging.getLogger(__name__)


class CreatorRunner(DataReportCenter):
    """
    A class to run multiple vision reator in a process simultaneously.

    """

    def create_csv(self, data):
        '''
        Use some data like this {key: value, } to create csv file
        Returns
        -------

        '''
        if data:
            os.makedirs(os.path.dirname(self.csv_file), exist_ok=True)
            logger.info("Create file: {}".format(self.csv_file))
            with open(self.csv_file, self.settings.get("FILE_MODES"), encoding=self.settings.get("FILE_DECODE"), errors='ignore') as out:
                fieldnames, content = data
                csv_out = csv.DictWriter(out, fieldnames=fieldnames)
                csv_out.writeheader()
                logger.info("Write data: {}".format(content))
                csv_out.writerows(content)

    def create_svg(self, style):
        '''
        Use some csv file by X_AXIS's key and Y_AXIS's key to create SVG file
        Returns
        -------

        '''
        if not self.settings.get("X_AXIS", None):
            raise ValueError("%s must have a X_AXIS" % type(self).__name__)
        elif not self.settings.get("Y_AXIS", None):
            raise ValueError("%s must have a Y_AXIS" % type(self).__name__)
        else:
            for csv_file, svg_file in self.file_dict.items():
                logger.info(
                    "Create {} ----------->   {}".format(self.csv_file, self.svg_file.split('/')[-1]))
                budget = pd.read_csv(
                    csv_file, encoding=self.settings.get("FILE_DECODE"))
                if style == 1:
                    bar_chart = pygal.Bar(
                        legend_at_bottom=True,
                        human_readable=True,
                        title=self.settings.get(
                            "DATA_REPORT_TITLE",
                            self.data_report.name))
                elif style == 2:
                    bar_chart = pygal.Pie(
                        legend_at_bottom=True,
                        human_readable=True,
                        title=self.settings.get(
                            "DATA_REPORT_TITLE",
                            self.data_report.name))
                else:
                    bar_chart = pygal.HorizontalBar(
                        legend_at_bottom=True, human_readable=True, title=self.settings.get(
                            "DATA_REPORT_TITLE", self.data_report.name))

                for index, row in budget.iterrows():
                    bar_chart.add(row[self.settings.get("X_AXIS")],
                                  row[self.settings.get("Y_AXIS")])
                bar_chart.render_to_file(svg_file)

    def create(self, data_report_name):
        """
        This method is to create csv and svg file
        Parameters
        ----------
        data_report_name : DataReport class's name

        Returns
        -------
        DataReport class
        """
        for data in self.get_data_from_data_report(data_report_name):
            self.create_csv(data)
        if self.data_report.settings.get("SVG_FILE"):
            self.create_svg(self.data_report.settings.get("SVG_STYLE"))
