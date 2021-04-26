data_dict = dict()
import csv

unique_patterns = set()

all_patterns = set(['NM_CLASS_NAMING_CONVENTION', 'DM_STRING_VOID_CTOR', 'RE_POSSIBLE_UNINTENDED_PATTERN',
                   'DLS_DEAD_LOCAL_INCREMENT_IN_RETURN', 'SE_NONSTATIC_SERIALVERSIONID',
                   'VA_FORMAT_STRING_USES_NEWLINE', 'DMI_BAD_MONTH', 'FI_EXPLICIT_INVOCATION',
                   'CNT_ROUGH_CONSTANT_VALUE', 'RE_CANT_USE_FILE_SEPARATOR_AS_REGULAR_EXPRESSION',
                   'SE_METHOD_MUST_BE_PRIVATE', 'RV_01_TO_INT', 'RC_REF_COMPARISON_BAD_PRACTICE_BOOLEAN',
                   'NM_LCASE_TOSTRING', 'IL_CONTAINER_ADDED_TO_ITSELF', 'UI_INHERITANCE_UNSAFE_GETRESOURCE',
                   'SA_SELF_COMPUTATION', 'BC_IMPOSSIBLE_DOWNCAST_OF_TOARRAY', 'SA_SELF_ASSIGNMENT',
                   'NM_SAME_SIMPLE_NAME_AS_SUPERCLASS', 'SA_DOUBLE_ASSIGNMENT', 'NM_SAME_SIMPLE_NAME_AS_INTERFACE',
                   'SA_SELF_COMPARISON', 'EC_NULL_ARG', 'BIT_AND_ZZ', 'BSHIFT_WRONG_ADD_PRIORITY',
                   'NM_FUTURE_KEYWORD_USED_AS_MEMBER_IDENTIFIER', 'RV_EXCEPTION_NOT_THROWN',
                   'DMI_RANDOM_USED_ONLY_ONCE', 'DMI_COLLECTIONS_SHOULD_NOT_CONTAIN_THEMSELVES', 'IMSE_DONT_CATCH_IMSE',
                   'DMI_USING_REMOVEALL_TO_CLEAR_COLLECTION', 'BIT_IOR', 'STCAL_STATIC_CALENDAR_INSTANCE',
                   'DLS_OVERWRITTEN_INCREMENT', 'BIT_SIGNED_CHECK', 'SE_NONLONG_SERIALVERSIONID',
                   'SE_READ_RESOLVE_IS_STATIC', 'SE_NONFINAL_SERIALVERSIONID', 'SE_READ_RESOLVE_MUST_RETURN_OBJECT',
                   'NM_BAD_EQUAL', 'NM_FUTURE_KEYWORD_USED_AS_IDENTIFIER', 'EQ_COMPARING_CLASS_NAMES',
                   'STCAL_STATIC_SIMPLE_DATE_FORMAT_INSTANCE', 'DM_RUN_FINALIZERS_ON_EXIT',
                   'FI_PUBLIC_SHOULD_BE_PROTECTED', 'ES_COMPARING_STRINGS_WITH_EQ', 'FE_TEST_IF_EQUAL_TO_NOT_A_NUMBER',
                   'NM_METHOD_NAMING_CONVENTION', 'NM_LCASE_HASHCODE', 'QBA_QUESTIONABLE_BOOLEAN_ASSIGNMENT',
                   'BIT_SIGNED_CHECK_HIGH_BIT', 'DM_STRING_CTOR', 'DMI_VACUOUS_SELF_COLLECTION_CALL',
                   'DM_INVALID_MIN_MAX', 'BIT_AND'])


