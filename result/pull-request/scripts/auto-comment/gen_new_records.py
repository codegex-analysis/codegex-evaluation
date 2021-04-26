import csv

if __name__ == '__main__':
    record_before_table = [row[:8] for row in csv.reader(open('config/records-before.csv', 'r'))]
    record_table = [row[:8] for row in csv.reader(open('config/record.csv', 'r'))]
    # for row in record_before_table:
    #     if row[6] != 5 and row[7] == 'TRUE':
    #         print('before', row)
    new_records_table = []
    for line_no, row in enumerate(record_table):
        if line_no == 0:
            new_records_table.append(['relative_path', 'html_url', 'path', 'commit_id', 'line', 'bug_type', 'priority',
                                      'comment_or_not'])
            continue
        if int(row[6]) != 5 and row[7] == 'TRUE':
            if row[:8] not in record_before_table:
                new_records_table.append(row[:8])
    csv.writer(open('config/new_records.csv', 'w')).writerows(new_records_table)