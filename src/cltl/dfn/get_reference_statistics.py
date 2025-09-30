import json
import os
from shutil import unregister_archive_format


def main():
    data_folder = "../../../data/DFN-corpus-based/"
  #  lexicon_path = data_folder+"nl_reference_lexicon.json"
    lexicon_path =  data_folder+"en_reference_lexicon.json"
    lexicon_name = os.path.basename(lexicon_path)
    nr_entries = 0
    total_annotations =0
    pos_dict= {}
    reference_dict = {}
    polysemy_dict = {}
    status_dict = {}
    project_annotations_dict = {}
    nr_annotations_dict = {}
    multiple_sources_dict = {}
    lex = json.loads(open(lexicon_path).read())
    nr_entries = len(lex)
    for lex_entry in lex:
        lex_info = lex.get(lex_entry)
        pos = lex_info['pos']
        if pos in pos_dict:
            pos_dict[pos]+=1
        else:
            pos_dict[pos] = 1
        references = lex_info['references']
     #   print(len(references), lex_entry, references.keys())
        polysemy = len(references)
        if polysemy in polysemy_dict:
            polysemy_dict[polysemy] +=1
        else:
            polysemy_dict[polysemy] = 1
        for reference in references:
            if reference in reference_dict:
                reference_dict[reference] += 1
            else:
                reference_dict[reference] = 1
            frame_info = references.get(reference)
            annotations = frame_info['annotations']
            if annotations is None:
            #    print(frame_info)
                print('no annotations for', lex_entry, reference)
                continue
            multiple_source = ""
            nr_annotations = len(annotations)
            if nr_annotations in nr_annotations_dict:
                nr_annotations_dict[nr_annotations] += 1
            else:
                nr_annotations_dict[nr_annotations] = 1
            for annotation in annotations:
                annotation_project = annotation['project']
                total_annotations+=1
                if annotation_project in project_annotations_dict:
                    project_annotations_dict[annotation_project] +=1
                else:
                    project_annotations_dict[annotation_project] = 1
                if multiple_source == "":
                    multiple_source=annotation_project
                elif multiple_source != annotation_project:
                    multiple_source=annotation_project
                    if lex_entry in multiple_sources_dict:
                        multiple_sources_dict[lex_entry] +=1
                    else:
                        multiple_sources_dict[lex_entry] = 2
                status = annotation['status']
                if status in status_dict:
                    status_dict[status]+=1
                else:
                    status_dict[status]=1
    average_polysemy = nr_entries/len(reference_dict)
    average_annotations = total_annotations/len(reference_dict)
    stats = {"name": lexicon_path, "total_entries": nr_entries, "pos": pos_dict, "reference_coverage": len(reference_dict), "references": reference_dict, "average_polysemy": average_polysemy, "polysemy_distribution": polysemy_dict, "status_distribution": status_dict, "average_annotations": average_annotations, "total_annotations": total_annotations, "project_annotation_distribution": project_annotations_dict, "nr_annotations_distribution": nr_annotations_dict, "multiple_sources": multiple_sources_dict}

    stats_path = data_folder+lexicon_name+"_stats.json"
    try:
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=4, ensure_ascii=False)
        print(f"Successfully saved JSON to {stats_path}")
    except Exception as e:
        print(f"Error saving JSON file: {str(e)}")


if __name__ == "__main__":
        main()