def calc_unique_pattern(pattern):
    if pattern == 'SA_SELF_COMPARISON':
        unique_patterns.add('SA_LOCAL_SELF_COMPARISON')
        unique_patterns.add('SA_FIELD_SELF_COMPARISON')
    elif pattern == 'SA_SELF_COMPUTATION':
        unique_patterns.add('SA_LOCAL_SELF_COMPUTATION')
        unique_patterns.add('SA_FIELD_SELF_COMPUTATION')
    elif pattern == 'SA_SELF_ASSIGNMENT':
        unique_patterns.add('SA_LOCAL_SELF_ASSIGNMENT')
        unique_patterns.add('SA_FIELD_SELF_ASSIGNMENT')
    elif pattern == 'SA_DOUBLE_ASSIGNMENT':
        unique_patterns.add('SA_FIELD_DOUBLE_ASSIGNMENT')
        unique_patterns.add('SA_LOCAL_DOUBLE_ASSIGNMENT')
    else:
        unique_patterns.add(pattern)


def load_data_dict():
    spotbugs_unmatched_table = [row for row in csv.reader(open('config/spotbugs-unmatched-result.csv', 'r'))]
    codegex_unmatched_table = [row for row in csv.reader(open('config/rbugs-unmatched-result.csv', 'r'))]
    matched_table = [row for row in csv.reader(open('config/matched-result.csv', 'r'))]
    spotbugs_unmatched_dict = dict()
    codegex_unmatched_dict = dict()
    matched_dict = dict()
    matched_all_dict = dict()
    for line_no, row in enumerate(spotbugs_unmatched_table):
        if line_no == 0:
            continue
        calc_unique_pattern(row[1])
        if row[1] not in spotbugs_unmatched_dict:
            spotbugs_unmatched_dict[row[1]] = 1
        else:
            spotbugs_unmatched_dict[row[1]] += 1
    for line_no, row in enumerate(codegex_unmatched_table):
        if line_no == 0:
            continue
        calc_unique_pattern(row[1])
        if row[1] not in codegex_unmatched_dict:
            codegex_unmatched_dict[row[1]] = 1
        else:
            codegex_unmatched_dict[row[1]] += 1
    for row in matched_table:
        calc_unique_pattern(row[1])
        if row[1] in spotbugs_unmatched_dict or row[1] in codegex_unmatched_dict:
            if row[1] not in matched_dict:
                matched_dict[row[1]] = 1
            else:
                matched_dict[row[1]] += 1
        else:
            if row[1] not in matched_all_dict:
                matched_all_dict[row[1]] = 1
            else:
                matched_all_dict[row[1]] += 1

    a_keys = [key for key in spotbugs_unmatched_dict if key not in matched_dict] + \
             [key for key in codegex_unmatched_dict if key not in matched_dict]
    for key in a_keys:
        matched_dict[key] = 0

    print("spotbugs_unmatched_dict", spotbugs_unmatched_dict)
    print("codegex_unmatched_dict", codegex_unmatched_dict)
    print("matched_dict", matched_dict)
    print("unique_patterns", unique_patterns)
    print("len unique_patterns", str(len(unique_patterns)))
    print("no violations patterns", list(all_patterns - unique_patterns))
    for key, value in matched_dict.items():
        data_dict[key] = {'STP': value, 'STN': 0, 'SFP': 0, 'SFN': 0, 'CTP': value, 'CTN': 0, 'CFP': 0, 'CFN': 0}

    for key, value in spotbugs_unmatched_dict.items():
        data_dict[key]['CFN'] = value
        data_dict[key]['STP'] += value

    for key, value in codegex_unmatched_dict.items():
        data_dict[key]['SFN'] = value
        data_dict[key]['CTP'] += value

    data_dict['Overlaps'] = {'STP': sum(matched_all_dict.values()), 'STN': 0, 'SFP': 0, 'SFN': 0,
                             'CTP': sum(matched_all_dict.values()), 'CTN': 0, 'CFP': 0, 'CFN': 0}


def calc_accuracy(TP, TN, FP, FN):
    if TP + TN + FP + FN == 0:
        return '-'
    return round((float(TP + TN) / float(TP + TN + FP + FN)) * 100, 2)


