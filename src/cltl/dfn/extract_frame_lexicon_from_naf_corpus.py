import argparse
from lxml import etree as et
import json
import os
import naf_util as util


def process_naf_file(naf_file, lexicon:{}, status):
        name = os.path.basename(naf_file)
        try:
            tree = et.parse(naf_file)
            root = tree.getroot()
            srl_layer = root.find('srl')
            term_layer = root.find('terms')
            mw_layer = root.find('multiwords')
            text_layer = root.find('text')
            if srl_layer is None:
                #print(f"No SRL layer found in {name}")
                return
            else:
                print('processing', name)
                # get all predicates (in a list)
                predicates = srl_layer.findall('predicate')
                for predicate in predicates:
                    if not predicate.get("status")==status:
                        continue
                    span = predicate.findall('span/target')
                    lemmas, poses, term_ids = util.getLemmaPosSpanFromTerms(span, term_layer, mw_layer)
                    mentions = util.get_mentions_from_targets(name, term_ids, term_layer, text_layer)
                    frames= util.getAnnotations(predicate, mentions)
                    lemma = "".join(set(lemmas))
                    pos = "".join(set(poses))
                    if lemma=="":
                        print('EMPTY lemma in', 'file', name, 'span', span)
                    else:
                        util.update_lexicon(lexicon, lemma, pos, frames)
                        print('nr of entries in', len(lexicon))
        except Exception as e:
            print('Error parsing', naf_file, e)

def main():
    """
    Main function to execute the NAF file processing.
    python extract_frame_lexicon_from_naf_corpus.py --path "/Users/piek/Desktop/DFN-final/DutchFrameNetData/data.2/nl"
    """
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Process NAF files from a specified directory.')
    parser.add_argument('--path', default="/Users/piek/Desktop/DFN-final/DutchFrameNetData/data.2/nl",
                        help='Path to the directory containing NAF files')
    parser.add_argument('--out', default="/Users/piek/Desktop/DFN-final/DutchFrameNetData/data.2/lexicon.json",
                        help='Path to the output file for the lexicon.json file')

    args = parser.parse_args()
    corpus_path = args.path
    lexicon_path = args.out

    # Get all NAF files
    naf_files = util.get_naf_files(corpus_path)

    # Print the number of NAF files found
    print(f"Found {len(naf_files)} NAF files in {corpus_path}")
    lexicon= {}
    status = "system"
    status = "manual"
    for file in naf_files[:500]:
        process_naf_file(file, lexicon, status)
    try:
        with open(lexicon_path, 'w', encoding='utf-8') as f:
            json.dump(lexicon, f, indent=4, ensure_ascii=False)
        print(f"Successfully saved JSON to {lexicon_path}")
    except Exception as e:
        print(f"Error saving JSON file: {str(e)}")


if __name__ == "__main__":
    main()
