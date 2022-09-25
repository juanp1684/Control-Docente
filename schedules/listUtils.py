


def filter_report_list_year(report_list, year):
    reports_in_year = list(filter(lambda report: report['report_time'].year == year, report_list))
    report_lists_by_month = []
    for i in range(1, 13):
        report_lists_by_month.append([report for report in reports_in_year if report['report_time'].month == i])
    report_counts = [len(reports_by_month) for reports_by_month in report_lists_by_month]
    return report_counts

def filter_report_list_month(report_list, month, year):
    reports_in_year = list(filter(lambda report: report['report_time'].year == year and report['report_time'].month == month, report_list))
    report_lists_by_month = []
    for i in range(1, 31):
        report_lists_by_month.append([report for report in reports_in_year if report['report_time'].day == i])
    report_counts = [len(reports_by_month) for reports_by_month in report_lists_by_month]
    return report_counts