def calc_precision(TP, TN, FP, FN):
    if TP + FP == 0:
        return '-'
    return round(float(TP) / float((TP + FP)) * 100, 2)


def calc_recall(TP, TN, FP, FN):
    if TP + FN == 0:
        return '-'
    return round(float(TP) / float((TP + FN)) * 100, 2)


def calc_f1(precision, recall):
    if precision == '-':
        return '-'
    if precision + recall == 0:
        return '-'
    return round(float(2 * precision * recall) / float(precision + recall), 2)


if __name__ == '__main__':
    load_data_dict()
    for key, value in data_dict.items():
        data_dict[key]['S_A'] = calc_accuracy(data_dict[key]['STP'], data_dict[key]['STN'],
                                              data_dict[key]['SFP'], data_dict[key]['SFN'])
        data_dict[key]['C_A'] = calc_accuracy(data_dict[key]['CTP'], data_dict[key]['CTN'],
                                              data_dict[key]['CFP'], data_dict[key]['CFN'])
        data_dict[key]['S_P'] = calc_precision(data_dict[key]['STP'], data_dict[key]['STN'],
                                              data_dict[key]['SFP'], data_dict[key]['SFN'])
        data_dict[key]['C_P'] = calc_precision(data_dict[key]['CTP'], data_dict[key]['CTN'],
                                              data_dict[key]['CFP'], data_dict[key]['CFN'])
        data_dict[key]['S_R'] = calc_recall(data_dict[key]['STP'], data_dict[key]['STN'],
                                              data_dict[key]['SFP'], data_dict[key]['SFN'])
        data_dict[key]['C_R'] = calc_recall(data_dict[key]['CTP'], data_dict[key]['CTN'],
                                              data_dict[key]['CFP'], data_dict[key]['CFN'])
        data_dict[key]['S_F1'] = calc_f1(data_dict[key]['S_P'], data_dict[key]['S_R'])
        data_dict[key]['C_F1'] = calc_f1(data_dict[key]['C_P'], data_dict[key]['C_R'])
    rows = [['Pattern', 'STP', 'STN', 'SFP', 'SFN', 'CTP', 'CTN', 'CFP', 'CFN', 'S_A', 'C_A', 'S_P', 'C_P',
             'S_R', 'C_R', 'S_F1', 'C_F1']]
    for key, value in data_dict.items():
        rows.append([key, value['STP'], value['STN'], value['SFP'], value['SFN'], value['CTP'], value['CTN'],
                     value['CFP'], value['CFN'], value['S_A'], value['C_A'], value['S_P'], value['C_P'], value['S_R'],
                     value['C_R'], value['S_F1'], value['C_F1']])
    all_cnt = [0] * 8
    for row in rows[1:]:
        for i in range(len(all_cnt)):
            all_cnt[i] += row[i + 1]
    S_all_a = calc_accuracy(all_cnt[0], all_cnt[1], all_cnt[2], all_cnt[3])
    C_all_a = calc_accuracy(all_cnt[4], all_cnt[5], all_cnt[6], all_cnt[7])
    S_all_p = calc_precision(all_cnt[0], all_cnt[1], all_cnt[2], all_cnt[3])
    C_all_p = calc_precision(all_cnt[4], all_cnt[5], all_cnt[6], all_cnt[7])
    S_all_r = calc_recall(all_cnt[0], all_cnt[1], all_cnt[2], all_cnt[3])
    C_all_r = calc_recall(all_cnt[4], all_cnt[5], all_cnt[6], all_cnt[7])
    rows.append(['Overall'] + all_cnt + [S_all_a, C_all_a, S_all_p, C_all_p, S_all_r, C_all_r,
                                         calc_f1(S_all_p, S_all_r),
                                         calc_f1(C_all_p, C_all_r)])
    csv.writer(open('config/pattern-rate.csv', 'w')).writerows(rows)
