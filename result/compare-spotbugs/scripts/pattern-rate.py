data_dict = dict()
import csv

# result table
data_dict = dict()

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





def load_data_dict():
    global data_dict
    spotbugs_unmatched_table = [row for row in csv.reader(open('config/spotbugs-unmatched-result.csv', 'r'))]
    codegex_unmatched_table = [row for row in csv.reader(open('config/rbugs-unmatched-result.csv', 'r'))]
    matched_table = [row for row in csv.reader(open('config/matched-result.csv', 'r'))]
    spotbugs_unmatched_dict = dict()
    codegex_unmatched_dict = dict()
    matched_dict = dict()
    # 行1 keys
    unique_patterns = set()
    # result table
    # 载入 spotbugs_unmatched_table 信息
    for line_no, row in enumerate(spotbugs_unmatched_table):
        if line_no == 0:
            continue
        unique_patterns.add(row[1])
        if row[1] not in spotbugs_unmatched_dict:
            spotbugs_unmatched_dict[row[1]] = 1
        else:
            spotbugs_unmatched_dict[row[1]] += 1
    # 载入 codegex_unmatched_table 信息
    for line_no, row in enumerate(codegex_unmatched_table):
        if line_no == 0:
            continue
        unique_patterns.add(row[1])
        if row[1] not in codegex_unmatched_dict:
            codegex_unmatched_dict[row[1]] = 1
        else:
            codegex_unmatched_dict[row[1]] += 1
    # 载入 matched_table 信息
    for line_no, row in enumerate(matched_table):
        if line_no == 0:
            continue
        unique_patterns.add(row[1])
        if row[1] not in matched_dict:
            matched_dict[row[1]] = 1
        else:
            matched_dict[row[1]] += 1
    # 分 pattern 计算 {STP, CTP, SFN, CFN, OL, STN, CTN, SFP, CFP}, 且(STN, CTN, SFP, CFP) = (0, 0, 0, 0)
    for pattern in unique_patterns:
        if pattern in matched_dict:
            OL = matched_dict[pattern]
        else:
            OL = 0
        if pattern in codegex_unmatched_dict:
            SFN = codegex_unmatched_dict[pattern]
        else:
            SFN = 0
        if pattern in spotbugs_unmatched_dict:
            CFN = spotbugs_unmatched_dict[pattern]
        else:
            CFN = 0
        STP = OL + CFN
        CTP = OL + SFN
        STN, CTN, SFP, CFP = 0, 0, 0, 0
        data_dict[pattern] = {'STP': STP,
                              'CTP': CTP,
                              'SFN': SFN,
                              'CFN': CFN,
                              'OL': OL,
                              'STN': STN,
                              'CTN': CTN,
                              'SFP': SFP,
                              'CFP': CFP}
    # print('归并前 data_dict keys:', len(data_dict.keys()))
    # 归并 只有overlaps的数据
    data_dict['Others'] = {'STP': 0,
                           'CTP': 0,
                           'SFN': 0,
                           'CFN': 0,
                           'OL': 0,
                           'STN': 0,
                           'CTN': 0,
                           'SFP': 0,
                           'CFP': 0}
    del_keys = set()
    others_pattern_cnt = 0
    for key, value in data_dict.items():
        if key == 'Others':
            continue
        if value['SFN'] == 0 and value['CFN'] == 0:
            others_pattern_cnt += 1
            for k, v in value.items():
                data_dict['Others'][k] += v
            del_keys.add(key)
    for key in del_keys:
        del data_dict[key]
    # print('归并后 data_dict keys:', len(data_dict.keys()) - 1)
    print('others_pattern_cnt: ', others_pattern_cnt)


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

    rows = [['Pattern', 'STP', 'CTP', 'SFN', 'CFN', 'OL', 'STN', 'CTN', 'SFP', 'CFP',
             'S_A', 'C_A', 'S_R', 'C_R', 'S_F1', 'C_F1']]
    for key, value in data_dict.items():
        rows.append([key, value['STP'], value['CTP'], value['SFN'], value['CFN'], value['OL'],
                     value['STN'], value['CTN'], value['SFP'], value['CFP'],
                     value['S_A'], value['C_A'], value['S_R'], value['C_R'], value['S_F1'], value['C_F1']])
    all_cnt = [0] * 9
    for row in rows[1:]:
        for i in range(len(all_cnt)):
            all_cnt[i] += row[i + 1]
    all_STP, all_CTP, all_SFN, all_CFN, all_STN, all_CTN, all_SFP, all_CFP = \
        all_cnt[0], all_cnt[1], all_cnt[2], all_cnt[3], all_cnt[5], all_cnt[6], all_cnt[7], all_cnt[8]
    S_all_a = calc_accuracy(all_STP, all_STN, all_SFP, all_SFN)
    C_all_a = calc_accuracy(all_CTP, all_CTN, all_CFP, all_CFN)
    S_all_p = calc_precision(all_STP, all_STN, all_SFP, all_SFN)
    C_all_p = calc_precision(all_CTP, all_CTN, all_CFP, all_CFN)
    S_all_r = calc_recall(all_STP, all_STN, all_SFP, all_SFN)
    C_all_r = calc_recall(all_CTP, all_CTN, all_CFP, all_CFN)
    S_all_f1 = calc_f1(S_all_p, S_all_r)
    C_all_f1 = calc_f1(C_all_p, C_all_r)
    rows.append(['Overall'] + all_cnt + [S_all_a, C_all_a, S_all_r, C_all_r, S_all_f1, C_all_f1])
    writer = csv.writer(open('config/pattern-rate.csv', 'w'))
    for row in rows:
        writer.writerow(row[:6] + row[10:])
