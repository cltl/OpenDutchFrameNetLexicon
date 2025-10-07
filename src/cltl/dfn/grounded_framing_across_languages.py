import json
from pathlib import Path
import json
from pathlib import Path

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

if __name__ == "__main__":
        main()
