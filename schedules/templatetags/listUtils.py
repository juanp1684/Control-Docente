from django import template

register = template.Library()

@register.simple_tag
def filter_report_list_year(report_list, year):
    reports_in_year = list(filter(lambda report: report['report_time'].year == year, report_list))
    report_lists_by_month = []
    for i in range(1, 13):
        report_lists_by_month.append([report for report in reports_in_year if report['report_time'].month == i])
    report_counts = [len(reports_by_month) for reports_by_month in report_lists_by_month]
    return report_counts

@register.simple_tag
def filter_report_list_month(report_list, month, year):
    reports_in_year = list(filter(lambda report: report['report_time'].year == year and report['report_time'].month == month, report_list))
    report_lists_by_month = []
    for i in range(1, 31):
        report_lists_by_month.append([report for report in reports_in_year if report['report_time'].day == i])
    report_counts = [len(reports_by_month) for reports_by_month in report_lists_by_month]
    return report_counts

@register.simple_tag
def create_reports_count_lists(all_reports, year, month):
    failed_reports = list(filter(lambda report: report['report_type'] == 'fallido', all_reports))
    missed_reports = list(filter(lambda report: report['report_type'] == 'omision', all_reports))
    succesful_reports = list(filter(lambda report: report['report_type'] == 'completado', all_reports))
    count_lists = []
    count_lists.append(filter_report_list_year(failed_reports, year))
    count_lists.append(filter_report_list_year(missed_reports, year))
    count_lists.append(filter_report_list_year(succesful_reports, year))
    count_lists.append(filter_report_list_month(failed_reports, month, year))
    count_lists.append(filter_report_list_month(missed_reports, month, year))
    count_lists.append(filter_report_list_month(succesful_reports, month, year))
    return count_lists
