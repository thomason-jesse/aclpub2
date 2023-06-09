import pandas as pd
import yaml
import numpy as np

submissions_df = pd.read_csv('data/Submission_Information.csv')
authors_df = pd.read_csv('data/Author_Information.csv')

entries = []
for idx in submissions_df.index:
    # Things we can pull directly from the submissions CSV
    # id, title, abstract
    sid = int(submissions_df['Submission ID'][idx])
    entry = {'id': sid,
             'file': '%s/%s_Paper.pdf' % (sid, sid),
             'title': submissions_df['Title'][idx],
             'abstract': submissions_df['Abstract'][idx],
             'archival': True}
    
    # authors
    entry_authors = []
    for auth_idx in range(1, 64):
        uid = submissions_df['%d: Username' % auth_idx][idx]
        if type(uid) is not str:
            break
        author_df = authors_df.loc[authors_df['Username'] == uid]
        auth_df_idx = author_df.index[0]
        author = {'first_name': author_df['First Name'][auth_df_idx],
                  'middle_name': author_df['Middle Name'][auth_df_idx],
                  'last_name': author_df['Last Name'][auth_df_idx],
                  'institution': author_df['Affiliation'][auth_df_idx],
                  'email': author_df['Email'][auth_df_idx],
                  'google_scholar': author_df['Google Scholar ID'][auth_df_idx],
                  'orcid': author_df['Orcid'][auth_df_idx],
                  'semantic_scholar': author_df['Semantic Scholar ID'][auth_df_idx]}
        entry_authors.append(author)
    entry['authors'] = entry_authors
    
    # attributes
    # NOTE: unsure if this is how presentation type is actually annotated; need to confirm
    presentation_type_raw = submissions_df['Acceptance Status'][idx]
    presentation_type = ('oral' if '-Oral' in presentation_type_raw else 
                         'findings' if 'findings' in presentation_type_raw else 'poster')
    entry_attributes = {'paper_type': submissions_df['Submission Type'][idx],
                        'presentation_type': presentation_type,
                        'submitted_area': submissions_df['Subject Area'][idx]}
    entry['attributes'] = entry_attributes
        
    # attachments
    attachments_l = submissions_df['Attachments'][idx]
    entry_attachments = []
    for att_str in attachments_l.split(', '):
        if 'SupMat__' in att_str:
            _, att = att_str.split('__')
        else:
            att = att_str
        if att == 'Paper':
            continue
        # NOTE: no idea where these files will live or how they will be named; softconf download only pulls PDFs; check
        att_entry = {'type': att, 'file': '%d/%d_%s.zip' % (sid, sid, att)}
        entry_attachments.append(att_entry)
    entry['attachments'] = entry_attachments
                    
    entries.append(entry)

with open(r'output.yaml', 'w') as f:
    outputs = yaml.dump(entries, f)
    print('file write status:', outputs)