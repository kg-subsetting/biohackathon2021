import sys
import pandas as pd

def count_instances(tsv_file):
    df = pd.read_csv(tsv_file, sep='\t')
    genes = df.loc[(df['node2'].eq('Q7187')) & (df['id'].str.contains('-P31-'))]['node1'].values.tolist()
    proteins = df.loc[(df['node2'].eq('Q8054')) & (df['id'].str.contains('-P31-'))]['node1'].values.tolist()
    chemicals = df.loc[(df['node2'].eq('Q11173')) & (df['id'].str.contains('-P31-'))]['node1'].values.tolist()
    diseases = df.loc[(df['node2'].eq('Q12136')) & (df['id'].str.contains('-P31-'))]['node1'].values.tolist()
    operon_match = len(df.loc[(df['node2'].eq('Q139677')) & (df['id'].str.contains('-P31-'))])
    acid_match = len(df.loc[(df['node2'].eq('Q11158')) & (df['id'].str.contains('-P31-'))])

    gene_statements = len(df.loc[df['node1'].isin(genes)])
    protein_statements = len(df.loc[df['node1'].isin(proteins)])
    chemical_statements = len(df.loc[df['node1'].isin(chemicals)])
    disease_statements = len(df.loc[df['node1'].isin(diseases)])
    
    
    print('Genes: ', len(genes))
    print('Proteins: ', len(proteins))
    print('Chemical Compounds: ', len(chemicals))
    print('Diseases: ', len(diseases))
    print('Operons: ', operon_match)
    print('Acids: ', acid_match)
    print()
    print('Gene Statements: ', gene_statements)
    print('Protein Statements: ', protein_statements)
    print('Chemical Compound Statements: ', chemical_statements)
    print('Disease Statements: ', disease_statements)
    print()
    print('All Items: ', len(df.drop_duplicates(subset=['node1'])))
    print('All Statements: ', len(df))



if __name__ == '__main__':
    count_instances(sys.argv[1])
