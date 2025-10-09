import json
from pathlib import Path
import json
from pathlib import Path

from collections import defaultdict, Counter, OrderedDict
import requests


def get_wikidata_label(uri, language='en'):
    # Extract Q number from URI
    q_number = uri.split('/')[-1]  # This works for URIs like 'http://www.wikidata.org/entity/Q12345'

    if not q_number.startswith('Q'):
        q_number = 'Q' + q_number

    # Add user agent header to comply with Wikidata's API policies
    headers = {
        'User-Agent': 'Mozilla/5.0 (compatible; MyWikidataBot/1.0; +http://example.org)',
    }

    url = f'https://www.wikidata.org/w/api.php?action=wbgetentities&ids={q_number}&format=json&languages={language}'

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes

        data = response.json()

        if 'error' in data:
            print(f"API Error for {q_number}: {data['error']}")
            return None

        if 'entities' in data and q_number in data['entities']:
            entity = data['entities'][q_number]
            if 'labels' in entity and language in entity['labels']:
                return entity['labels'][language]['value']
            else:
                print(f"No {language} label found for {q_number}")
                return None
        else:
            print(f"No entity data found for {q_number}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request failed for {q_number}: {str(e)}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON decode error for {q_number}: {str(e)}")
        print(f"Response content: {response.content}")
        return None
    except Exception as e:
        print(f"Unexpected error for {q_number}: {str(e)}")
        return None

def get_most_frequent_mention(expressions):
    most_frequent_name = "NONE"
    names = []
    for expression in expressions:
        if 'NOUN' in expression or 'PROPN' in expression:
            names.append(expression)
    if len(names) > 0:
        name_counts = Counter(names)
        most_frequent_name = name_counts.most_common(1)[0][0]
    return most_frequent_name

# def get_wikidata_label(uri, language='en'):
#     q_number = uri.split('/')[-1]  # This works for URIs like 'http://www.wikidata.org/entity/Q12345'
#     url = f'https://www.wikidata.org/w/api.php?action=wbgetentities&ids={q_number}&format=json&languages={language}'
#     try:
#         response = requests.get(url)
#         data = response.json()
#         return data['entities'][q_number]['labels'][language]['value']
#     except Exception as e:
#         print(f"Error retrieving label for {q_number}: {str(e)}")
#         print(url)
#         return None

def get_reference_dictionary(reference_lexicon, reference_dictionary, mention_dictionary):
    for lex_entry in reference_lexicon:
        lex_info = reference_lexicon.get(lex_entry)
        if 'references' in lex_info:
            references = lex_info['references']
            for reference in references:
                reference_info = references.get(reference)
                annotations = reference_info['annotations']
                for annotation in annotations:
                    if 'mention' in annotation:
                        for mention in annotation['mention']:
                            mention_id = mention["doc"]+":"+mention["term"]
                            if mention_id in mention_dictionary:
                                mention_dictionary[mention_id].append(reference)
                            else:
                                mention_dictionary[mention_id] = [reference]
                            if reference  in reference_dictionary:
                                reference_dictionary[reference].append((lex_entry, mention_id))
                            else:
                                reference_dictionary[reference] = [(lex_entry, mention_id)]

def get_frame_dictionary(frame_lexicon, frame_dictionary, mention_dictionary):
    for lex_entry in frame_lexicon:
        lex_info = frame_lexicon.get(lex_entry)
        if 'frames' in lex_info:
            frames = lex_info['frames']
            for frame in frames:
                frame_info = frames.get(frame)
                annotations = frame_info['annotations']
                for annotation in annotations:
                    if 'mention' in annotation:
                        for mention in annotation['mention']:
                            mention_id = mention["doc"]+":"+mention["term"]
                            if mention_id in mention_dictionary:
                                mention_dictionary[mention_id].append(frame)
                            else:
                                mention_dictionary[mention_id] = [frame]
                            if frame  in frame_dictionary:
                                frame_dictionary[frame].append(mention_id)
                            else:
                                frame_dictionary[frame] = [mention_id]


