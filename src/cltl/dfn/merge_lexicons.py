import json
import os
from pathlib import Path


def process_lexicons(merged_dict:{}, file):
    nr_entries = 0
    nr_new_entries = 0
    nr_matches = 0
    try:
        lex = json.loads(open(file).read())
        for lex_entry in lex:
            nr_entries += 1
            try:
                if lex_entry in merged_dict:
                    nr_matches += 1
                   # print('matched', lex_entry)
                    org_lex_entry_info = merged_dict.get(lex_entry)
                    lex_entry_info = lex.get(lex_entry)
                    for element in lex_entry_info:
                       try:
                            if not element in org_lex_entry_info:
                                info = lex_entry_info.get(element)
                                org_lex_entry_info[element]=info
                                if lex_entry=="stellen:VERB":
                                    print(org_lex_entry_info)
                            else:
                                if not org_lex_entry_info[element]==org_lex_entry_info[element]:
                                    print("Mismatch:")
                                    print(org_lex_entry_info[element], lex_entry_info[element])
                       except Exception as e:
                            print(f"Error merging JSON structure: {str(e)}", file, element, org_lex_entry_info[element])
                    org_frames = org_lex_entry_info['frames']
                    new_frames = lex_entry_info['frames']
                    for frame in new_frames:
                        try:
                            new_frame_info = new_frames.get(frame)
                            new_annotations = new_frame_info['annotations']
                            if frame in org_frames:
                                old_frame_info = org_frames.get(frame)
                                old_annotations = old_frame_info['annotations']
                                old_annotations.extend(new_annotations)
                                org_frames[frame]['annotations']= old_annotations
                            else:
                                org_frames[frame] = new_frame_info
                        except Exception as e:
                            print(f"Error merging JSON structure for frames: {str(e)}", file, 'frame', frame, type (new_frames), new_frame_info)
                    org_lex_entry_info['frames'] = org_frames
                    merged_dict[lex_entry] = org_lex_entry_info
                else:
                    nr_new_entries += 1
                    merged_dict[lex_entry]=lex.get(lex_entry)
            except Exception as e:
                print(f"Error processing JSON structure: {str(e)}", file, lex_entry)
    except json.JSONDecodeError as e:
        print("JSON Decode Error:")
        print(f"  Message : {e.msg}")
        print(f"  Line    : {e.lineno}")
        print(f"  Column  : {e.colno}")
        print(f"  Position: {e.pos}")
    except Exception as e:
        print(f"Error reading JSON file: {str(e)}", file, lex_entry)
    print(file.name, nr_entries, nr_matches, nr_new_entries)


def main():
    lexicons = ["lexicon-manual.json", "lexicon-system.json", "A1.json", "A2.json", "rbn_dfn_1_2.json"]
    root_dir = "."
    # filenames = os.walk(root_dir)

    root_dir = Path('./input')
    extension = '.json'
    files = root_dir.rglob(f'*{extension}')

    merged_dict = {}
    for file in files:
        if file.name in lexicons:
            print('Loading', file.name)
            process_lexicons(merged_dict, file)
    print('merged lexicon', len(merged_dict.items()))
    merged_lexicon_path = "./merged.json"
    try:
        with open(merged_lexicon_path, 'w', encoding='utf-8') as f:
            json.dump(merged_dict, f, indent=4, ensure_ascii=False)
        print(f"Successfully saved JSON to {merged_lexicon_path}")
    except Exception as e:
        print(f"Error saving JSON file: {str(e)}")


if __name__ == "__main__":
        main()
