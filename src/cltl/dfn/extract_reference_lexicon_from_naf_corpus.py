import argparse
from lxml import etree as et
import json
import os

from pandas.core.arrays.categorical import contains

import naf_util as util


def process_naf_file(naf_file, lexicon:{}, status, language):
        name = os.path.basename(naf_file)
        try:
            tree = et.parse(naf_file)
            root = tree.getroot()
            attr = "{http://www.w3.org/XML/1998/namespace}lang"
            attr_val = root.get(attr)
            if attr_val!=language:
                print('Wrong language tag', attr, attr_val, "in", naf_file)
                return
            coref_layer = root.find('coreferences')
            term_layer = root.find('terms')
            mw_layer = root.find('multiwords')
            text_layer = root.find('text')
            if coref_layer is None:
                print(f"No COREF layer found in {name}")
                return
            else:
                print('processing', name)
                # get all predicates (in a list)
                corefs = coref_layer.findall('coref')
                for coref in corefs:
                    if not coref.get("status")==status:
                        continue
                    span = coref.findall('span/target')
                    lemmas, poses, term_ids = util.getLemmaPosSpanFromTerms(span, term_layer, mw_layer)
                    mentions = util.get_mentions_from_targets(name, term_ids, term_layer, text_layer)
                    references= util.getReferenceAnnotations(coref, mentions)
                    lemma = "_".join(set(lemmas))
                    pos = "_".join(set(poses))
                    if lemma=="":
                        print('EMPTY lemma in', 'file', name, 'span', span)
                    else:
                        util.update_reference_lexicon(lexicon=lexicon, lemma=lemma, pos=pos, references=references)
                        print('nr of entries in', len(lexicon))
        except Exception as e:
            print('Error parsing', naf_file, e)
# <coref id="co12" status="manual" type="entity">
# <span>
# <target id="t193"/>
# <target id="t195"/>
# </span>
# <externalReferences>
# <externalRef reference="Q212" resource="http://www.wikidata.org" timestamp="2021-10-14T18:13:11UTC" source="undefined" reftype="entity"/>
# </externalReferences>
# </coref>
# <coref id="co13" status="manual" type="entity">
# <span>
# <target id="t216"/>
# </span>
# <externalReferences>
# <externalRef reference="Q212" resource="http://www.wikidata.org" timestamp="2021-10-14T18:13:37UTC" source="undefined" reftype="entity"/>
# </externalReferences>
# </coref>
# <coref id="co14" status="manual" type="event">
# <span>
# <target id="t200"/>
# </span>

def main():
    """
    Main function to execute the NAF file processing.
    python extract_frame_lexicon_from_naf_corpus.py --path "/Users/piek/Desktop/DFN-final/DutchFrameNetData/data.2/nl"
    """
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Process NAF files from a specified directory.')
    parser.add_argument('--language', default='nl', help='nl or en')
    parser.add_argument('--path', default="/Users/piek/Desktop/DFN-final/DutchFrameNetData.1/data.2/nl",
                        help='Path to the directory containing NAF files')
    parser.add_argument('--out', default="/Users/piek/Desktop/DFN-final/DutchFrameNetData.1/data.2/reference_lexicon.json",
                        help='Path to the output file for the lexicon.json file')

    args = parser.parse_args()
    corpus_path = args.path
    lexicon_path = args.out
    language = args.language

    # Get all NAF files
    naf_files = util.get_naf_files(corpus_path)

    # Print the number of NAF files found
    print(f"Found {len(naf_files)} NAF files in {corpus_path}")
    lexicon= {}
    status = "system"
    status = "manual"
    for file in naf_files[:500]:
        process_naf_file(file, lexicon, status, language )
    try:
        with open(lexicon_path, 'w', encoding='utf-8') as f:
            json.dump(lexicon, f, indent=4, ensure_ascii=False)
        print(f"Successfully saved JSON to {lexicon_path}")
    except Exception as e:
        print(f"Error saving JSON file: {str(e)}")


if __name__ == "__main__":
    main()
