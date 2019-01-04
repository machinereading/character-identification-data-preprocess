from stanfordcorenlp import StanfordCoreNLP
import json
nlp_parser = StanfordCoreNLP('C:\SWRC_DATA\stanford-corenlp-full-2018-10-05')
RAW_SCRIPT_PATH = 'data/raw_script.json'
OUTPUT_PATH = 'data/friendsnew.english.v4_gold_conll' # 이 파일명은 바꾸지 마세요
TARGET_EPISODE_ID = 's08_e01'
VIDEO_PICKLE_NAME = 'f001.pickle'

def read_raw_script():
    with open(RAW_SCRIPT_PATH, 'r', encoding='utf-8') as f:
        raw_script_obj = json.load(f)
    target_episode = None
    for item in raw_script_obj['episodes']:
        if (item['episode_id'] == TARGET_EPISODE_ID):
            target_episode = item
            break

    return target_episode

def generate_conll_data(raw_script):
    conll_datas = []
    for scene_count,scene in enumerate(raw_script['scenes']):
        doc_id = '/friends-' + TARGET_EPISODE_ID
        conll_datas.append('#begin document ({}); part00{}\n'.format(doc_id,str(scene_count)))
        for ut_count, utter in enumerate(scene['utterances']):
            speaker_list = utter['speakers']
            text = utter['transcript']
            if len(speaker_list) < 1 or len(text) < 1:
                continue

            speaker = speaker_list[0].replace(' ','_')

            props = {'annotators': 'tokenize,pos,lemma,ner', 'pipelineLanguage': 'en', 'outputFormat': 'conll'}
            result = nlp_parser.annotate(text, properties=props)
            conll_lines = result.split('\n')

            for conll_line in conll_lines:
                if (len(conll_line) < 2):
                    if (conll_datas[-1] != '\n'):
                        conll_datas.append('\n')
                else:
                    items = conll_line.split()
                    utid, word, lemma, pos, ner = items[0], items[1], items[2], items[3], items[4]
                    if (len(ner) > 6):
                        ner = ner[0:6]
                    if (ner == 'O'):
                        ner = '*'
                    else:
                        ner = '(' + ner + ')'

                    conll_datas.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (
                        doc_id, str(scene_count), str(int(utid)-1), word, pos, '*', lemma, '-', '-', speaker, ner, 'NOTIME', 'NOTIME', VIDEO_PICKLE_NAME, '-'
                    ))
        conll_datas.append('#end document\n')
    return conll_datas

def write_file_with_mention_detection(conll_datas):
    line_list = [line.strip() for line in conll_datas]
    line_len = len(line_list)
    touched = [False for _ in range(line_len)]

    ner_count = 0
    pronoun_count = 0
    general_noun_count = 0

    # PERSON NER Detect
    for ner_len in reversed(range(1, 5)):
        for i in range(line_len - ner_len):
            st = i
            en = i + ner_len

            is_ner = True
            for k in range(st, en):
                items = line_list[k].split()
                if (len(items) < 5):
                    is_ner = False
                    break
                t = items[10]
                if (touched[k] or t != '(PERSON)'):
                    is_ner = False
                    break

            if (is_ner):
                ner_count += 1
                if (ner_len > 1):
                    line_list[st] = line_list[st][:-1] + '(xxx'
                    line_list[en - 1] = line_list[en - 1][:-1] + 'xxx)'
                else:
                    line_list[st] = line_list[st][:-1] + '(xxx)'
                for k in range(st, en):
                    touched[k] = True

    # PRONOUN DETECT
    pronoun_list = ['i', 'my', 'me', 'mine', 'you', 'your', 'yours', 'she', 'her', 'hers', 'he', 'his', 'him', 'myself',
                    'yourself', 'herself', 'himself']
    pronoun_list_soyu = ['mine', 'hers', 'his', 'yours']
    for i in range(line_len):
        items = line_list[i].split()
        if (len(items) < 5):
            continue
        word = items[3].lower()
        pos = items[4]
        if (not touched[i]):
            if (('PRP' in pos and word in pronoun_list) or (word in pronoun_list_soyu)):
                pronoun_count += 1
                touched[i] = True
                line_list[i] = line_list[i][:-1] + '(xxx)'

    # PERSON
    f = open('data/personal_noun_list.txt', 'r', encoding='utf-8')
    personal_noun_list = [line.strip() for line in f]
    f.close()

    for i in range(line_len):
        items = line_list[i].split()
        if (len(items) < 5):
            continue
        word = items[3].lower()
        pos = items[4]
        if (not touched[i]):
            if (pos.startswith('NN') and 'S' not in pos and word in personal_noun_list):
                general_noun_count += 1
                touched[i] = True
                line_list[i] = line_list[i][:-1] + '(xxx)'

    print('NER Person', ner_count)
    print('Pronouns', pronoun_count)
    print('General Nouns', general_noun_count)

    f_write = open(OUTPUT_PATH, 'w', encoding='utf-8')
    for line in line_list:
        f_write.write(line + '\n')
    f_write.close()

    pass

if __name__ == '__main__':
    raw_script = read_raw_script()
    conll_data = generate_conll_data(raw_script)
    write_file_with_mention_detection(conll_data)
