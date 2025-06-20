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
        if term.get('id') == target:
            return term
        elif term.get('compound_type') == "endocentric":
            for element in term.getchildren():
                if element.get('id') == target:
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
    sentence_tokens = []
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
    sentence_ids = []
    for wf in text_layer.getchildren():
        for s in spans:
            token = {}
            if wf.get('id')==s.attrib.get('id'):
                sentence_id = wf.get('sent')
                if sentence_id not in sentence_ids:
                    sentence_ids.append(sentence_id)
                token = {"token_id":wf.get('id'), 'sent':sentence_id, 'offset':wf.get('offset'), 'length':wf.get('length')}
                tokens.append(token)
            else:
                components = wf.getchildren()
                for component in components:
                    if component.get('id')==s.attrib.get('id'):
                        sentence_id = component.get('sent')
                        if sentence_id not in sentence_ids:
                            sentence_ids.append(sentence_id)
                        token = {"token_id": component.get('id'), 'sent': sentence_id, 'offset': component.get('offset'),
                                 'length': component.get('length')}
                        tokens.append(token)

    for wf in text_layer.getchildren():
        sentence_id = wf.get('sent')
        if sentence_id in sentence_ids:
            sentence_tokens.append(wf.text)
    sentence = " ".join(sentence_tokens)
    sentence = sentence.replace("\n", "")
    mention = {"doc": file, 'term': "".join(term_ids), 'tokens' : tokens, "text": sentence}

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