def main():
    root_dir = Path('../../../data/DFN-corpus-based')
    reference_lexicon_file1 = "nl_reference_lexicon.json"
    reference_lexicon_file2 = "en_reference_lexicon.json"
    reference_lexicons1 = json.loads(open(Path.joinpath(root_dir, reference_lexicon_file1)).read())
    reference_lexicons2 = json.loads(open(Path.joinpath(root_dir, reference_lexicon_file2)).read())
    ref_mention_dict1 = {}
    mention_ref_dict1 = {}
    get_reference_dictionary(reference_lexicons1, ref_mention_dict1, mention_ref_dict1)
    ref_mention_dict2 = {}
    mention_ref_dict2 = {}
    get_reference_dictionary(reference_lexicons2, ref_mention_dict2, mention_ref_dict2)

    print('Nr of entities in', reference_lexicon_file1, len(ref_mention_dict1))
    print('Nr of mentions in', reference_lexicon_file1, len(mention_ref_dict1))
    print('Nr of entities in', reference_lexicon_file2, len(ref_mention_dict2))
    print('Nr of mentions in', reference_lexicon_file2, len(mention_ref_dict2))
    intersecting_references = list(set(ref_mention_dict1.keys()).intersection(ref_mention_dict2.keys()))
    print('Intersection of entities', len(intersecting_references))
    print(intersecting_references)

    frame_mention_dict1 = {}
    mention_frame_dict1 = {}
    frame_mention_dict2 = {}
    mention_frame_dict2 = {}

    frame_lexicons_file1 = ["nl_frame_element_lexicon.json", "nl_frame_lexicon.json"]
    frame_lexicons_file2 = ["en_frame_element_lexicon.json", "en_frame_lexicon.json"]

    for file in frame_lexicons_file1:
        frame_lexicon = json.loads(open(Path.joinpath(root_dir, file)).read())
        get_frame_dictionary(frame_lexicon, frame_mention_dict1, mention_frame_dict1)
    for file in frame_lexicons_file2:
        frame_lexicon = json.loads(open(Path.joinpath(root_dir, file)).read())
        get_frame_dictionary(frame_lexicon, frame_mention_dict2, mention_frame_dict2)

    grounded_framing = {reference_lexicon_file1: {"nr_of_entities": len(ref_mention_dict1), "nr_of_mentions":len(mention_ref_dict1)},
                        reference_lexicon_file2: {"nr_of_entities": len(ref_mention_dict2), "nr_of_mentions":len(mention_ref_dict2)},
                        "Nr_of_intersecting_entities": len(intersecting_references)}
    intersection_framings = []
    for entity in intersecting_references:
        entity_framing = {"referent": entity}
        mentions1 = ref_mention_dict1[entity]
        mentions2 = ref_mention_dict2[entity]
        framings = []
        print(entity, len(mentions1), len(mentions2))
        for lex_entry, mention1  in mentions1:
            if mention1 in mention_frame_dict1:
                frames1 = mention_frame_dict1[mention1]
                framings.append({"language": "nl",  "lex_entry": lex_entry, "mention": mention1, "frames": frames1})
        for lex_entry, mention2 in mentions2:
            if mention2 in mention_frame_dict2:
                frames2 = mention_frame_dict2[mention2]
                framings.append({"language": "en", "lex_entry": lex_entry, "mention": mention2, "frames": frames2})
        entity_framing.update({"framings": framings})
        intersection_framings.append(entity_framing)

    grounded_framing.update({"intersection_framing": intersection_framings})
    grounded_intersection_file = Path.joinpath(root_dir,"grounded_intersection_framing.json")
    with open(grounded_intersection_file, 'w', encoding='utf-8') as f:
        json.dump(intersection_framings, f, indent=4, ensure_ascii=False)
    print(f"Successfully saved JSON to {grounded_intersection_file}")
    csv_str = ""
    stats = {"Nr_of_intersecting_entities": len(intersecting_references)}
    nr_nl_mentions = 0
    nr_en_mentions = 0
    nr_en_only = 0
    nr_nl_only = 0
    nr_nl_and_en = 0
    entity_frames = []
    for entity_framing in intersection_framings:
        referent = entity_framing["referent"]
        referent_name = get_wikidata_label(referent, "en")
        nl_frames = []
        en_frames = []
        nl_en_frames = []
        nl_lexical_entries = []
        en_lexical_entries = []
        if "framings" in entity_framing:
            nl = False
            en = False
            for framing in entity_framing["framings"]:
                if framing["language"] == "nl":
                    nl_lexical_entries.append(framing["lex_entry"])
                    nl_frames.extend(framing["frames"])
                    nr_nl_mentions += 1
                    nl = True
                elif framing["language"] == "en":
                    en_lexical_entries.append(framing["lex_entry"])
                    en_frames.extend(framing["frames"])
                    en = True
                    nr_en_mentions += 1
            if en and nl:
                nr_nl_and_en += 1
            elif en:
                nr_en_only += 1
            elif nl:
                nr_nl_only += 1

        most_frequent_name = get_most_frequent_mention(nl_lexical_entries+en_lexical_entries)
        nl_lexical_entries =OrderedDict(sorted(Counter(nl_lexical_entries).items()))
        en_lexical_entries =OrderedDict(sorted(Counter(en_lexical_entries).items()))
        nl_en_frames = []
        for nl_frame in nl_frames:
            if nl_frame in en_frames:
                nl_en_frames.append(nl_frame)
        for en_frame in en_frames:
            if en_frame in nl_frames:
                nl_en_frames.append(en_frame)
        nl_en_frames = OrderedDict(sorted(Counter(nl_en_frames).items(), key=lambda x: x[1], reverse=True))
        nl_frames = OrderedDict(sorted(Counter(nl_frames).items(), key=lambda x: x[1], reverse=True))
        en_frames = OrderedDict(sorted(Counter(en_frames).items(), key=lambda x: x[1], reverse=True))

        csv_str += f"{referent},{referent_name},{most_frequent_name},{len(nl_frames)},{len(en_frames)},{len(nl_en_frames)}\n"
        entity_frames.append({"referent": referent, "label": referent_name, "most_frequent_mention": most_frequent_name, "nl_lexical_entries": nl_lexical_entries, "en_lexical_entries": en_lexical_entries, "nl_en_frames": nl_en_frames, "nl_frames": nl_frames, "en_frames": en_frames})
    stats.update({"nr_nl_mentions": nr_nl_mentions, "nr_en_mentions": nr_en_mentions, "nr_en_only": nr_en_only, "nr_nl_only": nr_nl_only, "nr_nl_and_en": nr_nl_and_en, "framings":entity_frames})
    grounded_stats_file = Path.joinpath(root_dir,"grounded_framing_english_dutch_stats.json")
    with open(grounded_stats_file, 'w', encoding='utf-8') as f:
        json.dump(stats, f, indent=4, ensure_ascii=False)
    print(f"Successfully saved JSON to {grounded_stats_file}")
    print(csv_str)


if __name__ == "__main__":
        main()
