import argparse
from typing import Any

from lxml import etree as et
import csv
import json
import os

def get_naf_files(folder_path):
    """
    Get all files with .naf extension from the specified folder path.
    
    Args:
        folder_path (str): Path to the folder to search for .naf files
        
    Returns:
        list: List of paths to .naf files
    """
    naf_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.naf'):
                naf_files.append(os.path.join(root, file))
    return naf_files

def process_naf_file(naf_file, lexicon:{}, status):
        name = os.path.basename(naf_file)
        try:
            tree = et.parse(naf_file)
            root = tree.getroot()
            srl_layer = root.find('srl')
            term_layer = root.find('terms')
            mw_layer = root.find('multiwords')
            text_layer = root.find('text')

            if srl_layer is  None:
               # print(f"No SRL layer found in {name}")
                return
            else:
                # get all predicates (in a list)
                predicates = srl_layer.findall('predicate')
                for predicate in predicates:
                    if not predicate.get("status")==status:
                        continue
                    span = predicate.findall('span/target')
                    lemmas, poses, term_ids = getLemmaPosSpanFromTerms(span, term_layer, mw_layer)
                    mentions = get_mentions_from_targets(name, term_ids, term_layer, text_layer)
                    frames= getAnnotations(predicate, mentions)
                    lemma = "".join(set(lemmas))
                    pos = "".join(set(poses))
                    if lemma=="":
                        print('EMPTY lemma in', 'file', name, 'span', span)
                    else:
                        key = lemma+":"+pos
                        if key in lexicon:
                            for frame in frames:
                                frame_info = frames.get(frame)
                                if frame in lexicon[key]['frames']:
                                    lexicon[key]['frames'][frame]['annotations'].extend(frame_info)
                                else:
                                    frame
                                    lexicon[key]['frames'][frame]={'annotations':frame_info}
                        else:
                            framedict = {}
                            for frame in frames:
                                frame_info = frames.get(frame)
                                if frame in lexicon:
                                    framedict[frame]['annotations'].append(frame_info)
                                else:
                                    framedict[frame]={'annotations':frame_info}
                            lexicon[key]={'lemma':lemma, 'pos': pos, 'frames': framedict}
        except Exception as e:
            print('Error parsing', naf_file, e)


def get_term_from_term_id(target, layer):
    # <term id="t262" lemma="Ummah" pos="PROPN" type="open" morphofeat="NNP">
    # <span> <target id="w262"/> </span>
    # </term>
    # <term id = "t391" lemma = "vliegramp" pos = "NOUN" type = "open" morphofeat = "N|soort|ev|neut__Number=Sing" compound_type = "endocentric" head = "t391.c1" >
    # <span> <target id = "w391"/> </span>
    # <component id = "t391.c0" pos = "NOUN" lemma = "vlieg">
    # <span> <target id = "w391.sub0"/> </span>
    # </component>
    # <component id = "t391.c1" pos = "NOUN" lemma = "ramp">
    # <span><target id = "w391.sub1"/></span>
    # </component>

    # <multiwords>
    # <mw id = "mw1" lemma = "indienen" pos = "VERB"  type = "phrasal">
    # <component id = "mw1.c1">
    # <span> <target id = "t24"/> </span>
    # </component>
    # <component  id = "mw1.c2">
    # <span> <target id = "t29"/> </span>
    # </component>
    # </mw>p

    for term in layer.getchildren():
        if term.get('id')==target:
            return term
        elif term.get('compound_type')=="endocentric":
            for element in term.getchildren():
                if element.get('id')==target:
                    return element
    return None

def getLemmaPosSpanFromTerms(span, term_layer, mw_layer):
    lemmas = []
    pos = []
    terms = []
    for s in span:
        id = s.attrib.get('id')
        term = get_term_from_term_id(id, term_layer)
        if term is None:
            term = get_term_from_term_id(id, mw_layer)
        if term is not None:
            terms.append(term)
        else:
            print('Could not find this term:', id)
    for term in terms:
        lemma = term.attrib.get('lemma')
        if lemma is not None:
            lemmas.append(lemma)
        p = term.attrib.get('pos')
        if p is not None:
            pos.append(p)
    return lemmas, pos, terms

def get_mentions_from_targets(file, targets, term_layer, text_layer):
    # targets can be terms or multiwords
    # in the former case, we can get the tokens that make up a term directly
    # in the latter case, we need to get the list of terms from the multiword to get the list of tokens.
    # a third case is when the target is compound component, in which case a subtoken needs to be retrieved
        # <wf sent="7" id="w144" length="17" offset="848">
        # MH17-nabestaanden<subtoken id="w144.sub0" length="4" offset="848">MH17</subtoken>
        # <subtoken id="w144.sub1" length="1" offset="852">-</subtoken>
        # <subtoken id="w144.sub2" length="12" offset="856">nabestaanden</subtoken>
        # </wf>
    spans = []
    tokens = []
    term_ids = []
    for target in targets:
        term_ids.append(target.attrib.get('id'))
        if target.get('id').startswith("t"):
            # this is a normal term so we get the word form ids
            spans = target.findall('span/target')
        else:
            for component in target.getchildren():
                component_span = component.findall('span/target')
                for cs in component_span:
                    term = get_term_from_term_id(cs.get('id'), term_layer)
                    if term is not None:
                        term_spans = term.findall('span/target')
                        spans.extend(term_spans)
    for wf in text_layer.getchildren():
        for s in spans:
            token = {}
            if wf.get('id')==s.attrib.get('id'):
                token = {"token_id":wf.get('id'), 'sent':wf.get('sent'), 'offset':wf.get('offset'), 'length':wf.get('length')}
                tokens.append(token)
            else:
                components = wf.getchildren()
                for component in components:
                    if component.get('id')==s.attrib.get('id'):
                        token = {"token_id": component.get('id'), 'sent': wf.get('sent'), 'offset': component.get('offset'),
                                 'length': component.get('length')}
                        tokens.append(token)
    mention = {"doc": file, 'term': "".join(term_ids), 'tokens' : tokens}

    return [mention]


def getAnnotations(predicate, mentions):
    frames = {}
    frame_info = predicate.findall('externalReferences/externalRef')
    status = predicate.attrib.get('status')
    for ref in frame_info:
        frame = ref.attrib.get('reference')
        if frame.startswith("http://premon.fbk.eu/resource/"):
            frame = frame[len("http://premon.fbk.eu/resource/"):]
        source = ref.attrib.get('source')
        t = ref.attrib.get('timestamp')
        reftype = ref.attrib.get('reftype')
        annotation = {'project': 'DutchFrameNet', 'status': status, 'annotator': source, 'timestamp': t, 'reftype': reftype, 'mention': []}
        for mention in mentions:
            annotation['mention'].append(mention)
        if frame in frames:
            frames[frame].append(annotation)
        else:
            frames[frame] = [annotation]
    return frames

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
    naf_files = get_naf_files(corpus_path)

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
